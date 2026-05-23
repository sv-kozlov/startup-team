---
name: shared-impact-analysis
description: Use when a change — feature, rule modification, integration update, process redesign, or release — must be assessed for its consequences across business processes, stakeholders, systems, APIs, data models, integrations, tests, documentation, operations, and delivery; each role scopes its own impact domain and routes the rest as handoffs.
---

# Shared Impact Analysis

## Purpose

Expose the full set of consequences that a proposed change produces across business, system, data, quality, operations, and delivery boundaries — before implementation begins. Impact analysis prevents late discovery of missing dependencies, broken assumptions, and upstream-downstream synchronization problems. It does not decide whether to proceed; it provides the evidence for the people who do.

## Use When

- A change request has arrived and the team does not yet know which processes, systems, integrations, tests, or stakeholders will be affected.
- A requirement change or rule modification arrives mid-sprint and the team must assess whether it fits the current scope or must be re-planned.
- A release or deployment is being prepared and the team must verify that all downstream consumers, dependent systems, and operational procedures are covered.
- A business process change will affect training materials, support procedures, user communications, or partner workflows that other teams own.
- A system or API change will affect existing consumers, contracts, data models, or test suites.
- An analytics or metric change affects existing dashboards, reports, or downstream data pipelines.
- A decision about scope, architecture, or technical approach must be informed by the full blast radius before it is finalized.

## Do Not Use When

- The task is deciding product priority or making architectural choices → Product Manager decides product priority; System Architect and Tech Lead make architecture decisions. Impact analysis informs those decisions; it does not make them.
- The task is root-cause analysis of a production incident → incident response and post-mortem are owned by DevOps/SRE; impact analysis is an input to that process, not its substitute.
- The task is writing the implementation plan or delivery schedule → Project Manager owns delivery planning; impact analysis identifies scope, not schedule.
- The change is fully contained within a single component and no external boundary is crossed → the owning engineering role handles the local assessment; escalate only if boundaries are actually crossed.

## Inputs

- Change description: what is proposed, what problem it solves, and what the intended outcome is.
- Affected processes, systems, integrations, and user groups known at the time of the request.
- Existing requirements, specifications, data models, API contracts, process diagrams, and test suites that may be affected.
- Release context: target release, delivery cadence, and known constraints.
- Ownership map: which role owns which affected artifact.
- Known dependencies and risks already recorded in the project.

## Workflow

1. **Decompose the change into a blast radius map.** List every artifact category that could be affected: business processes, stakeholder groups, business rules, requirements, functional specification, API contracts, data models, integrations, UI states, test suites, documentation, operational procedures, training materials, communications. Use a checklist to avoid silent omissions — absence of a category should be an explicit "not affected" decision, not a gap.

2. **Classify impact by domain and role ownership.** For each affected category, assign: the impact type (direct change required, review needed, monitoring required, or no change), the owning role, and the severity (blocker, significant, minor). Do not assess impact for domains you do not own — record them as scope for a handoff.

3. **Assess backward compatibility and transition risk.** For system and data changes: does the change break existing consumers? What is the migration path? Is the change reversible? For business and process changes: what is the transition state — can the old and new processes coexist during rollout, or is a hard cutover required?

4. **Identify dependencies and sequencing constraints.** Some impacts block others: if an API contract must change before frontend can adapt, that is a sequencing constraint. If a business rule change must be validated before the system specification can be updated, that is a dependency. Record these explicitly — not as assumptions but as tracked dependencies with owners and deadlines.

5. **Capture risks, assumptions, and migration considerations.** For each unresolved impact: what is the worst-case consequence if it is not addressed? What assumption is being made? Who owns the decision to accept the risk? Record these in the risk and dependency log — do not leave them as silent context.

6. **Define handoffs with expected artifacts.** For each impact outside the current role's ownership, create a handoff block: receiving role, impact description, expected artifact, acceptance criteria, and deadline. Do not attempt to assess or resolve impacts in domains you do not own.

## Outputs

- Blast radius map: table of impact categories, impact type, severity, and owner role.
- Risk and dependency log: each item with type (risk, dependency, assumption, sequencing constraint), owner, worst case, and resolution path.
- Migration and transition notes: backward compatibility assessment, rollout options, transition state description.
- Handoff tasks: one per affected domain outside the current role's ownership, with expected artifact and acceptance criteria.
- Impact analysis brief: compact summary of the change, affected scope, key risks, and recommended next steps — suitable for a planning or steering forum.

## Role Modes

### Business Analyst

Owns the business-side impact assessment: which business processes are affected, which stakeholders will be impacted, which business rules must be updated, which training and support materials must change, and what the business readiness implications are. Produces the business-side section of the impact brief. Does not assess API contracts, data models, integration changes, or test suites — those are handoffs to System Analyst. Does not assess delivery scheduling — that is a handoff to Project Manager.

## Boundaries

- Does not own product priority decisions or scope commitment → Product Manager decides whether the change is worth pursuing; Project Manager decides how it fits the delivery plan. Impact analysis provides evidence for those decisions.
- Does not own architecture decisions or engineering estimates → System Architect and Tech Lead own those; impact analysis identifies affected architecture components and routes the assessment as a handoff.
- Does not own the QA release decision or regression scope → QA Engineer owns test impact assessment; the blast radius map identifies affected areas, not the test plan.
- Does not turn every possible impact into a mandatory task → classify impact severity explicitly; minor items with low risk may be accepted as-is and recorded, not addressed.
- Does not hide unresolved impacts as assumptions → every unresolved impact must be classified, owned, and either resolved or explicitly accepted with a risk record.

## Named Patterns

### Good — Blast radius checklist with explicit "not affected"
```
Change: Add "gift card top-up" as an excluded order type for discount rules.
| Category           | Impact       | Severity | Owner         | Notes                             |
|--------------------|---|---|---|---|
| Business rules     | Direct change | Blocker  | BA            | BR-041 exception clause added     |
| Functional spec    | Review needed | Major    | SA            | Discount service behavior update  |
| API contract       | Additive      | Minor    | SA            | New order_type enum value         |
| Data model         | Not affected  | —        | —             | order_type already in schema      |
| Test suite         | Review needed | Major    | QA            | New test case for excluded type   |
| Documentation      | Update needed | Minor    | BA            | Business rule catalog update      |
| Training materials | Not affected  | —        | —             | No user-facing change             |
```
Every category explicitly assessed. "Not affected" is a decision, not a gap. Owners named per row.

### Bad — Narrative impact assessment
"This change might affect the discount calculation, and QA should probably add some tests. There might also be some documentation updates needed." No categories, no severities, no owners. The team discovers missing impacts at UAT.

### Good — Backward compatibility assessment
```
API change: Add optional field order_type (string, nullable) to POST /v1/orders.
Backward compatibility: SAFE — additive change. Existing consumers ignore unknown fields.
Consumer impact: 3 consumers identified (frontend, mobile app, partner API).
  - Frontend: no change required; field is not displayed in current UI.
  - Mobile app: update recommended to display order type; not blocking for release.
  - Partner API: no change required; field is not used in partner workflow.
Migration plan: None required. Field defaults to null for existing consumers.
```
Each consumer assessed individually. Compatibility decision is explicit with rationale.

### Bad — Undiscovered consumer impact
API change deployed. Frontend team discovers the change broke their null-handling in the order confirmation flow. Impact analysis did not enumerate consumers; the consumer list was assumed to be known.

### Good — Dependency with sequencing constraint
```
Dependency: QA cannot write test cases for gift card exclusion until System Analyst publishes
the updated functional specification (SYS-114 revision).
Owner: System Analyst. Expected artifact: SYS-114 v2 with gift card exclusion behavior.
Deadline: 2025-06-03 (two business days before QA sprint starts).
Sequencing risk: If SYS-114 v2 is late, QA sprint start is blocked.
```
Dependency is named, owned, and has an explicit deadline and risk description.

### Bad — Assumed dependency resolution
QA starts writing test cases based on the v1 spec. System Analyst publishes SYS-114 v2 with a different error-handling approach three days later. QA rewrites test cases. Impact analysis did not capture the dependency.

### Good — Risk accepted with record
```
Risk: Mobile app update (add order_type display) is deferred to the next release.
Impact: Mobile users will not see order type in order confirmation for one release cycle.
Accepted by: Product Manager (2025-05-28). Rationale: low-priority UX improvement;
does not affect core business rule enforcement.
Monitoring: No increase in support tickets about order type expected.
```
Risk is named, accepted by an accountable owner, and has a monitoring plan.

### Bad — Silent risk
Mobile app update silently omitted from impact log. Product Manager is surprised in post-release review to find that mobile users see no order type information. No record of whether this was a decision or an oversight.

### Good — Explicit "not affected" entries in the blast radius map
Each category in the impact checklist has an explicit pass/fail result, including categories determined to be not affected. Categories with "not affected" include a one-line rationale.
Example: "Training materials — not affected. Change is system-only; no user-facing workflow change."
The "not affected" entry prevents a reviewer from questioning whether the category was forgotten.

### Bad — Silent omission of impact categories
The impact log covers only the categories the analyst thought of. Stakeholders reviewing the log cannot tell whether missing categories are "not affected" or simply overlooked. Disputes arise at UAT when an omitted category turns out to be affected.

## Sources

### Priority 1 — Method canon

- ISO/IEC/IEEE 12207:2017 — Systems and software engineering — Software life cycle processes — https://standards.ieee.org/ieee/12207/5847/ (Section 6.3.7: software change management and impact assessment process)
- IIBA BABOK Guide v3 — Assess Proposed Solution task (Chapter 6: Solution Evaluation) and Assess Change task — https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/ (defines business analysis impact assessment scope)
- Ian Sommerville, "Software Engineering" (10th ed., Pearson) — Chapter on software change: change impact analysis, dependency analysis, and regression scope selection

### Priority 2 — Orientation

- Prosci ADKAR change management model — https://www.prosci.com/resources/articles/adkar-model (business-side readiness model; complements technical impact analysis with people and process readiness assessment)
- Scaled Agile Framework — PI Planning and impact assessment in SAFe — https://scaledagileframework.com/pi-planning/ (cross-team dependency and risk identification at program level)
- IEEE/ISO/IEC 29148:2018 — Requirements traceability as an impact assessment tool — https://standards.ieee.org/ieee/29148/6937/

### Priority 3 — Background

- Wikipedia — Change impact analysis — https://en.wikipedia.org/wiki/Change_impact_analysis
- Martin Fowler — Feature flags and progressive rollout strategies — https://martinfowler.com/articles/feature-toggles.html (orientation on rollout options that reduce blast radius of risky changes)

## Handoff

- Business-side impact assessed and documented → hand off section to System Analyst for system and API impact assessment.
- System and API impact assessed → hand off to QA for test impact assessment and regression scope.
- All impacts assessed → hand off impact brief to Project Manager for delivery planning and sequencing.
- Unresolved risk accepted with record → hand off risk record to Project Manager for tracking.
- Architecture impact identified → hand off to System Architect or Tech Lead with affected component description and impact type.
- Backward compatibility risk identified → hand off to System Analyst for API versioning decision via `shared-api-contract-design`.
