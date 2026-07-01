import logging
from discord import app_commands
import discord
from discord.ext import commands
from models import PBCategoryReprocess
from services import pb_service
from embeds import Embeds


class DisplayPbsCog(commands.Cog):
    def __init__(self, bot: commands.Bot, logger: logging.Logger | None = None):
        self.bot = bot
        self.logger = logger or logging.getLogger(__name__)
        self.logger.info("DisplayPbs cog initialized")

    @app_commands.command(
        name="display_pb_category",
        description="Display the PB category in a human-readable format.",
    )
    async def display_pb_category(
        self, interaction: discord.Interaction, category: int
    ):
        message = await interaction.channel.send(
            embed=Embeds.pb_category(pb_service.get_top_pbs_for_category(category))
        )

        pb_category_reprocess = PBCategoryReprocess(
            discord_message_id=message.id, category=category
        )
        pb_service.save_pb_category_reprocess(pb_category_reprocess)


async def setup(bot: commands.Bot):
    await bot.add_cog(DisplayPbsCog(bot))
