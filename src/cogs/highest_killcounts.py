from datetime import datetime
import logging
import os
import discord
from discord.ext import commands, tasks
from discord import app_commands
from sqlalchemy.orm import Session
from database import get_db
from models import HighestKCReprocess
from services import highest_kc_service
import sys
from pathlib import Path

# Get sibling dependencies
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))


class HighestKillcountCog(commands.Cog):
    def __init__(self, bot: commands.Bot, logger: logging.Logger | None = None):
        self.bot = bot
        self.logger = logger or logging.getLogger(__name__)
        self.logger.info("Static embed cog initialized")
        self.check_category_needs_updating.start()

    @tasks.loop(seconds=4)
    async def check_category_needs_updating(self):
        print("Checking if any categories need updating...")
        db: Session = next(get_db())
        highest_kc_reprocess = (
            db.query(HighestKCReprocess)
            .filter(HighestKCReprocess.next_update < datetime.now())
            .first()
        )
        if highest_kc_reprocess:
            print(
                f"Found category that needs updating: {highest_kc_reprocess.category}, message: {highest_kc_reprocess.discord_message_id}"
            )
            # Get the message thread by ID

            channel = await self.bot.fetch_channel(os.getenv("HIGHEST_KC_CHANNEL"))
            print(channel)
            if not channel:
                print("Could not find channel!")
                return

            message = await channel.fetch_message(
                highest_kc_reprocess.discord_message_id
            )

            new_embed: discord.Embed = await highest_kc_service.build_highest_kcs_embed(
                highest_kc_reprocess.category
            )
            print(new_embed.fields)
            # Edit the message with new data
            await message.edit(embed=new_embed)
            highest_kc_service.update_reprocess_record(
                message, highest_kc_reprocess.category
            )

        else:
            print("All clear!")
        db.commit()

    @app_commands.command(
        name="post_highest_kcs",
        description="Displays highest killcount embeds from scratch",
    )
    @app_commands.choices(
        category=[
            app_commands.Choice(name="God Wars Dungeon", value=0),
            app_commands.Choice(name="Wilderness", value=1),
            app_commands.Choice(name="Raids", value=2),
            app_commands.Choice(name="Slayer", value=3),
            app_commands.Choice(name="Money Bosses", value=4),
            app_commands.Choice(name="Other", value=5),
            app_commands.Choice(name="Trial Content", value=6),
            app_commands.Choice(name="Desert Treasure 2", value=7),
            app_commands.Choice(name="Misc Activities", value=8),
        ]
    )
    async def post_highest_kcs(self, interaction: discord.Interaction, category: int):

        # ------- Build the Highest KCs embed -------
        try:
            highest_kcs_embed = await highest_kc_service.build_highest_kcs_embed(
                category
            )
            message = await interaction.channel.send(embed=highest_kcs_embed)

        except Exception as e:
            await interaction.response.send_message(
                "Error building the highest kcs embed", e, ephemeral=True
            )

        # ------- Insert the record into the reprocess table -------
        highest_kc_service.insert_reprocess_record(message, category)


async def setup(bot: commands.Bot):
    await bot.add_cog(HighestKillcountCog(bot))
