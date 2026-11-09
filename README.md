# Student Dropout Risk Prediction — End-to-End ML Pipeline (LightGBM · XGBoost · MLflow · FastAPI · Docker · AWS Lambda)

An **early-warning system that flags college students likely to drop out after their first semester**, built as a complete machine-learning pipeline: data analysis → baselines → gradient-boosted models → experiment tracking → explanations → REST API → container deployment.

![Python](https://img.shields.io/badge/Python-3.12-blue) ![LightGBM](https://img.shields.io/badge/LightGBM-4.x-green) ![MLflow](https://img.shields.io/badge/MLflow-tracking-0194E2) ![FastAPI](https://img.shields.io/badge/FastAPI-API-009688) ![Docker](https://img.shields.io/badge/Docker-ready-2496ED) ![tests](https://img.shields.io/badge/API%20tests-7%20passing-brightgreen)

> Project 1 of 5 in my ML-engineer portfolio series (pipeline → RAG → LLM fine-tuning → monitoring/drift → multimodal).

## The problem
About **1 in 3** students in this dataset drops out. A college can only help students it identifies **in time**, so the model uses information available **after semester 1** (enrolment, family background, tuition status, first-semester results).

## Results (held-out test set, 885 students, evaluated once)

| Model | ROC-AUC | PR-AUC | Recall | Precision |
|---|---|---|---|---|
| **LightGBM, after semester 1 (early warning)** | **0.912** | **0.882** | 0.90 | 0.63 |
| LightGBM, after semester 2 (full data) | 0.934 | 0.909 | 0.92 | 0.62 |
| Logistic regression baseline (CV, sem 1) | 0.904 | 0.859 | — | — |

- Threshold **0.17** was chosen on out-of-fold training predictions with an **F2 score** (missing a dropout costs more than an extra counselling chat). At this threshold the model **catches 90% of dropouts (256 of 284)** but also flags 25% of students who would have stayed.
- At the default threshold of 0.5: recall 0.73, precision 0.84.
- Honest note: gradient boosting beat logistic regression only slightly (CV ROC-AUC 0.907 vs 0.904). The bigger wins came from **problem framing** (early-warning stage, cost-based threshold) and **leakage-free features**.

## What's inside

| Part | File | Content |
|---|---|---|
| EDA | `01_eda_and_cleaning.ipynb` (76 cells) | quality checks, target framing, statistical tests, leakage thinking |
| Baselines | `02_features_split_baselines.ipynb` (48 cells) | feature engineering, stratified split, dummy / LR / tree / RF |
| Models + MLflow | `03_lightgbm_xgboost_mlflow.ipynb` (61 cells) | tuning, MLflow runs, threshold, SHAP, calibration, export |
| Shared code | `src/features.py` | one feature pipeline used by notebooks **and** the API |
| API | `api/main.py` | FastAPI: `/predict`, `/predict/batch`, `/model-info`, `/health` |
| Lambda | `api/lambda_handler.py` | Mangum wrapper for AWS Lambda |
| Containers | `Dockerfile`, `Dockerfile.lambda` | local/any-cloud and AWS Lambda images |
| Tests + CI | `tests/`, `.github/workflows/tests.yml` | 7 API tests run on every push |
| Deploy guide | `DEPLOY_AWS_LAMBDA.md` | step-by-step AWS instructions |

## Key insights from the data
- Strongest signals: **units approved in semester 1** (approval rate), **tuition fees up to date**, **course**, **age at enrollment**, semester-1 grade.
- Students whose tuition fees are **not** up to date drop out at **87%**, versus **25%** for those who are up to date; scholarship holders drop out at 12% versus 39% for non-holders.
- Students who pass 0–2 units in semester 1 drop out 70–79% of the time; those passing 6+ units only ~7–20%.

## Quick start
```bash
git clone https://github.com/preetamvr1595/student-dropout-prediction.git
cd student-dropout-prediction
pip install -r requirements-dev.txt
jupyter notebook            # run notebooks 01 → 03 in order
mlflow ui --backend-store-uri sqlite:///mlflow.db     # browse the experiments
```

### Run the API
```bash
pip install -r requirements.txt
uvicorn api.main:app --reload          # open http://127.0.0.1:8000/docs
curl -X POST http://127.0.0.1:8000/predict -H "content-type: application/json" -d @examples/student_high_risk.json
```
Example response:
```json
{"dropout_probability": 0.9989, "risk_level": "very high", "flagged_at_risk": true, "threshold": 0.17,
 "top_factors": [{"feature": "...", "impact": 1.54, "direction": "raises risk"}, "..."]}
```

### Docker
```bash
docker build -t dropout-api .
docker run -p 8000:8000 dropout-api
```
AWS Lambda: see [DEPLOY_AWS_LAMBDA.md](DEPLOY_AWS_LAMBDA.md).

## Verified vs not verified
- ✅ Notebooks executed end-to-end with zero errors; API tests pass (7/7); live `uvicorn` server and the Lambda handler (simulated API-Gateway event) respond correctly.
- ⚠️ The Dockerfiles and the AWS deployment were **not built or deployed** in my build environment (no Docker daemon / AWS account there). They follow the standard patterns; run the commands above and open an issue if anything fails.

## Dataset
*Predict Students' Dropout and Academic Success* (UCI ML Repository #697) — 4,424 students, 35 columns, from a Portuguese higher-education institution. Realinho, Machado, Baptista & Martins (2021), *Data* 7(11):146. CC BY 4.0.

## Limitations
- Data from one institution and one period; retrain before using elsewhere.
- Course and gender help prediction but should be reviewed for fairness before real use. SHAP importance is not causal evidence.
- Predictions should trigger *support*, never penalties.

## FAQ
**How accurate is the dropout prediction?** ROC-AUC ≈ 0.91 on held-out students using only first-semester data.
**Why LightGBM?** Fast, handles categorical codes natively, strong on tabular data.
**Can I deploy it on AWS Lambda?** Yes — `Dockerfile.lambda` + `api/lambda_handler.py`.

## Series
[numpy-mastery](https://github.com/preetamvr1595/numpy-mastery) · [pandas](https://github.com/preetamvr1595/pandas) · [matplotlib](https://github.com/preetamvr1595/matplotlib) · [seaborn](https://github.com/preetamvr1595/seaborn) · [imdb-sentiment-analysis](https://github.com/preetamvr1595/imdb-sentiment-analysis)

If this helped you, please ⭐ star the repo.

*Keywords: student dropout prediction, machine learning pipeline, LightGBM, XGBoost, MLflow, FastAPI, Docker, AWS Lambda, SHAP, MLOps, education data mining*
