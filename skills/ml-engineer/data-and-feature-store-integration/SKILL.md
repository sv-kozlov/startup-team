---
name: data-and-feature-store-integration
description: Use when integrating a model with a feature store (online or offline), designing online/offline feature retrieval, ensuring point-in-time correctness in training, or coordinating feature schema and SLA with the data engineering team.
family: method
profile_level: Senior+
---

# Data and Feature Store Integration

## Purpose

Connect the ML model to a managed, reliable feature supply — so training and serving use identical, versioned features, and training data is free of future-leakage from incorrect time joins. Prevent train/serving skew originating from two different feature computation paths.

## Use When

- A model will consume features from a feature store (Feast, Hopsworks, Redis, Tecton, or custom).
- Training data needs to be assembled with point-in-time correct historical features (as-of-date joins).
- The same feature computation must serve both offline training and online inference.
- Coordinating with the data engineering team on feature schema, TTL, and data SLA.
- Migrating model features from ad-hoc SQL in training notebooks to a governed feature store.

## Do Not Use When

- Features are computed from raw data inside the training script with no shared store — use `feature-engineering-and-validation`.
- The task is monitoring feature drift in production — use `ml-observability-and-drift`.
- The task is designing the data pipeline (ETL, warehouse) — handoff to `data-engineer`.

## Inputs

- Feature list from the feature schema (from `feature-engineering-and-validation`).
- Feature store backend and its API client library.
- Training dataset time window and entity keys.
- Online serving SLA (latency budget for feature retrieval at inference time).
- Data engineer contact for source-of-truth discussion and SLA negotiation.

## Workflow

1. **Categorize features: online vs. offline.** Online features: retrieved at inference time from a low-latency store (Redis, DynamoDB, Hopsworks online store). Offline features: available only for training, batch scoring, or when staleness is acceptable.
2. **Define feature schemas.** For each feature: name, dtype, entity key, description, TTL (for online), data source, computation logic, owner. Register in the feature store's schema registry.
3. **Ensure point-in-time correctness for training.** When assembling training data from historical feature tables, use a point-in-time join: for each entity at a given event timestamp, retrieve the feature value that was valid at that time — not the value that would be computed from future data.
4. **Validate train/serving alignment.** Compare feature values retrieved via offline (training) vs. online (serving) paths for the same entity at the same timestamp. Any divergence is a source of train/serving skew.
5. **Set TTL for online features.** A feature not refreshed within its TTL returns a null or stale value. Define the TTL based on the staleness tolerance of the model. Log and monitor TTL violations at serving time.
6. **Negotiate SLA with data-engineer.** Agree on: freshness (how old a feature can be), latency (how quickly new data propagates to the online store), and incident response when the pipeline is late.
7. **Write a feature retrieval integration test.** Fetch a known entity at a known timestamp from both offline and online paths. Assert identical values (within tolerance for float precision).

## Outputs

- Feature schema definitions registered in the feature store.
- Point-in-time-correct training dataset assembly script.
- Online feature retrieval client integrated into the inference service.
- Train/serving alignment validation report.
- SLA agreement document (freshness, latency, incident response) with data engineering.

## Named Patterns

### Good — Point-in-time join with Feast
```python
from feast import FeatureStore
import pandas as pd

store = FeatureStore(repo_path="feature_repo/")

entity_df = pd.DataFrame({
    "user_id":    ["u001", "u002", "u003"],
    "event_timestamp": pd.to_datetime(["2024-05-01", "2024-06-15", "2024-07-10"]),
})

# Retrieves feature values as they were at each event_timestamp — not today's values
training_df = store.get_historical_features(
    entity_df=entity_df,
    features=["user_stats:tenure_days", "user_stats:amount_30d", "user_stats:category_mode"],
).to_df()
```
Each row gets the feature value that was actually available at the prediction time — no future leakage from the feature store.

### Bad — Joining features without time alignment
```python
# Get current feature values and join to historical events
features_today = store.get_online_features(
    features=["user_stats:tenure_days"], entity_rows=[{"user_id": uid} for uid in user_ids]
).to_df()

events = events.merge(features_today, on="user_id")   # today's features + historical events
```
Future feature values (computed after the event) contaminate the training set. Offline AUC is inflated.

### Good — Online feature retrieval at inference time
```python
from feast import FeatureStore
from fastapi import FastAPI
from pydantic import BaseModel

store = FeatureStore(repo_path="feature_repo/")
app = FastAPI()

class PredictRequest(BaseModel):
    user_id: str
    amount: float

@app.post("/predict")
def predict(req: PredictRequest):
    # Retrieve online features by entity key
    online_features = store.get_online_features(
        features=["user_stats:tenure_days", "user_stats:category_mode"],
        entity_rows=[{"user_id": req.user_id}],
    ).to_dict()

    if online_features["user_stats__tenure_days"][0] is None:
        # TTL expired or entity not found — use fallback
        tenure_days = DEFAULT_TENURE_DAYS
    else:
        tenure_days = online_features["user_stats__tenure_days"][0]

    X = [[req.amount, tenure_days, online_features["user_stats__category_mode"][0]]]
    prob = float(model.predict_proba(X)[0, 1])
    return {"fraud_probability": prob}
```
Online features fetched by entity key at inference time — same computation path as training features.

### Bad — Two different feature computations for train and serving
Training SQL: `AVG(amount) over last 30 days` from the data warehouse.
Serving code: `SUM(amount) / COUNT(*) over last 7 days` from Redis.
Different aggregation windows → train/serving skew → unexplained production quality gap.

### Good — TTL violation monitoring
```python
# Log TTL status per feature at inference time
import time, json

def get_feature_with_ttl_check(store, entity_rows, features, ttl_seconds):
    t0 = time.time()
    result = store.get_online_features(features=features, entity_rows=entity_rows).to_dict()
    latency = (time.time() - t0) * 1000
    for feat in features:
        val = result.get(feat.replace(":", "__"), [None])[0]
        log_metric("feature_retrieved", {"feature": feat, "is_null": val is None,
                                         "latency_ms": latency})
```

## Boundaries

- Owns feature store integration: schema registration, point-in-time retrieval, online/offline alignment, TTL, and SLA negotiation interface.
- Does not own data pipeline construction, ETL, or warehouse → `data-engineer` (owns source-of-truth and pipeline SLA).
- Does not own feature engineering logic (signal selection, transformation) → `feature-engineering-and-validation`.
- Does not own monitoring of feature drift in production → `ml-observability-and-drift`.

## Sources

### Priority 1 — Feature store documentation
- Feast Documentation — https://docs.feast.dev/
- Hopsworks Feature Store — https://docs.hopsworks.ai/
- MLflow Feature Engineering — https://mlflow.org/docs/latest/

### Priority 2 — Architecture and methodology
- Chip Huyen: Designing ML Systems, Ch. 5 (Feature Engineering) — book reference
- Tecton: What is a Feature Store? — https://www.tecton.ai/blog/what-is-a-feature-store/
- ML Test Score (Breck et al.) — https://research.google/pubs/pub46555/

### Priority 3 — Practice orientation
- Made With ML: Feature Store — https://madewithml.com/
- Full Stack Deep Learning: Data — https://fullstackdeeplearning.com/

## Handoff

- Data pipeline, ETL, warehouse, data SLA → `data-engineer`.
- Feature engineering signal design and Pipeline construction → `feature-engineering-and-validation`.
- Feature drift monitoring in production → `ml-observability-and-drift`.
- Online feature retrieval integrated into the serving layer → `model-serving-and-inference`.
