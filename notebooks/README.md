# Notebooks

Run the notebooks in order:

| # | Notebook | Description |
|---|---------|-------------|
| 1 | `01_eda_and_cleaning.ipynb` | Exploratory data analysis, quality checks, statistical tests, leakage audit |
| 2 | `02_features_split_baselines.ipynb` | Feature engineering, stratified split, dummy/LR/tree/RF baselines |
| 3 | `03_lightgbm_xgboost_mlflow.ipynb` | LightGBM & XGBoost tuning, MLflow tracking, threshold optimization, SHAP |

## Prerequisites

```bash
pip install -r requirements-dev.txt
```

## MLflow UI

After running notebook 03, browse experiments:

```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db
```
