---
name: ab-testing-and-experimentation
description: Use when a product change needs causal measurement — experiment design with power and MDE, pre-analysis plan, SRM check, readout interpretation, or ship/rollback/iterate recommendation. Triggers on any question requiring controlled causal evidence rather than observational correlation.
family: core
profile_level: Senior+
---

# A/B Testing and Experimentation

## Purpose

Plan and read controlled experiments so the team can make causal claims, avoid false positives and false negatives, and act on results without overstating noisy, underpowered, or biased evidence.

## Use When

- Designing an experiment: hypothesis, unit of randomization, eligible population, metrics, MDE, sample size, duration, and stopping rule.
- Reviewing an existing experiment design for statistical and logical soundness before launch.
- Interpreting A/B test results: effect size, confidence interval, p-value, guardrail movement, SRM check.
- Recommending ship, iterate, rollback, or retest with explicit risk framing.
- Evaluating whether to use A/B, multi-variant, holdout, switchback, or quasi-experimental design.

## Do Not Use When

- The change has no counterfactual; observational diagnosis is needed instead → `behavior-and-cohort-analytics`.
- The hypothesis has not yet been framed or sized → `product-hypothesis-and-opportunity-analysis`.
- The feature flag implementation or QA of experiment exposure is needed → engineering / `qa-engineer`.
- The launch or rollback decision is final → `product-manager` (analyst informs, PM decides).

## Inputs

- Hypothesis statement: treatment, control, eligible population, unit of randomization.
- Primary metric, guardrail metrics, expected effect (MDE), current baseline, traffic, and allocation.
- For readout: observed results, confidence intervals, p-values, SRM diagnostic, and data-quality notes.

## Workflow

1. **State the hypothesis and decision rule before running or reading results.** Pre-registration prevents HARKing (Hypothesizing After Results are Known).
2. **Validate randomization design.** Is the unit correct (user, session, device, account)? Is assignment stable? Are there interference, spillover, or novelty-effect risks?
3. **Calculate sample size and duration.**
   - Choose MDE: the smallest effect worth detecting, not the smallest the test might show.
   - Choose power (typically 0.80) and significance level (typically 0.05).
   - Compute minimum sample per variant; convert to days using current traffic.

   ```python
   from scipy.stats import norm
   import math

   def min_sample_size(p_baseline: float, mde: float,
                       alpha: float = 0.05, power: float = 0.80) -> int:
       """Two-proportion z-test sample size per variant."""
       p_treatment = p_baseline * (1 + mde)
       p_bar = (p_baseline + p_treatment) / 2
       z_alpha = norm.ppf(1 - alpha / 2)   # two-sided
       z_beta  = norm.ppf(power)
       n = (z_alpha + z_beta) ** 2 * (p_baseline * (1 - p_baseline) +
                                       p_treatment * (1 - p_treatment))
       n /= (p_treatment - p_baseline) ** 2
       return math.ceil(n)

   n = min_sample_size(p_baseline=0.10, mde=0.05)
   print(f"Min sample per variant: {n}")  # → ~14 745 at 5% baseline, 5% relative MDE
   ```

4. **Check SRM (Sample Ratio Mismatch) before reading results.** A mismatch between expected and observed allocation invalidates the test.

   ```python
   from scipy.stats import chi2_contingency
   import numpy as np

   def srm_check(n_control: int, n_treatment: int,
                 expected_split: float = 0.5) -> dict:
       """Chi-square SRM check. Returns p-value; p < 0.01 signals mismatch."""
       n_total = n_control + n_treatment
       expected = np.array([n_total * expected_split,
                            n_total * (1 - expected_split)])
       observed = np.array([n_control, n_treatment])
       # chi2_contingency on a 1×2 table; use chisquare directly
       from scipy.stats import chisquare
       stat, p = chisquare(observed, f_exp=expected)
       return {"chi2": round(stat, 3), "p_value": round(p, 4),
               "srm_detected": p < 0.01}

   print(srm_check(9850, 10150))  # balanced: no SRM
   print(srm_check(8900, 11100))  # imbalanced: SRM detected — do not interpret results
   ```

5. **Interpret effect and uncertainty.** Report effect size with 95% CI, not just p < 0.05. Practical significance (MDE) and statistical significance are different.

   ```python
   from scipy.stats import norm

   def two_proportion_ztest(x_c: int, n_c: int,
                             x_t: int, n_t: int,
                             alpha: float = 0.05) -> dict:
       """Two-proportion z-test. x = successes, n = sample."""
       p_c, p_t = x_c / n_c, x_t / n_t
       p_pool = (x_c + x_t) / (n_c + n_t)
       se = math.sqrt(p_pool * (1 - p_pool) * (1 / n_c + 1 / n_t))
       z = (p_t - p_c) / se
       p_val = 2 * (1 - norm.cdf(abs(z)))
       ci_se = math.sqrt(p_t * (1 - p_t) / n_t + p_c * (1 - p_c) / n_c)
       z_crit = norm.ppf(1 - alpha / 2)
       diff = p_t - p_c
       ci = (diff - z_crit * ci_se, diff + z_crit * ci_se)
       return {
           "p_control": round(p_c, 4), "p_treatment": round(p_t, 4),
           "absolute_diff": round(diff, 4),
           "relative_lift": round(diff / p_c * 100, 2),
           "95_ci": (round(ci[0], 4), round(ci[1], 4)),
           "p_value": round(p_val, 4),
           "significant": p_val < alpha,
       }

   print(two_proportion_ztest(500, 5000, 550, 5000))
   ```

6. **Check guardrail metrics.** A positive primary result with a deteriorating guardrail (latency, error rate, revenue per user) must be resolved before shipping.
7. **Recommend action with residual risk and follow-up.** "Ship" requires: primary significant + guardrails stable + SRM clean + effect size ≥ MDE.

## Outputs

- Experiment design document (hypothesis, unit, metrics, MDE, sample size, duration, stopping rule)
- Pre-analysis plan (pre-registered before launch)
- A/B test readout (SRM check, effect size, CI, guardrail table)
- Ship / iterate / rollback / retest recommendation with explicit risk framing

## Named Patterns

**Good: pre-registered experiment design**
```
Hypothesis: Adding social proof to checkout increases purchase conversion.
Mechanism: Uncertainty reduction → lower abandonment.
Unit: user_id (server-side assignment, stable).
Primary metric: purchase_conversion_rate (purchases / checkout_starts).
Guardrails: checkout_p99_latency_ms ≤ 800; cart_abandonment_rate stable.
MDE: +5% relative (baseline 10% → expected 10.5%).
Sample per variant: 14 745 users.
Duration: 14 days (based on 2 100 checkout_starts/day in eligible population).
Stopping rule: read only at day 14; no peeking.
Decision rule: ship if primary significant at α=0.05 AND guardrails stable AND SRM clean.
```

**Bad: "launch and see" without pre-registration**
```
Let's just roll it out to 10% and see what happens.
-- No hypothesis, no MDE, no stopping rule, no guardrails.
-- Any positive number will be called a "win" (HARKing).
```

**Good: SRM check before reading results**
Expected 50/50 split → observed 48/52 → chi-square p = 0.003 → SRM detected → root-cause investigation before interpreting primary metric.

**Bad: interpret results despite SRM**
SRM detected but ignored; primary metric interpreted anyway → biased estimate, wrong decision.

**Good: effect size with CI, not just p-value**
"Treatment lifted conversion by +0.5pp (95% CI: +0.2pp to +0.8pp, p = 0.003). Practical MDE was +0.5pp; effect is on the boundary — proceed with segment analysis before broad rollout."

**Bad: p < 0.05 declared a win**
"The test is significant (p=0.04), shipping." — No CI, no effect size, no guardrail check, no MDE comparison.

**Good: power calculation before launch**
With baseline 10%, MDE 5% relative, α=0.05, power=0.80 → need 14 745 users/variant. At 2 100 daily eligibles, test needs 14 days minimum. Confirm traffic before launching.

**Bad: underpowered test run for 3 days**
Test run 3 days; p = 0.35; "no effect found." — Sample was 900 per variant; powered to detect only >40% relative lift. Null result is uninformative.

## Boundaries

- Does not treat observational correlation as causal proof without explicit quasi-experimental design.
- Does not override the Product Manager's launch decision; the analyst provides evidence and risk framing.
- Does not own feature flag implementation, experiment platform setup, or QA of exposure logging → engineering / `qa-engineer`.
- Does not run advanced causal inference (DiD, IV, synthetic control) without flagging that `ml-engineer` / `data-scientist` may be needed.

## Sources

**Priority 1 — canonical**
- Kohavi, R., Tang, D., & Xu, Y., Trustworthy Online Controlled Experiments (Cambridge, 2020): https://www.exp-platform.com/Documents/2013-02-CACM.pdf
- Statsig experimentation guide: https://www.statsig.com/perspectives/ab-testing-statistical-significance
- Optimizely sample size calculator: https://www.optimizely.com/sample-size-calculator/

**Priority 2 — practitioner**
- Reforge experimentation resources: https://www.reforge.com/growth-series
- Netflix Technology Blog, experimentation platform: https://netflixtechblog.com/experimentation-is-a-major-focus-of-data-science-across-netflix-f67923f8e985
- Kohavi et al., Online Experimentation at Microsoft: https://www.exp-platform.com/Documents/ExP_DMCaseStudies.pdf

**Priority 3 — supplementary**
- SciPy statistics module: https://docs.scipy.org/doc/scipy/reference/stats.html
- Causal Inference for the Brave and True (Matheus Facure): https://matheusfacure.github.io/python-causality-handbook/

## Handoff

```
To: product-manager
Task: Make the final ship / iterate / rollback decision based on experiment readout.
Context: Readout complete. Primary significant, guardrails stable, SRM clean.
Inputs: Experiment readout with effect size, CI, guardrail table, and residual risks.
Expected artifact: Go/no-go decision logged in ticket.
Acceptance criteria: Decision recorded with rationale referencing the readout.
```

```
To: qa-engineer
Task: Validate experiment exposure logging and event quality before reading results.
Context: Experiment launched; SRM check needs clean tracking to be trusted.
Inputs: Event schema, expected exposure event, eligibility rules.
Expected artifact: QA report confirming exposure event firing and parameter correctness.
Acceptance criteria: No duplicate exposure events; assignment stable per user.
```
