from __future__ import annotations

import os
from typing import Dict

CONFIDENCE_WEIGHT = float(os.getenv("C_WEIGHT", 50))
IMPACT_WEIGHT = float(os.getenv("I_WEIGHT", 30))
TIMELINESS_WEIGHT = float(os.getenv("T_WEIGHT", 20))

IMPACT_MAP = {
    "email-only": 0.4,
    "credential": 0.9,
    "token": 1.0,
    "db_dump_with_pii": 0.95,
}


def impact_factor(structured_fields: Dict[str, any]) -> float:
    if structured_fields.get("token"):
        return IMPACT_MAP["token"]
    if structured_fields.get("password") or structured_fields.get("password_present"):
        return IMPACT_MAP["credential"]
    if structured_fields.get("pii_records"):
        return IMPACT_MAP["db_dump_with_pii"]
    return IMPACT_MAP["email-only"]


def timeliness_factor(first_seen, last_seen) -> float:
    if not first_seen or not last_seen:
        return 0.4
    delta_days = (last_seen - first_seen).days or 1
    if delta_days <= 7:
        return 1.0
    if delta_days <= 30:
        return 0.7
    return 0.5


def compute_score(confidence: float, structured_fields: Dict[str, any], first_seen, last_seen) -> int:
    impact = impact_factor(structured_fields)
    timeliness = timeliness_factor(first_seen, last_seen)
    score = round((confidence * CONFIDENCE_WEIGHT) + (impact * IMPACT_WEIGHT) + (timeliness * TIMELINESS_WEIGHT))
    return min(score, 100)

