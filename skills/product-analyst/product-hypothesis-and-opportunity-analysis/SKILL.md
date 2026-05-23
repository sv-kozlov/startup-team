---
name: product-hypothesis-and-opportunity-analysis
description: Use when a product idea, growth opportunity, or funnel constraint must be turned into a falsifiable hypothesis, opportunity size estimate, and validation plan before building. Triggers on any request to evaluate whether a product bet is worth making, and what evidence would change the decision.
family: core
profile_level: Senior+
---

# Product Hypothesis and Opportunity Analysis

## Purpose

Turn product ideas and growth opportunities into falsifiable hypotheses with explicit assumptions, opportunity size estimates, and cheapest-sufficient validation plans — so teams invest in the right bets and learn fast from the wrong ones.

## Use When

- Framing a product hypothesis from a feature idea, user complaint, metric drop, or strategic bet.
- Sizing an opportunity: revenue potential, retention impact, CAC improvement, or acquisition gain.
- Building a validation plan for pre-build discovery, MVP, post-launch, or growth experiment.
- Diagnosing the constrained step in a growth funnel (acquisition, activation, retention, monetization, referral).
- Evaluating growth quality: separating volume from sustainable, margin-positive growth.

## Do Not Use When

- The decision about which opportunity to pursue belongs to the Product Manager → `product-manager`.
- The hypothesis is already framed and needs an experiment designed → `ab-testing-and-experimentation`.
- The task requires qualitative user research (interviews, usability studies) → `ui-ux-designer` / `ux-researcher`.
- The task is financial modeling or pricing strategy → `product-manager` + finance.

## Inputs

- Product idea, user pain point, metric anomaly, strategic initiative, or growth constraint.
- Available signals: funnel data, cohort data, revenue, churn, channel mix, competitor context.
- Decision threshold: what evidence would be enough to build, not build, or pivot?
- Timeline and resource constraints for validation.

## Workflow

1. **Write the hypothesis in structured form.**
   ```
   For [user segment],
   [proposed change] will cause [expected behavior change]
   which will improve [product/business outcome metric]
   by approximately [expected magnitude]
   within [time window].
   ```
   The hypothesis is falsifiable: there is a specific outcome that would prove it wrong.

2. **List the load-bearing assumptions.**
   Identify the 2–5 beliefs that must be true for the idea to work. Rank them by uncertainty and impact. The highest-uncertainty, highest-impact assumption gets validated first.

3. **Size the opportunity.**
   - Top-down: addressable user segment × conversion improvement × revenue per user.
   - Bottom-up: cohort analysis of similar past changes, or funnel simulation.
   - Use ranges, not point estimates. State confidence level and which assumption drives the range.

   ```python
   # Opportunity size: improving D7 retention in activation cohort
   eligible_users_per_week = 12_000
   current_d7_retention = 0.28
   target_d7_retention = 0.33      # hypothesis: +5pp absolute
   arpu_retained = 4.20            # USD per retained user per month

   incremental_users = eligible_users_per_week * (target_d7_retention - current_d7_retention)
   monthly_revenue_upside = incremental_users * arpu_retained * 4  # ~4 weeks/month
   print(f"Incremental retained users/week: {incremental_users:.0f}")
   print(f"Monthly revenue upside: ${monthly_revenue_upside:,.0f}")
   # Sensitivity: repeat for retention range 30%–35% to bracket estimate
   ```

4. **Choose the cheapest valid evidence.**
   Ordered by cost and speed: existing data analysis → instrumentation check → prototype → targeted experiment → rollout.
   Match the evidence type to the assumption type: behavioral data for behavioral assumptions, qualitative for motivational, experiments for causal.

5. **Identify the growth constraint.**
   For growth-oriented hypotheses, map the AARRR funnel (Acquisition → Activation → Retention → Referral → Revenue) and locate the step with the largest gap between its output and the next step's input. That is the constraint worth addressing first.

6. **Define success, failure, and inconclusive thresholds before analysis.**
   "Success" = primary metric moves by ≥ X within Y days with Z confidence.
   "Failure" = primary metric is flat or negative after sufficient power.
   "Inconclusive" = effect exists but is below MDE or data is underpowered.

7. **Separate growth quality from growth volume.**
   Segment results by acquisition channel, cohort, or user intent to avoid celebrating volume that does not convert to retention or monetization.

8. **Document risks, confounders, and follow-up questions.**

## Outputs

- Hypothesis statement (structured form)
- Assumption and risk map (ranked by uncertainty × impact)
- Opportunity size estimate (with range and sensitivity)
- Validation plan (evidence type, measurement approach, success/failure thresholds)
- Growth funnel constraint diagnosis
- Decision criteria for build / no build / pivot

## Named Patterns

**Good: structured hypothesis with falsifiable outcome**
```
For new mobile users (day 0–7 cohort),
adding an in-app onboarding checklist will increase feature discovery actions (≥ 3 distinct features used)
which will improve D7 retention from 28% to 33%
within 14 days of launch.
Falsified if: D7 retention does not improve by ≥ 2pp after 14 days with n ≥ 10 000 per variant.
```

**Bad: vague directional wish**
```
If we improve onboarding, users will be more engaged and retention will go up.
-- No segment, no mechanism, no metric, no magnitude, no falsifiability.
```

**Good: opportunity size with explicit sensitivity range**
```
Base case: +5pp D7 retention × 12 000 eligible/week × $4.20 ARPU = $25 200/month.
Low case:  +2pp = $10 080/month.
High case: +8pp = $40 320/month.
Key driver: assumed ARPU for activated cohort — validated from cohort data (P1 assumption).
```

**Bad: point estimate without assumptions**
```
"This will generate $25K/month" — no range, no stated assumption, no sensitivity.
```

**Good: growth constraint identification before choosing a fix**
Funnel: Install → Register → First action → Retained (D7).
Step gaps: Install→Register 70%, Register→First action 45%, First action→D7 retained 28%.
Largest absolute gap: Register→First action (55% drop). Fix activation before acquisition volume.

**Bad: adding users at top of funnel when activation is broken**
CAC spent on acquisition while activation converts at 45%. Every additional install loses 55% before the product is tried. Opportunity cost: fixing activation is 2–3× more capital-efficient at this stage.

**Good: cheapest sufficient evidence first**
Assumption: "Users don't use feature X because they don't know it exists."
Cheapest test: check % of users who viewed the feature entry point. If >80% viewed but didn't click, discoverability is not the problem — value proposition is. Saves 2-week experiment.

**Bad: jumping to experiment before checking existing data**
Building a 2-week A/B test to "prove the hypothesis" before checking whether the behavior is already measurable in logs. Common outcome: data already shows the answer.

## Boundaries

- Does not own the decision about which opportunity to build → `product-manager`.
- Does not own qualitative user research or UX discovery → `ui-ux-designer` / `ux-researcher`.
- Does not replace experiment design for causal validation → `ab-testing-and-experimentation`.
- Does not own marketing channel execution or campaign strategy.

## Sources

**Priority 1 — canonical**
- Kohavi, R. et al., Trustworthy Online Controlled Experiments (Cambridge, 2020): https://www.exp-platform.com/Documents/2013-02-CACM.pdf
- Croll, A. & Yoskovitz, B., Lean Analytics (2013): https://leananalyticsbook.com/
- Teresa Torres, Opportunity Solution Tree: https://www.producttalk.org/opportunity-solution-tree/

**Priority 2 — practitioner**
- Reforge Growth Model resources: https://www.reforge.com/growth-series
- Amplitude, Product-Led Growth Guide: https://amplitude.com/blog/product-led-growth
- Andrew Chen, The Cold Start Problem: https://andrewchen.com/

**Priority 3 — supplementary**
- Lenny Rachitsky newsletter (hypothesis framing, growth loops): https://www.lennysnewsletter.com/
- Crystal Widjaja, data and growth at Gojek: https://www.reforge.com/artifacts/

## Handoff

```
To: product-manager
Task: Review opportunity size and decide whether to prioritize this hypothesis.
Context: Hypothesis framed, opportunity sized, validation plan ready. Priority decision needed.
Inputs: Hypothesis statement, opportunity size (range), validation plan, key assumptions.
Expected artifact: Priority decision (build / hold / defer) logged with rationale.
Acceptance criteria: Decision references the stated assumptions and opportunity range.
```

```
To: ab-testing-and-experimentation
Task: Design a controlled experiment to validate the primary hypothesis.
Context: Hypothesis is pre-registered with expected mechanism and success criteria.
Inputs: Hypothesis statement, primary metric, MDE, eligible population, current baseline.
Expected artifact: Experiment design with sample size, duration, stopping rule.
Acceptance criteria: Sample size calculation confirmed; randomization unit validated.
```

```
To: ux-researcher
Task: Conduct qualitative research to validate the motivational assumption.
Context: Quantitative data shows the behavior gap but cannot explain user motivation.
Inputs: Behavioral data summary, list of open motivational questions, target user segment.
Expected artifact: Research synthesis with validated/invalidated motivational assumptions.
Acceptance criteria: Each listed assumption is addressed with evidence from at least 5 sessions.
```
