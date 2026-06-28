from datetime import datetime

from sqlalchemy.orm import Session

from database import get_db
from models import Activity, Submission


def create_pb_submission(
    metric: str, activity: str, players_string: str, imgur_link: str
):
    db: Session = next(get_db())

    # Get the activity ID from the database based on the activity name
    activity_record = (
        db.query(Activity).filter(Activity.activity_name == activity).first()
    )

    # Insert to submission table
    submission = Submission(
        metric=metric,
        activity=activity_record.id if activity_record else None,
        players=players_string,
        create_time=datetime.now(),
        imgur_url=imgur_link,
        is_approved=False,
    )

    db.add(submission)
    db.commit()
    db.refresh(submission)
    db.close()
    return submission.id


def approve_or_deny_pb_submission(submission_id: int, is_approved: bool):
    db: Session = next(get_db())

    # Get the submission record from the database based on the submission ID
    submission_record = (
        db.query(Submission).filter(Submission.id == submission_id).first()
    )

    if submission_record:
        submission_record.is_approved = is_approved
        db.commit()
        db.refresh(submission_record)
        db.close()
        return True
    else:
        db.close()
        return False


def get_top_pbs_for_category(category: int):
    """
    Retrieves the top 3 approved submissions for each activity
    within the specified category.
    """
    db: Session = next(get_db())

    try:
        # Get all activities for the given category
        activities = db.query(Activity).filter(Activity.category == category).all()

        # Initialize display dictionary with activity names as keys
        # Each value will be a list of up to 3 submission dictionaries
        display = {activity.activity_name: [] for activity in activities}

        for activity in activities:
            # Get the top 3 approved submissions, newest first
            top_submissions = (
                db.query(Submission)
                .filter(
                    Submission.activity == activity.id,
                    Submission.is_approved,
                )
                .order_by(Submission.metric.asc())
                .limit(3)
                .all()
            )

            # Build list of submission data
            submission_list = []
            for submission in top_submissions:
                submission_list.append(
                    {
                        "metric": submission.metric,
                        "players": submission.players,
                        "create_time": submission.create_time,
                        "imgur_url": submission.imgur_url,
                    }
                )

            # Assign the list (empty if no submissions)
            display[activity.activity_name] = submission_list

        return display

    finally:
        db.close()
