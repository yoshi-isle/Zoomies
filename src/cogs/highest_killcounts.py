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
        try:
            if category < 0 or category > len(all_boss_groups) - 1:
                await interaction.response.send_message(
                    f"Invalid category. Please choose a number between 0 and {len(all_boss_groups) - 1}.",
                    ephemeral=True,
                )
                return

            await interaction.response.defer()
            wom_client = WiseOldManClient()
            await wom_client._connect()
            data = {}
            group: HiscoreBossGroup = all_boss_groups[category]

            try:
                for boss in group.bosses:
                    normies, irons = await wom_client.get_top_placements_hiscores(
                        metric=boss
                    )

                    def extract_value(obj):
                        if hasattr(obj.data, "kills"):
                            return obj.data.kills
                        elif hasattr(obj.data, "count"):
                            return obj.data.count
                        return 0  # or raise an error / log it

                    data[boss] = {
                        "normie": {
                            "name": normies[0].player.username,
                            "kills": extract_value(normies[0]),
                        },
                        "iron": {
                            "name": irons[0].player.username,
                            "kills": extract_value(irons[0]),
                        },
                    }

                    def get_score(data):
                        """Safely extract and convert the relevant score/kills/level value to int."""
                        if hasattr(data, "kills"):
                            value = data.kills
                        elif hasattr(data, "score"):
                            value = data.score
                        elif hasattr(data, "count"):
                            value = data.count
                        elif hasattr(data, "experience"):
                            value = data.experience
                        elif hasattr(data, "level"):
                            value = data.level
                        else:
                            value = 0
                        try:
                            return int(float(value)) if value is not None else 0
                        except (TypeError, ValueError):
                            return 0

                    data[boss] = {
                        "normie": {
                            "name": normies[0].player.username,
                            "kills": extract_value(normies[0]),
                        },
                        "iron": {
                            "name": irons[0].player.username,
                            "kills": extract_value(irons[0]),
                        },
                    }
            except Exception as e:
                print("Failed section, skipping it", e)

            await interaction.followup.send(embed=Embeds.highest_kcs(data, group.name))

        except Exception as e:
            await interaction.response.send_message(e)


async def setup(bot: commands.Bot):
    await bot.add_cog(HighestKillcountCog(bot))
