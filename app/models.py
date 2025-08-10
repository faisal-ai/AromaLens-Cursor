from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, ForeignKey, Text, JSON, DateTime, func
from .db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    compounds: Mapped[list[Compound]] = relationship("Compound", back_populates="user")


class Ingredient(Base):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    cas_number: Mapped[str | None] = mapped_column(String(64), nullable=True)
    tags: Mapped[str | None] = mapped_column(String(512), nullable=True)
    volatility_class: Mapped[str | None] = mapped_column(String(32), nullable=True)  # top|heart|base
    default_odour_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    compound_ingredients: Mapped[list[CompoundIngredient]] = relationship("CompoundIngredient", back_populates="ingredient")


class Compound(Base):
    __tablename__ = "compounds"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user: Mapped[User | None] = relationship("User", back_populates="compounds")
    ingredients: Mapped[list[CompoundIngredient]] = relationship("CompoundIngredient", back_populates="compound", cascade="all, delete-orphan")
    analyses: Mapped[list[Analysis]] = relationship("Analysis", back_populates="compound", cascade="all, delete-orphan")


class CompoundIngredient(Base):
    __tablename__ = "compound_ingredients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    compound_id: Mapped[int] = mapped_column(ForeignKey("compounds.id", ondelete="CASCADE"))
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"))
    percentage: Mapped[float] = mapped_column(Float)

    compound: Mapped[Compound] = relationship("Compound", back_populates="ingredients")
    ingredient: Mapped[Ingredient] = relationship("Ingredient", back_populates="compound_ingredients")


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    compound_id: Mapped[int] = mapped_column(ForeignKey("compounds.id", ondelete="CASCADE"))
    model: Mapped[str] = mapped_column(String(128))
    prompt_version: Mapped[str] = mapped_column(String(64))
    prompt_text: Mapped[str] = mapped_column(Text)
    raw_response: Mapped[str] = mapped_column(Text)
    result_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())

    compound: Mapped[Compound] = relationship("Compound", back_populates="analyses")