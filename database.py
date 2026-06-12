import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from models import Base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=False)   # echo=True for debugging
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Create tables if they don't exist yet"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency pattern - recommended for cogs"""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()