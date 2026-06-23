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
        name="build_table_of_contents",
        description="Displays highest killcount embeds from scratch",
        link1="",
        link2="",
        link3="",
        link4="",
        link5="",
        link6="",
        link7="",
        link8="",
    )
    async def build_table_of_contents():
        pass

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
        try:
            if category < 0 or category > len(all_boss_groups) - 1:
                await interaction.response.send_message(
                    f"Invalid category. Please choose a number between 0 and {len(all_boss_groups) - 1}.",
                    ephemeral=True,
                )
                return

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
                            return obj.data.kills, "KC"
                        elif hasattr(obj.data, "score"):
                            return obj.data.score, "KC"
                        elif hasattr(obj.data, "experience"):
                            return obj.data.experience, "XP"
                        return 0, "ERROR"

                    main_amount, _ = extract_value(normies[0])
                    iron_amount, terminology = extract_value(irons[0])

                    data[boss] = {
                        "emote": group.emotes[group.bosses.index(boss)],
                        "normie": {
                            "name": normies[0].player.username,
                            "kills": main_amount,
                            "terminology": terminology,
                        },
                        "iron": {
                            "name": irons[0].player.username,
                            "kills": iron_amount,
                            "terminology": terminology,
                        },
                    }

            except Exception as e:
                print("Failed section, skipping it", e)

            await interaction.channel.send(embed=Embeds.highest_kcs(data, group.name))

        except Exception as e:
            await interaction.response.send_message(e)


async def setup(bot: commands.Bot):
    await bot.add_cog(HighestKillcountCog(bot))
