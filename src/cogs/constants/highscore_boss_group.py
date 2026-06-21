import wom


class HiscoreBossGroup:
    def __init__(self, name, url, bosses):
        self.name = name
        self.url = url
        self.bosses = bosses


all_boss_groups = [
    HiscoreBossGroup(
        name="God Wars Dungeon",
        url="https://oldschool.runescape.wiki/images/General_Graardor.png?4dd90",
        bosses=[
            wom.Metric.CommanderZilyana,
            wom.Metric.GeneralGraardor,
            wom.Metric.KrilTsutsaroth,
            wom.Metric.Kreearra,
            wom.Metric.Nex,
        ],
    ),
    HiscoreBossGroup(
        name="Wilderness",
        url="https://oldschool.runescape.wiki/images/Calvar%27ion_%28enraged%29.png?6268f",
        bosses=[
            wom.Metric.ChaosFanatic,
            wom.Metric.CrazyArchaeologist,
            wom.Metric.Artio,
            wom.Metric.Callisto,
            wom.Metric.Calvarion,
            wom.Metric.Vetion,
            wom.Metric.Spindel,
            wom.Metric.Venenatis,
            wom.Metric.Scorpia,
            wom.Metric.ChaosElemental,
            wom.Metric.KingBlackDragon,
            wom.Metric.CorporealBeast,
        ],
    ),
    HiscoreBossGroup(
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
    ),
    HiscoreBossGroup(
        name="Slayer",
        url="https://oldschool.runescape.wiki/images/Cerberus.png?47f4c",
        bosses=[
            wom.Metric.DagannothSupreme,
            wom.Metric.DagannothPrime,
            wom.Metric.DagannothRex,
            wom.Metric.Skotizo,
            wom.Metric.Kraken,
            wom.Metric.AbyssalSire,
            wom.Metric.GrotesqueGuardians,
            wom.Metric.ThermonuclearSmokeDevil,
            wom.Metric.Cerberus,
            wom.Metric.AlchemicalHydra,
            wom.Metric.Araxxor,
            wom.Metric.ShellbaneGryphon,
        ],
    ),
    HiscoreBossGroup(
        name="Money Bosses",
        url="https://oldschool.runescape.wiki/images/Zulrah_%28tanzanite%29.png?fd984",
        bosses=[
            wom.Metric.Zulrah,
            wom.Metric.Vorkath,
            wom.Metric.PhantomMuspah,
            wom.Metric.Nightmare,
            wom.Metric.PhosanisNightmare,
            wom.Metric.TheGauntlet,
            wom.Metric.TheCorruptedGauntlet,
        ],
    ),
    HiscoreBossGroup(
        name="Other",
        url="https://oldschool.runescape.wiki/images/The_Mimic.png?b45f4",
        bosses=[
            wom.Metric.BarrowsChests,
            wom.Metric.LunarChests,
            wom.Metric.GiantMole,
            wom.Metric.DerangedArchaeologist,
            wom.Metric.Sarachnis,
            wom.Metric.KalphiteQueen,
            wom.Metric.Obor,
            wom.Metric.Bryophyta,
            wom.Metric.Mimic,
            wom.Metric.Hespori,
            wom.Metric.Zalcano,
            wom.Metric.TheRoyalTitans,
            wom.Metric.Yama,
            wom.Metric.Amoxliatl,
            wom.Metric.Brutus,
            wom.Metric.DoomOfMokhaiotl,
        ],
    ),
    HiscoreBossGroup(
        name="Trial Content",
        url="https://oldschool.runescape.wiki/images/JalTok-Jad.png?7e369",
        bosses=[
            wom.Metric.TzTokJad,
            wom.Metric.TzKalZuk,
            wom.Metric.SolHeredit,
            wom.Metric.ColosseumGlory,
        ],
    ),
    HiscoreBossGroup(
        name="Desert Treasure 2",
        url="https://oldschool.runescape.wiki/images/The_Leviathan.png?d588a",
        bosses=[
            wom.Metric.DukeSucellus,
            wom.Metric.TheLeviathan,
            wom.Metric.Vardorvis,
            wom.Metric.TheWhisperer,
        ],
    ),
    HiscoreBossGroup(
        name="Misc Activities",
        url="https://oldschool.runescape.wiki/images/Clue_scroll_%28master%29_detail.png?f3c22",
        bosses=[
            wom.Metric.ClueScrollsAll,
            wom.Metric.Tempoross,
            wom.Metric.GuardiansOfTheRift,
            wom.Metric.BountyHunterHunter,
            wom.Metric.LastManStanding,
            wom.Metric.CollectionsLogged,
            wom.Metric.Overall,
            wom.Metric.Ehb,
            wom.Metric.Ehp,
        ],
    ),
]
