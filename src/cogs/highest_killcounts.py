import logging
import os
import discord
import wom
from discord.ext import commands
from discord import app_commands
from embeds import Embeds
from typing import List, Tuple

class HighestKillcountCog(commands.Cog):
    def __init__(self, bot: commands.Bot, logger: logging.Logger | None = None):
        self.bot = bot
        self.logger = logger or logging.getLogger(__name__)
        self.logger.info("Static embed cog initialized")

    @app_commands.command(name="post_highest_kcs", description="Displays highest killcount embeds from scratch")
    async def post_highest_kcs(
        self,
        interaction: discord.Interaction,
        category: int = 1
    ):
        await interaction.response.defer(thinking=True)
        wom = WiseOldManClient()
        await wom._connect()
        data = {}
        group = all_boss_groups[category-1]
        for boss in group.bosses:
            if category == 1:
                metric = boss
                category_name = 'God Wars Dungeon'
            elif category == 2:
                metric = boss
                category_name = 'Raids'

            normies, irons = await wom.get_top_placements_hiscores(metric=metric)

            data[boss] = {
                "normie": {
                    "name": normies[0].player.username,
                    "kills": normies[0].data.kills
                },
                "iron": {
                    "name": irons[0].player.username,
                    "kills": irons[0].data.kills
                }
            }

        await interaction.channel.send(embed=Embeds.highest_kcs(data, category_name))
        await interaction.response.send_message(f"Displaying the highest KCs, {interaction.user.mention}!", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(HighestKillcountCog(bot))


KITTY_GROUP_ID: int = 1165


class WiseOldManClient:
    def __init__(self) -> None:
        wom_token = os.getenv("WOM_TOKEN")
        self.client = wom.Client(wom_token)
        self.logger = logging.getLogger("discord")

    async def _connect(self) -> None:
        await self.client.start()

    async def _disconnect(self) -> None:
        await self.client.close()

    async def get_top_placements_players(self, players: List[wom.GroupHiscoresEntry], placements: int = 1) -> Tuple[List[wom.Player], List[wom.Player]]:
        top_placements_normal_players = [player for player in players if player.player.type == wom.PlayerType.Regular][:placements]
        top_placements_iron_players = [
            player
            for player in players
            if player.player.type
            in (
                wom.PlayerType.Ironman,
                wom.PlayerType.Hardcore,
                wom.PlayerType.Ultimate,
            )
        ][:placements]
        return top_placements_normal_players, top_placements_iron_players

    async def get_top_placements_hiscores(
        self,
        metric: wom.Metric,
        group_id: int = KITTY_GROUP_ID,
        number_of_ranks: int = 30,
        placements: int = 1,
    ) -> Tuple[List[wom.Player], List[wom.Player]]:
        
        result = await self.client.groups.get_hiscores(id=group_id, metric=metric, limit=number_of_ranks)
        
        if result.is_ok:
            return await self.get_top_placements_players(players=result.unwrap(), placements=placements)
        else:
            self.logger.critical("WOM error: %s" % result.unwrap_err)

        return [], []

from dataclasses import dataclass
from typing import List

import wom


@dataclass()
class HiscoreBossGroup:
    name: str
    url: str
    bosses: List[wom.Bosses]


gwd = HiscoreBossGroup(
    name="God Wars Dungeon",
    url="https://oldschool.runescape.wiki/images/General_Graardor.png?4dd90",
    bosses=[
        wom.Metric.CommanderZilyana,
        wom.Metric.GeneralGraardor,
        wom.Metric.KrilTsutsaroth,
        wom.Metric.Kreearra,
        wom.Metric.Nex
    ],
)

# wilderness = HiscoreBossGroup(
#     name="Wilderness",
#     url="https://oldschool.runescape.wiki/images/Calvar%27ion_%28enraged%29.png?6268f",
#     bosses=[
#         wom.Bosses.Callisto,
#         wom.Bosses.Vetion,
#         wom.Bosses.Venenatis,
#         wom.Bosses.Artio,
#         wom.Bosses.Calvarion,
#         wom.Bosses.Spindel,
#         wom.Bosses.Scorpia,
#         wom.Bosses.ChaosElemental,
#         wom.Bosses.KingBlackDragon,
#         wom.Bosses.CorporealBeast,
#         wom.Bosses.ChaosFanatic,
#         wom.Bosses.CrazyArchaeologist,
#     ],
# )

# slayer = HiscoreBossGroup(
#     name="Slayer",
#     url="https://oldschool.runescape.wiki/images/Cerberus.png?47f4c",
#     bosses=[
#         wom.Bosses.GrotesqueGuardians,
#         wom.Bosses.AbyssalSire,
#         wom.Bosses.Kraken,
#         wom.Bosses.Cerberus,
#         wom.Bosses.ThermonuclearSmokeDevil,
#         wom.Bosses.AlchemicalHydra,
#         wom.Bosses.Skotizo,
#         wom.Bosses.DagannothSupreme,
#         wom.Bosses.DagannothPrime,
#         wom.Bosses.DagannothRex,
#     ],
# )

raids = HiscoreBossGroup(
    name="Raids",
    url="https://oldschool.runescape.wiki/images/Verzik_Vitur_%28final_form%29.png?f9733",
    bosses=[
        wom.Metric.ChambersOfXeric,
        wom.Metric.ChambersOfXericChallenge,
        wom.Metric.TheatreOfBlood,
        wom.Metric.TheatreOfBloodHard,
        wom.Metric.TombsOfAmascut,
        wom.Metric.TombsOfAmascutExpert,
    ],
)

# money_bosses = HiscoreBossGroup(
#     name="Money Bosses",
#     url="https://oldschool.runescape.wiki/images/Zulrah_%28tanzanite%29.png?fd984",
#     bosses=[
#         wom.Bosses.Zulrah,
#         wom.Bosses.Vorkath,
#         wom.Bosses.PhantomMuspah,
#         wom.Bosses.Nightmare,
#         wom.Bosses.PhosanisNightmare,
#     ],
# )

# tzhaar = HiscoreBossGroup(
#     name="Tzhaar",
#     url="https://oldschool.runescape.wiki/images/JalTok-Jad.png?7e369",
#     bosses=[
#         wom.Bosses.TzTokJad,
#         wom.Bosses.TzKalZuk,
#     ],
# )

# gauntlet = HiscoreBossGroup(
#     name="Gauntlet",
#     url="https://oldschool.runescape.wiki/images/Crystalline_Hunllef.png?7737a",
#     bosses=[
#         wom.Bosses.TheGauntlet,
#         wom.Bosses.TheCorruptedGauntlet,
#     ],
# )

# dt2 = HiscoreBossGroup(
#     name="Desert Treasure 2",
#     url="https://oldschool.runescape.wiki/images/The_Leviathan.png?d588a",
#     bosses=[
#         wom.Bosses.DukeSucellus,
#         wom.Bosses.TheLeviathan,
#         wom.Bosses.Vardorvis,
#         wom.Bosses.TheWhisperer,
#     ],
# )

# other = HiscoreBossGroup(
#     name="Other",
#     url="https://oldschool.runescape.wiki/images/The_Mimic.png?b45f4",
#     bosses=[
#         wom.Bosses.BarrowsChests,
#         wom.Bosses.GiantMole,
#         wom.Bosses.DerangedArchaeologist,
#         wom.Bosses.Sarachnis,
#         wom.Bosses.KalphiteQueen,
#         wom.Bosses.Obor,
#         wom.Bosses.Bryophyta,
#         wom.Bosses.Mimic,
#         wom.Bosses.Hespori,
#         wom.Bosses.Zalcano,
#     ],
# )

# activities = HiscoreBossGroup(
#     name="Activities",
#     url="https://oldschool.runescape.wiki/images/Clue_scroll_%28master%29_detail.png?f3c22",
#     bosses=[
#         wom.Activities.ClueScrollsAll,
#         wom.Activities.ClueScrollsBeginner,
#         wom.Activities.ClueScrollsEasy,
#         wom.Activities.ClueScrollsMedium,
#         wom.Activities.ClueScrollsHard,
#         wom.Activities.ClueScrollsElite,
#         wom.Activities.ClueScrollsMaster,
#         wom.Activities.GuardiansOfTheRift,
#         wom.Activities.BountyHunterHunter,
#         wom.Activities.LastManStanding,
#     ],
# )


all_boss_groups = [
    gwd,
    raids,
    # wilderness,
    # slayer,
    # money_bosses,
    # tzhaar,
    # gauntlet,
    # dt2,
    # other,
    # activities,
]
