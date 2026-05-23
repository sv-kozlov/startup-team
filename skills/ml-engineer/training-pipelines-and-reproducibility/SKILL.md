---
name: training-pipelines-and-reproducibility
description: Use when writing, reviewing, or repairing a model training pipeline — to ensure the run is parametrized, seed-fixed, version-pinned, CI-executable, and fully reproducible by a second independent run with the same configuration.
family: code
profile_level: Senior+
---

# Training Pipelines and Reproducibility

## Purpose

Make every training run an auditable, repeatable artifact. A pipeline that cannot be reproduced is a liability: the team cannot validate results, safely retrain, or bisect a quality regression. A CI-integrated pipeline is the minimum bar for a production model.

## Use When

- Writing a training script for a new model.
- Migrating training from a notebook to a production-grade script.
- A teammate cannot reproduce a reported model performance number.
- Adding a retraining trigger to an existing model.
- Setting up CI for ML training as part of a new project.

## Do Not Use When

- The feature set has not been designed and validated → use `feature-engineering-and-validation` first.
- The task is defining the evaluation protocol → use `ml-problem-framing-and-data-design`.
- The task is deploying the trained model → use `model-serving-and-inference`.
- The task is tracking experiments across many runs → use `experiment-tracking-and-registry`.

## Inputs

- Validated feature set and fitted Pipeline (from `feature-engineering-and-validation`).
- Data version reference (snapshot ID, S3 path with hash, or DWH table version).
- Hyperparameter ranges or fixed values from prior experiments.
- Target metric from the ML problem statement.

## Workflow

1. **Parametrize the run.** All hyperparameters, data paths, random seeds, output paths, and metric thresholds come from a config file (YAML/JSON) or CLI flags — not hardcoded in the script.
2. **Pin versions.** Record: data version (hash or snapshot ID), library versions (`pip freeze` or `conda env export`), and git commit SHA. Write these to the experiment tracker before training begins.
3. **Fix randomness.** Set `random_state` in all sklearn estimators; set `torch.manual_seed`, `np.random.seed`, and `PYTHONHASHSEED` for deep learning runs. Document that reproducibility is approximate for GPU training (non-deterministic CUDA ops).
4. **Write modular train script.** Separate: data loading, preprocessing, model training, evaluation, and artifact saving. Each step is independently testable.
5. **Evaluate on hold-out.** After training, run evaluation on the test split. Log all metrics, not just the primary one. Save confusion matrix or calibration plot as an artifact.
6. **Emit a quality gate.** If primary metric < threshold, fail the script with a non-zero exit code. The CI pipeline fails; no bad model is registered.
7. **Log to experiment tracker.** Log params, metrics, and all artifacts (model file, feature schema, evaluation report) in one run context before the script exits.
8. **Run in CI.** The training script must be executable via `python train.py --config config.yaml` with no interactive prompts. A CI job triggers it on data or code changes and fails on regression.

## Outputs

- `train.py` (or equivalent) with parametrized, modular structure.
- `config.yaml` / `config.json` with all hyperparameters and path references.
- Experiment tracker run with params, metrics, and artifacts.
- CI workflow definition (GitHub Actions / GitLab CI / Jenkins) for training.
- Reproducibility test: documented result of running the same config twice on the same data.

## Named Patterns

### Good — Parametrized training script with MLflow logging
```python
import argparse, yaml, mlflow, numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score
import joblib

def train(cfg: dict):
    np.random.seed(cfg["seed"])
    # --- data loading (from versioned snapshot) ---
    X_train, y_train = load_data(cfg["data"]["train_path"])
    X_val,   y_val   = load_data(cfg["data"]["val_path"])

    model = GradientBoostingClassifier(
        n_estimators=cfg["model"]["n_estimators"],
        max_depth=cfg["model"]["max_depth"],
        learning_rate=cfg["model"]["lr"],
        random_state=cfg["seed"],
    )

    with mlflow.start_run():
        mlflow.log_params(cfg["model"])
        mlflow.log_param("seed", cfg["seed"])
        mlflow.log_param("data_version", cfg["data"]["version"])

        model.fit(X_train, y_train)
        auc = roc_auc_score(y_val, model.predict_proba(X_val)[:, 1])
        mlflow.log_metric("auc_val", auc)

        if auc < cfg["quality_gate"]["min_auc"]:
            raise ValueError(f"AUC {auc:.4f} below gate {cfg['quality_gate']['min_auc']}")

        mlflow.sklearn.log_model(model, artifact_path="model")
        joblib.dump(model, "model.pkl")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    with open(args.config) as f:
        cfg = yaml.safe_load(f)
    train(cfg)
```

### Bad — Hardcoded notebook converted to script
```python
# train.py
import pandas as pd
df = pd.read_csv("/home/user/data/my_data_v3_final.csv")
model = GradientBoostingClassifier(n_estimators=500)
model.fit(df.drop("label", axis=1), df["label"])
import joblib; joblib.dump(model, "model_final.pkl")
print("AUC:", 0.87)
```
No config, no logging, no quality gate, no reproducibility. Path is local. AUC is hardcoded.

### Good — Quality gate as CI step
```yaml
# .github/workflows/train.yml
jobs:
  train:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r requirements.txt
      - run: python train.py --config config/prod.yaml
        env:
          MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_URI }}
```
CI fails if quality gate is not met. No bad model reaches the registry.

### Bad — Training triggered manually, results shared via Slack
"I ran it and got 0.91, here's the pkl." Unreproducible; no audit trail; no gate.

### Good — Reproducibility test documented
```
Run 1 (2026-05-20, commit abc123, data v2024-10): AUC val = 0.8812
Run 2 (2026-05-21, commit abc123, data v2024-10): AUC val = 0.8812
Delta: 0.0000  ✓ Reproducible on CPU. GPU training: delta ≤ 0.001 acceptable.
```

## Boundaries

- Owns training script structure, parametrization, reproducibility, and CI integration.
- Does not own experiment comparison and model registry promotion → `experiment-tracking-and-registry`.
- Does not own feature design or leakage elimination → `feature-engineering-and-validation`.
- Does not own model deployment and serving → `model-serving-and-inference`.

## Sources

### Priority 1 — Framework documentation
- MLflow: Tracking — https://mlflow.org/docs/latest/tracking.html
- scikit-learn: Pipeline — https://scikit-learn.org/stable/modules/compose.html
- PyTorch: Reproducibility — https://pytorch.org/docs/stable/notes/randomness.html

### Priority 2 — Engineering practice
- Martin Fowler: CD4ML — https://martinfowler.com/articles/cd4ml.html
- ML Test Score (Breck et al.) — https://research.google/pubs/pub46555/
- The Twelve-Factor App — https://12factor.net/

### Priority 3 — Orientation
- Full Stack Deep Learning: Training — https://fullstackdeeplearning.com/
- Made With ML: Training — https://madewithml.com/

## Handoff

- Experiment comparison and model registry → `experiment-tracking-and-registry`.
- Feature design and leakage fixes → `feature-engineering-and-validation`.
- Model deployment and API → `model-serving-and-inference`.
- CI/CD platform configuration and infrastructure → `devops-sre`.
