from __future__ import annotations

import json
import logging
import os
import time
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import List

from prometheus_client import Counter, Gauge

from .crypto import encrypt_raw_snippet
from .db import LeakItem, get_session
from .normalizer import normalize_robin_output

logger = logging.getLogger(__name__)

INGEST_COUNTER = Counter("robin_ingest_total", "Total items accepted for processing", ["source"])
BACKLOG_GAUGE = Gauge("robin_ingest_backlog", "Approximate queued items awaiting worker")


def ingest_payload(payload: str | bytes | dict | list, source: str = "webhook") -> List[str]:
    """Normalize and persist payload, returning IDs for worker processing."""
    if isinstance(payload, (bytes, bytearray)):
        payload = payload.decode("utf-8", errors="ignore")
    normalized_items = normalize_robin_output(payload)
    stored_ids: List[str] = []
    INGEST_COUNTER.labels(source=source).inc(len(normalized_items))
    from .workers import process_item  # late import

    for item in normalized_items:
        raw = item.get("raw")
        if isinstance(raw, str):
            raw_bytes = raw.encode("utf-8")
        elif isinstance(raw, bytes):
            raw_bytes = raw
        else:
            raw_bytes = json.dumps(item, default=str).encode("utf-8")

        ciphertext, nonce, tag = encrypt_raw_snippet(raw_bytes)
        hash_key = sha256(
            (
                item["target"].value.lower()
                + item["leak_type"].lower()
                + raw_bytes.decode("utf-8", errors="ignore")
            ).encode("utf-8")
        ).hexdigest()

        with get_session() as session:
            existing = session.query(LeakItem).filter_by(hash_key=hash_key).one_or_none()
            if existing:
                existing.raw_ciphertext = ciphertext
                existing.raw_nonce = nonce
                existing.raw_tag = tag
                existing.target_type = item["target"].type
                existing.target_value = item["target"].value
                existing.leak_type = item["leak_type"]
                existing.source = item["source"]
                existing.first_seen = item["first_seen"]
                existing.last_seen = item["last_seen"]
                existing.structured_fields = item["structured_fields"]
                existing.confidence = item["confidence"]
                existing.tags = item["tags"]
                existing.notes = item.get("notes")
                session.add(existing)
                leak_id = str(existing.id)
            else:
                leak = LeakItem(
                    target_type=item["target"].type,
                    target_value=item["target"].value,
                    leak_type=item["leak_type"],
                    source=item["source"],
                    first_seen=item["first_seen"],
                    last_seen=item["last_seen"],
                    raw_ciphertext=ciphertext,
                    raw_nonce=nonce,
                    raw_tag=tag,
                    structured_fields=item["structured_fields"],
                    confidence=item["confidence"],
                    tags=item["tags"],
                    notes=item.get("notes"),
                    hash_key=hash_key,
                )
                session.add(leak)
                session.flush()
                leak_id = str(leak.id)

        process_item.delay(leak_id)
        stored_ids.append(leak_id)
        logger.info("ingest.enqueue", extra={"module": "ingest", "item_id": leak_id, "source": source})
    BACKLOG_GAUGE.set(len(stored_ids))
    return stored_ids


@dataclass
class DirectoryWatcher:
    path: Path
    interval: int = int(os.getenv("ROBIN_WATCH_INTERVAL", "5"))

    def run_forever(self) -> None:
        self.path.mkdir(parents=True, exist_ok=True)
        logger.info("watcher.start", extra={"module": "ingest", "path": str(self.path)})
        while True:
            for file in list(self.path.glob("*")):
                if file.is_file():
                    try:
                        payload = file.read_text(encoding="utf-8")
                        ingest_payload(payload, source="watcher")
                        archive = file.with_suffix(file.suffix + ".processed")
                        file.rename(archive)
                    except Exception as exc:
                        logger.exception("watcher.error", extra={"module": "ingest", "path": str(file)})
            time.sleep(self.interval)

