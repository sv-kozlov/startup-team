---
name: product-metrics
description: Use when success metrics, north star logic, metric trees, OKR alignment, or guardrail metrics for a product initiative must be defined. Covers outcome-level metric framing, metric hierarchy construction, and the handoff of measurement methodology to product-analyst.
family: method
profile_level: Senior+
---

# Product Metrics

## Purpose

Define what product success means and how decisions will be evaluated — before the work starts. A metric frame is not a reporting dashboard; it is a decision instrument. It answers: what outcome are we targeting, what signals tell us we are moving toward it, and what guardrails tell us we are breaking something important.

## Use When

- A product initiative lacks a clear success metric.
- The team is debating whether a feature "worked" after launch.
- OKRs or quarterly targets must be translated into product-level metric commitments.
- A Product Analyst needs a clear product question and decision rule to design an experiment or dashboard.
- North star alignment is needed across teams working on related initiatives.

## Do Not Use When

- Statistical methodology, experiment design, or significance calculation is needed — hand off to `product-analyst`.
- Dashboard implementation, data pipeline, or instrumentation is needed — hand off to `product-analyst` or engineering.
- Metric results must be interpreted after the fact — use `launch-and-post-launch`.
- The task is to prioritize initiatives based on expected metric impact — use `prioritization-and-tradeoffs`.

## Inputs

- Product goal and the business objective it serves.
- User behavior model: what actions indicate value being delivered.
- Existing metric baselines and historical benchmarks.
- Known measurement constraints: what events are instrumented, what is not yet tracked.
- OKR context from leadership or product strategy.

## Workflow

1. **Anchor to the product outcome.** State the user and business outcome the initiative targets. Avoid output metrics (features shipped, stories completed) — focus on behavior change or business result.
2. **Define the north star metric.** Choose one metric that best captures whether the product is delivering value to users and the business simultaneously. The north star must be leading (responsive to product decisions within weeks) and causal (strongly correlated with long-term retention or revenue).
3. **Build the metric tree.** Decompose the north star into 2–4 input metrics that drive it. For each input, identify the product actions or user behaviors that move it. This creates the chain: product action → input metric → north star → business outcome.
4. **Set guardrail metrics.** Name the metrics that must not degrade while pursuing the primary outcome. Common guardrails: latency, error rate, churn of adjacent segments, revenue per user, support ticket volume. Guardrails define what "winning badly" looks like.
5. **Align with OKRs.** Map the metric tree to the relevant OKR: which Key Result does this initiative contribute to? Is the expected metric movement sufficient to meaningfully shift the KR?
6. **Specify the measurement frame.** Define: measurement window (e.g., 30-day retention), segmentation (e.g., activated users in the SMB cohort), expected direction (increase / decrease / stabilize), and minimum detectable effect if relevant.
7. **Mark measurement risks.** List any instrumentation gaps, attribution ambiguity, or confounding events that would make measurement unreliable. Flag for `product-analyst`.
8. **Hand off.** Pass the complete metric frame to `product-analyst` for methodology, dashboard design, and experiment setup. Pass the success criteria to `product-hypothesis-management`.

## Outputs

- North star metric with rationale and time-to-signal estimate.
- Metric tree: input metrics and their links to user actions.
- Guardrail metrics with acceptable degradation thresholds.
- OKR alignment mapping.
- Measurement frame: window, segmentation, expected direction, effect size.
- Measurement risk log and handoff to `product-analyst`.

## Named Patterns

### Good — Outcome metric with causal chain
"North star: weekly active teams (teams that complete ≥2 collaborative sessions per week). Input metrics: invite acceptance rate, session completion rate, return session within 7 days. Guardrail: individual user latency p95 must not increase. Rationale: WAT predicts 12-month retention (r=0.72 in historical data)."

### Bad — Output metric disguised as outcome
"Success metric: we shipped the collaboration feature on time and it has no P0 bugs." This measures delivery quality, not product outcome. No learning, no decision instrument.

### Good — North star that balances user and business value
North star captures a behavior that reflects real user value AND predicts long-term revenue. Example: "Activated paying teams" — requires both activation (user value) and payment (business value).

### Bad — North star that optimizes for vanity
"Total users" or "page views." Easy to move with marketing spend or dark patterns; does not predict retention or revenue. Teams maximize the metric without creating value.

### Good — OKR aligned metric tree
"OKR: Grow SMB segment ARR by 20%. Key Result: Increase SMB 90-day retention to 65%. Product metric: 30-day activation rate for SMB (target: 55%). Input metric: percentage of SMBs who invite ≥3 team members within 7 days."
Each level is connected; the product metric is the causal lever for the KR.

### Bad — OKR with disconnected product work
"OKR: Grow SMB ARR by 20%. Product initiative: redesign the navigation." No connection between the initiative and the business metric. Cannot attribute result; cannot learn.

### Good — Guardrail metric prevents winning badly
"Primary: increase checkout conversion rate. Guardrail: return rate must not increase more than 2pp. Guardrail: CS ticket volume for payment issues must not increase." Prevents optimizing checkout by hiding information users need.

### Bad — No guardrails
Checkout conversion increases 4pp but return rate doubles and NPS drops 12 points. No one defined what "winning badly" looked like, so no one stopped the experiment.

## Boundaries

- Does not own statistical methodology, significance testing, or dashboard implementation — `product-analyst`.
- Does not own data pipeline, instrumentation, or event tracking setup — engineering.
- Does not interpret post-launch metric results — `launch-and-post-launch`.
- Does not invent metric baselines or benchmarks; uses existing data or flags the gap.

## Sources

### Priority 1 — Metrics frameworks and north star
- Marty Cagan, "Inspired" — metric framing in product chapters
- Reforge, North Star Framework — https://www.reforge.com/blog/north-star-metric
- Amplitude, Product Metrics Guide — https://amplitude.com/blog/product-metrics

### Priority 2 — OKR and metric trees
- John Doerr, "Measure What Matters" — OKR methodology
- Lenny Rachitsky, product metrics — https://www.lennysnewsletter.com/
- John Cutler on metric trees — https://cutlefish.substack.com/

### Priority 3 — Supplementary
- Mixpanel, metric guides — https://mixpanel.com/blog/
- Mind the Product on metrics — https://www.mindtheproduct.com/

## Handoff

- Dashboard design, event instrumentation, and statistical methodology → `product-analyst`.
- Experiment success criteria and decision rule → `product-hypothesis-management`.
- OKR metric mapping to leadership or strategy review → `product-stakeholder-alignment`.
- Post-launch interpretation of metric results → `launch-and-post-launch`.
