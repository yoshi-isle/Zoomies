import logging
import discord
from discord.ext import commands
from discord import app_commands
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Activity
import sys
from pathlib import Path
from services import time_service, pb_service

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
        self, interaction: discord.Interaction, activity: str, pb_obtained: str
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
            "Your submission is valid and ready",
            ephemeral=True,
        )

        pb_service.create_pb_submission(
            metric=int_metric,
            activity=activity,
            players_string="Test, 123",
        )

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
