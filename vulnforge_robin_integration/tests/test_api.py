from fastapi.testclient import TestClient

from ..api.app import app


def test_ingest_list_and_decrypt():
    with TestClient(app) as client:
        payload = {
            "source": "test",
            "payload": {
                "target": {"type": "domain", "value": "example.com"},
                "leak_type": "credentials",
                "source": "unit-test",
                "structured_fields": {
                    "email": "demo@example.com",
                    "password_present": True,
                },
                "raw": "user:demo@example.com pass:Secret",
            },
        }
        resp = client.post("/ingest", json=payload)
        assert resp.status_code == 200
        resp = client.get("/items")
        data = resp.json()
        assert data["total"] == 1
        item_id = data["items"][0]["id"]

        decrypt_resp = client.post(
            f"/items/{item_id}/decrypt", json={"reviewer_password": "testpass"}
        )
        assert decrypt_resp.status_code == 200
        assert "user:demo@example.com" in decrypt_resp.json()["raw_snippet"]
