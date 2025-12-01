from datetime import datetime

from ..scoring import compute_score


def test_compute_score_high_impact():
    first = datetime(2024, 8, 1)
    last = datetime(2024, 8, 3)
    score = compute_score(
        confidence=0.9,
        structured_fields={"password_present": True},
        first_seen=first,
        last_seen=last,
    )
    assert score >= 80
