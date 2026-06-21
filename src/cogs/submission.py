import logging
import discord
from discord.ext import commands
from discord import app_commands
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Activity

class SubmissionCog(commands.Cog):
    def __init__(self, bot: commands.Bot, logger: logging.Logger | None = None):
        self.bot = bot
        self.logger = logger or logging.getLogger(__name__)
        self.logger.info("Submission cog initialized")

    @app_commands.command(name="ping", description="ping")
    async def ping(
        self,
        interaction: discord.Interaction,
    ):
        
        await interaction.response.send_message(f"pong {interaction.user.mention}!", ephemeral=True)

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
                app_commands.Choice(name=activity.activity_name, value=activity.activity_name)
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
    ):
        await interaction.response.send_message(
            f"Submitting: **{activity}**",
            ephemeral=True,
        )

    @app_commands.command(name="list_activities", description="Show all activities stored in the database")
    async def list_activities(self, interaction: discord.Interaction):
        db: Session = next(get_db())
        try:
            all_activities = db.query(Activity).order_by(Activity.activity_name).all()
            if not all_activities:
                await interaction.response.send_message("No activities found in the database.", ephemeral=True)
                return

            activity_text = "\n".join(f"- {activity.activity_name}" for activity in all_activities)
            if len(activity_text) > 1900:
                activity_text = activity_text[:1900] + "\n...and more"

            await interaction.response.send_message(
                f"Available activities:\n{activity_text}",
                ephemeral=True,
            )
        finally:
            db.close()

async def setup(bot: commands.Bot):
    await bot.add_cog(SubmissionCog(bot))