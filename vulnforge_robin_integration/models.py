from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, validator


class TargetModel(BaseModel):
    type: str = Field(..., description="Type of target: domain, email, ip, etc.")
    value: str = Field(..., description="Target identifier")


class CanonicalItem(BaseModel):
    """Canonical schema shared between ingest, workers, and API."""

    id: UUID = Field(default_factory=uuid4)
    target: TargetModel
    leak_type: str
    source: str
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    raw_snippet: bytes = Field(..., description="AES-GCM ciphertext")
    structured_fields: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = Field(0.5, ge=0.0, le=1.0)
    tags: List[str] = Field(default_factory=list)
    enrichment: Dict[str, Any] = Field(default_factory=dict)
    score: int = 0
    actions: List[Dict[str, Any]] = Field(default_factory=list)
    notes: Optional[str] = None


class IngestRequest(BaseModel):
    source: str = Field(default="webhook")
    payload: Dict[str, Any]


class ActionCreate(BaseModel):
    action: str
    actor: str
    notes: Optional[str] = None


class ActionRecord(BaseModel):
    action: str
    actor: str
    notes: Optional[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ItemFilter(BaseModel):
    leak_type: Optional[str] = None
    tag: Optional[str] = None
    min_score: Optional[int] = None
    max_score: Optional[int] = None
    limit: int = Field(default=50, le=200)
    offset: int = Field(default=0, ge=0)


class ItemListResponse(BaseModel):
    total: int
    items: List[CanonicalItem]


class RawSnippetRequest(BaseModel):
    reviewer_password: str


class HealthResponse(BaseModel):
    status: str
    broker_ok: bool
    db_ok: bool

