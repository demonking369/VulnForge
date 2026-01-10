from __future__ import annotations

import logging
import os
from contextlib import contextmanager
from datetime import datetime
from typing import Dict, Generator, Optional

from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
    Text,
    create_engine,
    func,
    select,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship, scoped_session, sessionmaker
from sqlalchemy.sql import expression
from uuid import uuid4

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/vulnforge_robin.db")

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = scoped_session(
    sessionmaker(bind=engine, autoflush=False, autocommit=False)
)
Base = declarative_base()


class LeakItem(Base):
    __tablename__ = "leak_items"

    id = Column(
        PGUUID(as_uuid=True) if "postgres" in DATABASE_URL else String,
        primary_key=True,
        default=uuid4,
    )
    target_type = Column(String(64), nullable=False)
    target_value = Column(String(512), nullable=False, index=True)
    leak_type = Column(String(128), nullable=False)
    source = Column(String(256), nullable=False)
    first_seen = Column(DateTime(timezone=True))
    last_seen = Column(DateTime(timezone=True))
    raw_ciphertext = Column(LargeBinary, nullable=False)
    raw_nonce = Column(LargeBinary, nullable=False)
    raw_tag = Column(LargeBinary, nullable=False)
    structured_fields = Column(JSON, default=dict)
    confidence = Column(Float, default=0.5)
    tags = Column(JSON, default=list)
    enrichment = Column(JSON, default=dict)
    score = Column(Integer, default=0)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), onupdate=func.now(), server_default=func.now()
    )
    hash_key = Column(String(128), unique=True, index=True)

    actions = relationship(
        "ActionLog", back_populates="item", cascade="all,delete-orphan"
    )


class ActionLog(Base):
    __tablename__ = "action_logs"

    id = Column(Integer, primary_key=True)
    item_id = Column(
        PGUUID(as_uuid=True) if "postgres" in DATABASE_URL else String,
        ForeignKey("leak_items.id", ondelete="CASCADE"),
        nullable=False,
    )
    action = Column(String(64), nullable=False)
    actor = Column(String(128), nullable=False)
    notes = Column(Text)
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow)

    item = relationship(
        "LeakItem",
        back_populates="actions",
        primaryjoin="ActionLog.item_id==LeakItem.id",
    )


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    logger.info("database.initialized", extra={"module": "db"})


@contextmanager
def get_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
