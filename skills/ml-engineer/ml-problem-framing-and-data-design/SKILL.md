---
name: ml-problem-framing-and-data-design
description: Use when a new ML task arrives or an existing one is unclear — to define the ML problem precisely, choose target metrics and evaluation protocol, design the dataset schema, and establish data validation rules before any training begins.
family: method
profile_level: Senior+
---

# ML Problem Framing and Data Design

## Purpose

Turn a vague product request into a concrete ML problem with measurable criteria and a validated data foundation. Prevent wasted training cycles caused by wrong metrics, leaky datasets, or misaligned business and model objectives.

## Use When

- A new ML feature or model is being scoped.
- The team disagrees on what "good model performance" means.
- The data source is new or insufficiently understood.
- A previous model failed in production and the root cause may be a framing issue.
- Preparing an ML feasibility assessment for product or stakeholders.

## Do Not Use When

- The problem is already framed and validated — move to `feature-engineering-and-validation`.
- The task is writing a training script — use `training-pipelines-and-reproducibility`.
- The task is deploying an already-evaluated model — use `model-serving-and-inference`.
- Business metric interpretation is the main question — handoff to `product-analyst`.

## Inputs

- Product brief: the problem the ML solution should solve and the business metric it should affect.
- Available data sources with rough schema, volume, and recency.
- Constraints: latency budget, cost per inference, legal/privacy requirements, explainability demands.
- Existing baselines or heuristics used in production.

## Workflow

1. **Translate product goal to ML objective.** Name the ML task type (classification, regression, ranking, generation). Identify the ground-truth label: what it represents, who produces it, and how reliable it is.
2. **Define offline metrics.** Choose primary metric (AUC-ROC, F1, NDCG, RMSE, etc.) aligned with the product goal. Add calibration check if the model output is used as a probability. Specify the positive class clearly.
3. **Design evaluation protocol.** Decide on split strategy: random, temporal, or group-aware. Define the train/val/test time windows. Confirm no future data leaks into training.
4. **Assess feasibility.** Check label availability and noise. Estimate class imbalance. Verify that the data volume supports meaningful evaluation (rule of thumb: ≥30 positives in the test set for binary classification).
5. **Design dataset schema.** List required features with types, ranges, and provenance. Mark features at risk of leakage (computed from the target or from future events).
6. **Define data validation rules.** Specify: expected null rates per column, value ranges, referential integrity, distribution checks on key features. These become the automated checks run before every training run.
7. **Write ML problem statement.** One-page doc: task type, label, primary metric, evaluation protocol, data sources, known risks (label noise, distribution shift, privacy), and the definition of "production-ready" for this model.

## Outputs

- ML problem statement document (task, label, metric, evaluation protocol, constraints, risks).
- Dataset schema with column types, ranges, and leakage risk flags.
- Data validation rule set (to be implemented in the training pipeline).
- Baseline performance expectation (random, majority-class, or simple heuristic) to anchor evaluation.

## Named Patterns

### Good — Metric aligned with product outcome
```
Product goal: reduce false-positive fraud blocks (currently blocking 2% of valid transactions).
ML task: binary classification, predict fraudulent transaction.
Primary metric: precision at fixed recall ≥ 0.90 (we accept missing some fraud to avoid blocking valid users).
Secondary: AUC-ROC for model comparison across thresholds.
Calibration check: reliability diagram on hold-out set.
```
The metric directly encodes the business trade-off. Threshold is set on the validation set to meet the recall constraint.

### Bad — Accuracy as the sole metric on imbalanced data
```
Dataset: 98% legitimate, 2% fraud.
Metric: accuracy.
Result: model predicts "legitimate" for everything → 98% accuracy, zero fraud caught.
```
Accuracy hides the failure. Use precision/recall/F1 or AUC-ROC.

### Good — Temporal split for time-series data
```
Train: data from 2023-01 to 2024-06
Val:   data from 2024-07 to 2024-09  (gap to avoid leakage from concurrent events)
Test:  data from 2024-10 to 2024-12
```
Future events cannot influence the training window. Evaluation reflects the realistic deployment scenario.

### Bad — Random split on temporal data
```python
X_train, X_test = train_test_split(df, test_size=0.2, random_state=42)
```
Future rows appear in train; past rows appear in test. Offline metrics look inflated; production performance is worse.

### Good — Leakage risk annotation in schema
```
feature: is_first_order        # OK — computed from historical orders only
feature: delivery_time_minutes # RISK: computed after order completion; label is "refund requested"
feature: support_ticket_count  # RISK: tickets opened after the event we predict
```
Risky features are flagged before engineering begins, not discovered after a suspiciously high AUC.

### Bad — Discovering leakage from a 0.99 AUC
Leakage found after three weeks of training iterations. The feature was obvious in hindsight.

## Boundaries

- Owns ML problem framing, evaluation protocol design, and data validation rule definition.
- Does not own business metric interpretation or A/B experiment design → `product-analyst`.
- Does not own data pipeline construction or warehouse SLA → `data-engineer`.
- Does not own system integration specifications → `system-analyst`.

## Sources

### Priority 1 — ML methodology canon
- Google Rules of Machine Learning — https://developers.google.com/machine-learning/guides/rules-of-ml
- scikit-learn: Model evaluation — https://scikit-learn.org/stable/modules/model_evaluation.html

### Priority 2 — Evaluation and framing practice
- ML Test Score (Breck et al., 2017) — https://research.google/pubs/pub46555/
- Chip Huyen: Designing ML Systems, Ch. 2 — book reference (O'Reilly, 2022)

### Priority 3 — Background
- Made With ML: Data — https://madewithml.com/

## Handoff

- Business metric ownership and A/B experiment interpretation → `product-analyst`.
- Data pipeline construction, warehouse, ETL → `data-engineer`.
- System integration contracts and API specifications → `system-analyst`.
- Feature engineering on the validated schema → `feature-engineering-and-validation`.
