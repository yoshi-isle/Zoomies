from datetime import date, datetime
from sqlalchemy import DateTime, Integer, String, Boolean, BigInteger, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Activity(Base):
    __tablename__ = "activity"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    activity_name: Mapped[str] = mapped_column(String(50), nullable=False)
    category: Mapped[int] = mapped_column(Integer, nullable=False)
    is_time_based: Mapped[bool] = mapped_column(Boolean, nullable=False)
    emoji: Mapped[str] = mapped_column(String(50), nullable=True)
    team_size: Mapped[int] = mapped_column(Integer, nullable=False)

    def __repr__(self):
        return f"<Activity(id={self.id}, name='{self.activity_name}')>"


class Submission(Base):
    __tablename__ = "submission"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    activity: Mapped[int] = mapped_column(Integer, nullable=False)
    create_time: Mapped[date] = mapped_column(Date, nullable=False)
    players: Mapped[str] = mapped_column(String(250), nullable=False)
    metric: Mapped[int] = mapped_column(BigInteger, nullable=False)
    imgur_url: Mapped[str] = mapped_column(String(50), nullable=True)
    is_approved: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<Submission(id={self.id}, metric={self.metric})>"


class HighestKCReprocess(Base):
    __tablename__ = "highest_kc_reprocess"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    discord_message_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    category: Mapped[int] = mapped_column(Integer, nullable=False)
    next_update: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    def __repr__(self):
        return f"<HighestKCReprocess(id={self.id}, category={self.category})>"


class PBCategoryReprocess(Base):
    __tablename__ = "pb_category_reprocess"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    discord_message_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    category: Mapped[int] = mapped_column(Integer, nullable=False)

    def __repr__(self):
        return f"<PBCategory(id={self.id}, category={self.category})>"
