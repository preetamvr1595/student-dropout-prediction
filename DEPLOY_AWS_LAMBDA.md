# Deploy the API on AWS Lambda (container image)

> Not tested by me (no AWS account in my build environment). These are the standard steps. Replace `ACCOUNT_ID` and the region.

| Step | Command / action |
|---|---|
| 0 | Install Docker and the AWS CLI. Run `aws configure` with an IAM user that can use ECR and Lambda. |
| 1 | Create a registry: `aws ecr create-repository --repository-name dropout-api --region ap-south-1` |
| 2 | Log in: `aws ecr get-login-password --region ap-south-1 \| docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com` |
| 3 | Build: `docker build -f Dockerfile.lambda -t dropout-api-lambda .` |
| 4 | Tag: `docker tag dropout-api-lambda:latest ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/dropout-api:latest` |
| 5 | Push: `docker push ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/dropout-api:latest` |
| 6 | In the AWS console open **Lambda → Create function → Container image**, pick the image, set memory to **1024 MB** and timeout to **30 s**. |
| 7 | **Configuration → Function URL → Create** (auth type `NONE` for a public demo, or `AWS_IAM`). |
| 8 | Test: `curl -X POST <function-url>/predict -H "content-type: application/json" -d @examples/student_high_risk.json` |

**Cost:** Lambda's free tier is generous, so a demo costs about nothing; ECR storage is a few cents.
**Cold start:** the first request after idle time takes a few seconds (the model loads). Later requests are fast.
**Security:** a `NONE`-auth Function URL is public. Delete the function when you finish the demo, or use `AWS_IAM`.
