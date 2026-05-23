---
name: feature-engineering-and-validation
description: Use when designing, building, or auditing the feature set for a model — to eliminate leakage, wrap transformations in a fitted Pipeline, validate train-vs-serving distribution alignment, and ensure feature consistency between offline training and online inference.
family: code
profile_level: Senior+
---

# Feature Engineering and Validation

## Purpose

Build a feature set that is predictive, free of data leakage, and behaviorally identical at training time and serving time. Prevent the most common source of production model failures: a gap between the features seen during training and the features delivered at inference.

## Use When

- Designing features for a new model.
- Reviewing an existing feature set for leakage or train/serving skew.
- Refactoring raw transformations from a notebook into a reusable, testable Pipeline.
- Investigating unexpectedly high offline AUC that does not replicate in production.
- Preparing features for a feature store integration.

## Do Not Use When

- The ML problem is not yet framed → use `ml-problem-framing-and-data-design` first.
- The task is writing the training loop or hyperparameter search → use `training-pipelines-and-reproducibility`.
- The task is integrating with an existing feature store → use `data-and-feature-store-integration`.

## Inputs

- Dataset schema with column types, ranges, and leakage risk flags (from `ml-problem-framing-and-data-design`).
- Raw data from the agreed source; time window for train and the expected serving time window.
- Business intuition or domain knowledge about potential predictive signals.

## Workflow

1. **Audit for leakage.** For each candidate feature: is it computable from data available strictly before the prediction time? Features derived from the target, from post-event data, or from future-event aggregates are excluded.
2. **Define transformations.** Choose encoding (ordinal, one-hot, target encoding), scaling (StandardScaler, MinMaxScaler), and imputation strategy (median, mode, constant). Document the choice and reason.
3. **Wrap in a fitted Pipeline.** Use `sklearn.pipeline.Pipeline` or equivalent. `fit()` is called once, only on `X_train`. The same fitted object is used for `transform()` on val, test, and serving data.
4. **Validate distribution alignment.** Compare key feature distributions between train and the expected serving population. Use PSI or KS-test for continuous features; chi-squared for categorical. Flag divergences.
5. **Check feature importance.** After a first training run, use permutation importance or SHAP to verify that high-importance features are not leakage proxies.
6. **Test properties.** Write property-based tests: null rate within expected range, value range, no infinite values, output dtype after transform.
7. **Document feature schema.** For each feature: name, type, source column, transformation, expected range, leakage risk (yes/no/mitigated), and serving availability.

## Outputs

- Fitted `Pipeline` object (or equivalent) serializable as part of model artifact.
- Feature schema document.
- Distribution alignment report (PSI/KS per feature, flagged drifts).
- Feature property tests.

## Named Patterns

### Good — Leakage-free Pipeline with temporal split
```python
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier

# Temporal split — no shuffle
train = df[df["event_date"] < "2024-07-01"]
val   = df[(df["event_date"] >= "2024-07-01") & (df["event_date"] < "2024-10-01")]
test  = df[df["event_date"] >= "2024-10-01"]

numeric_cols = ["amount", "tenure_days"]
cat_cols     = ["category", "channel"]

preprocessor = ColumnTransformer([
    ("num", Pipeline([("impute", SimpleImputer(strategy="median")),
                      ("scale", StandardScaler())]), numeric_cols),
    ("cat", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1), cat_cols),
])

pipe = Pipeline([("prep", preprocessor), ("clf", GradientBoostingClassifier())])
pipe.fit(train[numeric_cols + cat_cols], train["label"])
val_pred = pipe.predict_proba(val[numeric_cols + cat_cols])[:, 1]
```
fit on train only; identical transform applied to val, test, and serving.

### Bad — Re-fitting scaler on test data
```python
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.fit_transform(X_test)   # fit on test leaks test statistics
```
Test statistics bleed into scaler parameters; AUC is inflated.

### Good — PSI for distribution alignment check
```python
import numpy as np

def psi(train_col: np.ndarray, serve_col: np.ndarray, buckets: int = 10) -> float:
    breaks = np.nanpercentile(train_col, np.linspace(0, 100, buckets + 1))
    breaks[0] -= 1e-6; breaks[-1] += 1e-6
    exp = np.histogram(train_col, bins=breaks)[0] / len(train_col)
    act = np.histogram(serve_col, bins=breaks)[0] / len(serve_col)
    exp = np.clip(exp, 1e-6, None); act = np.clip(act, 1e-6, None)
    return float(np.sum((act - exp) * np.log(act / exp)))

for col in numeric_cols:
    v = psi(train[col].dropna().values, serving_sample[col].dropna().values)
    print(f"{col}: PSI={v:.3f}  {'WARN' if v > 0.1 else 'OK'}")
```
PSI < 0.1: stable; 0.1–0.25: monitor; > 0.25: investigate before deploying.

### Bad — No train/serving alignment check
Model is trained on features from the data warehouse. Serving feature computation differs (different SQL, different aggregation window). Metrics drop 15% in production. Root cause takes two weeks to find.

### Good — Feature property test with pytest
```python
import pytest
import numpy as np

def test_pipeline_output_no_nulls(fitted_pipe, X_val):
    out = fitted_pipe.named_steps["prep"].transform(X_val)
    assert not np.isnan(out).any(), "NaN in transformed output"

def test_pipeline_output_shape(fitted_pipe, X_val):
    out = fitted_pipe.named_steps["prep"].transform(X_val)
    assert out.shape[1] == len(numeric_cols) + len(cat_cols)
```

### Bad — No tests on the transformation output
"The scaler worked in the notebook." Production data has a new category → OrdinalEncoder raises ValueError at 2 AM.

## Boundaries

- Owns feature design, leakage elimination, Pipeline construction, and train/serving alignment.
- Does not own data pipeline construction or warehouse ETL → `data-engineer`.
- Does not own feature store integration specifics (online retrieval, TTL, schema registry) → `data-and-feature-store-integration`.
- Does not own model training loop or hyperparameter search → `training-pipelines-and-reproducibility`.

## Sources

### Priority 1 — Framework documentation
- scikit-learn: Pipelines — https://scikit-learn.org/stable/modules/compose.html
- scikit-learn: Preprocessing — https://scikit-learn.org/stable/modules/preprocessing.html
- pandas Documentation — https://pandas.pydata.org/docs/

### Priority 2 — Engineering and methodology
- Google Rules of ML, Rule #16–20 (feature engineering) — https://developers.google.com/machine-learning/guides/rules-of-ml
- Chip Huyen: Designing ML Systems, Ch. 5 — book reference
- ML Test Score (Breck et al.) — https://research.google/pubs/pub46555/

### Priority 3 — Practice orientation
- Made With ML: Feature Engineering — https://madewithml.com/

## Handoff

- Data pipeline construction, DWH source tables → `data-engineer`.
- Feature store schema and online/offline retrieval design → `data-and-feature-store-integration`.
- Training loop and hyperparameter optimization → `training-pipelines-and-reproducibility`.
- Leakage or framing issue discovered → `ml-problem-framing-and-data-design` to revise the problem statement.
