import base64
import os
import tempfile

import pytest

# Ensure deterministic crypto key and DB for tests
os.environ.setdefault("ENCRYPTION_KEY_BASE64", base64.b64encode(b"0" * 32).decode())
tmp_db = tempfile.NamedTemporaryFile(delete=False)
os.environ.setdefault("DATABASE_URL", f"sqlite:///{tmp_db.name}")
os.environ.setdefault("REVIEWER_PASSWORD", "testpass")
os.environ.setdefault("CELERY_EAGER", "1")


@pytest.fixture(autouse=True)
def clean_db():
    from ..db import Base, engine

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
