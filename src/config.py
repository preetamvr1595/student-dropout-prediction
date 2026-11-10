"""Application configuration loaded from environment variables."""
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = os.getenv("MODEL_PATH", str(PROJECT_ROOT / "models" / "model_sem1.joblib"))
META_PATH = os.getenv("META_PATH", str(PROJECT_ROOT / "models" / "model_meta.json"))
THRESHOLD = float(os.getenv("THRESHOLD", "0.17"))
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")
