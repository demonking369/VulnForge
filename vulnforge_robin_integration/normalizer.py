from __future__ import annotations

import json
import re
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional

from .models import TargetModel

DATE_PAT = re.compile(r"(\d{4}-\d{2}-\d{2})")
TARGET_PAT = re.compile(r"Target\s*[:\-]\s*(?P<value>[^\n]+)", re.IGNORECASE)
TAG_PAT = re.compile(r"#tag:(\w+)")


def _parse_markdown(content: str) -> Dict[str, Any]:
    structured: Dict[str, Any] = {}
    target_match = TARGET_PAT.search(content)
    if target_match:
        target_value = target_match.group("value").strip()
    else:
        target_value = "unknown"
    leak_type_match = re.search(
        r"Leak Type\s*[:\-]\s*(?P<lt>[^\n]+)", content, re.IGNORECASE
    )
    leak_type = leak_type_match.group("lt").strip() if leak_type_match else "unknown"
    source_match = re.search(
        r"Source\s*[:\-]\s*(?P<src>[^\n]+)", content, re.IGNORECASE
    )
    source = source_match.group("src").strip() if source_match else "robin"

    first_seen = _extract_date(content, "First Seen")
    last_seen = _extract_date(content, "Last Seen")

    tags = TAG_PAT.findall(content)
    structured["sections"] = _extract_sections(content)

    return {
        "target": TargetModel(type="domain", value=target_value),
        "leak_type": leak_type,
        "source": source,
        "first_seen": first_seen,
        "last_seen": last_seen,
        "structured_fields": structured,
        "confidence": 0.6,
        "tags": tags,
        "raw": content.encode("utf-8"),
    }


def _extract_sections(content: str) -> Dict[str, str]:
    sections = {}
    current = None
    lines = content.splitlines()
    for line in lines:
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = ""
        elif current:
            sections[current] += line + "\n"
    return sections


def _extract_date(content: str, label: str) -> Optional[datetime]:
    pattern = re.compile(rf"{label}\s*[:\-]\s*(?P<date>[^\n]+)", re.IGNORECASE)
    match = pattern.search(content)
    if not match:
        return None
    date_str = match.group("date")
    m = DATE_PAT.search(date_str)
    if not m:
        return None
    try:
        return datetime.fromisoformat(m.group(1))
    except ValueError:
        return None


def normalize_robin_output(payload: Any) -> List[Dict[str, Any]]:
    """Normalize raw Robin payload (Markdown or dict) into canonical dicts."""
    if isinstance(payload, str):
        payload = payload.strip()
        if payload.startswith("{"):
            raw_obj = json.loads(payload)
            return [_normalize_dict(raw_obj)]
        return [_parse_markdown(payload)]
    if isinstance(payload, dict):
        return [_normalize_dict(payload)]
    if isinstance(payload, list):
        return [_normalize_dict(p) for p in payload]
    raise ValueError("Unsupported payload type")


def _normalize_dict(obj: Dict[str, Any]) -> Dict[str, Any]:
    target_info = obj.get("target") or {}
    target = TargetModel(
        type=target_info.get("type", "domain"),
        value=target_info.get("value") or target_info.get("name") or "unknown",
    )

    def _parse_dt(value: Any) -> Optional[datetime]:
        if not value:
            return None
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            m = DATE_PAT.search(str(value))
            if m:
                try:
                    return datetime.fromisoformat(m.group(1))
                except ValueError:
                    return None
            return None

    structured = obj.get("structured_fields") or {}
    tags = obj.get("tags") or []

    return {
        "target": target,
        "leak_type": obj.get("leak_type") or obj.get("category") or "unknown",
        "source": obj.get("source") or "robin",
        "first_seen": _parse_dt(obj.get("first_seen")),
        "last_seen": _parse_dt(obj.get("last_seen")),
        "structured_fields": structured,
        "confidence": float(obj.get("confidence", 0.5)),
        "tags": tags,
        "raw": (obj.get("raw_snippet") or obj.get("raw") or ""),
        "notes": obj.get("notes"),
    }
