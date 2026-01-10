from __future__ import annotations

import logging
import os
import threading
from typing import Generator, List
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, PlainTextResponse, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from sqlalchemy.orm import Session

from ..crypto import decrypt_raw_snippet
from ..db import ActionLog, LeakItem, get_session, init_db
from ..ingest import DirectoryWatcher, ingest_payload
from ..models import (
    ActionCreate,
    CanonicalItem,
    HealthResponse,
    IngestRequest,
    ItemListResponse,
    RawSnippetRequest,
    TargetModel,
)
from ..workers import app as celery_app
from .dashboard import render_dashboard

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="VulnForge Robin Integration", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db() -> Generator[Session, None, None]:
    with get_session() as session:
        yield session


def serialize_item(leak: LeakItem) -> CanonicalItem:
    return CanonicalItem(
        id=leak.id,
        target=TargetModel(type=leak.target_type, value=leak.target_value),
        leak_type=leak.leak_type,
        source=leak.source,
        first_seen=leak.first_seen,
        last_seen=leak.last_seen,
        raw_snippet=leak.raw_ciphertext,
        structured_fields=leak.structured_fields or {},
        confidence=leak.confidence or 0.5,
        tags=leak.tags or [],
        enrichment=leak.enrichment or {},
        score=leak.score or 0,
        actions=[
            {
                "action": action.action,
                "actor": action.actor,
                "notes": action.notes,
                "timestamp": action.timestamp.isoformat(),
            }
            for action in leak.actions
        ],
        notes=leak.notes,
    )


@app.on_event("startup")
async def startup_event():
    init_db()
    watch_path = os.getenv("ROBIN_OUTPUT_DIR")
    if watch_path:
        watcher = DirectoryWatcher(path=Path(watch_path))

        def _run_watcher():
            try:
                watcher.run_forever()
            except Exception:  # pragma: no cover
                logger.exception("watcher.crash")

        threading.Thread(target=_run_watcher, daemon=True).start()
        logger.info("watcher.thread.started", extra={"path": watch_path})


@app.get("/", response_class=HTMLResponse)
async def dashboard():
    return render_dashboard()


@app.post("/ingest")
async def ingest_endpoint(request: IngestRequest):
    ids = ingest_payload(request.payload, source=request.source)
    return {"ingested": len(ids), "ids": ids}


@app.get("/items", response_model=ItemListResponse)
async def list_items(
    leak_type: str | None = Query(default=None),
    tag: str | None = Query(default=None),
    min_score: int | None = Query(default=None),
    max_score: int | None = Query(default=None),
    limit: int = Query(default=50, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    query = db.query(LeakItem)
    if leak_type:
        query = query.filter(LeakItem.leak_type == leak_type)
    if tag:
        query = query.filter(LeakItem.tags.contains([tag]))
    if min_score is not None:
        query = query.filter(LeakItem.score >= min_score)
    if max_score is not None:
        query = query.filter(LeakItem.score <= max_score)

    total = query.count()
    items = query.order_by(LeakItem.created_at.desc()).offset(offset).limit(limit).all()
    return ItemListResponse(total=total, items=[serialize_item(item) for item in items])


@app.get("/items/{item_id}", response_model=CanonicalItem)
async def get_item(item_id: str, db: Session = Depends(get_db)):
    leak = db.get(LeakItem, item_id)
    if not leak:
        raise HTTPException(status_code=404, detail="Item not found")
    return serialize_item(leak)


@app.post("/items/{item_id}/actions")
async def create_action(
    item_id: str, action: ActionCreate, db: Session = Depends(get_db)
):
    leak = db.get(LeakItem, item_id)
    if not leak:
        raise HTTPException(status_code=404, detail="Item not found")
    record = ActionLog(
        item_id=item_id, action=action.action, actor=action.actor, notes=action.notes
    )
    db.add(record)
    db.flush()
    logger.info("action.recorded", extra={"item_id": item_id, "action": action.action})
    return {"status": "ok"}


@app.post("/items/{item_id}/decrypt")
async def decrypt_snippet(
    item_id: str, body: RawSnippetRequest, db: Session = Depends(get_db)
):
    if body.reviewer_password != os.getenv("REVIEWER_PASSWORD"):
        raise HTTPException(status_code=403, detail="Invalid reviewer password")
    leak = db.get(LeakItem, item_id)
    if not leak:
        raise HTTPException(status_code=404, detail="Item not found")
    plaintext = decrypt_raw_snippet(leak.raw_ciphertext, leak.raw_nonce, leak.raw_tag)
    return {"raw_snippet": plaintext.decode("utf-8", errors="ignore")}


@app.get("/healthz", response_model=HealthResponse)
async def healthz(db: Session = Depends(get_db)):
    broker_ok = False
    try:
        db.execute("SELECT 1")
        db_ok = True
    except Exception:
        db_ok = False
    try:
        insp = celery_app.control.inspect(timeout=1)
        ping = insp.ping() if insp else None
        broker_ok = bool(ping)
    except Exception:
        broker_ok = False
    status = "ok" if db_ok and broker_ok else "degraded"
    return HealthResponse(status=status, broker_ok=broker_ok, db_ok=db_ok)


@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
