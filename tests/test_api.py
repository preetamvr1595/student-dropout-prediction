import json
from pathlib import Path

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)
EX = Path(__file__).resolve().parent.parent / "examples"


def load(name):
    return json.loads((EX / name).read_text())


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_model_info():
    r = client.get("/model-info").json()
    assert r["stage"] == "end_of_sem1" and 0 < r["threshold"] < 1


def test_high_risk_student_is_flagged():
    r = client.post("/predict", json=load("student_high_risk.json"))
    assert r.status_code == 200
    body = r.json()
    assert body["flagged_at_risk"] is True and body["dropout_probability"] > 0.5
    assert len(body["top_factors"]) == 5


def test_low_risk_student_not_flagged():
    body = client.post("/predict", json=load("student_low_risk.json")).json()
    assert body["flagged_at_risk"] is False and body["risk_level"] == "low"


def test_batch():
    r = client.post("/predict/batch", json=load("batch.json"))
    assert r.status_code == 200 and len(r.json()) == 2


def test_missing_field_is_rejected():
    bad = load("student_high_risk.json"); bad.pop("age_at_enrollment")
    assert client.post("/predict", json=bad).status_code == 422


def test_unseen_category_code_does_not_crash():
    s = load("student_high_risk.json"); s["course"] = 99999
    assert client.post("/predict", json=s).status_code == 200
