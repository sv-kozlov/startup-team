---
name: sql-and-data-analysis
description: Use when a product question requires reproducible SQL — funnels, cohorts, retention, window functions, segmentation, or experiment reads — or when a stakeholder needs a decision-oriented dashboard brief. Triggers on any task of turning raw event or transaction data into an auditable analytical output.
family: core
profile_level: Senior+
---

# SQL and Data Analysis

## Purpose

Turn product questions into auditable SQL logic and decision-ready outputs — from ad hoc queries to dashboard specifications — without creating production pipelines or certifying enterprise reporting.

## Use When

- Writing or reviewing SQL for funnels, cohorts, retention, conversion, churn, monetization, or experiment reads.
- Validating metric logic: joins, filters, time windows, grain, deduplication, and null handling.
- Translating an ambiguous product question into queryable entities and measures.
- Specifying a dashboard brief: audience, decision, metric definitions, chart type, refresh cadence, and owner.
- Reviewing an existing dashboard for decision fit, metric quality, and stale-data risk.

## Do Not Use When

- The task requires production pipeline creation, data contracts, or DWH model design → `data-engineer`.
- The task requires certifying enterprise-level governed reporting or a shared semantic layer → `data-analyst` / `data-bi`.
- The task requires advanced statistical modeling or ML feature engineering → `python-and-tooling-for-analytics`.

## Inputs

- Business question and expected decision.
- Schema description, table names, event definitions, metric definitions, and time-zone rules.
- Known caveats: bot traffic, test users, delayed events, missing values, duplicates, platform splits.
- For dashboard tasks: audience, recurring decision, action workflow, alert thresholds.

## Workflow

1. **Clarify entity grain.** Is the unit a user, account, session, order, event, or experiment unit? Mixing grains is the most common source of wrong answers.
2. **Define inclusion/exclusion rules.** Time windows, test-user filters, bot exclusions, platform scope, event deduplication logic.
3. **Build incrementally with CTEs.** Each CTE is a named reasoning step: easier to audit, debug, and explain. Avoid nested subqueries > 2 levels deep.
4. **Use window functions for ordering, cohorts, first/last events, and period comparisons.**
5. **Validate at each step.** Compare intermediate counts to known totals, dashboards, or historical baselines before proceeding.
6. **Apply EXPLAIN for expensive queries.** Confirm index use; identify seq scans on large tables.
7. **For dashboard tasks:** identify the decision, separate monitoring vs. diagnostic vs. executive views, specify chart type to match the comparison task (trend, funnel, distribution, or composition), and name the data owner, refresh cadence, and alert threshold.
8. **Return SQL plus caveats.** State assumptions, known gaps, and checks required before results are used in a decision.

## Outputs

- SQL or pseudo-SQL with named CTEs and inline comments
- Metric validation checklist
- Intermediate-count audit plan
- Result interpretation notes
- Dashboard brief (audience, decision, metrics, charts, cadence, owner, alert thresholds)

## Named Patterns

**Good: CTE-based cohort retention query**
```sql
-- Cohort retention: % of users from acquisition week who return N weeks later
WITH cohort_base AS (
    -- Step 1: identify each user's first active week
    SELECT
        user_id,
        DATE_TRUNC('week', MIN(event_ts))::date AS cohort_week
    FROM user_events
    WHERE event_name = 'session_start'
      AND event_ts >= '2024-01-01'
      AND NOT is_test_user           -- explicit exclusion
    GROUP BY user_id
),
weekly_activity AS (
    -- Step 2: all active weeks per user (deduplicated)
    SELECT DISTINCT
        user_id,
        DATE_TRUNC('week', event_ts)::date AS active_week
    FROM user_events
    WHERE event_name = 'session_start'
),
cohort_activity AS (
    -- Step 3: join cohort base with activity, compute week offset
    SELECT
        cb.cohort_week,
        wa.active_week,
        (wa.active_week - cb.cohort_week) / 7 AS weeks_since_cohort,
        COUNT(DISTINCT cb.user_id) AS retained_users
    FROM cohort_base cb
    JOIN weekly_activity wa USING (user_id)
    GROUP BY 1, 2, 3
),
cohort_sizes AS (
    SELECT cohort_week, COUNT(*) AS cohort_size
    FROM cohort_base
    GROUP BY cohort_week
)
SELECT
    ca.cohort_week,
    ca.weeks_since_cohort,
    ca.retained_users,
    cs.cohort_size,
    ROUND(ca.retained_users * 100.0 / cs.cohort_size, 1) AS retention_pct
FROM cohort_activity ca
JOIN cohort_sizes cs USING (cohort_week)
WHERE ca.weeks_since_cohort BETWEEN 0 AND 12
ORDER BY ca.cohort_week, ca.weeks_since_cohort;
```

**Bad: spaghetti subquery without grain control**
```sql
-- Antipattern: unclear grain, no test-user exclusion, nested without comments
SELECT user_id, count(*) FROM (
  SELECT * FROM events WHERE ts > '2024-01-01'
) t GROUP BY 1
-- What is being counted? What exclusions apply? What does the output mean?
```

**Good: funnel with explicit ordering**
```sql
-- Funnel: registration → first purchase within 7 days
WITH registration AS (
    SELECT user_id, MIN(event_ts) AS reg_ts
    FROM user_events WHERE event_name = 'registration_complete'
    GROUP BY user_id
),
purchase AS (
    SELECT user_id, MIN(event_ts) AS purchase_ts
    FROM user_events WHERE event_name = 'purchase_confirmed'
    GROUP BY user_id
)
SELECT
    COUNT(DISTINCT r.user_id)                                       AS step_1_registered,
    COUNT(DISTINCT p.user_id)                                       AS step_2_purchased_7d,
    ROUND(COUNT(DISTINCT p.user_id) * 100.0 /
          NULLIF(COUNT(DISTINCT r.user_id), 0), 1)                 AS conversion_pct
FROM registration r
LEFT JOIN purchase p
    ON r.user_id = p.user_id
    AND p.purchase_ts BETWEEN r.reg_ts AND r.reg_ts + INTERVAL '7 days';
```

**Bad: implicit grain leads to double-counting**
```sql
-- Joining events without deduplication inflates user counts
SELECT e1.user_id, e2.event_name
FROM events e1 JOIN events e2 ON e1.user_id = e2.user_id
-- Cartesian explosion; no grain control
```

**Good: EXPLAIN before running on large tables**
```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT user_id, SUM(revenue) FROM orders
WHERE created_at >= '2024-01-01'
GROUP BY user_id;
-- Verify: index scan on created_at; no full seq scan on 100M-row table
```

**Good: dashboard brief tied to a decision**
```
Dashboard: Experiment Monitoring — Feature X
Audience: Product Manager + Growth Lead (checked daily during experiment)
Decision: Ship / iterate / rollback on day 14.
Primary metric: checkout_conversion_rate (treatment vs. control, 95% CI)
Guardrail: p99 checkout_latency_ms (alert if > 800ms)
Chart: time-series with confidence bands, separate control/treatment lines
Refresh: hourly; SRM check badge on header
Owner: [product-analyst-name]
```

**Bad: dashboard without decision or owner**
```
Dashboard: "Metrics overview"
Charts: 47 panels, no filter defaults, no documented metric formulas, no named owner
-- No one knows which number to act on; staleness undetected
```

## Boundaries

- Does not create production pipelines, data contracts, or DWH models → `data-engineer`.
- Does not certify enterprise-level governed reporting → `data-analyst` / `data-bi`.
- Does not own BI platform implementation (Tableau, Looker, Superset deployment) → `data-bi`.
- Dashboard briefs are requirements; BI platform builds the dashboard.

## Sources

**Priority 1 — canonical**
- PostgreSQL Window Functions Tutorial: https://www.postgresql.org/docs/current/tutorial-window.html
- PostgreSQL EXPLAIN Documentation: https://www.postgresql.org/docs/current/using-explain.html
- Amplitude SQL for Product Analytics: https://amplitude.com/product-analytics

**Priority 2 — practitioner**
- Mode SQL Tutorial (funnels, cohorts, window functions): https://mode.com/sql-tutorial/
- Tableau Dashboard Best Practices: https://help.tableau.com/current/pro/desktop/en-us/dashboards_best_practices.htm
- Power BI Dashboard Design Tips: https://learn.microsoft.com/en-us/power-bi/create-reports/service-dashboards-design-tips

**Priority 3 — supplementary**
- Caio Doin, SQL patterns for product analytics: https://medium.com/
- dbt Best Practices (model naming, grain documentation): https://docs.getdbt.com/best-practices

## Handoff

```
To: data-engineer
Task: Productionize the cohort retention query as a scheduled dbt model or pipeline job.
Context: Ad hoc query validated; now needed as a recurring data mart for the dashboard.
Inputs: Validated SQL, grain definition, SLA requirement, target refresh cadence.
Expected artifact: Production model with tests and documented lineage.
Acceptance criteria: Model passes dbt tests; latency meets SLA; query plan reviewed.
```

```
To: data-bi
Task: Build the dashboard in [BI platform] from the attached brief.
Context: Dashboard brief specifies audience, decision, metrics, charts, cadence, and owner.
Inputs: Dashboard brief with metric formulas, source table refs, filter defaults, alert thresholds.
Expected artifact: Published dashboard matching brief specifications.
Acceptance criteria: All metrics match formula in brief; alert thresholds configured; owner named.
```
