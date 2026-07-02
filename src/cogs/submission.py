import logging
import os
import discord
from discord.ext import commands
from discord import Embed, app_commands
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Activity
import sys
from pathlib import Path
from services import time_service, pb_service
import pyimgur

# Get sibling dependencies
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))


class SubmissionCog(commands.Cog):
    def __init__(self, bot: commands.Bot, logger: logging.Logger | None = None):
        self.bot = bot
        self.logger = logger or logging.getLogger(__name__)
        self.logger.info("Submission cog initialized")

    async def activity_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        db: Session = next(get_db())
        try:
            query = db.query(Activity)
            if current:
                query = query.filter(Activity.activity_name.ilike(f"%{current}%"))
            activities = query.order_by(Activity.activity_name).limit(25).all()
            return [
                app_commands.Choice(
                    name=activity.activity_name, value=activity.activity_name
                )
                for activity in activities
            ]
        finally:
            db.close()

    @app_commands.command(name="submit_a_pb", description="Submit a PB for an activity")
    @app_commands.describe(activity="Choose the activity to submit a PB for")
    @app_commands.autocomplete(activity=activity_autocomplete)
    async def submit_a_pb(
        self,
        interaction: discord.Interaction,
        activity: str,
        pb_obtained: str,
        player_names: str,
        image: discord.Attachment | None = None,
    ):
        # Get the activity from the db
        db: Session = next(get_db())
        try:
            activity_record = (
                db.query(Activity)
                .filter(Activity.activity_name.ilike(activity))
                .first()
            )
        except Exception as e:
            await interaction.response.send_message("Error", e)

        changelog_channel_id = os.getenv("CHANGELOG_CHANNEL")
        changelog_channel = self.bot.get_channel(int(changelog_channel_id))

        if activity_record.is_time_based:
            is_valid, int_metric = time_service.is_valid_time_format(pb_obtained)

            if not is_valid:
                await interaction.response.send_message(
                    "Invalid time format. Please use MM:ss.ms format and make sure the time is divisible by 0.6.",
                    ephemeral=True,
                )
                return
        else:
            try:
                int_metric = int(pb_obtained)
                if int_metric < 0:
                    raise ValueError("Metric must be a non-negative integer.")
            except ValueError:
                await interaction.response.send_message(
                    "Invalid metric. Please provide a non-negative integer.",
                    ephemeral=True,
                )
                return

        await interaction.response.send_message(
            f"Thanks! Your submission has been sent for approval! Once it's approved, it will show up in {changelog_channel.jump_url}",
            ephemeral=True,
        )

        if image:
            if not image.content_type.startswith("image/"):
                await interaction.response.send_message(
                    "Invalid image type. Please upload a valid image.", ephemeral=True
                )
                return

            imgur_client = pyimgur.Imgur(os.getenv("IMGUR_CLIENT_ID"))
            test = imgur_client.upload_image(
                url=image.url,
                title=f"PB Submission for {activity} by {interaction.user.name}",
            )
            imgur_link = test.link

        id = pb_service.create_pb_submission(
            metric=int_metric,
            activity=activity,
            players_string=player_names,
            imgur_link=imgur_link if image else "",
        )

        approval_channel_id = os.getenv("APPROVAL_CHANNEL")
        if not approval_channel_id:
            await interaction.response.send_message(
                "APPROVAL_CHANNEL is not configured in .env.", ephemeral=True
            )
            return

        approval_channel = self.bot.get_channel(int(approval_channel_id))
        if not approval_channel:
            await interaction.response.send_message(
                f"Approval channel not found in the server (<{approval_channel_id}>). Please check the configuration.",
                ephemeral=True,
            )

        embed = Embed(
            title="New PB Submission",
        )

        embed.color = discord.Color.yellow()

        embed.add_field(name="Activity", value=activity, inline=False)
        embed.add_field(name="PB Obtained", value=pb_obtained, inline=False)
        embed.add_field(name="Player(s)", value=player_names, inline=False)

        if image:
            embed.set_image(url=imgur_link)

        embed.set_footer(text=id)
        message = await approval_channel.send(embed=embed)
        await message.add_reaction("✅")
        await message.add_reaction("❌")

    @app_commands.command(
        name="list_activities", description="Show all activities stored in the database"
    )
    async def list_activities(self, interaction: discord.Interaction):
        db: Session = next(get_db())
        try:
            all_activities = db.query(Activity).order_by(Activity.activity_name).all()
            if not all_activities:
                await interaction.response.send_message(
                    "No activities found in the database.", ephemeral=True
                )
                return

            activity_text = "\n".join(
                f"- {activity.activity_name}" for activity in all_activities
            )

            await interaction.response.send_message(
                f"Available activities:\n{activity_text}",
                ephemeral=True,
            )
        finally:
            db.close()


async def setup(bot: commands.Bot):
    await bot.add_cog(SubmissionCog(bot))
