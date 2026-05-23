---
name: architecture-review-and-governance
description: Use when running architecture reviews, conformance checks, exception handling, fitness-function tracking, or architecture governance cadence for a system or domain — classifying which changes are architecturally significant, preparing review packages, and routing exceptions. Not for delivery governance, QA release gates, or enterprise portfolio governance.
family: lead
profile_level: Lead+
---

# Architecture Review and Governance

## Purpose

Run architecture review and governance for a system or domain: classify architecturally significant changes, verify conformance to agreed architecture, evaluate exceptions, track fitness functions, and maintain a governance cadence. Produce review findings that are actionable, exception records that have expiry dates, and a cadence that does not block delivery without reason.

## Use When

- A change is architecturally significant (boundary, integration, NFR, technology choice, data ownership).
- An architecture review board, peer review, or approval gate is required before delivery of a significant change.
- A deviation or exception to the agreed architecture must be evaluated, approved, or rejected with conditions.
- Conformance of implemented system to agreed architecture must be checked at a milestone or checkpoint.
- Fitness functions must be defined, tracked, or violated — triggering a review.
- A governance cadence (monthly architecture review, quarterly debt review) must be structured and maintained.

## Do Not Use When

- The task is delivery governance, sprint planning, release gate ownership, or dates → handoff to `project-manager`.
- The task is QA release testing, regression testing, or defect cycle management → handoff to `qa-engineer`.
- The task is enterprise-level governance body, portfolio review, or corporate standards → handoff to enterprise-architect.
- The task is writing the ADR for a decision that is being reviewed → `architecture-decision-records`.
- The task is making the architectural design decision itself → use the relevant design skill first.

## Inputs

- Proposed change brief, ADR draft, or design package from the requesting team.
- Agreed target architecture, architecture principles, and standards for the domain.
- NFR catalog and current fitness function status.
- Existing exception register and pending revisit triggers.
- Stakeholders: engineering leads, tech lead, QA, DevOps/SRE, security, product, data.

## Workflow

1. **Classify the change.** Is it architecturally significant? A change is significant if it touches: component boundary, integration pattern, NFR target, data ownership, technology choice with lock-in risk, or trust boundary. Routine changes (bug fixes, small features within established patterns) do not need architecture review.
2. **Prepare a review package.** Requester provides: proposed change brief, affected components and integrations, NFR impact (if any), ADR draft with alternatives. Architecture review board does not design for the team — it reviews what the team has prepared.
3. **Run the review.** Focused session (30–60 min) or async review against a checklist. Review criteria: alignment with target architecture, NFR impact, coupling introduced, security and observability properties, maintainability and reversibility.
4. **Classify the outcome.** Four outcomes: Approved (change is aligned), Approved with conditions (change is approved but conditions must be met before or after delivery), Changes required (blocking issues that must be resolved before delivery), Rejected with rationale (change contradicts agreed architecture without valid exception case).
5. **Process exceptions.** If a deviation from agreed architecture is justified: create an exception record with scope, owner, rationale, time bound, and revisit trigger. Exceptions without expiry are technical debt by another name.
6. **Track fitness functions.** For each governance-tracked property (e.g., "no cross-schema queries", "p99 checkout < 300ms", "all services have structured logs"), record current status at each review cadence. A violated fitness function triggers a focused review.
7. **Update the decision log.** Every governance decision (approval, condition, exception, rejection) is logged with date, scope, participants, and outcome. Exceptions are indexed in the exception register with revisit dates.

## Outputs

- Architecture review note: scope, findings, outcome (approved/conditions/changes/rejected).
- Conformance check note: current state vs agreed architecture, gaps, and remediation items.
- Exception record: scope, owner, rationale, time bound, revisit trigger.
- Fitness function status dashboard update.
- Updated decision log entries and exception register.

## Named Patterns

### Good — Architecture review gate with fitness function
```
Fitness function (automated, CI): No service may declare a direct dependency on another service's database schema.
Trigger: CI build for OrderService detects a SQL query against payments.transactions table.
Action: Pull request blocked. Architecture review required. Owner notified.
Review outcome: Exception record created. Migration to event-based integration by 2026-08-01.
```

### Bad — Architecture review as a bureaucratic checkpoint
Every change, no matter the size, must pass an architecture review. Review consists of a 2-hour meeting with 12 participants. Outcome is a vague "approved pending further discussion." Teams route around the process by reframing changes as "refactoring."

### Good — Significance classification that enables fast delivery
```
Architecturally significant (requires review):
- New external integration
- Change to component boundary
- Technology choice with >6-month lock-in
- NFR target change above agreed threshold

Not architecturally significant (no review):
- Feature addition within established component pattern
- Bug fix within existing integration
- UI change without new API contract
```
Teams know in advance whether a change needs review. Small changes ship without friction.

### Bad — Review scope undefined
Every team asks "do we need architecture review for this?" The architecture team answers case-by-case with inconsistent criteria. Uncertainty slows delivery. Some significant changes are never reviewed because teams avoid asking.

### Good — Exception with expiry and owner
```
Exception-009: LegacyReporting reads OrderDB directly
Owner: Data Team (DataEng Lead)
Rationale: Full migration blocked until LegacyReporting refactor in Q3.
Time bound: Expires 2026-09-01.
Revisit trigger: LegacyReporting deployment complete or date, whichever is earlier.
Status: Active. Tracked in sprint backlog of Data Team.
```

### Bad — Exception without expiry
```
Exception: We share the database because of legacy reasons.
```
No owner, no expiry, no revisit trigger. Three years later, nobody remembers what the "legacy reason" was. The exception is now permanent architecture.

### Good — Governance cadence with agenda
```
Monthly Architecture Review:
1. Fitness function dashboard: any violations? (15 min)
2. Pending ADRs for review: 2 this month (30 min)
3. Exception register: revisit triggers due this month (10 min)
4. New significant change requests (15 min)
Total: 70 min max. No significant change review → cancel the slot.
```

## Boundaries

- Does not own delivery governance, sprint planning, release dates, or budget → `project-manager`.
- Does not own QA release gates, regression testing, or defect cycle → `qa-engineer`.
- Does not own enterprise-level governance bodies or portfolio reviews → enterprise-architect.
- Does not make the architectural design decision for the team — reviews what the team has designed.

## Sources

### Priority 1 — Canonical References
- TOGAF Standard — Architecture Governance techniques: https://pubs.opengroup.org/togaf-standard/adm-techniques/chap33.html
- ISO/IEC/IEEE 42010 — Architecture Description Standard: https://www.iso.org/standard/74393.html
- SEI — Architecture Tradeoff Analysis Method (ATAM): https://resources.sei.cmu.edu/library/asset-view.cfm?assetid=513908
- Neal Ford et al. — Building Evolutionary Architectures (fitness functions): https://evolutionaryarchitecture.com/

### Priority 2 — Practitioner Guidance
- Mark Richards, Neal Ford — Fundamentals of Software Architecture: https://www.developertoarchitect.com/lessons/
- ThoughtWorks Tech Radar — fitness function–driven development: https://www.thoughtworks.com/radar/techniques/fitness-function-driven-development
- Microsoft Cloud Adoption Framework — governance: https://learn.microsoft.com/azure/cloud-adoption-framework/govern/

### Priority 3 — Supplementary
- InfoQ — architecture governance and review practices: https://www.infoq.com/architecture-design/
- Software Engineering Radio — governance and evolutionary architecture episodes: https://www.se-radio.net/

## Handoff

- Delivery sequencing following a governance decision → `project-manager`.
- QA verification of NFR or functional conditions attached to approval → `qa-engineer`.
- Design revision required by review findings → originating team + relevant design skill.
- Exception record migration into the debt registry → `architectural-risk-and-technical-debt`.
- ADR for the reviewed decision → `architecture-decision-records`.
