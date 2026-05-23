---
name: python-and-tooling-for-analytics
description: Use when SQL and dashboards are insufficient for an analytical task — statistical tests, cohort modeling, visualization, simulation, or ML-impact framing. Triggers when reproducible Python analysis, pandas pipelines, scipy statistical tests, or evaluation of ML feature impact from a product analytics perspective is needed.
family: advanced
profile_level: Senior+
---

# Python and Tooling for Analytics

## Purpose

Support reproducible product analysis and statistical validation when SQL queries or BI dashboards are not sufficient — using pandas pipelines, scipy statistical tests, cohort modeling, and ML-product framing — without entering ML engineering, production pipeline, or model training territory.

## Use When

- Running statistical tests: chi-square, two-proportion z-test, t-test, Mann-Whitney, or bootstrap confidence intervals.
- Building reproducible cohort calculations, funnel models, or LTV simulations in Python.
- Creating visualization artifacts for analysis memos or team presentations.
- Cleaning and joining analytical datasets extracted from the data warehouse.
- Evaluating ML feature product impact: translating model output into user-facing metrics, defining online/offline metric alignment, and framing a handoff to Data Science.
- Automating repetitive analytical tasks (scheduled metric pulls, anomaly flagging, report generation).

## Do Not Use When

- The task requires production pipelines, Airflow DAGs, or data engineering → `data-engineer`.
- The task requires ML model training, feature engineering, hyperparameter tuning, or deployment → `ml-engineer` / `data-scientist`.
- The task requires governed recurring enterprise reporting → `data-analyst` / `data-bi`.
- SQL alone is sufficient — prefer SQL for reproducibility and auditability at query level.

## Inputs

- Dataset extracts (CSV, Parquet, database connection), schema, metric definitions.
- Analytical question and expected output type (test result, chart, table, simulation).
- Statistical requirements: test type, significance level, power, effect size.
- For ML-adjacent tasks: ML use case description, model output format, eligible population, product goal.

## Workflow

1. **Keep raw data immutable.** Load once; do not overwrite. Document data source, extraction date, and any known caveats as comments or a `metadata` dict at the top of the notebook.

2. **Use explicit pandas transformations — no method chains longer than 3 steps without an intermediate variable.**

   ```python
   import pandas as pd
   from pathlib import Path

   # Load and document
   df_raw = pd.read_parquet("data/user_events_2024_q1.parquet")
   EXTRACTION_DATE = "2024-04-01"  # disclosed
   PLATFORM_SCOPE = ["ios", "android", "web"]  # disclosed
   EXCLUDE_TEST_USERS = True

   # Step 1: filter
   df = df_raw.copy()
   if EXCLUDE_TEST_USERS:
       df = df[~df["is_test_user"]]
   df = df[df["platform"].isin(PLATFORM_SCOPE)]

   # Step 2: compute metric per user
   user_metrics = (
       df.groupby("user_id")
         .agg(
             session_count=("session_id", "nunique"),
             revenue_usd=("revenue_usd", "sum"),
             first_event_ts=("event_ts", "min"),
         )
         .reset_index()
   )

   # Step 3: validate counts before proceeding
   assert len(user_metrics) > 0, "Empty dataset after filters"
   print(f"Users after filter: {len(user_metrics):,}")
   print(user_metrics.describe())
   ```

3. **Run the appropriate statistical test and report the full result — not just the p-value.**

   ```python
   from scipy import stats
   import numpy as np
   import math

   # Chi-square test for conversion rate difference (A/B readout)
   def chi2_conversion_test(x_control: int, n_control: int,
                             x_treatment: int, n_treatment: int,
                             alpha: float = 0.05) -> dict:
       table = [[x_control, n_control - x_control],
                [x_treatment, n_treatment - x_treatment]]
       chi2, p_val, dof, _ = stats.chi2_contingency(table, correction=False)
       p_c = x_control / n_control
       p_t = x_treatment / n_treatment
       diff = p_t - p_c
       # Wilson CI for the difference (approximate)
       se = math.sqrt(p_t*(1-p_t)/n_treatment + p_c*(1-p_c)/n_control)
       z = stats.norm.ppf(1 - alpha / 2)
       return {
           "p_control":       round(p_c, 4),
           "p_treatment":     round(p_t, 4),
           "absolute_diff":   round(diff, 4),
           "relative_lift_pct": round(diff / p_c * 100, 2),
           "95_ci":           (round(diff - z*se, 4), round(diff + z*se, 4)),
           "chi2":            round(chi2, 3),
           "p_value":         round(p_val, 4),
           "significant":     p_val < alpha,
           "dof":             dof,
       }

   result = chi2_conversion_test(480, 5000, 540, 5000)
   print(result)
   ```

4. **For ML-product framing, translate model output to user-facing metrics.**

   ```python
   # ML-adjacent: measure product impact of a recommendation model
   # Step 1: join model scores to user activity
   model_scores = pd.read_csv("data/rec_model_scores.csv")  # user_id, score, variant
   activity = pd.read_csv("data/user_activity.csv")         # user_id, clicked, purchased

   merged = model_scores.merge(activity, on="user_id", how="left")

   # Step 2: compare product metrics by model variant, not model quality metric
   impact = (
       merged.groupby("variant")
             .agg(
                 click_rate=("clicked", "mean"),
                 purchase_rate=("purchased", "mean"),
                 users=("user_id", "count"),
             )
             .reset_index()
   )
   print(impact)
   # Key principle: report click_rate and purchase_rate, NOT precision/recall.
   # Precision/recall are model quality metrics — handoff those to Data Science.
   ```

5. **Use bootstrap for non-normal distributions (revenue, LTV).**

   ```python
   def bootstrap_mean_ci(series: pd.Series, n_boot: int = 2000,
                          alpha: float = 0.05, seed: int = 42) -> tuple:
       rng = np.random.default_rng(seed)
       boots = [rng.choice(series.values, size=len(series), replace=True).mean()
                for _ in range(n_boot)]
       lower = np.percentile(boots, 100 * alpha / 2)
       upper = np.percentile(boots, 100 * (1 - alpha / 2))
       return round(lower, 2), round(upper, 2)

   ci = bootstrap_mean_ci(user_metrics["revenue_usd"])
   print(f"95% CI for mean ARPU: {ci}")
   ```

6. **Make notebooks restartable top-to-bottom.** Every cell must run in order from a clean kernel. Move reusable functions into named functions or utility modules; avoid copy-pasted code blocks.

7. **Document outputs inline.** Every chart title includes the question it answers. Every table header includes the metric formula. Every statistical result discloses n, time window, and exclusions.

## Outputs

- Reproducible notebook or script with documented filters, transformations, and statistical results
- Statistical test result (test statistic, p-value, CI, effect size, interpretation)
- Cohort or funnel model output (table or chart)
- ML-product metric brief (product impact framing, online metric definitions, Data Science handoff)
- Visualization artifacts for analytical memos
- Automation stub (scheduled metric pull, anomaly flag, report template)

## Named Patterns

**Good: documented pandas pipeline with intermediate validation**
See Workflow step 2 — named intermediate variables, explicit filters, `assert` and `print` for validation.

**Bad: chain of 12 `.pipe().query().groupby().merge()` without intermediate checkpoints**
Impossible to debug, audit, or explain. One wrong filter silently propagates.

**Good: full statistical result with CI**
Report: p_control=0.096, p_treatment=0.108, absolute_diff=+0.012, relative_lift=+12.5%, 95_CI=(+0.003, +0.021), p_value=0.009. Not just "p=0.009".

**Bad: p-value only**
"p=0.009 — significant." No effect size, no CI, no n, no time window. Unactionable for a decision memo.

**Good: raw data immutable; filtered copies named**
`df_clean`, `df_experiment_cohort`, `df_control` — each named, each documented. `df_raw` never modified.

**Bad: `df = df[df.x > 0]` repeated 4 times in different cells with different definitions of "clean"**
State of `df` is undefined after cell 7; reproducibility broken.

**Good: ML-product framing — product metrics, not model metrics**
"The recommendation model variant shows +4pp click-through and +2.1pp purchase conversion. Model quality metrics (nDCG, precision@k) are provided in the Data Science evaluation report — see handoff."

**Bad: reporting nDCG as the product success metric**
"The new model achieves nDCG@10 = 0.42 vs. 0.38 baseline — a success." nDCG is a model quality metric; the product team cannot interpret it as user value.

## Boundaries

- Does not build production ML systems, Airflow DAGs, or data pipelines → `data-engineer`.
- Does not own ML model training, feature engineering, hyperparameter tuning → `ml-engineer` / `data-scientist`.
- Does not replace governed BI for recurring enterprise reporting.
- Does not claim statistical results without disclosing n, time window, exclusions, and test assumptions.

## Sources

**Priority 1 — canonical**
- pandas Documentation: https://pandas.pydata.org/docs/
- SciPy Statistics Module: https://docs.scipy.org/doc/scipy/reference/stats.html
- NumPy Random Generator: https://numpy.org/doc/stable/reference/random/generator.html

**Priority 2 — practitioner**
- Rule et al., Ten Simple Rules for Reproducible Research in Jupyter Notebooks: https://arxiv.org/abs/1810.08055
- Causal Inference for the Brave and True (Matheus Facure): https://matheusfacure.github.io/python-causality-handbook/
- scikit-learn Model Evaluation: https://scikit-learn.org/stable/modules/model_evaluation.html

**Priority 3 — supplementary**
- EconML Documentation (uplift, causal ML for product analysts): https://econml.azurewebsites.net/
- Google ML Crash Course, classification metrics: https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall

## Handoff

```
To: data-scientist
Task: Evaluate causal uplift and model quality for [ML use case].
Context: Product metrics defined; model output framed from product perspective. Model quality evaluation and feature engineering needed.
Inputs: Online metric definitions, experiment design, model output format, product goal.
Expected artifact: Model quality evaluation report (nDCG, precision, uplift); feature importance notes.
Acceptance criteria: Offline metrics aligned with online product metrics; uplift estimate provided.
```

```
To: data-engineer
Task: Productionize the Python analysis as a scheduled pipeline or dbt model.
Context: Ad hoc Python analysis validated; recurring production version needed.
Inputs: Notebook with documented logic, source tables, transformation steps, output schema.
Expected artifact: Production pipeline with tests, scheduling, and monitoring.
Acceptance criteria: Output matches notebook results; latency meets agreed SLA.
```
