from __future__ import annotations
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..db import get_db
from .. import models, schemas

router = APIRouter()


@router.post("/bulk_upsert", response_model=List[schemas.IngredientRead])
def bulk_upsert_ingredients(items: List[schemas.IngredientCreate], db: Session = Depends(get_db)):
    created_or_existing: list[models.Ingredient] = []
    for item in items:
        name = item.name.strip()
        result = db.execute(select(models.Ingredient).where(models.Ingredient.name.ilike(name))).scalar_one_or_none()
        if result is None:
            ingredient = models.Ingredient(
                name=name,
                cas_number=item.cas_number,
                tags=",".join(item.tags) if item.tags else None,
                volatility_class=item.volatility_class,
                default_odour_notes=item.default_odour_notes,
            )
            db.add(ingredient)
            db.flush()
            created_or_existing.append(ingredient)
        else:
            # Update select fields
            if item.cas_number:
                result.cas_number = item.cas_number
            if item.tags:
                result.tags = ",".join(item.tags)
            if item.volatility_class:
                result.volatility_class = item.volatility_class
            if item.default_odour_notes:
                result.default_odour_notes = item.default_odour_notes
            created_or_existing.append(result)
    db.commit()
    return created_or_existing


@router.get("", response_model=List[schemas.IngredientRead])
def list_ingredients(q: Optional[str] = Query(None), limit: int = 100, db: Session = Depends(get_db)):
    stmt = select(models.Ingredient)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(models.Ingredient.name.ilike(like))
    stmt = stmt.limit(limit)
    results = db.execute(stmt).scalars().all()
    return results