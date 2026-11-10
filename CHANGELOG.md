# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-11-10

### Added
- End-to-end ML pipeline: EDA, feature engineering, model training
- LightGBM and XGBoost model comparison with MLflow tracking
- FastAPI REST API with `/predict`, `/predict/batch`, `/model-info`, `/health`
- AWS Lambda deployment via Mangum wrapper
- Docker and Docker Lambda container images
- 7 automated API tests with pytest
- GitHub Actions CI/CD pipeline
- Comprehensive documentation and deployment guide

### Model Performance (Held-out Test Set, n=885)
- LightGBM ROC-AUC: 0.912
- LightGBM PR-AUC: 0.882
- Recall at threshold 0.17: 90% (256/284 dropouts caught)
