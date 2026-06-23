from datetime import datetime

from sqlalchemy.orm import Session

from database import get_db
from models import Activity, Submission


def create_pb_submission(metric: str, activity: str, players_string: str):
    db: Session = next(get_db())

    # Get the activity ID from the database based on the activity name
    activity_record = (
        db.query(Activity).filter(Activity.activity_name == activity).first()
    )

    # insert to submission table
    submission = Submission(
        metric=metric,
        activity=activity_record.id if activity_record else None,
        players=players_string,
        create_time=datetime.now(),
        imgur_url="",
        is_approved=False,
    )

    db.add(submission)
    db.commit()
    db.refresh(submission)
    db.close()
