from __future__ import annotations
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from ..db import get_db
from .. import models, schemas

router = APIRouter()


def _get_or_create_ingredient(db: Session, name: str) -> models.Ingredient:
    result = db.execute(select(models.Ingredient).where(models.Ingredient.name.ilike(name))).scalar_one_or_none()
    if result:
        return result
    ingredient = models.Ingredient(name=name.strip())
    db.add(ingredient)
    db.flush()
    return ingredient


@router.post("", response_model=schemas.CompoundRead)
def create_compound(data: schemas.CompoundCreate, db: Session = Depends(get_db)):
    compound = models.Compound(name=data.name, description=data.description)
    db.add(compound)
    db.flush()

    items_out: list[dict] = []
    for item in data.items:
        if item.ingredient_id is None and not item.ingredient_name:
            raise HTTPException(status_code=400, detail="Each item requires ingredient_id or ingredient_name")
        if item.ingredient_id is not None:
            ingredient = db.get(models.Ingredient, item.ingredient_id)
            if not ingredient:
                raise HTTPException(status_code=404, detail=f"Ingredient {item.ingredient_id} not found")
        else:
            ingredient = _get_or_create_ingredient(db, item.ingredient_name or "")
        ci = models.CompoundIngredient(compound_id=compound.id, ingredient_id=ingredient.id, percentage=item.percentage)
        db.add(ci)
        items_out.append({"ingredient_id": ingredient.id, "ingredient_name": ingredient.name, "percentage": item.percentage})
    db.commit()
    return {"id": compound.id, "name": compound.name, "description": compound.description, "items": items_out}


@router.get("/{compound_id}", response_model=schemas.CompoundRead)
def get_compound(compound_id: int, db: Session = Depends(get_db)):
    compound = db.get(models.Compound, compound_id)
    if not compound:
        raise HTTPException(status_code=404, detail="Compound not found")
    items = [
        {"ingredient_id": ci.ingredient_id, "ingredient_name": ci.ingredient.name, "percentage": ci.percentage}
        for ci in compound.ingredients
    ]
    return {"id": compound.id, "name": compound.name, "description": compound.description, "items": items}


@router.put("/{compound_id}", response_model=schemas.CompoundRead)
def update_compound(compound_id: int, data: schemas.CompoundCreate, db: Session = Depends(get_db)):
    compound = db.get(models.Compound, compound_id)
    if not compound:
        raise HTTPException(status_code=404, detail="Compound not found")
    compound.name = data.name
    compound.description = data.description

    # Delete existing items
    db.execute(delete(models.CompoundIngredient).where(models.CompoundIngredient.compound_id == compound.id))
    db.flush()

    items_out: list[dict] = []
    for item in data.items:
        if item.ingredient_id is None and not item.ingredient_name:
            raise HTTPException(status_code=400, detail="Each item requires ingredient_id or ingredient_name")
        if item.ingredient_id is not None:
            ingredient = db.get(models.Ingredient, item.ingredient_id)
            if not ingredient:
                raise HTTPException(status_code=404, detail=f"Ingredient {item.ingredient_id} not found")
        else:
            ingredient = _get_or_create_ingredient(db, item.ingredient_name or "")
        ci = models.CompoundIngredient(compound_id=compound.id, ingredient_id=ingredient.id, percentage=item.percentage)
        db.add(ci)
        items_out.append({"ingredient_id": ingredient.id, "ingredient_name": ingredient.name, "percentage": item.percentage})
    db.commit()
    return {"id": compound.id, "name": compound.name, "description": compound.description, "items": items_out}