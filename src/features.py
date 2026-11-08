"""Shared data/feature code — used by notebooks, training script and API (one source of truth)."""
import re
import numpy as np
import pandas as pd

TARGET_RAW = "Target"
CATEGORICAL = ["marital_status", "application_mode", "application_order", "course",
               "daytime_evening_attendance", "previous_qualification", "nacionality",
               "mothers_qualification", "fathers_qualification", "mothers_occupation",
               "fathers_occupation"]
BINARY = ["displaced", "educational_special_needs", "debtor", "tuition_fees_up_to_date",
          "gender", "scholarship_holder", "international"]


def snake(c: str) -> str:
    c = c.replace("﻿", "").strip().lower().replace("'", "")
    return re.sub(r"[^a-z0-9]+", "_", c).strip("_")


def load_raw(path: str = "data/students_raw.csv") -> pd.DataFrame:
    df = pd.read_csv(path, sep=None, engine="python", encoding="utf-8-sig")
    df.columns = [snake(c) for c in df.columns]
    return df


def add_target(df: pd.DataFrame) -> pd.DataFrame:
    """1 = Dropout, 0 = Graduate or still Enrolled."""
    df = df.copy()
    df["dropout"] = (df["target"] == "Dropout").astype(int)
    return df


def sem2_columns(df: pd.DataFrame):
    return [c for c in df.columns if "2nd_sem" in c]


def feature_columns(df: pd.DataFrame, stage: str = "end_of_sem1"):
    """stage='end_of_sem1' -> early-warning model (no 2nd-semester data);
       stage='end_of_sem2'  -> full model."""
    drop = {"target", "dropout"}
    cols = [c for c in df.columns if c not in drop]
    if stage == "end_of_sem1":
        cols = [c for c in cols if "2nd_sem" not in c]
    return cols


def _ratio(a, b):
    a = a.astype(float); b = b.astype(float)
    return pd.Series(np.where(b > 0, a / np.where(b > 0, b, 1), 0.0), index=a.index)


def engineer(df: pd.DataFrame) -> pd.DataFrame:
    """Add simple, leakage-free ratio features."""
    df = df.copy()
    for s in ("1st", "2nd"):
        enr = df.get(f"curricular_units_{s}_sem_enrolled")
        if enr is None:
            continue
        appr = df[f"curricular_units_{s}_sem_approved"]
        ev = df[f"curricular_units_{s}_sem_evaluations"]
        df[f"approval_rate_{s}_sem"] = _ratio(appr, enr)
        df[f"eval_rate_{s}_sem"] = _ratio(ev, enr)
        df[f"pass_per_eval_{s}_sem"] = _ratio(appr, ev)
    return df


def prepare(df: pd.DataFrame, stage: str = "end_of_sem1"):
    """Return X (with categorical dtype for tree models) and y."""
    df = engineer(add_target(df))
    cols = feature_columns(df, stage)
    X = df[cols].copy()
    for c in CATEGORICAL:
        if c in X:
            X[c] = X[c].astype("category")
    return X, df["dropout"]
