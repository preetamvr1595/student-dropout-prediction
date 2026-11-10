# Models

| File | Description |
|------|-------------|
| `model_sem1.joblib` | Trained LightGBM classifier (end-of-semester-1 features) |
| `model_meta.json` | Feature list, categorical columns, threshold, and stage |
| `lgbm_search.csv` | LightGBM hyperparameter search results |
| `xgb_search.csv` | XGBoost hyperparameter search results |
| `mlflow_runs_summary.csv` | MLflow experiment run metrics summary |
| `test_confusion.png` | Confusion matrix on held-out test set |

## Threshold
Operating threshold: **0.17** (F2-optimized for early warning recall)
