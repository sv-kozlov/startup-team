---
name: ml-testing-and-validation
description: Use when you need to verify correctness of ML code, validate data properties, run offline model evaluation, or maintain a regression test suite that guards against model quality degradation across retraining cycles.
family: method
profile_level: Senior+
---

# ML Testing and Validation

## Purpose

Systematically verify that the ML system is correct at three levels: code (functions behave as specified), data (inputs satisfy expected properties), and model (quality metrics meet defined thresholds on held-out data). Without structured testing, quality regressions are discovered in production.

## Use When

- Writing or reviewing ML code (preprocessing functions, training loop, evaluation logic).
- Validating a new dataset before it is used for training.
- Establishing the evaluation protocol for a model before the first training run.
- Adding a regression guard to prevent a previously measured quality level from deteriorating.
- Investigating a suspected model regression after a retraining cycle.

## Do Not Use When

- The evaluation protocol has not been defined → `ml-problem-framing-and-data-design` first.
- The task is monitoring model quality in production (drift, business metrics) → `ml-observability-and-drift`.
- The task is QA strategy and release-level regression testing → handoff to `qa-engineer`.

## Inputs

- ML problem statement with defined metrics and evaluation protocol.
- Validated feature set and fitted Pipeline.
- Training and test dataset snapshots (versioned).
- Golden dataset: a small, curated set of examples with known expected predictions (hand-labeled or canonically agreed).

## Workflow

### Code-level tests (unit + integration)
1. Test preprocessing functions in isolation: known input → expected output (type, range, no NaN).
2. Test Pipeline end-to-end: fit on small synthetic data → transform produces correct shape and dtype.
3. Test evaluation functions: known predictions and labels → expected metric value.
4. Test serialization: save and load model → identical predictions on the same input.

### Data property tests
5. For each column in the training dataset: assert expected null rate, value range, dtype, and cardinality (for categoricals). Use `pytest` assertions or Great Expectations suites.
6. Assert temporal integrity: no future-dated rows in train; no train rows in test by event_date.
7. Assert label distribution: positive rate within expected range (e.g., 0.01–0.10 for fraud).

### Offline model evaluation
8. Train on the agreed train split; evaluate on the held-out test split only once (no multiple test evaluations that invalidate the split).
9. Compute primary metric (AUC-ROC, F1, precision@recall, NDCG, etc.) and secondary metrics.
10. Calibration check: plot reliability diagram; compute expected calibration error (ECE) if the model output is used as a probability.
11. Error analysis: inspect false positives and false negatives. Find systematic failure modes (by segment, time period, or feature range).
12. Bias check: compute metric disaggregated by protected or business-relevant segments.
13. Document results in an evaluation report. Compare to baseline and to the previous production model.

### Regression test (golden dataset)
14. After each retraining, run predictions on the golden dataset. Assert that all predictions match expected outputs within tolerance. A divergence signals a breaking change.

## Outputs

- `tests/` directory with unit, integration, and data property tests.
- Evaluation report: primary and secondary metrics, calibration plot, error analysis, bias check, comparison to baseline.
- Golden dataset with expected predictions (stored in version control).
- Regression test result (pass/fail with diff against expected).

## Named Patterns

### Good — Pytest unit test for preprocessing function
```python
import numpy as np
import pytest
from myproject.features import clip_and_log_transform

def test_clip_and_log_transform_positive():
    arr = np.array([1.0, 10.0, 1000.0])
    result = clip_and_log_transform(arr, upper=500.0)
    assert result.shape == arr.shape
    assert np.all(result >= 0)
    assert not np.any(np.isnan(result))

def test_clip_and_log_transform_zeros_handled():
    arr = np.array([0.0, -1.0, 5.0])
    result = clip_and_log_transform(arr, upper=500.0)
    assert not np.any(np.isnan(result))
```

### Bad — No tests, "it worked in the notebook"
Preprocessing function is a lambda in the notebook. Production data has edge cases (zeros, nulls, new categories). The service crashes or silently produces NaN predictions.

### Good — Data property test with pytest
```python
import pandas as pd, pytest

@pytest.fixture
def train_df():
    return pd.read_parquet("data/snapshots/2024-10/train.parquet")

def test_label_distribution(train_df):
    rate = train_df["label"].mean()
    assert 0.01 <= rate <= 0.15, f"Unexpected positive rate: {rate:.4f}"

def test_no_nulls_in_required_cols(train_df):
    required = ["amount", "tenure_days", "category", "label"]
    nulls = train_df[required].isnull().sum()
    assert nulls.sum() == 0, f"Nulls found:\n{nulls[nulls > 0]}"

def test_temporal_integrity(train_df):
    assert train_df["event_date"].max() < pd.Timestamp("2024-07-01"), \
        "Train set contains data from the validation window"
```

### Good — Calibration check
```python
from sklearn.calibration import calibration_curve
import matplotlib.pyplot as plt

prob_true, prob_pred = calibration_curve(y_test, y_prob, n_bins=10)
plt.figure(figsize=(6, 6))
plt.plot(prob_pred, prob_true, marker="o", label="Model")
plt.plot([0, 1], [0, 1], linestyle="--", label="Perfect calibration")
plt.xlabel("Mean predicted probability"); plt.ylabel("Fraction of positives")
plt.title("Reliability diagram"); plt.legend()
plt.savefig("artifacts/calibration.png")
```
ECE (Expected Calibration Error) logged as a metric; if the model is used as a probability score, calibration matters as much as AUC.

### Bad — Evaluating on test multiple times until satisfied
```
Run 1: AUC = 0.83. Not great. Let's tune.
Run 3: AUC = 0.87. Ship it.
```
The test set has been used for model selection → it is no longer a held-out set. Real test performance is unknown.

### Good — Golden dataset regression test
```python
import joblib, numpy as np

def test_golden_dataset_regression():
    model = joblib.load("model.pkl")
    golden = np.load("tests/golden/inputs.npy")
    expected = np.load("tests/golden/expected_probs.npy")
    actual = model.predict_proba(golden)[:, 1]
    np.testing.assert_allclose(actual, expected, atol=1e-4,
        err_msg="Model predictions diverged from golden dataset")
```
Catches silent regressions caused by dependency updates, config changes, or unexpected data drift in the training set.

## Boundaries

- Owns ML code testing, data property validation, offline model evaluation, and model regression tests.
- Does not own production drift monitoring and alerting → `ml-observability-and-drift`.
- Does not own QA strategy, release-level regression testing, or end-to-end product testing → `qa-engineer`.
- Does not own evaluation protocol definition → `ml-problem-framing-and-data-design`.

## Sources

### Priority 1 — Framework and methodology
- scikit-learn: Model evaluation — https://scikit-learn.org/stable/modules/model_evaluation.html
- scikit-learn: Calibration — https://scikit-learn.org/stable/modules/calibration.html
- ML Test Score (Breck et al., 2017) — https://research.google/pubs/pub46555/

### Priority 2 — Engineering practice
- Model Cards (Mitchell et al.) — https://arxiv.org/abs/1810.03993
- Google Rules of ML, Rule #28–35 — https://developers.google.com/machine-learning/guides/rules-of-ml
- Great Expectations — https://docs.greatexpectations.io/

### Priority 3 — Orientation
- Made With ML: Evaluation — https://madewithml.com/
- Chip Huyen: Designing ML Systems, Ch. 6 — book reference

## Handoff

- Production monitoring of deployed model quality and drift → `ml-observability-and-drift`.
- QA strategy and release-level regression testing → `qa-engineer`.
- Evaluation protocol revision (metric choice, split strategy) → `ml-problem-framing-and-data-design`.
- Data quality issues in the source tables → `data-engineer`.
