# Makefile for Student Dropout Prediction Pipeline

.PHONY: install test run docker-build docker-run clean lint

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v --tb=short

run:
	uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

docker-build:
	docker build -t dropout-predictor .

docker-run:
	docker run -p 8000:8000 dropout-predictor

docker-lambda-build:
	docker build -f Dockerfile.lambda -t dropout-lambda .

lint:
	flake8 src/ api/ tests/ --max-line-length 120

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache mlruns mlflow.db

help:
	@echo "Available targets:"
	@echo "  install          Install production dependencies"
	@echo "  install-dev      Install development dependencies"
	@echo "  test             Run API tests"
	@echo "  run              Start FastAPI dev server"
	@echo "  docker-build     Build Docker image"
	@echo "  docker-run       Run Docker container"
	@echo "  lint             Run flake8 linter"
	@echo "  clean            Remove caches and temp files"
