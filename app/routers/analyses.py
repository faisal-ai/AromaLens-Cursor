from __future__ import annotations
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..db import get_db
from .. import models, schemas
from ..services.analysis import analyze_formula
from ..services.groq_client import get_groq_model_name

router = APIRouter()


@router.post("/run/{compound_id}", response_model=schemas.AnalysisRead)
def run_analysis(compound_id: int, db: Session = Depends(get_db)):
    compound = db.get(models.Compound, compound_id)
    if not compound:
        raise HTTPException(status_code=404, detail="Compound not found")

    formula = [(ci.ingredient.name, ci.percentage) for ci in compound.ingredients]
    if not formula:
        raise HTTPException(status_code=400, detail="Compound has no ingredients")

    prompt_text, raw_response, parsed = analyze_formula(formula)

    analysis = models.Analysis(
        compound_id=compound.id,
        model=get_groq_model_name(),
        prompt_version="v1",
        prompt_text=prompt_text,
        raw_response=raw_response,
        result_json=parsed,
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return analysis


@router.get("/by_compound/{compound_id}", response_model=List[schemas.AnalysisRead])
def list_analyses(compound_id: int, db: Session = Depends(get_db)):
    stmt = select(models.Analysis).where(models.Analysis.compound_id == compound_id).order_by(models.Analysis.id.desc())
    results = db.execute(stmt).scalars().all()
    return results