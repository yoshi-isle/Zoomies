import logging
import discord
from discord.ext import commands
from discord import app_commands
from embeds import Embeds
from cogs.constants.highscore_boss_group import HiscoreBossGroup, all_boss_groups
from cogs.services.wom_client import WiseOldManClient


class HighestKillcountCog(commands.Cog):
    def __init__(self, bot: commands.Bot, logger: logging.Logger | None = None):
        self.bot = bot
        self.logger = logger or logging.getLogger(__name__)
        self.logger.info("Static embed cog initialized")

    @app_commands.command(
        name="post_highest_kcs",
        description="Displays highest killcount embeds from scratch",
    )
    async def post_highest_kcs(self, interaction: discord.Interaction, category: int):
        wom_client = WiseOldManClient()
        await wom_client._connect()
        data = {}
        group: HiscoreBossGroup = all_boss_groups[category]

        for boss in group.bosses:
            normies, irons = await wom_client.get_top_placements_hiscores(metric=boss)
            data[boss] = {
                "normie": {
                    "name": normies[0].player.username,
                    "kills": normies[0].data.kills,
                },
                "iron": {
                    "name": irons[0].player.username,
                    "kills": irons[0].data.kills,
                },
            }

        await interaction.channel.send(embed=Embeds.highest_kcs(data, group.name))
        await interaction.response.send_message(
            f"Displaying the highest KCs, {interaction.user.mention}!", ephemeral=True
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(HighestKillcountCog(bot))
