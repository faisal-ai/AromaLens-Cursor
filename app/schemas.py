from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field


class IngredientBase(BaseModel):
    name: str
    cas_number: Optional[str] = None
    tags: Optional[List[str]] = None
    volatility_class: Optional[str] = Field(None, pattern="^(top|heart|base)$")
    default_odour_notes: Optional[str] = None


class IngredientCreate(IngredientBase):
    pass


class IngredientRead(IngredientBase):
    id: int

    class Config:
        from_attributes = True


class CompoundIngredientIn(BaseModel):
    ingredient_id: Optional[int] = None
    ingredient_name: Optional[str] = None
    percentage: float


class CompoundBase(BaseModel):
    name: str
    description: Optional[str] = None


class CompoundCreate(CompoundBase):
    items: List[CompoundIngredientIn]


class CompoundRead(CompoundBase):
    id: int
    items: List[dict]

    class Config:
        from_attributes = True


class AnalysisResult(BaseModel):
    summary: str
    olfactive_family: List[str] = []
    top_notes: List[dict] = []
    heart_notes: List[dict] = []
    base_notes: List[dict] = []
    accords: List[dict] = []
    volatility_profile: dict = {}
    projection: Optional[str] = None
    longevity_hours: Optional[float] = None
    similar_popular_scents: List[dict] = []
    improvement_suggestions: List[dict] = []
    safety_compliance: Optional[dict] = None
    risks: List[dict] = []
    confidence: Optional[float] = None


class AnalysisRead(BaseModel):
    id: int
    compound_id: int
    model: str
    prompt_version: str
    prompt_text: str
    raw_response: str
    result_json: Optional[AnalysisResult]

    class Config:
        from_attributes = True