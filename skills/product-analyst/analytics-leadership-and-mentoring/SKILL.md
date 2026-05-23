---
name: analytics-leadership-and-mentoring
description: Use when the analytics function needs operating standards, method governance, analytical quality gates, team mentoring, or cross-team alignment on metrics and methodology. Triggers on Lead-level responsibilities: setting the analytical bar, coordinating analysts across teams, resolving priority conflicts, and developing junior and mid-level analysts.
family: lead
profile_level: Lead+
---

# Analytics Leadership and Mentoring

## Purpose

Run product analytics as a reliable, high-quality decision-support function — by setting methodology standards, quality gates, analytical best practices, prioritization discipline, and professional development of the team.

## Use When

- Setting or reviewing analytical methodology standards for the team or guild.
- Triaging and prioritizing the analytics backlog across multiple product teams.
- Conducting analytical reviews: method fit, data quality, conclusion validity, and artifact completeness.
- Onboarding, mentoring, or leveling up junior and mid-level analysts.
- Coordinating metric governance across teams: resolving conflicting definitions, ownerless metrics, or methodology drift.
- Leading the analytics function through ambiguity: shifting product strategy, new data infrastructure, or cross-team dependency conflicts.

## Do Not Use When

- The task is analytical work itself → use the appropriate core or advanced skill.
- The task requires product strategy, roadmap decisions, or feature prioritization → `product-manager`.
- The task requires data engineering leadership or data platform governance → `data-engineer` lead.
- The task requires delivery governance, sprint planning, or resource allocation → `project-manager`.
- The task requires ML platform or data science leadership → `ml-engineer` / `data-scientist` lead.

## Inputs

- Team goals, analytics backlog, stakeholder requests, and delivery constraints.
- Analytical artifacts to review: memos, experiment designs, dashboards, metric dictionaries.
- Team composition: analyst levels, specializations, growth areas.
- Known methodology issues: conflicting definitions, weak evidence standards, missing guardrails.
- Cross-team dependencies: metric ownership conflicts, BI platform changes, data availability risks.

## Workflow

1. **Triage and prioritize the analytics backlog.**
   - Classify each request: exploration, recurring reporting, instrumentation, experiment, or strategic analysis.
   - Score by decision value × urgency × risk of no analysis.
   - Separate high-leverage strategic work from routine operational requests; protect capacity for the former.
   - Assign ownership and expected artifact with explicit acceptance criteria.

2. **Define and maintain methodology standards.**
   Core standards every analyst on the team should apply:
   - Hypothesis pre-registration before experiment launch.
   - Effect size + CI + guardrail check before any experiment "success" claim.
   - Cohort composition check before any retention/conversion trend interpretation.
   - Data quality validation before publishing metrics to stakeholders.
   - Explicit causal vs. observational framing in every analytical output.
   - Limitation and confidence disclosure in every artifact.

3. **Conduct structured analytical reviews.**
   Review checklist:
   ```
   [ ] Is the business question and decision stated?
   [ ] Is the entity grain correct and explicitly stated?
   [ ] Are test users, bots, and known data issues excluded?
   [ ] Is the statistical method appropriate for the question?
   [ ] Is effect size reported with CI, not just p-value?
   [ ] Are guardrail metrics checked?
   [ ] Are limitations and confidence level disclosed?
   [ ] Is the recommendation actionable and addressed to a named owner?
   [ ] Is the artifact reproducible (SQL/notebook restartable, sources named)?
   ```

4. **Mentor analysts with concrete, specific feedback.**
   Feedback principles:
   - Point to the specific claim, not general quality ("This conclusion is causal but the design is observational — suggest rewording to directional signal or proposing an experiment").
   - Distinguish method issues (which require learning investment) from execution issues (which require attention, not training).
   - Give positive feedback on good analytical discipline to reinforce the standard.
   - Use real artifacts as teaching material, with permission.

5. **Resolve metric governance conflicts.**
   When multiple teams measure the same concept differently:
   - Document both definitions with their business context and use case.
   - Propose a canonical definition with explicit segments or views for cases that need divergence.
   - Own the arbitration process; do not let conflicts become invisible.

6. **Coordinate cross-team analytical dependencies.**
   Patterns that require lead involvement: shared metric definitions, joint experiment populations, data availability risks from DWH changes, conflicting experiment launches that contaminate each other.

7. **Escalate when limits are reached.** Escalate to Product Manager when priority conflicts involve product strategy. Escalate to Data Engineer when data quality issues block multiple teams. Escalate to leadership when methodology conflicts cannot be resolved at the team level.

## Outputs

- Analytics backlog triage and prioritization
- Methodology standards document (team or guild level)
- Analytical review feedback (structured, with specific issue flags)
- Metric governance decision (canonical definition, ownership map)
- Mentoring plan (growth areas, practice artifacts, learning path)
- Cross-team handoff coordination plan

## Named Patterns

**Good: structured analytical review with specific flags**
```
Review: Experiment readout — Feature X checkout test
Method: Two-proportion z-test. Appropriate for binary primary metric. OK.
Grain: user_id. OK.
SRM check: Not found in the document. Required before interpreting results. [FLAG: add SRM check]
Effect size: Reported as p=0.03. CI not reported. [FLAG: add 95% CI and absolute effect size]
Guardrails: Not mentioned. [FLAG: add payment_failure_rate and latency_p99 checks]
Limitations: "Results are directional." Vague. [FLAG: specify what makes them directional — underpowered? Observational? Seasonal?]
Recommendation: "The test worked." Not actionable. [FLAG: rewrite as ship/iterate/rollback with risk framing]
```

**Bad: vague review feedback**
"The analysis is not strong enough. Please improve it." — No specific issue, no fix path, no learning.

**Good: hypothesis pre-registration as team standard**
Team norm: every experiment has a pre-analysis plan filed in Confluence before launch, with primary metric, MDE, stopping rule, and decision criteria. Post-hoc "we found this interesting segment" results are flagged as exploratory, not primary.

**Bad: experiment culture without pre-registration**
Any positive segment result becomes the headline. HARKing is endemic. False positive rate rises; team loses calibration over 6 months.

**Good: mentoring with real artifact + specific growth target**
"Here's your experiment readout from last week. You correctly identified the SRM — great. The next skill to develop: reporting CI and practical significance alongside p-value. Here's an example from [colleague]'s readout. Try applying it to the current experiment before the next review."

**Bad: generic growth advice**
"You need to work on your statistical skills." — No specific gap, no concrete next step, no example.

**Good: metric governance — canonical definition with documented divergence**
```
Canonical definition: MAU = unique user_id with ≥ 1 session_start in rolling 28 days, excluding test users.
Exception: Growth team uses MAU = unique user_id with ≥ 1 purchase in 28 days for LTV cohort analysis.
  → Documented in metric dictionary; both labeled; no silent divergence.
```

**Bad: silently different MAU definitions across teams**
Growth team's MAU = 2.1M. Product team's MAU = 3.4M. Leadership meeting confusion. Root cause: undocumented divergence between activity definition and purchase definition.

## Boundaries

- Does not become Product Manager, Tech Lead, or Project Manager in the absence of those roles.
- Does not centralize analytical decisions that belong to individual team owners.
- Does not do the analytical work itself when reviewing; provides structured feedback and routing.
- Does not override the Data Engineer's ownership of data infrastructure governance.
- Does not set ML platform standards → `ml-engineer` / `data-scientist` lead.

## Sources

**Priority 1 — canonical**
- Kohavi, R. et al., Trustworthy Online Controlled Experiments (Cambridge, 2020): https://www.exp-platform.com/Documents/2013-02-CACM.pdf
- dbt Analytics Engineering Best Practices: https://docs.getdbt.com/best-practices
- Google Engineering Practices, Code Review (adapted for analytical review): https://google.github.io/eng-practices/

**Priority 2 — practitioner**
- Reforge, Building an Analytics Organization: https://www.reforge.com/
- Crystal Widjaja, Data and Growth at Gojek: https://www.reforge.com/artifacts/
- Bain, Leading Analytics Teams: https://www.bain.com/insights/topics/advanced-analytics/

**Priority 3 — supplementary**
- Lenny Rachitsky, Building a data-driven product culture: https://www.lennysnewsletter.com/
- Andrew Chen, Data team best practices: https://andrewchen.com/

## Handoff

```
To: product-manager
Task: Resolve priority conflict between analytical requests from two product teams.
Context: Two teams request the same analyst capacity for competing high-priority experiments in the same sprint.
Inputs: Both requests with business context, decision value, and timeline.
Expected artifact: Priority decision with rationale; one request deferred or resourced differently.
Acceptance criteria: Decision made and communicated to both teams.
```

```
To: data-engineer
Task: Investigate data quality issue blocking two product teams' metric reliability.
Context: Metric governance review identified a systematic data quality problem upstream.
Inputs: Metric dictionary entries, affected tables, observed discrepancy, business impact.
Expected artifact: Root cause identified; fix timeline confirmed.
Acceptance criteria: Affected metrics return to expected values; incident documented.
```
