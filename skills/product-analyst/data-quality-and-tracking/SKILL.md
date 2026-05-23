---
name: data-quality-and-tracking
description: Use when product decisions depend on correct event data — tracking plan design, event schema specification, naming conventions, validation rules, instrumentation acceptance criteria, or data-quality diagnosis. Triggers when tracking is missing, broken, ambiguous, or untested, or when a new feature needs its analytics instrumentation specified before development.
family: core
profile_level: Senior+
---

# Data Quality and Tracking

## Purpose

Make product analytics data reliable enough for measurement and decisions by specifying what events to collect, how to name and validate them, and what breaks the data before it reaches analysis.

## Use When

- Creating or reviewing tracking plans and event specifications for a new feature, flow, or experiment.
- Defining event parameters, identity resolution rules, and platform-specific instrumentation requirements.
- Diagnosing suspicious metric behavior: missing data, duplicates, inflated counts, broken funnels, or inconsistent definitions across platforms.
- Setting analytics acceptance criteria: what must pass before a feature ships.
- Establishing event naming conventions and data-quality standards for a product team.

## Do Not Use When

- The task requires implementing tracking code in the codebase → engineering (frontend/backend).
- The task requires DWH pipeline design, data contracts, or table governance → `data-engineer`.
- The task requires full regression testing of the product → `qa-engineer`.
- The task requires data platform or CDP configuration → `data-engineer` / platform team.

## Inputs

- User flows and feature specifications (wireframes, PRDs, or user-story descriptions).
- Existing tracking plan or event catalog, if any.
- Current data quality issues, known gaps, or instrumentation bugs.
- Target analytics platform (Amplitude, Segment, Snowplow, Mixpanel, custom) and identity model.
- Development timeline and platform scope (web, iOS, Android, backend server-side).

## Workflow

1. **Map the analytical decision to required events.** Start from the metric and the experiment/analysis question, not from a list of UI interactions. Each event should answer a specific question.
2. **Define each event in full.**
   - `event_name`: verb_object in snake_case; context-specific, not generic (`checkout_started`, not `button_clicked`).
   - `trigger_moment`: exact user action or system state that fires the event.
   - `actor`: user, system, or background process.
   - `properties`: required and optional; type, allowed values, null policy, PII flag.
   - `identity`: user_id (authenticated), anonymous_id (pre-auth), device_id (mobile); stitching rule.
   - `platform_scope`: web / iOS / Android / server-side; emit location.
   - `example payload`: concrete JSON example with realistic values.
3. **Apply naming conventions.**
   - Verb-object: `purchase_completed`, `onboarding_step_viewed`, `experiment_assigned`.
   - Consistent tense: past-tense events for completed actions, present for state transitions.
   - No platform prefixes in the event name unless the event is genuinely platform-specific.
4. **Define validation rules.**
   - Required properties: list; reject or flag events missing required fields.
   - Allowed values: enums for categorical properties.
   - Deduplication key: `(user_id, event_name, event_ts)` or `event_uuid`.
   - Time-zone rule: all timestamps in UTC.
   - Test-user exclusion: tag and exclude by property, not by post-hoc filtering.
5. **Write analytics acceptance criteria.**
   Conditions that must pass before the feature ships (these are QA scenarios for tracking, not product QA):
   - Event fires on the correct trigger for each defined scenario.
   - All required properties are present and correct.
   - No duplicate events within the deduplication window.
   - Test-user tag fires correctly; events excluded from production analytics.
   - Cross-platform property values are consistent where the same concept is tracked on multiple platforms.
6. **Diagnose data-quality issues.**
   Common root causes: event not firing (missed trigger), property missing (wrong scope), duplicates (double-emit on retry or re-render), identity mismatch (pre/post-auth stitching gap), timezone mismatch.

   ```python
   import pandas as pd

   def diagnose_event_quality(df: pd.DataFrame, event_name: str,
                               required_props: list[str],
                               dedup_keys: list[str]) -> dict:
       """
       Basic data quality check for a single event type.
       df: events DataFrame with columns matching the event schema.
       """
       subset = df[df["event_name"] == event_name].copy()
       total = len(subset)
       if total == 0:
           return {"error": f"No events found for {event_name}"}

       # Missing required properties
       missing = {prop: int(subset[prop].isna().sum())
                  for prop in required_props if prop in subset.columns}
       missing_cols = [p for p in required_props if p not in subset.columns]

       # Duplicate events
       dup_count = int(subset.duplicated(subset=dedup_keys).sum())

       # Summary
       return {
           "event_name": event_name,
           "total_events": total,
           "missing_required_props": missing,
           "missing_columns_in_schema": missing_cols,
           "duplicate_events": dup_count,
           "duplicate_rate_pct": round(dup_count / total * 100, 2),
       }

   # Example usage
   issues = diagnose_event_quality(
       df=events_df,
       event_name="checkout_started",
       required_props=["user_id", "cart_value_usd", "item_count", "platform"],
       dedup_keys=["user_id", "event_name", "event_ts"],
   )
   print(issues)
   ```

7. **Escalate pipeline, lineage, freshness, or DWH problems.** If the root cause is upstream (late-arriving data, schema change in the source, broken ETL), document and route to Data Engineering; do not attempt to fix it in analysis.

## Outputs

- Tracking plan (event catalog with full specifications)
- Event schema (properties, types, validation rules, example payload)
- Analytics acceptance criteria (QA scenarios for instrumentation)
- Data-quality issue brief (root cause, impact, owners, required fix)
- Naming convention guide for the product team

## Named Patterns

**Good: event specification with all required fields**
```yaml
event_name: checkout_started
trigger_moment: User taps "Proceed to checkout" button; fires once per checkout session initiation.
actor: user
platform: iOS, Android, web
properties:
  user_id:         {type: string, required: true,  pii: false, note: "null if anonymous"}
  anonymous_id:    {type: string, required: true,  pii: false}
  cart_value_usd:  {type: number, required: true,  pii: false, validation: "> 0"}
  item_count:      {type: integer, required: true, pii: false, validation: ">= 1"}
  platform:        {type: string, required: true,  allowed: [ios, android, web]}
  experiment_ids:  {type: array,  required: false, note: "active experiment assignments"}
  is_test_user:    {type: boolean, required: true, note: "must be true for QA users"}
identity: user_id (if auth) | anonymous_id (pre-auth); stitched at login
dedup_key: [user_id, event_name, event_ts] within 60s window
example_payload: |
  {"event_name": "checkout_started", "user_id": "u_123", "anonymous_id": "a_456",
   "cart_value_usd": 49.99, "item_count": 2, "platform": "ios",
   "experiment_ids": ["exp_checkout_v2"], "is_test_user": false}
```

**Bad: vague event entry**
```
event: checkout
properties: user, cart, platform
-- No trigger moment, no property types, no validation, no identity model, no example.
```

**Good: test-user exclusion built into the schema**
Property `is_test_user: true` set by QA; all downstream queries exclude with `WHERE NOT is_test_user`. Contamination-free from day 1.

**Bad: post-hoc test-user filtering**
"We'll exclude test users later in the query." Leads to inconsistent exclusions across analyses; some queries forget; data is contaminated in dashboards.

**Good: naming that encodes context**
`onboarding_step_viewed` (step_name, step_number) vs. `screen_viewed` (screen_name).
Context-specific name makes event catalog self-documenting; screen_viewed requires documentation lookup.

**Bad: generic names**
`click`, `view`, `action` — require external documentation to understand; break when the same name is reused for semantically different events.

**Good: acceptance criteria before ship**
```
AC-1: checkout_started fires exactly once per checkout initiation (no double-emit on re-render).
AC-2: cart_value_usd is present and > 0 in 100% of events.
AC-3: is_test_user = true for all QA device events; false for real user events.
AC-4: event fires on iOS, Android, and web (three separate QA test runs).
```

**Bad: "we'll check the data after launch"**
Broken tracking discovered post-launch; experiment metrics are invalid; rollback or re-run required.

## Boundaries

- Does not implement tracking code in the frontend or backend → engineering.
- Does not own DWH table design, data contracts, or ETL scheduling → `data-engineer`.
- Does not perform full product regression testing → `qa-engineer`.
- Does not own the analytics platform (CDP, event router) configuration → platform / data-engineer.

## Sources

**Priority 1 — canonical**
- Twilio Segment Tracking Plan Guide: https://segment.com/docs/protocols/tracking-plan/
- Amplitude Data Planning Guide: https://amplitude.com/docs/data/sources/instrument-track-unique-users
- Snowplow Event Specifications: https://docs.snowplow.io/docs/fundamentals/schemas/

**Priority 2 — practitioner**
- Mixpanel Data Modeling Guide: https://docs.mixpanel.com/docs/tracking-methods/choosing-the-right-method
- dbt Data Testing Best Practices: https://docs.getdbt.com/best-practices/writing-custom-generic-tests
- Avo Analytics Governance: https://www.avo.app/blog/

**Priority 3 — supplementary**
- GoodData, Event Data Quality: https://www.gooddata.com/blog/event-tracking-best-practices/
- Lenny Rachitsky newsletter (tracking at scale): https://www.lennysnewsletter.com/

## Handoff

```
To: engineering (frontend/backend)
Task: Implement tracking events per the attached event specifications and analytics acceptance criteria.
Context: Tracking plan signed off; implementation needed before feature launch.
Inputs: Event specification doc with trigger moment, properties, types, validation rules, example payloads.
Expected artifact: Implemented events passing all analytics acceptance criteria.
Acceptance criteria: AC list in the tracking plan — all items pass in staging and production QA.
```

```
To: data-engineer
Task: Investigate upstream data quality issue: [specific issue description].
Context: Diagnostic shows [missing/duplicate/stale] data; root cause suspected to be in the pipeline.
Inputs: Data-quality issue brief with affected events, impact scope, and timeline.
Expected artifact: Root cause identified, fix implemented or timeline confirmed.
Acceptance criteria: Affected metrics return to baseline within agreed SLA.
```
