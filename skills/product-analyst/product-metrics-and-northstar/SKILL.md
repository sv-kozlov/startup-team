---
name: product-metrics-and-northstar
description: Use when a product decision needs a measurable metric system, North Star, unit-economics framing, metric dictionary, or guardrail set. Triggers on metric design, metric tree construction, KPI decomposition, LTV/CAC/ARPU analysis, or any question of "what should we track and why."
family: core
profile_level: Senior+
---

# Product Metrics and North Star

## Purpose

Design a coherent metric system that connects user value, business outcomes, and decisions the team can act on — from North Star down to diagnostic indicators and financial unit economics.

## Use When

- Building or revising a metric tree, North Star metric, or KPI decomposition for a product or team.
- Choosing primary, secondary, guardrail, and diagnostic metrics for a feature, launch, or experiment.
- Creating or auditing a metric dictionary with formulas, owners, segments, data sources, and SLAs.
- Framing unit economics: LTV, CAC, payback period, ARPU/ARPPU, churn, margin, or monetization layer.
- Evaluating whether growth is volume-driven or economically sustainable.

## Do Not Use When

- The question is about product strategy, roadmap prioritization, or which feature to build → `product-manager`.
- The task requires DWH table design, production data mart construction, or pipeline scheduling → `data-engineer`.
- The task requires enterprise BI semantic layer governance or recurring corporate reporting → `data-analyst` / `data-bi`.
- The question is purely about experiment design → `ab-testing-and-experimentation`.

## Inputs

- Product goal, user problem, or strategic initiative to support.
- User journey, target segment, and moment of realized value.
- Available events, tables, existing dashboards, or current metric definitions.
- Revenue model, cost structure, cohort data, acquisition channels (for unit economics).

## Workflow

1. **State the decision and the product outcome.** What changes in the world if the metric moves? Who acts on it?
2. **Map the value chain.** Identify the user behavior that best reflects realized value; this is the North Star candidate.
3. **Decompose outcome → input → diagnostic metrics.**
   - Outcome metric: what the product is ultimately optimizing (e.g., weekly active paying users).
   - Input metrics: leading behaviors that drive the outcome (e.g., activation rate, feature adoption, upgrade conversion).
   - Diagnostic metrics: signals to explain why an input moved (e.g., onboarding step completion, load time P95).
4. **Add guardrails.** Cover quality, cost, negative effects, reliability, and UX harm. A metric without guardrails is a target waiting to be gamed.
5. **Apply the HEART / North Star sanity checks.** Is the metric controllable by the team? Sensitive enough to detect real change in a reasonable window? Interpretable by non-analysts? Hard to game without actually improving the product?
6. **Layer unit economics when financially relevant.**
   - Define the economic unit: user, account, order, cohort, subscription.
   - Separate gross revenue, net revenue, CAC, incentives, and operational costs.
   - Use cohort-based LTV where possible; avoid single-number long-horizon extrapolation without sensitivity analysis.
   - Segment by channel, product, geography, plan, or customer type when economics differ materially.
7. **Document every metric.** Formula, source table and grain, refresh cadence, owner, exclusion rules, key segments, known caveats.
8. **Review for metric conflicts.** Metrics that can be simultaneously optimized in ways that harm each other signal a design problem.

## Outputs

- Metric tree (outcome → input → diagnostic, with guardrails)
- Metric dictionary (formula, source, grain, cadence, owner, segments, caveats)
- North Star and input metric recommendation
- Primary / secondary / guardrail metric table for a feature or experiment
- Unit economics summary (LTV/CAC/payback, ARPU, segment profitability)
- Financial-impact recommendation with assumptions and sensitivity

## Named Patterns

**Good: metric with clear definition and SLA**
```
north_star: Weekly Active Paying Users (WAPU)
formula: COUNT(DISTINCT user_id) WHERE payment_confirmed_at IS NOT NULL
  AND event_ts >= date_trunc('week', CURRENT_DATE) - INTERVAL '7 days'
grain: user, weekly
owner: product-analyst, Growth team
guardrail: day-7 payment failure rate < 3%
known_caveat: excludes users on free trial; trial counts tracked separately
```

**Bad: ambiguous metric**
```
north_star: "engagement"
formula: undefined
-- no owner, no exclusions, no guardrail, "engagement" means different things to every stakeholder
```

**Good: cohort LTV with explicit assumptions**
```python
# LTV estimate with explicit cohort and assumption disclosure
arpu_m1 = cohort_revenue.query("cohort_month == '2024-01'")["revenue_per_user"].mean()
monthly_retention = 0.72  # observed 12-month average; disclosed as assumption
ltv_12m = arpu_m1 * sum(monthly_retention ** t for t in range(12))
print(f"LTV 12m (disclosed assumptions): {ltv_12m:.2f}")
```

**Bad: LTV without retention curve**
```python
ltv = arpu * 12  # assumes 100% retention — almost never true, never disclosed
```

**Good: metric tree decomposition**
```
Revenue
└── ARPU x MAU
    ├── ARPU = conversion_rate x avg_order_value
    │   ├── guardrail: refund rate < 5%
    │   └── guardrail: support ticket rate stable
    └── MAU = new_users + retained_users - churned_users
        └── guardrail: day-30 retention >= baseline
```

**Bad: flat KPI list without tree**
```
KPIs: revenue, DAU, ARPU, retention, NPS, page views, sessions, support tickets
-- no hierarchy, no guardrails, no owner per metric, 8 metrics with equal weight
```

**Good: segment-aware unit economics**
Separate LTV/CAC by acquisition channel; organic vs paid users differ by 2–3× in LTV.

**Bad: blended CAC / LTV ignoring channel mix**
Blending obscures which channels are profitable; misleads growth investment decisions.

## Boundaries

- Does not own product strategy, roadmap, or prioritization decisions → `product-manager`.
- Does not design DWH, production data marts, or ETL pipelines → `data-engineer`.
- Does not govern enterprise BI semantic layers → `data-analyst` / `data-bi`.
- Does not set pricing strategy autonomously; framing is shared with `product-manager` and finance.

## Sources

**Priority 1 — canonical**
- Amplitude, What is a North Star Metric: https://amplitude.com/blog/2018/03/21/product-north-star-metric
- Google HEART Framework (Rodden, Hutchinson, Fu, 2010): https://static.googleusercontent.com/media/research.google.com/zh-CN//pubs/archive/36299.pdf
- Stripe SaaS Metrics Guide: https://stripe.com/resources/more/saas-metrics

**Priority 2 — practitioner**
- a16z 16 Startup Metrics: https://a16z.com/16-startup-metrics/
- Reforge Growth Model resources: https://www.reforge.com/growth-series
- Croll, A. & Yoskovitz, B., Lean Analytics (2013): https://leananalyticsbook.com/

**Priority 3 — supplementary**
- Lenny Rachitsky, Good metrics vs. vanity metrics (newsletter): https://www.lennysnewsletter.com/
- Andrew Chen, The Power User Curve: https://andrewchen.com/power-user-curve/

## Handoff

```
To: product-manager
Task: Validate metric tree alignment with product strategy and roadmap.
Context: Metric tree designed; owner assignment and priority conflicts need product decision.
Inputs: Draft metric tree, proposed guardrails, known conflicts.
Expected artifact: Confirmed North Star and metric ownership per team.
Acceptance criteria: Each metric has a named owner and is tied to a product goal.
```

```
To: data-engineer
Task: Confirm source tables, grain, freshness, and lineage for metric dictionary.
Context: Metric dictionary drafted; data availability and SLA need validation.
Inputs: Metric dictionary with source, grain, refresh cadence requirements.
Expected artifact: Confirmed sources, latency SLAs, and known gaps.
Acceptance criteria: Every metric has a confirmed source and a stated latency SLA.
```
