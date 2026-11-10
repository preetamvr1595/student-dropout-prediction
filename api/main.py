"""Student dropout early-warning API (FastAPI).

Run locally:  uvicorn api.main:app --reload
Docs:         http://127.0.0.1:8000/docs
"""
import json
from pathlib import Path
from typing import List

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, create_model

from src.features import CATEGORICAL, engineer

ROOT = Path(__file__).resolve().parent.parent
MODEL = joblib.load(ROOT / "models" / "model_sem1.joblib")
META = json.loads((ROOT / "models" / "model_meta.json").read_text())

FEATURES = META["features"]
THRESHOLD = META["threshold"]
LEVELS = META["levels"]
ENGINEERED = {c for c in FEATURES if c.startswith(("approval_rate_", "eval_rate_", "pass_per_eval_"))}
INPUT_FIELDS = [c for c in FEATURES if c not in ENGINEERED]
# Fields the model needs (raw columns). Floats for rates/grades, ints for the rest.
FLOAT_FIELDS = {"curricular_units_1st_sem_grade", "unemployment_rate", "inflation_rate", "gdp"}

Student = create_model(
    "Student",
    **{c: (float if c in FLOAT_FIELDS else int, Field(...)) for c in INPUT_FIELDS},
)


class Factor(BaseModel):
    feature: str
    impact: float = Field(description="Contribution to risk (log-odds). Positive = raises risk.")
    direction: str


class Prediction(BaseModel):
    dropout_probability: float
    risk_level: str
    flagged_at_risk: bool
    threshold: float
    top_factors: List[Factor]


app = FastAPI(
    title="Student Dropout Early-Warning API",
    description="Predicts the probability that a student will drop out, using data available after semester 1.",
    version="1.0.0",
)


def _risk_level(p: float) -> str:
    b2 = max(0.5, THRESHOLD + 0.05)
    b3 = max(0.8, b2 + 0.05)
    return "low" if p < THRESHOLD else "medium" if p < b2 else "high" if p < b3 else "very high"


def _frame(records: List[dict]) -> pd.DataFrame:
    df = engineer(pd.DataFrame(records))
    X = df[FEATURES].copy()
    for c in CATEGORICAL:
        if c in X:
            codes = X[c].astype(int)
            X[c] = pd.Categorical(codes.where(codes.isin(LEVELS[c])), categories=LEVELS[c])  # unseen code -> missing
    return X


def _predict(records: List[dict]) -> List[Prediction]:
    X = _frame(records)
    proba = MODEL.predict_proba(X)[:, 1]
    contrib = MODEL.booster_.predict(X, pred_contrib=True)[:, :-1]  # last col = bias
    out = []
    for i, p in enumerate(proba):
        top = np.argsort(-np.abs(contrib[i]))[:5]
        factors = [Factor(feature=FEATURES[j], impact=round(float(contrib[i, j]), 3),
                          direction="raises risk" if contrib[i, j] > 0 else "lowers risk") for j in top]
        out.append(Prediction(dropout_probability=round(float(p), 4), risk_level=_risk_level(float(p)),
                              flagged_at_risk=bool(p >= THRESHOLD), threshold=THRESHOLD, top_factors=factors))
    return out


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/model-info")
def model_info():
    return {k: META[k] for k in ("stage", "model", "threshold", "test_metrics", "train_rows")} | {
        "n_features": len(FEATURES), "required_inputs": INPUT_FIELDS}


@app.post("/predict", response_model=Prediction)
def predict(student: Student):  # type: ignore[valid-type]
    return _predict([student.model_dump()])[0]


@app.post("/predict/batch", response_model=List[Prediction])
def predict_batch(students: List[Student]):  # type: ignore[valid-type]
    if not 1 <= len(students) <= 1000:
        raise HTTPException(status_code=422, detail="Send between 1 and 1000 students.")
    return _predict([s.model_dump() for s in students])
