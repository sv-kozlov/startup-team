---
name: behavior-and-cohort-analytics
description: Use when the team needs to understand what users actually do — funnel drop-offs, retention curves, cohort comparisons, activation patterns, churn diagnosis, or behavioral segmentation. Triggers on any question of "where are we losing users and why does their behavior differ across groups."
family: advanced
profile_level: Senior+
---

# Behavior and Cohort Analytics

## Purpose

Diagnose user behavior patterns — funnels, retention, cohorts, activation, churn, and segmentation — and connect them to product decisions, without claiming causality from observational data alone.

## Use When

- Analyzing funnel conversion and drop-off steps at user, session, or event level.
- Building cohort retention curves (D1/D7/D30/D90) and comparing cohorts across time, acquisition channel, or feature exposure.
- Diagnosing activation: what behaviors predict retention; which users reach the "aha moment."
- Identifying churn patterns: when users leave, what they did before leaving, which segments churn differently.
- Preparing quantitative behavioral input for product discovery or UX research.
- Segmenting users by behavioral dimension (frequency, depth, recency, monetization, platform, intent).

## Do Not Use When

- Causal claims about behavior are needed → `ab-testing-and-experimentation`.
- The question is about metric design or business outcome framing → `product-metrics-and-northstar`.
- The research question requires qualitative user motivation → `ui-ux-designer` / `ux-researcher`.
- The data question requires pipeline or DWH work → `data-engineer`.

## Inputs

- User journey definition: which events constitute each step.
- Segments of interest: acquisition channel, cohort, platform, plan, geography, user intent.
- Time windows: cohort definition period, observation window, analysis dates.
- Known tracking caveats: test users, delayed events, missing platforms, identity stitching gaps.

## Workflow

1. **Choose the correct analysis frame.**
   - Funnel: ordered sequence completion; use when the user must complete steps in a defined order.
   - Cohort retention: % of a group returning at interval N; use when repeating behavior matters.
   - RFM / frequency segmentation: recency, frequency, monetization buckets; use for engagement quality.
   - Path analysis: free-form sequence discovery; use when the journey is not predefined.
   - Churn diagnosis: identify the last-active date and pre-churn behavior pattern.

2. **Define each behavioral step precisely.** Ambiguous step definitions (e.g., "viewed product" vs. "viewed product detail page for ≥ 3 seconds") produce different funnels — specify exactly.

3. **Build cohort retention with explicit SQL.**

   ```sql
   -- D1/D7/D30 retention: % of acquisition cohort active on day N
   WITH cohort AS (
       SELECT
           user_id,
           DATE(MIN(event_ts)) AS cohort_date
       FROM user_events
       WHERE event_name = 'registration_complete'
         AND NOT is_test_user
       GROUP BY user_id
   ),
   daily_activity AS (
       SELECT DISTINCT
           user_id,
           DATE(event_ts) AS active_date
       FROM user_events
       WHERE event_name = 'session_start'
   ),
   cohort_activity AS (
       SELECT
           c.cohort_date,
           (da.active_date - c.cohort_date) AS day_offset,
           COUNT(DISTINCT c.user_id) AS retained_users
       FROM cohort c
       JOIN daily_activity da USING (user_id)
       WHERE (da.active_date - c.cohort_date) IN (0, 1, 7, 14, 30)
       GROUP BY 1, 2
   ),
   sizes AS (
       SELECT cohort_date, COUNT(*) AS cohort_size
       FROM cohort GROUP BY cohort_date
   )
   SELECT
       ca.cohort_date,
       ca.day_offset,
       ca.retained_users,
       s.cohort_size,
       ROUND(ca.retained_users * 100.0 / s.cohort_size, 1) AS retention_pct
   FROM cohort_activity ca
   JOIN sizes s USING (cohort_date)
   ORDER BY ca.cohort_date, ca.day_offset;
   ```

4. **Separate acquisition mix effects from product behavior effects.** If cohort composition changes (different channel mix, different geography), retention change may reflect who entered the funnel, not how the product changed.

5. **Use window functions for first/last event, sequences, and inter-event timing.**

   ```sql
   -- Time from registration to first purchase (activation lag analysis)
   WITH user_journey AS (
       SELECT
           user_id,
           MIN(CASE WHEN event_name = 'registration_complete' THEN event_ts END)
               AS registration_ts,
           MIN(CASE WHEN event_name = 'purchase_confirmed' THEN event_ts END)
               AS first_purchase_ts
       FROM user_events
       WHERE NOT is_test_user
       GROUP BY user_id
   )
   SELECT
       CASE
           WHEN first_purchase_ts IS NULL THEN 'never_purchased'
           WHEN first_purchase_ts - registration_ts <= INTERVAL '1 day' THEN 'day_1'
           WHEN first_purchase_ts - registration_ts <= INTERVAL '7 days' THEN 'day_2_7'
           ELSE 'day_8_plus'
       END AS activation_bucket,
       COUNT(*) AS users
   FROM user_journey
   GROUP BY 1 ORDER BY 2 DESC;
   ```

6. **Compare meaningful segments, not arbitrary slices.** Segment by a dimension with a hypothesis attached: "organic vs. paid users behave differently because of intent." Avoid segmenting into 15 dimensions without a prior question.

7. **Look for timing, recurrence, depth, and sequence patterns.** When do users first complete the key action? How often do they return? How many features do they use? What do churners do in their last session?

8. **State what the data explains and what needs qualitative research.** Quantitative data shows the pattern; qualitative data explains the motivation.

## Outputs

- Funnel or cohort analysis brief (step-by-step conversion, drop-off, retention curve)
- Behavioral segment summary (RFM, feature-usage depth, intent clusters)
- Retention / churn diagnostic (when users leave, pre-churn behavior, segment differences)
- Behavioral questions for UX research (why users drop off or churn at the identified step)

## Named Patterns

**Good: retention curve with cohort comparison**
Plot D1/D7/D30/D90 curves for cohorts entering before and after a product change. If post-change cohorts show materially different D30 retention (+5pp or more), the change is a candidate for causal investigation via experiment.

**Bad: single-cohort snapshot without comparison**
"D7 retention is 28%." Without a baseline cohort comparison or time trend, this number is unactionable. Is 28% improving, stable, or deteriorating?

**Good: acquisition-mix control in retention comparison**
"Cohort A (April) shows higher D30 retention than Cohort B (March). However, Cohort A has 30% higher share of organic users; adjusting for channel mix, the retention difference narrows to +2pp — within noise."

**Bad: cohort comparison without composition check**
"Our retention improved after the campaign launch." — The campaign brought a different user segment; the product did not change. Without composition check, the improvement is attributed to the wrong cause.

**Good: churn diagnosis with pre-churn signal**
Last-7-day behavior before churn: 60% of churned users had 0 sessions in their last 7 days of activity (gradual fade, not abrupt). Key predictive signal: users who use feature X at least twice in first 7 days have 2× lower D30 churn.

**Bad: churn defined as "inactivity for 30 days" applied retroactively**
Definition applied retroactively means some "churned" users actually came back; churn rate is overstated. Define churn window prospectively or use a survival-analysis approach.

**Good: funnel with platform split**
Checkout funnel split by iOS, Android, web shows 15pp lower iOS conversion at payment step. Directs investigation to iOS-specific payment flow before blending numbers.

**Bad: blended funnel hiding platform split**
Blended checkout conversion appears stable; deterioration on iOS masked by growth on web. Issue goes undetected for 3 weeks.

## Boundaries

- Does not claim causality from cohort or funnel observations without an experiment → `ab-testing-and-experimentation`.
- Does not replace qualitative UX research for explaining user motivation → `ui-ux-designer` / `ux-researcher`.
- Does not design production pipelines for behavioral data → `data-engineer`.
- Does not own product feature decisions based on behavioral diagnosis alone.

## Sources

**Priority 1 — canonical**
- Amplitude Funnel Analysis: https://amplitude.com/docs/analytics/charts/funnel-analysis/funnel-analysis-build
- Amplitude Behavioral Cohorts: https://amplitude.com/docs/analytics/behavioral-cohorts
- PostgreSQL Window Functions: https://www.postgresql.org/docs/current/tutorial-window.html

**Priority 2 — practitioner**
- Google Analytics 4, Funnel Exploration: https://support.google.com/analytics/answer/9327974
- Mixpanel Retention Analysis: https://docs.mixpanel.com/docs/reports/retention
- Reforge Retention deep-dives: https://www.reforge.com/blog/retention-engagement-addiction

**Priority 3 — supplementary**
- Andrew Chen, The Power User Curve: https://andrewchen.com/power-user-curve/
- Lenny Rachitsky, Retention benchmarks by category: https://www.lennysnewsletter.com/

## Handoff

```
To: ux-researcher
Task: Investigate qualitative reasons behind [specific behavioral drop-off or churn pattern].
Context: Quantitative data shows [X% drop at step Y / churn spike in segment Z]; motivation is unknown.
Inputs: Behavioral analysis summary, identified step, affected segment description, hypothesized reasons.
Expected artifact: Research synthesis addressing the hypothesized motivational factors.
Acceptance criteria: Each hypothesis is supported or refuted with evidence from ≥ 5 user sessions.
```

```
To: ab-testing-and-experimentation
Task: Design a controlled experiment to validate the causal hypothesis derived from behavioral diagnosis.
Context: Behavioral analysis identified [pattern]; causal validation needed before product investment.
Inputs: Behavioral finding, proposed intervention, primary metric, eligible population, baseline.
Expected artifact: Experiment design with sample size, duration, stopping rule.
Acceptance criteria: Pre-analysis plan registered before experiment launch.
```
