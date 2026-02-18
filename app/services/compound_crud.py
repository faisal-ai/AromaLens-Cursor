"""Simple CRUD operations for compounds - MVP version"""
from sqlalchemy.orm import Session
from app import models
from typing import List, Dict


def create_compound(db: Session, name: str, description: str, ingredients: List[Dict]) -> int:
    """
    Create compound with ingredients

    Args:
        db: Database session
        name: Compound name
        description: Optional description
        ingredients: List of {"name": str, "percentage": float}

    Returns:
        Compound ID
    """
    compound = models.Compound(name=name, description=description)
    db.add(compound)
    db.flush()

    for ing in ingredients:
        # Get or create ingredient by name
        ingredient = db.query(models.Ingredient).filter(
            models.Ingredient.name == ing["name"]
        ).first()

        if not ingredient:
            ingredient = models.Ingredient(name=ing["name"])
            db.add(ingredient)
            db.flush()

        ci = models.CompoundIngredient(
            compound_id=compound.id,
            ingredient_id=ingredient.id,
            percentage=ing["percentage"]
        )
        db.add(ci)

    db.commit()
    return compound.id


def get_all_compounds(db: Session, search: str = "") -> List[Dict]:
    """
    Get all compounds with optional search

    Args:
        db: Database session
        search: Optional search query (filters by name)

    Returns:
        List of compound summaries
    """
    query = db.query(models.Compound)
    if search:
        query = query.filter(models.Compound.name.ilike(f"%{search}%"))

    compounds = query.order_by(models.Compound.updated_at.desc()).all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "description": c.description or "",
            "ingredient_count": len(c.ingredients),
            "updated_at": c.updated_at
        }
        for c in compounds
    ]


def get_compound(db: Session, compound_id: int) -> Dict:
    """
    Get compound with full ingredient details

    Args:
        db: Database session
        compound_id: Compound ID

    Returns:
        Full compound data with ingredients or None
    """
    compound = db.get(models.Compound, compound_id)
    if not compound:
        return None

    return {
        "id": compound.id,
        "name": compound.name,
        "description": compound.description or "",
        "ingredients": [
            {"name": ci.ingredient.name, "percentage": ci.percentage}
            for ci in compound.ingredients
        ]
    }


def delete_compound(db: Session, compound_id: int):
    """
    Delete compound (cascade deletes ingredients)

    Args:
        db: Database session
        compound_id: Compound ID to delete
    """
    compound = db.get(models.Compound, compound_id)
    if compound:
        db.delete(compound)
        db.commit()
