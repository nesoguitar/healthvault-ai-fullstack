"""
Minimal smoke test. Full endpoint tests would spin up a test database
(e.g. via a Postgres testcontainer) and override `get_db`; that wiring is
left for the test suite to grow into as business logic is added.
"""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_root():
    response = client.get("/")
    assert response.status_code == 200
