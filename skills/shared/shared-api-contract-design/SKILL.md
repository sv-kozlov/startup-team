---
name: shared-api-contract-design
description: Use when an API contract must be specified, implemented, or evolved — covering resource modeling, protocol selection, error shapes, backward compatibility, idempotency, pagination, versioning, and contract documentation. Applies at requirements-specification level and implementation level; each consuming role applies the method within its own ownership boundary.
---

# Shared API Contract Design

## Purpose

Produce API contracts that are unambiguous, stable across releases, and evolvable without coordinated redeploys. Make the contract the single source of truth for resource shape, error taxonomy, compatibility obligations, and versioning policy — regardless of whether it is being authored as a specification or implemented as production code.

## Use When

- A new REST or gRPC API surface must be designed before implementation starts.
- An existing contract needs backward compatibility analysis before adding, deprecating, or removing fields.
- Multiple teams must align on a shared contract before parallel implementation begins.
- Error shapes, pagination strategy, or idempotency behavior need to be standardized.
- A versioning or deprecation policy must be documented for the contract.
- A contract change must be validated in CI.

## Do Not Use When

- The discussion is asynchronous event and message contracts → `event-driven-integration`.
- The discussion is platform-wide API style guide or governance → `tech-lead` / `system-architect`.
- The discussion is requirements elicitation behind the API, not the contract itself → `requirements-elicitation` (System Analyst).
- The discussion is client-side data fetching or state management → role-local skills (`fullstack-data-flow`, `api-integration-frontend`, `api-integration-mobile`).
- The discussion is internal error type design within a single service → role-local error-handling skill.

## Role Modes

**System Analyst** — Specify the contract at the requirements level. Identify consumers, choose protocol with rationale, model resources and state transitions, define the error taxonomy (one shape per API family), specify idempotency and pagination rules, set versioning and deprecation policy, and produce an OpenAPI 3.1 outline or gRPC `.proto` draft as a handoff brief for Engineering. Does not write production code or generate implementation artifacts.

**Backend Go Developer** — Implement the contract from the spec. Generate Go code from the OpenAPI / `.proto` file (do not handwrite the wire layer). Enforce backward compatibility rules in code: additive-only for minor versions, new major version for breaking changes. Make every state-changing operation idempotent using `Idempotency-Key`. Publish the contract artifact in a versioned location and run a schema diff tool in CI on every change.

**Python Developer** — Implement the contract in FastAPI or gRPC. Derive Pydantic v2 models as the schema source; let FastAPI generate OpenAPI from them. Apply RFC 7807 error shapes via a shared exception handler. Run `oasdiff` or `buf breaking` in CI. For gRPC: use protobuf, enforce additive evolution.

**Fullstack Developer** — Own the type boundary between client and server. Treat the OpenAPI 3.1 file as the single source of truth. Generate TypeScript types using `openapi-typescript` and validate in CI (`tsc --noEmit`) that both ends are typed from one schema. No manual type duplication across client and server.

## Inputs

- Business capability or user scenario being exposed.
- Consumer list: internal services, web frontend, mobile clients, third-party integrators.
- Existing contract version, deprecation schedule, and traffic mix.
- NFRs: latency budget, throughput, security and auth model, compliance constraints.
- Known idempotency, pagination, and ordering requirements.
- Existing ADRs or style guide entries that apply.

## Workflow

1. **Identify consumers and operations.** State who calls this API and why before naming endpoints. Distinguish read, write, state-transition, and event-publishing operations.

2. **Choose the protocol.** Use three criteria: client compatibility, schema evolution needs, performance budget. Default: REST + OpenAPI 3.1 for external/public and browser clients; gRPC + protobuf for internal high-throughput service-to-service. Document the choice rationale.

3. **Model resources and operations.** For REST: resources are nouns; CRUD maps to GET/POST/PUT/PATCH/DELETE; explicit state transitions use sub-action suffixes (`:cancel`, `:approve`). For gRPC: services, methods, and message types reflect domain operations. Align names with the ubiquitous language.

4. **Write or generate the schema.** For REST: OpenAPI 3.1 YAML as the source of truth; generate implementation code from it — do not handwrite the wire layer. For gRPC: `.proto` file is the source of truth. Define field names, types, required/optional status, validation constraints, and nullability.

5. **Specify the error taxonomy.** One error shape per API family: RFC 7807 Problem Details for REST (`type`, `title`, `status`, `code`, `instance`), status details for gRPC. Each business error condition maps to a distinct machine-readable code and HTTP/gRPC status.

6. **Define idempotency, pagination, and filtering.** For state-changing POST operations: document whether idempotency is guaranteed and how — `Idempotency-Key` header with server-stored key→response mapping and TTL. For list operations: cursor-based pagination for live/large datasets; offset only for bounded, stable datasets.

7. **Set backward compatibility rules.** Additive changes (new optional fields, new endpoints) are safe on minor versions. Breaking changes (rename, retype, remove, semantic change) require a new major version, deprecation window of 6–12 months, and a migration guide. Mark deprecated fields in the schema with a sunset date.

8. **Publish and validate.** Publish the contract artifact in a versioned, discoverable location (`docs/api/openapi.yaml`, schema registry). Run a contract diff tool in CI on every PR that changes the schema. No manual sync allowed.

## Outputs

- OpenAPI 3.1 document or `.proto` file as the versioned source of truth.
- Error taxonomy: error code list with HTTP/gRPC status, cause, and recovery hint.
- Idempotency specification: key, TTL, duplicate behavior.
- Pagination strategy: cursor vs offset decision with rationale.
- Versioning and deprecation policy documented in the repo.
- Contract change log per release.
- CI validation step (schema diff, type generation check).

## Named Patterns

### Good — Resource-oriented REST
```
GET    /v1/orders            — list (cursor pagination)
POST   /v1/orders            — create (Idempotency-Key required)
GET    /v1/orders/{id}       — read
PATCH  /v1/orders/{id}       — partial update
POST   /v1/orders/{id}:cancel — explicit state transition
```
Resources are nouns. State transitions that do not fit CRUD use a sub-action suffix, not an RPC-style verb endpoint.

### Bad — RPC over REST
```
POST /v1/createOrder
POST /v1/getOrderById
POST /v1/updateOrderStatus
```
Loses HTTP caching, breaks intermediary semantics, makes resource modeling implicit.

### Good — Additive schema evolution
```yaml
Order:
  properties:
    id:       { type: string, format: uuid }
    status:   { type: string }
    currency: { type: string, description: "Added in v1.2; optional; server defaults to tenant currency." }
```
New optional field. Old consumers ignore unknown fields. No breaking change.

### Bad — Breaking field type change
Renaming `amount` (decimal) to `amount_cents` (integer) on the same endpoint version. Every consumer that stored or displayed the field now produces wrong results silently.

### Good — RFC 7807 error shape
```json
{
  "type": "https://api.example.com/errors/insufficient-funds",
  "title": "Insufficient account balance",
  "status": 422,
  "code": "INSUFFICIENT_FUNDS",
  "detail": "Available: 45.00 USD; requested: 120.00 USD",
  "instance": "/v1/payments/abc123"
}
```
Machine-readable `code` for programmatic handling; one shape across all endpoints; one error parser for all clients.

### Bad — Per-endpoint error shape
One endpoint returns `{ "error": "..." }`, another returns `{ "message": "...", "code": 42 }`. Frontend and mobile write multiple parsers; QA cannot write shared error-handling tests.

### Good — Idempotency specification
```
POST /v1/payments — Idempotency-Key: <client-generated UUID>
Server stores key → response for 24h TTL.
Duplicate within TTL: returns original response, no side effect.
Duplicate after TTL: treated as a new request.
Missing key: HTTP 400, code IDEMPOTENCY_KEY_REQUIRED.
```
Safe to retry on network failure. Prevents double-charge, duplicate order, double inventory decrement.

### Bad — "Clients should not retry"
Implies the contract is not idempotent. Networks make this obligation impossible to honor under real failure conditions.

### Good — Cursor pagination
```
GET /v1/orders?cursor=eyJpZCI6...&limit=50
→ { "items": [...], "next_cursor": "eyJpZCI6..." }
```
Stable under concurrent inserts and deletes. Scales to millions of rows.

### Bad — Offset pagination on live data
```
GET /v1/orders?offset=10000&limit=50
```
Inserts shift the window; items are skipped or duplicated; deep pages degrade.

## Boundaries

- Does not own the platform-wide API style guide or governance → `tech-lead` / `system-architect`.
- Does not own functional requirements behind the API → `system-analyst` (requirements-elicitation, functional-specification).
- Does not own asynchronous event and message contracts → `event-driven-integration`.
- Does not own client-side contract consumption or data fetching → role-local integration skills.
- Does not own internal error type design within a single service → role-local error handling skill.

## Sources

### Priority 1 — Protocol canon
- OpenAPI Specification 3.1 — https://spec.openapis.org/oas/v3.1.0
- OpenAPI best practices — https://learn.openapis.org/best-practices.html
- RFC 7807 Problem Details for HTTP APIs — https://www.rfc-editor.org/rfc/rfc7807
- RFC 9110 HTTP Semantics — https://www.rfc-editor.org/rfc/rfc9110
- Protocol Buffers — https://protobuf.dev/
- gRPC Core Concepts — https://grpc.io/docs/what-is-grpc/core-concepts/

### Priority 2 — Design orientation
- Google API Improvement Proposals (AIPs) — https://google.aip.dev/
- Microsoft REST API Guidelines — https://github.com/microsoft/api-guidelines
- OWASP API Security Top 10 — https://owasp.org/API-Security/
- Stripe API documentation as a reference — https://stripe.com/docs/api

### Priority 3 — Pattern background
- microservices.io API patterns — https://microservices.io/patterns/
- martinfowler.com on API design — https://martinfowler.com/
