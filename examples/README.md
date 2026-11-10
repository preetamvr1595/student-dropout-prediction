# Example Payloads

Use these JSON files to test the API:

```bash
# Single high-risk student
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d @examples/student_high_risk.json

# Single low-risk student
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d @examples/student_low_risk.json

# Batch prediction (3 students)
curl -X POST http://localhost:8000/predict/batch -H "Content-Type: application/json" -d @examples/batch.json
```
