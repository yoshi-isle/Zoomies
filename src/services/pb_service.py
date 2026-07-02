from datetime import datetime

from sqlalchemy.orm import Session

from database import get_db
from models import Activity, PBCategoryReprocess, Submission


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
        activities = (
            db.query(Activity)
            .filter(Activity.category == category)
            .all()
            .sort(key=lambda x: x.activity_name)
        )

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
            display[activity.activity_name] = (submission_list, activity.emoji)

        return display

    finally:
        db.close()


def save_pb_category_reprocess(pb_category_reprocess):
    db: Session = next(get_db())
    try:
        db.add(pb_category_reprocess)
        db.commit()
        db.refresh(pb_category_reprocess)
        return pb_category_reprocess
    finally:
        db.close()


def get_pb_submission_by_id(submission_id: int):
    db: Session = next(get_db())
    try:
        submission_record = (
            db.query(Submission).filter(Submission.id == submission_id).first()
        )
        return submission_record
    finally:
        db.close()


def get_pb_category_reprocess_by_category(category: int):
    db: Session = next(get_db())
    try:
        pb_category_reprocess_record = (
            db.query(PBCategoryReprocess)
            .filter(PBCategoryReprocess.category == category)
            .first()
        )
        return pb_category_reprocess_record
    finally:
        db.close()


def get_activity_by_id(activity_id: int):
    db: Session = next(get_db())
    try:
        activity_record = db.query(Activity).filter(Activity.id == activity_id).first()
        return activity_record
    finally:
        db.close()


def get_placement_for_activity(
    activity_id: int, metric: int, is_time_based: bool = True
):
    """
    Selects from the activity and orders by metric. Get's the placement of the metric based on the other records.
    """
    db: Session = next(get_db())
    try:
        if is_time_based:
            # For time-based activities, lower metric is better
            placement = (
                db.query(Submission)
                .filter(
                    Submission.activity == activity_id,
                    Submission.is_approved,
                    Submission.metric < metric,
                )
                .count()
                + 1
            )
        else:
            # For non-time-based activities, higher metric is better
            placement = (
                db.query(Submission)
                .filter(
                    Submission.activity == activity_id,
                    Submission.is_approved,
                    Submission.metric > metric,
                )
                .count()
                + 1
            )

        return placement
    finally:
        db.close()
