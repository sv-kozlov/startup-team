---
name: launch-and-post-launch
description: Use when product launch readiness must be assessed from the product side, or when post-launch results must be interpreted and converted into a next product decision. Covers product-level launch criteria, rollout strategy, post-launch metric review, and next-step recommendation.
family: method
profile_level: Senior+
---

# Launch and Post-Launch

## Purpose

Connect launch decisions to product goals, readiness criteria, measurement setup, and learning — and then convert post-launch results into a clear next product decision: scale, iterate, roll back, or investigate. Launch is not the finish line; it is the start of learning at production scale.

## Use When

- A feature, product, or significant change is approaching launch and product-side readiness must be assessed.
- Product launch criteria, risks, or go / no-go logic need clarification.
- Post-launch metrics, analytics results, or user signals must be synthesized into a product recommendation.
- The team must decide whether to scale, iterate, roll back, or investigate after observing post-launch behavior.

## Do Not Use When

- Release process, deployment pipeline, and operational readiness — hand off to engineering / DevOps.
- QA sign-off, regression coverage, and release quality — hand off to `qa-engineer`.
- Marketing campaign design, channel planning, and customer communications — hand off to marketing.
- Metric methodology, statistical interpretation, and dashboard design — hand off to `product-analyst`.

## Inputs

- Product goal and hypothesis for the launch (from `product-hypothesis-management` or `product-metrics`).
- Release scope and what is and is not included in this release.
- Post-launch metrics: activation, retention, conversion, usage, error rates, NPS/CSAT changes.
- Analytics events readiness: are the critical events instrumented and verified?
- Go-to-market context: messaging, target segment, timing, support readiness.
- Known risks: regulatory, technical, operational, or reputational.

## Workflow

1. **Clarify the launch objective.** State the product outcome expected from this launch, the success metric, and the time window for measurement. Connect to the hypothesis decision rule if one exists.
2. **Define product-side launch criteria.** List the product conditions that must be true before launching: hypothesis is clear, success metric is defined and instrumented, guardrail metrics are active, rollout strategy is agreed, and rollback procedure is defined.
3. **Map readiness across functions.** Identify what each adjacent function must confirm: QA sign-off (→ `qa-engineer`), analytics instrumentation (→ `product-analyst`), delivery status (→ `project-manager`), go-to-market readiness (→ marketing), support briefing (→ support lead). Flag any open items.
4. **Set the rollout strategy.** Choose: full launch, percentage rollout, feature flag by segment, geography, or user tier. Name the criteria for expanding rollout (metric above threshold) and the criteria for pausing or rolling back (guardrail metric breached, error rate spike).
5. **Record launch risks and owners.** For each risk: what is the failure mode, who owns detection, what is the response action, and at what threshold does it trigger. Do not leave risks as vague concerns.
6. **Post-launch: compare results to prediction.** After the measurement window, compare actual metric movement to the decision rule. Classify the result: confirmed (go forward), disconfirmed (stop or roll back), inconclusive (extend window or change measurement).
7. **Produce the next-decision recommendation.** Based on result: scale (full rollout, invest in next improvement), iterate (specific change that addresses the observed gap), roll back (metric harm confirmed), investigate (unexpected result; deeper analytics needed), or kill and learn (hypothesis was wrong; document learning).

## Outputs

- Product-side launch criteria checklist.
- Readiness map across functions with open items flagged.
- Rollout strategy with expansion and rollback thresholds.
- Launch risk register with owners and response triggers.
- Post-launch review: result vs prediction, decision outcome.
- Next-decision recommendation with rationale.

## Named Patterns

### Good — Phased rollout with expansion criteria
"Launch to 10% of SMB cohort for 2 weeks. Expand to 100% if: (a) 7-day team activation rate in experiment group > 38%, (b) error rate does not exceed 0.5%, (c) support tickets do not increase > 15%. Roll back if: activation < 25% OR error rate > 2%."
Clear thresholds; no ambiguity about when to expand or stop.

### Bad — Big-bang launch with no rollback plan
"We launch to all users on Monday." No staged rollout, no metrics being monitored, no rollback procedure defined. When something goes wrong, the response is improvised under pressure.

### Good — Post-launch review with decision classification
"Prediction: activation +10pp. Result: activation +7pp, within inconclusive range (±5pp margin). Decision: extend measurement window by 2 weeks and investigate whether the new segment (enterprise) is diluting the signal."

### Bad — Post-launch celebration without learning
Launch metrics are reported as green. Team moves to next initiative without recording what assumptions were confirmed, what was inconclusive, or what should be different next time. Learning is lost.

### Good — Instrumentation verified before launch
"Analytics readiness: all 4 critical events are instrumented and verified in staging. The PM and product analyst reviewed event schemas 3 days before launch. No gaps."

### Bad — Launch before instrumentation
"We will add proper tracking in the next sprint." Post-launch metric data is missing, incomplete, or unreliable. The team cannot tell whether the launch worked.

### Good — Problem-first post-launch interpretation
"Activation improved but NPS for the affected segment dropped 8 points. We investigate: are users completing onboarding but experiencing friction downstream? The metric result is ambiguous; we do not scale yet."

### Bad — Selective metric reading
"Activation improved, so the launch was a success." Guardrail metrics (NPS, support volume) are ignored because they are inconvenient. The team misses a signal that the improvement created downstream harm.

## Boundaries

- Does not own release process, deployment, or infrastructure rollback — engineering / DevOps.
- Does not own marketing campaign design, communications, or channel strategy — marketing.
- Does not own QA sign-off, regression, or release quality process — `qa-engineer`.
- Does not own statistical interpretation of experiment results — `product-analyst`.
- Does not own delivery status, milestone tracking, or escalation — `project-manager`.

## Sources

### Priority 1 — Product launch and learning
- Marty Cagan, "Inspired" — launch and learning chapters
- Teresa Torres, "Continuous Discovery Habits" — learning loops and decision rules
- Reforge on product launches — https://www.reforge.com/blog

### Priority 2 — Feature flags and rollout strategy
- LaunchDarkly, feature flag best practices — https://launchdarkly.com/blog/
- Martin Fowler on feature toggles — https://martinfowler.com/articles/feature-toggles.html
- Lenny Rachitsky on launches — https://www.lennysnewsletter.com/

### Priority 3 — Supplementary
- Mind the Product on go-to-market and launch — https://www.mindtheproduct.com/
- John Cutler on post-launch learning — https://cutlefish.substack.com/

## Handoff

- Release process, deployment, and rollback → engineering / `devops-sre`.
- QA sign-off and regression coverage → `qa-engineer`.
- Analytics instrumentation and statistical interpretation → `product-analyst`.
- Go-to-market, messaging, and customer communications → marketing.
- Delivery status and milestone tracking → `project-manager`.
- Hypothesis decision rule update after post-launch result → `product-hypothesis-management`.
