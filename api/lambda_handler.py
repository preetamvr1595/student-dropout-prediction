"""AWS Lambda entry point: wraps the FastAPI app with Mangum (API Gateway / Function URL)."""
from mangum import Mangum

from api.main import app

handler = Mangum(app, lifespan="off")
