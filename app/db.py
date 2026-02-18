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
    """Initialize database and seed ingredients if empty"""
    # Import models here to ensure metadata is populated
    from . import models  # noqa: F401
    Base.metadata.create_all(bind=engine)

    # Seed ingredients from knowledge base if empty
    _seed_ingredients_if_empty()


def _seed_ingredients_if_empty() -> None:
    """One-time seeding of ingredients from knowledge base"""
    import json
    from . import models

    db = SessionLocal()
    try:
        # Check if ingredients already exist
        if db.query(models.Ingredient).count() > 0:
            return  # Already seeded

        # Load knowledge base
        knowledge_path = os.path.join(os.path.dirname(__file__), "knowledge/ingredients_seed.json")
        if not os.path.exists(knowledge_path):
            print(f"Warning: Knowledge base not found at {knowledge_path}")
            return

        with open(knowledge_path) as f:
            data = json.load(f)

        # Seed ingredients
        for item in data:
            ingredient = models.Ingredient(
                name=item["name"],
                cas_number=item.get("cas"),
                volatility_class=item.get("volatility"),
                tags=",".join(item.get("family", []))
            )
            db.add(ingredient)

        db.commit()
        print(f"✓ Seeded {len(data)} ingredients from knowledge base")

    except Exception as e:
        print(f"Warning: Failed to seed ingredients: {e}")
        db.rollback()
    finally:
        db.close()