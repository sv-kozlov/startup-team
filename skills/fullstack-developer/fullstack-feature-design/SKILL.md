---
name: fullstack-feature-design
description: Use when designing or decomposing a web feature end-to-end — from user scenario to API contract, data schema, UI states, backend service shape, and test plan. Covers vertical slice decomposition, layer boundary decisions, proportionality of architecture choice to problem size, and ADR authoring for non-obvious trade-offs.
family: method
profile_level: Senior+
---

# Fullstack Feature Design

## Purpose

Shape a feature so all layers — UI, API, backend logic, data — fit together without hidden coupling, with a test plan and an observable production path. Optimize for a vertical slice a new team member can follow from the HTTP handler to the database row without a guide.

## Use When

- Starting a new user-facing feature that touches both client and server.
- Decomposing a product requirement into tasks across frontend and backend.
- Reviewing a proposed design where layer coupling, API shape, or data model is unclear.
- Deciding how deep the architecture should go: CRUD endpoint vs domain model vs event-driven.

## Do Not Use When

- The feature is frontend-only with no backend changes → focus on `fullstack-data-flow`.
- The task is purely an API contract change without UI impact → `api-contract-design-fullstack`.
- The scope requires redesigning cross-service boundaries or platform topology → handoff to `system-architect`.
- The task requires eliciting or formalizing business requirements → handoff to `system-analyst`.

## Inputs

- User scenario or job story: who does what and why.
- Existing API contracts, data schema, and current component tree.
- NFRs: latency budget, expected data volume, security model.
- Team context: monolith vs services, frontend framework, backend language.

## Workflow

1. State the user scenario in one sentence. Name the happy path and the two most likely failure paths.
2. Draft the API contract sketch first: resource, method, request shape, response shape, error codes. Do not implement yet — agree on the shape with the team.
3. Identify the data change: new table/column, updated schema, or read-only. If schema changes, plan the expand/migrate/contract sequence now, not at deploy time.
4. Define UI states: loading, success, error, empty, optimistic. Map each state to an API response or local state. States without designs are future bugs.
5. Decide the backend service shape: single endpoint or orchestrated calls, synchronous or async, database or cache. Choose the simplest shape that meets the load profile.
6. Write the test plan: which layer owns what test — component test for UI states, contract test for API shape, integration test for DB writes, e2e for the critical path.
7. Identify the release sequence: is a feature flag needed? Can frontend and backend deploy independently? Which deploy step exposes the feature to users?
8. Write an ADR or PR description for any non-obvious choice: why this data shape, why async, why this error handling strategy.

## Outputs

- API contract sketch (OpenAPI fragment or TypeScript interface) agreed before implementation.
- Data schema change plan with expand/migrate/contract steps if applicable.
- UI state inventory mapped to API responses.
- Test plan per layer (component, contract, integration, e2e).
- Release sequence with feature flag decision.
- ADR or PR description for non-obvious trade-offs.

## Named Patterns

### Good — Scenario-first, contract-second
Start by writing the user scenario:
```
User edits a product. They see a loading indicator. On success, the list refreshes. On conflict (another edit), they see a specific error. On network failure, their input is preserved.
```
Then derive the API contract from the scenario. The error case `409 Conflict` exists because the scenario names it — not because the developer expected it.

### Bad — Implementation-first design
The developer adds a database column, writes the handler, then decides the API shape based on what was easy to return. The client receives a shape optimized for the server's ORM, not for the UI state machine.

### Good — Proportional architecture
A simple CRUD resource ships as: one database table, one REST endpoint, one repository function, one React component with `useQuery`. No event sourcing, no sagas, no CQRS — until the load profile or complexity justifies it.

### Bad — Architecture for hypothetical scale
A single internal tool with 50 users ships with Kafka, CQRS event store, separate read/write models, and a microservices mesh. Five engineers change five services for one bug fix.

### Good — UI states from contract
```typescript
type OrderState =
  | { status: 'loading' }
  | { status: 'success'; data: Order }
  | { status: 'error'; code: 'CONFLICT' | 'NOT_FOUND' | 'NETWORK' }
  | { status: 'empty' };

// The error union is derived from the API contract error codes.
// No runtime surprises about which codes to handle.
```

### Bad — Undeclared error handling
The component renders a generic "Something went wrong" message. The API contract has three error codes the UI never handles differently. Users cannot recover from a correctable error.

### Good — Release sequence planned upfront
1. Backend: add new column (nullable, no constraint) — deploy.
2. Backend: new endpoint behind feature flag — deploy.
3. Frontend: new UI behind same feature flag — deploy.
4. Enable flag for 5% → 100%.
5. Cleanup: remove flag, add NOT NULL constraint.

Each step is reversible. No step exposes incomplete work to users.

### Bad — Big bang deploy
Frontend and backend changes in one PR. Feature flag deferred to "later". The first deploy breaks the UI because the API column doesn't exist yet.

## Boundaries

- Owns feature-level design decisions: API shape, data schema, UI states, test plan, release sequence.
- Does not own cross-service architecture, bounded contexts, or platform topology → `system-architect`.
- Does not own team-wide layout standards across multiple services → `tech-lead`.
- Does not own requirements elicitation or formal specification → `system-analyst`.
- Does not own the UX concept or interaction design → `ui-ux-designer`.

## Sources

### Priority 1 — Feature design canon
- OpenAPI Specification 3.1 — https://spec.openapis.org/oas/v3.1.0
- React Documentation (state and effects) — https://react.dev/
- MDN Web Docs — https://developer.mozilla.org/
- RFC 7807 Problem Details for HTTP APIs — https://www.rfc-editor.org/rfc/rfc7807

### Priority 2 — Design orientation
- The Twelve-Factor App — https://12factor.net/
- martinfowler.com on feature toggles — https://martinfowler.com/articles/feature-toggles.html
- martinfowler.com on vertical slice architecture — https://martinfowler.com/

### Priority 3 — Pattern background
- web.dev — https://web.dev/
- ThoughtWorks Technology Radar — https://www.thoughtworks.com/radar

## Handoff

- Cross-service and platform architecture decisions → `system-architect`.
- Team-wide standards across multiple services → `tech-lead`.
- Requirements elicitation and formal specification → `system-analyst`.
- UX concept and interaction design → `ui-ux-designer`.
- Deep backend data layer or concurrency design → `fullstack-data-flow` or backend specialist (`backend-go-developer` / `python-developer`).
- Release infrastructure and deployment platform → `devops-sre`.
