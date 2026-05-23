---
name: ml-observability-and-drift
description: Use when setting up or improving production monitoring for a deployed model — to detect feature drift, prediction drift, and business-metric degradation, and to maintain a runbook with retraining triggers and rollback procedures.
family: method
profile_level: Senior+
---

# ML Observability and Drift

## Purpose

Keep the model trustworthy in production by making degradation visible before it affects users. Offline metrics measure what the model can do; production monitoring measures what it is doing. Every model enters production with pre-defined thresholds, alerts, and a documented retraining path.

## Use When

- Deploying a model to production and defining its monitoring setup.
- A model has been in production for weeks without monitoring — adding it retroactively.
- Investigating a reported quality drop ("the model seems worse lately").
- Designing the retraining trigger and rollback policy before deployment.
- Hardening an existing monitoring setup after a production incident.

## Do Not Use When

- The model has not been deployed → `model-serving-and-inference` first.
- The task is offline model evaluation → `ml-testing-and-validation`.
- The task is alerting/paging routing layer configuration → handoff to `devops-sre`.
- The task is product metric analysis and A/B experiment interpretation → handoff to `product-analyst`.

## Inputs

- Deployed model version with known offline metrics.
- Access to prediction logs (input features, model output, optionally delayed labels).
- Training data distribution (reference distribution for drift comparison).
- Agreed business success metric (conversion rate, fraud catch rate, etc.).
- Latency and throughput SLA for the serving endpoint.

## Workflow

1. **Define what to monitor before deployment.** Three signal types: (a) input distribution (feature drift), (b) output distribution (prediction drift), (c) outcome metric (business-side proxy with label delay).
2. **Instrument the inference endpoint.** Log input features (or their statistics), model output distribution, and request metadata (model version, latency, status code) to a storage backend (ClickHouse, BigQuery, Kafka).
3. **Compute feature drift.** Daily or hourly, compare the live input distribution to the training reference distribution. Use PSI for continuous features (threshold: 0.1 = warn, 0.25 = alert), chi-squared or JS divergence for categoricals.
4. **Compute prediction drift.** Monitor the distribution of model output scores. A shift in mean score or score variance signals a change in input population or model behavior.
5. **Monitor outcome metric (with label delay).** Track the business metric (e.g., fraud catch rate computed on labeled transactions with 24h delay, click-through rate). Set a statistical alert on regression from baseline.
6. **Define retraining trigger.** At least one of: PSI > 0.25 on key feature; prediction drift beyond ±2σ; business metric drops > X% from baseline over a rolling window; time-based trigger (monthly retraining regardless).
7. **Define rollback procedure.** Load the previous Production-stage model version from the registry. No retraining required. Rollback completes in minutes. Document in the runbook.
8. **Write the runbook.** Sections: monitoring dashboard link, alert conditions, first-response steps, retraining trigger decision tree, rollback procedure, contact list.
9. **Review alerts quarterly.** Dead alerts (never fire) or noisy alerts (fire too often) reduce trust. Adjust thresholds based on observed distribution.

## Outputs

- Monitoring pipeline: feature and prediction statistics logged to storage backend.
- Drift dashboard (Grafana or equivalent) with reference lines and alert bands.
- Alert rules with documented thresholds.
- Runbook: retraining trigger decision tree + rollback steps.
- Quarterly alert review record.

## Named Patterns

### Good — PSI-based feature drift check
```python
import numpy as np

def psi(reference: np.ndarray, current: np.ndarray, buckets: int = 10) -> float:
    """
    PSI interpretation:
      < 0.10 : stable — no action
      0.10–0.25 : monitor — investigate root cause
      > 0.25 : alert — consider retraining
    """
    breaks = np.nanpercentile(reference, np.linspace(0, 100, buckets + 1))
    breaks[0] -= 1e-6; breaks[-1] += 1e-6
    ref_pct = np.histogram(reference, bins=breaks)[0] / len(reference)
    cur_pct = np.histogram(current,   bins=breaks)[0] / len(current)
    ref_pct = np.clip(ref_pct, 1e-6, None)
    cur_pct = np.clip(cur_pct, 1e-6, None)
    return float(np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct)))

# Run daily
for col in monitored_features:
    p = psi(train_reference[col].values, daily_serving[col].values)
    log_metric(f"psi_{col}", p)
    if p > 0.25:
        fire_alert(f"Feature drift alert: {col} PSI={p:.3f}")
```
Thresholds are set before deployment, not discovered after an incident.

### Bad — No drift monitoring
Model deployed. Six months later, business reports a quality drop. Investigation takes two weeks. Cause: a data pipeline change altered one feature's distribution. PSI would have caught it on day 3.

### Good — Runbook retraining decision tree
```
Alert fires: PSI > 0.25 on `tenure_days`
Step 1: Check if data pipeline changed (query data-engineer).
  → If yes: fix pipeline, validate data, retrain.
  → If no: check for population shift (new marketing campaign?).
Step 2: Evaluate if prediction drift is also present (check dashboard).
  → If prediction drift > 2σ: trigger retraining.
  → If only feature drift: monitor for 3 more days.
Step 3: If business metric drops > 5% from 30-day baseline: immediate retrain.

Rollback: load fraud-detector/Archived (version N-1) via MLflow client. No retraining needed.
ETA rollback: < 15 minutes.
```

### Bad — Retraining triggered by intuition
"Sales said the model is bad. Let's retrain." No documented trigger, no rollback plan, no measurement of whether the new model is better.

### Good — Prediction score distribution monitoring
```python
import pandas as pd
from scipy import stats

def score_drift_zscore(baseline_scores: pd.Series, current_scores: pd.Series) -> float:
    """KS statistic: > 0.1 with p < 0.01 = alert."""
    ks_stat, p_value = stats.ks_2samp(baseline_scores, current_scores)
    return ks_stat, p_value

ks, p = score_drift_zscore(reference_scores, today_scores)
if ks > 0.1 and p < 0.01:
    fire_alert(f"Prediction drift: KS={ks:.3f}, p={p:.4f}")
```

### Good — Structured monitoring log per inference request
```python
import json, time
from datetime import datetime, timezone

def log_inference(request_id, features, score, model_version, latency_ms):
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "request_id": request_id,
        "model_version": model_version,
        "score": float(score),
        "latency_ms": latency_ms,
        # log feature statistics, not raw PII
        "amount_bucket": bucket(features["amount"], [0, 100, 1000, 10000]),
        "tenure_bucket": bucket(features["tenure_days"], [0, 30, 180, 365]),
    }
    logger.info(json.dumps(record))
```
PII-safe feature statistics enable drift computation without storing raw user data.

## Boundaries

- Owns production model monitoring: feature drift, prediction drift, business metric proxy, retraining trigger, and rollback runbook.
- Does not own alerting/paging routing or observability infrastructure → `devops-sre`.
- Does not own product A/B experiment interpretation or business metric ownership → `product-analyst`.
- Does not own offline model evaluation → `ml-testing-and-validation`.

## Sources

### Priority 1 — Methodology and tooling
- scikit-learn: Calibration — https://scikit-learn.org/stable/modules/calibration.html
- Evidently AI Documentation — https://docs.evidentlyai.com/
- OpenTelemetry Semantic Conventions — https://opentelemetry.io/docs/specs/semconv/

### Priority 2 — Engineering and reliability
- Google SRE Book — https://sre.google/sre-book/table-of-contents/
- ML Test Score (Breck et al.) — https://research.google/pubs/pub46555/
- Chip Huyen: Designing ML Systems, Ch. 8 — book reference

### Priority 3 — Practice orientation
- Made With ML: Monitoring — https://madewithml.com/
- Reliable ML (Google) — https://research.google/pubs/reliable-machine-learning-in-the-wild/

## Handoff

- Alert routing, paging, observability infrastructure → `devops-sre`.
- Business metric interpretation, A/B experiment → `product-analyst`.
- Retraining triggered → `training-pipelines-and-reproducibility` + `experiment-tracking-and-registry`.
- Feature drift root cause in source data → `data-engineer`.
- Offline evaluation of candidate retrained model → `ml-testing-and-validation`.
