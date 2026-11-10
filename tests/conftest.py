import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client():
    """Create a test client for the FastAPI app."""
    from api.main import app
    with TestClient(app) as c:
        yield c
