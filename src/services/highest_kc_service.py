from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from database import get_db
from embeds import Embeds
from models import HighestKCReprocess
from services.wom_client import WiseOldManClient
import sys
from pathlib import Path
from constants import highscore_boss_group

# Get sibling dependencies
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))


def update_reprocess_record(discord_message_id: int):
    """
    Helper method that updates the reprocess record's timestamp
    """
    db: Session = next(get_db())
    highest_kc_reprocess = (
        db.query(HighestKCReprocess)
        .filter(HighestKCReprocess.discord_message_id == discord_message_id.id)
        .first()
    )
    highest_kc_reprocess.next_update = datetime.now() + timedelta(hours=6)
    db.commit()
    db.close()


def insert_reprocess_record(
    discord_message_id: int,
    category: int,
):
    """
    Helper method that inserts the reprocess record
    """
    db: Session = next(get_db())
    highest_kc_reprocess = HighestKCReprocess(
        discord_message_id=discord_message_id.id,
        category=category,
        next_update=datetime.now() + timedelta(hours=6),
    )
    db.add(highest_kc_reprocess)
    db.commit()
    db.close()


async def build_highest_kcs_embed(category: int):
    """
    Helper method that fetches top placements and builds an embed
    """
    wom_client = WiseOldManClient()
    await wom_client._connect()
    data = {}
    group: highscore_boss_group.HiscoreBossGroup = highscore_boss_group.all_boss_groups[
        category
    ]

    try:
        for boss in group.bosses:
            normies, irons = await wom_client.get_top_placements_hiscores(metric=boss)

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

    embed = Embeds.highest_kcs(data, group.name)
    return embed
