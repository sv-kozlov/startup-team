---
name: model-serving-and-inference
description: Use when deploying a model as an online REST/gRPC service, a batch pipeline, or a streaming consumer — to design the inference layer with schema validation, latency budgets, export formats, and a clear ML API contract for backend integration.
family: code
profile_level: Senior+
---

# Model Serving and Inference

## Purpose

Deliver model predictions reliably and within agreed latency, cost, and accuracy constraints. The inference layer is the boundary between the ML system and the product; its contract must be explicit, stable, and observable.

## Use When

- Deploying a trained model as an API endpoint (online inference).
- Building a batch scoring pipeline for periodic predictions.
- Setting up a streaming consumer that scores events in near-real time.
- Exporting a model to ONNX or TorchScript for cross-runtime serving.
- Defining the ML API contract for a backend integration.
- Optimizing inference latency or cost (quantization, batching, caching).

## Do Not Use When

- The model has not been evaluated and passed a quality gate → `ml-testing-and-validation` first.
- The task is monitoring model quality in production → `ml-observability-and-drift`.
- The task is designing the product service that calls the model → handoff to `backend-developers`.
- The task is infrastructure setup (K8s, GPU nodes, autoscaling) → handoff to `devops-sre`.

## Inputs

- Trained, registered model artifact (from `experiment-tracking-and-registry`).
- Evaluation report confirming production readiness.
- ML API requirements: latency SLA (p95/p99), throughput (RPS), payload schema, error semantics.
- Deployment target: online service, scheduled batch, or streaming consumer.

## Workflow

### Online inference
1. **Define the API contract.** Request schema (feature names, types, ranges), response schema (prediction, probability, version), error codes (422 for invalid input, 500 for model error, 503 for unavailability).
2. **Implement with schema validation.** Use Pydantic models to validate input before model call. Return 422 with field-level errors on schema violation.
3. **Load the model once at startup.** Avoid loading on every request. Use a singleton or lifespan context.
4. **Set latency budget and measure it.** Define p95 and p99 targets. Add `/health` and `/metrics` endpoints. Instrument with OpenTelemetry spans.
5. **Handle errors explicitly.** Model inference exceptions → 500 with error code (not traceback). Include a fallback or circuit-breaker for graceful degradation.
6. **Export for portability.** Export to ONNX or TorchScript when the runtime differs from the training environment (e.g., Java/Go backend or edge device).

### Batch inference
1. **Parametrize the batch job.** Data source path, output path, model version, and date range as config/CLI arguments.
2. **Vectorize inference.** Use `predict_proba(X_batch)` on chunks; avoid row-by-row prediction loops.
3. **Write predictions with job metadata.** Include `model_version`, `run_date`, `input_hash` in the output table.
4. **Schedule and alert.** Define the schedule (Airflow DAG / Prefect flow / cron). Set an SLA alert if the job does not complete within the window.

### Streaming inference
1. **Consume from broker.** Kafka/Pulsar consumer; commit offset only after successful prediction write.
2. **Assemble features at consumption time.** Retrieve online features from the feature store; do not trust the event payload to carry all features.
3. **Handle backpressure.** Limit concurrent model calls; use a bounded worker pool.

## Outputs

- Online: FastAPI/gRPC service with Pydantic schema, `/predict`, `/health`, `/metrics` endpoints.
- Batch: parametrized scoring script or Airflow/Prefect DAG with output schema.
- Streaming: Kafka consumer with feature assembly and offset management.
- ML API contract document (endpoint, request/response schema, error codes, latency SLA).
- ONNX or TorchScript export artifact (where applicable).

## Named Patterns

### Good — FastAPI endpoint with Pydantic validation
```python
from fastapi import FastAPI
from pydantic import BaseModel, validator
from contextlib import asynccontextmanager
import mlflow.sklearn, numpy as np

MODEL = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global MODEL
    MODEL = mlflow.sklearn.load_model("models:/fraud-detector/Production")
    yield

app = FastAPI(lifespan=lifespan)

class PredictRequest(BaseModel):
    amount: float
    tenure_days: int
    category: str

    @validator("amount")
    def amount_positive(cls, v):
        if v <= 0:
            raise ValueError("amount must be positive")
        return v

class PredictResponse(BaseModel):
    fraud_probability: float
    model_version: str = "fraud-detector/Production"

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    X = np.array([[req.amount, req.tenure_days]])
    prob = float(MODEL.predict_proba(X)[0, 1])
    return PredictResponse(fraud_probability=prob)

@app.get("/health")
def health():
    return {"status": "ok"}
```
Model loaded once. Input validated before model call. Schema enforced via Pydantic.

### Bad — Raw dict and per-request model load
```python
@app.post("/predict")
def predict(data: dict):
    model = joblib.load("model.pkl")          # loaded on every request
    X = np.array([[data["amount"], data["tenure"]]])
    return {"prob": model.predict_proba(X)[0, 1]}
```
No validation, no schema, model loaded per request → high latency and uncontrolled errors.

### Good — ONNX export for cross-runtime serving
```python
import torch, torch.onnx

dummy_input = torch.randn(1, input_dim)
torch.onnx.export(
    model,
    dummy_input,
    "model.onnx",
    input_names=["features"],
    output_names=["logits"],
    dynamic_axes={"features": {0: "batch_size"}, "logits": {0: "batch_size"}},
    opset_version=17,
)
```
ONNX model runs in Go/Java/C++ runtimes without a Python dependency.

### Bad — Pickle in production with no format contract
Model saved as `model_final_v2.pkl`. Loaded in production via `joblib.load`. Scikit-learn version mismatch breaks deserialization silently on the next library update.

### Good — Batch inference with vectorized prediction
```python
import pandas as pd, mlflow.sklearn

model = mlflow.sklearn.load_model("models:/churn-predictor/Production")
chunks = pd.read_parquet("s3://data/scoring/2024-12/", chunksize=50_000)
results = []
for chunk in chunks:
    probs = model.predict_proba(chunk[feature_cols])[:, 1]
    chunk["churn_prob"] = probs
    chunk["model_version"] = "churn-predictor/Production"
    results.append(chunk[["user_id", "churn_prob", "model_version"]])
pd.concat(results).to_parquet("s3://data/predictions/2024-12/", index=False)
```

### Bad — Row-by-row loop
```python
for _, row in df.iterrows():
    pred = model.predict([row[feature_cols].values])[0]
```
10× to 100× slower than vectorized `predict_proba(X_batch)`. Unacceptable for batch jobs over millions of rows.

## Boundaries

- Owns inference layer: API, batch, streaming, export format, ML API contract, latency and cost within the model service.
- Does not own product service business logic or orchestration wrapping the ML service → `backend-developers`.
- Does not own infrastructure provisioning (K8s, GPU allocation, autoscaling) → `devops-sre`.
- Does not own production quality monitoring and drift detection → `ml-observability-and-drift`.

## Sources

### Priority 1 — Framework documentation
- FastAPI — https://fastapi.tiangolo.com/
- Pydantic — https://docs.pydantic.dev/
- ONNX — https://onnx.ai/
- PyTorch: TorchScript — https://pytorch.org/docs/stable/jit.html
- MLflow: Model Registry — https://mlflow.org/docs/latest/model-registry.html

### Priority 2 — Engineering and reliability
- The Twelve-Factor App — https://12factor.net/
- OpenTelemetry Semantic Conventions — https://opentelemetry.io/docs/specs/semconv/
- Chip Huyen: Designing ML Systems, Ch. 7 — book reference

### Priority 3 — Practice orientation
- Full Stack Deep Learning: Deployment — https://fullstackdeeplearning.com/
- Made With ML: Serving — https://madewithml.com/

## Handoff

- Product service wrapping the ML API → `backend-python-developer` / `backend-go-developer`.
- K8s deployment, GPU nodes, autoscaling, CI/CD platform → `devops-sre`.
- Production quality monitoring and drift detection → `ml-observability-and-drift`.
- Model registration and staging → `experiment-tracking-and-registry`.
- System integration specification → `system-analyst`.
