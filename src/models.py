from datetime import date
from sqlalchemy import Integer, String, Boolean, BigInteger, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class HighestKC(Base):
    __tablename__ = "highest_killcount"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message_id: Mapped[str] = mapped_column(String(50), nullable=False)
    last_processed: Mapped[date] = mapped_column(Date, nullable=False)


class Activity(Base):
    __tablename__ = "activity"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    activity_name: Mapped[str] = mapped_column(String(50), nullable=False)
    is_time_based: Mapped[bool] = mapped_column(Boolean, nullable=False)
    emoji: Mapped[str] = mapped_column(String(50), nullable=True)
    team_size: Mapped[int] = mapped_column(Integer, nullable=False)

    def __repr__(self):
        return f"<Activity(id={self.id}, name='{self.activity_name}')>"


class Submission(Base):
    __tablename__ = "submission"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    create_time: Mapped[date] = mapped_column(Date, nullable=False)
    players: Mapped[str] = mapped_column(String(250), nullable=False)
    metric: Mapped[int] = mapped_column(BigInteger, nullable=False)
    imgur_url: Mapped[str] = mapped_column(String(50), nullable=True)

    def __repr__(self):
        return f"<Submission(id={self.id}, metric={self.metric})>"


class HighestKCReprocess(Base):
    __tablename__ = "highest_kc_reprocess"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    discord_message_id: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[int] = mapped_column(Integer, nullable=False)
    metric: Mapped[int] = mapped_column(Integer, nullable=False)
    last_updated: Mapped[date] = mapped_column(Date, nullable=True)

    def __repr__(self):
        return f"<Submission(id={self.id}, metric={self.metric})>"
