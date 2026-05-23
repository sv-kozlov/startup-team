---
name: api-contract-design
description: Role-specific addendum for api-contract-design in the System Analyst context. Use shared-api-contract-design for the full method. This file contains specification-level patterns — consumer identification, protocol rationale, handoff brief format.
family: method
profile_level: Senior+
superseded_by: shared-api-contract-design
---

# API Contract Design — System Analyst Addendum

> **Primary skill:** `shared-api-contract-design` at `skills/shared/shared-api-contract-design/SKILL.md`.
> This file is a role-specific addendum. Follow the shared skill's Workflow and apply the System Analyst–specific constraints below.

## System Analyst Scope

The System Analyst applies `shared-api-contract-design` at the **requirements-specification level**:

- Identifies consumers, use cases, and operations before naming any endpoint.
- Chooses the protocol with documented rationale; does not finalize implementation choice.
- Models resources and state transitions in alignment with the ubiquitous language.
- Produces an OpenAPI 3.1 outline or gRPC `.proto` draft as a **handoff brief** for Engineering — not production code.
- Does not generate server stubs, write handlers, or implement validation logic.

## SA-Specific Constraints

1. **Consumer list is mandatory before schema work.** Name every consumer (team, system, external integrator) and the operations they need. Undocumented consumers are an open risk.
2. **Protocol rationale must be explicit.** State why REST vs gRPC vs SOAP — client compatibility, schema evolution needs, existing ecosystem. Do not default without justification.
3. **Error taxonomy first.** Define the full list of business error conditions with HTTP/gRPC status, machine-readable code, cause, and recovery hint before handing off schema to Engineering. Gaps discovered later are costly.
4. **Backward compatibility is a requirements decision.** State the versioning policy and deprecation window in the contract brief; Engineering enforces it in code.
5. **Handoff brief format** — the output is a specification artifact, not implementation: OpenAPI YAML outline with `operationId`, `summary`, field names, types, and `$ref` to error schema. Not runnable code.

## SA-Specific Named Patterns

### Good — Consumer identification table
```
API: POST /v1/orders
Consumers:
  - Web frontend (React, browser) — place order from cart
  - Mobile app (iOS, Android) — repeat order from history
  - Internal fulfillment-service — receive new order events
Trigger: user completes checkout or repeats past order
```
Every subsequent decision (protocol, pagination, error shape) is grounded in real consumer needs.

### Bad — Schema before consumers
Designing endpoint shape without knowing who calls it or why. Leads to over-fetching, missing fields, or protocol mismatch discovered in review.

### Good — Protocol rationale in the brief
```
Protocol: REST + OpenAPI 3.1
Rationale:
  - Browser client requires HTTP/1.1 compatibility (gRPC not supported natively).
  - Schema evolution is additive-only; no streaming required.
  - Public-facing; OpenAPI enables third-party client generation.
Decision owner: System Analyst + Tech Lead sign-off.
```

### Bad — Protocol assumed without rationale
"We'll use REST" with no documented reason. A later decision to switch to gRPC has no baseline to compare against.

### Good — Error taxonomy table (handoff brief format)
```
Error code            | HTTP | Cause                        | Recovery hint
----------------------|------|------------------------------|-------------------------------
INSUFFICIENT_FUNDS    | 422  | Balance < requested amount   | Replenish balance or reduce order
ORDER_ALREADY_CANCELLED | 409 | Order in terminal state     | Fetch current order state
IDEMPOTENCY_KEY_REQUIRED | 400 | Header missing            | Include Idempotency-Key header
```
Engineering implements this table as a mapper; QA tests each row.

### Bad — Error documentation by example only
"Returns 422 if something is wrong with the order." Engineering invents codes; QA cannot write reproducible tests; clients parse strings.

### Good — Versioning policy in the brief
```
Versioning:
  - Minor (additive): new optional fields, new endpoints — no consumer action required.
  - Major (breaking): rename, retype, remove, semantic change — new URL version (/v2),
    deprecation window 6 months, migration guide required.
  - Deprecation marked in schema: `deprecated: true`, `x-sunset: 2026-11-01`.
```

## Handoff

- Requirements behind the API not yet gathered → `requirements-elicitation`.
- Functional scenarios driving API design → `functional-specification`.
- Async event and message schemas → `event-driven-integration`.
- Platform-wide API style guide → `system-architect` / `tech-lead`.
- API implementation code → Engineering (Backend Go Developer / Python Developer / Fullstack Developer).
