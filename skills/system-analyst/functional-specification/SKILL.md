---
name: functional-specification
description: Use when translating gathered requirements into a testable, developer-ready functional specification — SRS section, scenario, state machine, business rules, error cases, acceptance criteria, or implementation tasking.
family: method
profile_level: Senior+
---

# Functional Specification

## Purpose

Produce a specification precise enough that development, QA, and stakeholders share the same understanding of what the system must do, under which conditions, and how it must handle deviations. Requirements become unambiguous, testable, and traceable to their source.

## Use When

- A feature needs an SRS section, functional specification, or technical tasking document.
- System behavior, scenarios, states, validations, or errors must be formally described.
- Development or QA needs an implementation-ready description they can work from without recurring clarification.
- Acceptance criteria are missing, vague, or not connected to system behavior.
- A change request requires a before/after behavioral description.

## Do Not Use When

- Requirements are not yet gathered or are still contradictory — start with `requirements-elicitation`.
- The task is specifying an API wire shape — use `api-contract-design`.
- The task is specifying entity structures and ER models — use `data-modeling`.
- The task is specifying NFR quality constraints — use `non-functional-requirements`.
- The task is architectural design — hand off to `system-architect`.

## Inputs

- Validated requirements set from `requirements-elicitation` or equivalent.
- Business rules, user flows, UI state descriptions, or existing system behavior.
- API constraints, data entity list, security and permission rules.
- Known decisions, assumptions, out-of-scope exclusions, and open questions.
- Target audience: developers, QA, product owner, or combined.

## Workflow

1. Define scope and out-of-scope behavior for this specification. State what the specification covers and what it explicitly excludes.
2. Identify actors, their roles, permissions, and system entry points for each scenario covered.
3. For each scenario: write preconditions, main flow, alternative flows, and exception flows. Make each step an observable system action or user action.
4. Specify validations: field constraints, business rule enforcement, permission checks, state guards. Each validation must have a testable failure response.
5. Describe state model where applicable: entities, allowed states, transitions, guards, and side effects of transitions.
6. Specify error cases: each error condition, its cause, the system response (code, message, action), and recovery path.
7. Link behavior to API, data, integration, and UI artifacts by reference. Do not duplicate artifact content; reference it.
8. Write acceptance criteria for each functional requirement using given-when-then form. Each criterion must be independently testable.
9. Record open questions with owner and impact; flag assumptions that require validation.

## Outputs

- Functional specification document or section.
- SRS section with numbered requirements (shall statements).
- Scenario and edge-case list with pre/main/alt/exception flows.
- State model description or state table.
- Acceptance criteria in given-when-then form.
- Developer-ready tasking with cross-references to API, data, and integration specs.

## Named Patterns

### Good — Testable "shall" requirement
```
REQ-045: The system shall reject a password change request
when the new password matches any of the user's last 5 passwords,
returning HTTP 422 with error code PASSWORD_REUSE_FORBIDDEN.
```
Actor, condition, behavior, and observable outcome present. QA writes one test per requirement.

### Bad — Requirement as vague policy
```
The system must handle password security properly.
```
"Properly" is not testable. Engineering will implement its own interpretation; QA has no criterion.

### Good — Given-when-then acceptance criterion
```
Given: a registered user with status Active
When: the user submits a login request with a valid email and correct password
Then: the system returns HTTP 200 with a session token valid for 24 hours
  And: the last_login_at field is updated in the user record
  And: a login_success event is emitted to the audit log
```
Three observable outcomes; all independently verifiable.

### Bad — Acceptance criterion as feature summary
```
Users should be able to log in successfully.
```
Cannot be tested as written. Does not specify what "success" looks like at the system level.

### Good — State transition table
```
Order state transitions:
  Draft      → Confirmed   (trigger: submit, guard: payment_method_attached)
  Confirmed  → Processing  (trigger: payment_captured)
  Processing → Shipped     (trigger: fulfillment_dispatched)
  Processing → Cancelled   (trigger: cancel, guard: within_cancellation_window)
  Shipped    → Delivered   (trigger: delivery_confirmed)
  Any        → Cancelled   (trigger: admin_cancel, guard: role=admin)
Side effect on Cancelled: emit OrderCancelled event; initiate refund if payment was captured.
```
States, transitions, guards, and side effects explicit. No ambiguity about what happens on admin cancellation.

### Bad — State logic embedded in prose
"If the order was already shipped, cancellation might still be possible depending on the situation." QA cannot test "depending on the situation"; developers will implement differently.

### Good — Explicit error taxonomy
```
POST /v1/orders — error responses:
  400 INVALID_REQUEST      — malformed payload or missing required field
  422 INSUFFICIENT_FUNDS   — account balance below requested amount
  422 ITEM_UNAVAILABLE     — one or more items are out of stock
  409 DUPLICATE_ORDER      — idempotency key already used for a completed order
  503 SERVICE_UNAVAILABLE  — downstream payment service unreachable
```
Each error has a code, a cause, and a distinct HTTP status. Frontend and QA know exactly what to handle.

### Bad — Generic error handling
"The system returns an error if something goes wrong." No codes, no causes, no distinction between client and server errors.

## Boundaries

- Owns: functional scenarios, state logic, validation rules, error taxonomy, acceptance criteria, developer-ready tasking.
- Does not own: API wire format design — that is `api-contract-design`.
- Does not own: entity structure and ER modeling — that is `data-modeling`.
- Does not own: UX solution design — that is `ui-ux-designer`.
- Does not own: test strategy and regression scope — that is `qa-engineer`.
- Does not own: architecture decisions — that is `system-architect`.
- Does not own: production code structure — that is Engineering.

## Sources

### Priority 1 — Standards
- IEEE/ISO/IEC 29148:2018 Requirements Engineering — https://standards.ieee.org/content/ieee-standards/en/standard/29148-2018.html
- Karl Wiegers, Joy Beatty: Software Requirements, 3rd ed. — book reference, Microsoft Press
- Gojko Adzic: Specification by Example — book reference, Manning

### Priority 2 — Scenarios and acceptance
- Alistair Cockburn: Writing Effective Use Cases — book reference, Addison-Wesley
- Alistair Cockburn: Use Case 2.0 — https://www.ivarjacobson.com/publications/books/use-case-2-0
- Atlassian acceptance criteria guide — https://www.atlassian.com/work-management/project-management/acceptance-criteria
- Atlassian definition of ready — https://www.atlassian.com/agile/project-management/definition-of-ready

### Priority 3 — Background
- IIBA BABOK Guide v3 — https://www.iiba.org/career-resources/a-business-analysis-body-of-knowledge/babok/
- Scrum Guide — https://scrumguides.org/scrum-guide.html

## Handoff

- Missing or contradictory requirements before specification → `requirements-elicitation`.
- API wire contract design → `api-contract-design`.
- Entity and data model design → `data-modeling`.
- NFR quality constraints → `non-functional-requirements`.
- UX flow and interaction design → `ui-ux-designer`.
- Architecture decisions surfaced during specification → `system-architect`.
- Test strategy and regression scope → `qa-engineer`.
