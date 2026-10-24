import uuid

from fastapi.testclient import TestClient

from app.main import app, rolls
from app.models import Rarity

client = TestClient(app)


def test_roll_returns_stable_shape():
    response = client.post("/roll")

    assert response.status_code == 200
    body = response.json()
    assert set(body) == {"roll_id", "rarity"}
    assert body["rarity"] in {tier.value for tier in Rarity}
    uuid.UUID(body["roll_id"])  # raises if not a valid UUID


def test_roll_is_stored_for_later_generation():
    body = client.post("/roll").json()
    assert rolls[body["roll_id"]].value == body["rarity"]
