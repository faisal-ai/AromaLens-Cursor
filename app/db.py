from __future__ import annotations
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./perfume.db")

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()

# For SQLite, need check_same_thread=False for multithreaded FastAPI
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, echo=False, future=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    # Import models here to ensure metadata is populated
    from . import models  # noqa: F401
    Base.metadata.create_all(bind=engine)