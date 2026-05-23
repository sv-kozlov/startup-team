---
name: experiment-tracking-and-registry
description: Use when setting up systematic experiment logging, comparing training runs, promoting models through staged registry, writing model cards, or managing the champion/challenger lifecycle for a production model.
family: method
profile_level: Senior+
---

# Experiment Tracking and Registry

## Purpose

Turn a sequence of training runs into a governed, auditable history. Prevent the "which model is this?" problem in production and the "I can't find that run" problem in research. A model enters production only by passing through a staged registry with a documented rationale.

## Use When

- Starting a series of experiments for a new model and needing a consistent logging structure.
- Comparing multiple runs to select the best model for promotion.
- Promoting a model from Staging to Production in the registry.
- Writing a model card before a production deployment.
- Setting up a champion/challenger or shadow deployment scheme.
- Investigating a production incident: tracing which model version was serving at a given time.

## Do Not Use When

- The training pipeline is not yet reproducible → `training-pipelines-and-reproducibility` first.
- The task is monitoring model quality after deployment → `ml-observability-and-drift`.
- The task is writing or reviewing the training script → `training-pipelines-and-reproducibility`.

## Inputs

- Reproducible training pipeline with parametrized config.
- Agreed primary and secondary metrics from the ML problem statement.
- Tracker backend (MLflow, Weights & Biases, Comet, Neptune).
- Model registry (MLflow Model Registry, HuggingFace Hub, custom).

## Workflow

1. **Define experiment structure before the first run.** Set an experiment name, tags (model type, use case, team), and the set of logged params and metrics. Document the schema; do not invent it per run.
2. **Log everything in one run context.** Params, metrics (at every epoch or at end-of-training), dataset version reference, git SHA, config file as artifact, fitted model, evaluation report.
3. **Name runs meaningfully.** Use a naming convention: `{model_type}-{key_param}-{date}`. Avoid "run_1", "test", "final_final".
4. **Compare runs on the same metric.** Use the tracker's comparison view. The primary metric is the comparison criterion. Do not promote based on a metric not defined in the problem statement.
5. **Apply a quality gate before promotion.** Minimum thresholds for primary metric (e.g., AUC ≥ 0.85) and guardrail metrics (e.g., latency p95 ≤ 200 ms, calibration ECE ≤ 0.05). Document gate in the ADR or PR.
6. **Register the selected model with stage `Staging`.** Link the registry entry to the experiment run_id. Add tags: data version, feature schema version, git SHA.
7. **Write a model card.** Intended use, training data description, metrics disaggregated by segment, known limitations, fairness considerations, recommended use conditions.
8. **Promote to `Production` after staging validation.** Staging validation includes: online shadow test or canary, QA sign-off on golden dataset, runbook is written and reviewed.
9. **Archive superseded versions.** Transition the old Production version to `Archived`. Do not delete; rollback must be possible by loading the archived version.

## Outputs

- Experiment tracker entries: runs with params, metrics, artifacts, tags.
- Registry entries for promoted models with stage history (None → Staging → Production → Archived).
- Model card (intended use, data description, metrics, limitations, fairness).
- Promotion decision record (quality gate results, sign-off, linked issues).

## Named Patterns

### Good — Structured MLflow logging with model registration
```python
import mlflow
from mlflow.models.signature import infer_signature

with mlflow.start_run(run_name="xgb-depth6-lr005-2026-05") as run:
    mlflow.set_tags({"model_type": "xgboost", "use_case": "fraud", "team": "ml-platform"})
    mlflow.log_params({"n_estimators": 500, "max_depth": 6, "lr": 0.05, "seed": 42})
    mlflow.log_param("data_version", "snapshot-2024-10")
    mlflow.log_param("git_sha", "abc1234")

    model.fit(X_train, y_train)
    metrics = evaluate(model, X_val, y_val)    # returns dict of metric name → value
    mlflow.log_metrics(metrics)
    mlflow.log_artifact("artifacts/evaluation_report.html")

    if metrics["auc_val"] < 0.85:
        raise ValueError("Quality gate failed")

    signature = infer_signature(X_val, model.predict(X_val))
    mlflow.xgboost.log_model(model, "model", signature=signature,
                              registered_model_name="fraud-detector")

# Promote to Staging after run completes
client = mlflow.tracking.MlflowClient()
client.transition_model_version_stage(
    name="fraud-detector", version="3", stage="Staging",
    archive_existing_versions=False
)
```

### Bad — Untracked experiments in files
```
model_v1.pkl, model_v2.pkl, model_best.pkl, model_final.pkl, model_final_v2_real.pkl
```
No params logged. No metrics. No data version. Impossible to reproduce. Production model identity unclear.

### Good — Model card structure
```markdown
# Model Card: fraud-detector v3

## Intended Use
Binary classification of payment transactions as fraudulent. Intended for use in real-time fraud scoring endpoint with score > 0.7 triggering a manual review queue.

## Training Data
Snapshot 2024-10: 1.2M transactions, 2023-01 to 2024-06. Positive rate: 2.3%.

## Evaluation Results (test split 2024-10 to 2024-12)
| Metric | Value |
|--------|-------|
| AUC-ROC | 0.912 |
| Precision @ Recall=0.90 | 0.68 |
| ECE | 0.032 |

### Disaggregated metrics
| Segment | AUC |
|---------|-----|
| High-value transactions (>1000 USD) | 0.931 |
| Mobile channel | 0.887 |

## Limitations
Performance degrades on transaction types introduced after 2024-06. Not suitable for international transactions (training data: domestic only).

## Fairness
No demographic features used. Segment analysis by transaction channel shows acceptable metric parity.
```

### Bad — No model card, no limitations documented
Model deployed. Six months later, support team discovers it has 60% AUC on mobile. No one knew; it was not measured.

### Good — Champion/challenger traffic split
```yaml
# serving config
champion: fraud-detector/Production         # 90% traffic
challenger: fraud-detector/Staging-v4      # 10% traffic
comparison_metric: precision_at_recall_90
comparison_window: 7 days
decision: auto-promote if challenger wins by >2pp with p<0.05
```

## Boundaries

- Owns experiment logging, model registry lifecycle, model cards, and promotion governance.
- Does not own training script logic → `training-pipelines-and-reproducibility`.
- Does not own production monitoring and drift alerting → `ml-observability-and-drift`.
- Does not own A/B experiment product metric interpretation → `product-analyst`.

## Sources

### Priority 1 — Framework documentation
- MLflow: Tracking — https://mlflow.org/docs/latest/tracking.html
- MLflow: Model Registry — https://mlflow.org/docs/latest/model-registry.html
- Weights & Biases documentation — https://docs.wandb.ai/

### Priority 2 — Methodology
- Model Cards (Mitchell et al., 2019) — https://arxiv.org/abs/1810.03993
- ML Test Score (Breck et al., 2017) — https://research.google/pubs/pub46555/
- Chip Huyen: Designing ML Systems, Ch. 9 — book reference

### Priority 3 — Practice
- Made With ML: Tracking — https://madewithml.com/
- Full Stack Deep Learning: Experiment Management — https://fullstackdeeplearning.com/

## Handoff

- Training pipeline reproducibility → `training-pipelines-and-reproducibility`.
- Production serving of the registered model → `model-serving-and-inference`.
- Post-deployment monitoring and drift detection → `ml-observability-and-drift`.
- A/B product experiment interpretation → `product-analyst`.
- Quality gate failure requiring problem re-framing → `ml-problem-framing-and-data-design`.
