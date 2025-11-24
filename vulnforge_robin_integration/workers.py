from __future__ import annotations

import asyncio
import logging
import os

from celery import Celery
from prometheus_client import Counter

from .db import LeakItem, get_session
from .enricher import enrich
from .scoring import compute_score

logger = logging.getLogger(__name__)

BROKER_URL = os.getenv("BROKER_URL", "redis://localhost:6379/0")
RESULT_BACKEND = os.getenv("RESULT_BACKEND", BROKER_URL)

app = Celery(
    "vulnforge_robin",
    broker=BROKER_URL,
    backend=RESULT_BACKEND,
    include=["vulnforge_robin_integration.workers"],
)
if os.getenv("CELERY_EAGER") == "1":
    app.conf.task_always_eager = True

PROCESSED_COUNTER = Counter(
    "robin_items_processed_total", "Total processed items via worker"
)


@app.task(name="vulnforge_robin.process_item")
def process_item(leak_id: str) -> None:
    logger.info("worker.process_item.start", extra={"item_id": leak_id})
    with get_session() as session:
        leak: LeakItem | None = session.get(LeakItem, leak_id)
        if not leak:
            logger.warning("worker.process_item.missing", extra={"item_id": leak_id})
            return
        structured = leak.structured_fields or {}
        try:
            enrichment = asyncio.run(enrich(structured, leak.target_value))
        except Exception as exc:
            logger.exception(
                "worker.enrich.error", extra={"item_id": leak_id, "error": str(exc)}
            )
            enrichment = {"error": str(exc)}

        leak.enrichment = enrichment
        leak.score = compute_score(
            leak.confidence or 0.5, structured, leak.first_seen, leak.last_seen
        )
        session.add(leak)
        logger.info(
            "worker.process_item.completed",
            extra={"item_id": leak_id, "score": leak.score},
        )
        PROCESSED_COUNTER.inc()
