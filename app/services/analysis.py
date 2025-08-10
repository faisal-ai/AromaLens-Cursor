from __future__ import annotations
import json
from typing import Any, Dict, List, Tuple
from pathlib import Path
from dataclasses import dataclass
from rapidfuzz import process, fuzz

from ..services.groq_client import get_groq_client, get_groq_model_name


@dataclass
class KnowledgeItem:
    name: str
    aliases: List[str]
    family: List[str]
    primary_notes: List[str]
    volatility: str | None
    typical_range_pct: List[float] | None
    allergens: List[str] | None


def load_knowledge() -> List[KnowledgeItem]:
    path = Path(__file__).resolve().parent.parent / "knowledge" / "ingredients_seed.json"
    data = json.loads(path.read_text())
    items: List[KnowledgeItem] = []
    for row in data:
        items.append(
            KnowledgeItem(
                name=row.get("name"),
                aliases=row.get("aliases", []) or [],
                family=row.get("family", []) or [],
                primary_notes=row.get("primary_notes", []) or [],
                volatility=row.get("volatility"),
                typical_range_pct=row.get("typical_range_pct"),
                allergens=row.get("allergens") or [],
            )
        )
    return items


_KNOWLEDGE = load_knowledge()
_NAME_INDEX = [k.name for k in _KNOWLEDGE] + [a for k in _KNOWLEDGE for a in k.aliases]


def normalize_formula(items: List[Tuple[str, float]]) -> List[Tuple[str, float]]:
    total = sum(p for _, p in items) or 1.0
    return [(name, round(p * 100.0 / total, 4)) for name, p in items]


def match_knowledge(name: str) -> KnowledgeItem | None:
    # Fuzzy match against names and aliases
    candidates = {}
    for k in _KNOWLEDGE:
        best = max(
            [fuzz.WRatio(name, k.name)] + [fuzz.WRatio(name, alias) for alias in k.aliases],
            default=0,
        )
        candidates[k.name] = best
    best_name, score = max(candidates.items(), key=lambda x: x[1])
    if score >= 85:
        for k in _KNOWLEDGE:
            if k.name == best_name:
                return k
    return None


def derive_features(normalized: List[Tuple[str, float]]):
    volatility = {"top": 0.0, "heart": 0.0, "base": 0.0}
    notes_weight: Dict[str, float] = {}
    families: Dict[str, float] = {}
    allergens: set[str] = set()

    for name, pct in normalized:
        k = match_knowledge(name)
        if k and k.volatility in volatility:
            volatility[k.volatility] += pct
        if k:
            for n in k.primary_notes:
                notes_weight[n] = notes_weight.get(n, 0.0) + pct
            for f in k.family:
                families[f] = families.get(f, 0.0) + pct
            for a in (k.allergens or []):
                allergens.add(a)

    # Normalize volatility to 100
    vol_total = sum(volatility.values()) or 1.0
    for key in volatility:
        volatility[key] = round(volatility[key] * 100.0 / vol_total, 2)

    families_sorted = sorted(families.items(), key=lambda x: x[1], reverse=True)
    top_families = [name for name, _ in families_sorted[:3]]

    notes_sorted = sorted(notes_weight.items(), key=lambda x: x[1], reverse=True)

    return {"volatility_profile": volatility, "olfactive_family": top_families, "notes_sorted": notes_sorted, "allergens": sorted(list(allergens))}


JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "olfactive_family": {"type": "array", "items": {"type": "string"}},
        "top_notes": {"type": "array"},
        "heart_notes": {"type": "array"},
        "base_notes": {"type": "array"},
        "accords": {"type": "array"},
        "volatility_profile": {"type": "object"},
        "projection": {"type": ["string", "null"]},
        "longevity_hours": {"type": ["number", "null"]},
        "similar_popular_scents": {"type": "array"},
        "improvement_suggestions": {"type": "array"},
        "safety_compliance": {"type": ["object", "null"]},
        "risks": {"type": "array"},
        "confidence": {"type": ["number", "null"]}
    },
    "required": ["summary", "olfactive_family", "top_notes", "heart_notes", "base_notes", "accords", "volatility_profile", "similar_popular_scents", "improvement_suggestions", "risks"],
    "additionalProperties": True
}


SYSTEM_PROMPT = (
    "You are an expert perfumer and fragrance evaluator. Analyze the provided formula by olfactive families, note pyramid, accords, diffusion, and longevity."
    " Consider IFRA awareness in advisory tone only."
    " Return STRICT JSON that conforms to the provided JSON schema. Do not include any non-JSON text."
)


def build_user_prompt(normalized_items: List[Tuple[str, float]], derived: dict) -> str:
    lines = ["Formula (normalized to 100%):"]
    for name, pct in normalized_items:
        lines.append(f"- {name}: {pct:.4f}%")
    lines.append("")
    lines.append("Derived features:")
    lines.append(json.dumps(derived, ensure_ascii=False))
    lines.append("")
    lines.append("Return JSON with keys: summary, olfactive_family, top_notes, heart_notes, base_notes, accords, volatility_profile, projection, longevity_hours, similar_popular_scents, improvement_suggestions, safety_compliance, risks, confidence.")
    return "\n".join(lines)


def call_llm_with_retries(prompt_text: str, schema: dict, max_retries: int = 2) -> dict:
    client = get_groq_client()
    if client is None:
        # Fallback if no API key
        return {
            "summary": "No LLM configured; returning heuristic-only advisory.",
            "olfactive_family": [],
            "top_notes": [],
            "heart_notes": [],
            "base_notes": [],
            "accords": [],
            "volatility_profile": {},
            "projection": None,
            "longevity_hours": None,
            "similar_popular_scents": [],
            "improvement_suggestions": [],
            "safety_compliance": {"flags": ["advisory-only"], "notes": "Set GROQ_API_KEY to enable full analysis."},
            "risks": [],
            "confidence": 0.0,
        }
    model = get_groq_model_name()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt_text},
        {"role": "user", "content": f"JSON schema: {json.dumps(schema)}"},
    ]
    last_text = ""
    for attempt in range(max_retries + 1):
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.2,
            max_tokens=1200,
        )
        last_text = resp.choices[0].message.content or ""
        # try to locate JSON in the output
        start = last_text.find("{")
        end = last_text.rfind("}")
        if start != -1 and end != -1 and end > start:
            maybe_json = last_text[start : end + 1]
            try:
                data = json.loads(maybe_json)
                # minimally validate required keys
                for k in schema.get("required", []):
                    if k not in data:
                        raise ValueError(f"Missing key {k}")
                return data
            except Exception:
                messages.append({"role": "user", "content": "The previous response was not valid JSON per schema. Return valid JSON only."})
                continue
    # Fallback minimal result
    return {
        "summary": "Preliminary analysis generated with limited certainty.",
        "olfactive_family": [],
        "top_notes": [],
        "heart_notes": [],
        "base_notes": [],
        "accords": [],
        "volatility_profile": {},
        "projection": None,
        "longevity_hours": None,
        "similar_popular_scents": [],
        "improvement_suggestions": [],
        "safety_compliance": {"flags": ["advisory-only"], "notes": "Run formal IFRA checks."},
        "risks": [],
        "confidence": 0.2,
    }


def analyze_formula(formula: List[Tuple[str, float]]) -> tuple[str, str, dict]:
    normalized = normalize_formula(formula)
    derived = derive_features(normalized)
    user_prompt = build_user_prompt(normalized, derived)
    result = call_llm_with_retries(user_prompt, JSON_SCHEMA)
    return user_prompt, json.dumps(result, ensure_ascii=False), result