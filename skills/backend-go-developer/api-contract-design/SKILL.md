---
name: api-contract-design
description: Role-specific addendum for api-contract-design in the Backend Go Developer context. Use shared-api-contract-design for the full method. This file contains Go-specific code examples and implementation constraints.
family: method
profile_level: Senior+
superseded_by: shared-api-contract-design
---

# API Contract Design — Go Addendum

> **Primary skill:** `shared-api-contract-design` at `skills/shared/shared-api-contract-design/SKILL.md`.
> This file is a role-specific addendum. Follow the shared skill's Workflow and apply the Go-specific constraints below.

## Go Implementation Constraints

Apply these in addition to the shared skill's Workflow:

1. **Generate, do not handwrite the wire layer.** Use `oapi-codegen` for OpenAPI → Go, `protoc` + `buf` for protobuf. Never write handler signatures or request/response structs by hand.
2. **Run `buf breaking` in CI** against the previous tag for every `.proto` change. For OpenAPI, run `oasdiff breaking` on every PR that touches `openapi.yaml`.
3. **Idempotency-Key header** — extract in middleware; store key → serialized response in Redis with a documented TTL; return `409 Conflict` if key already exists and processing is in progress; return cached response when complete.
4. **gRPC error codes** — map domain errors to `google.golang.org/grpc/codes` in a dedicated mapper function; never return `codes.Unknown` for a business error.
5. **Protobuf field numbers** are stable identifiers. Never reuse a deleted field number; mark removed fields with `reserved`.

## Go-Specific Named Patterns

### Good — Code generation from OpenAPI
```go
// buf.gen.yaml (for protobuf)
version: v1
plugins:
  - plugin: go
    out: gen/go
    opt: paths=source_relative
  - plugin: go-grpc
    out: gen/go
    opt: paths=source_relative

// For REST: oapi-codegen generates:
// - Server interface (implement, don't handwrite)
// - Request/response types from OpenAPI schemas
// - Strict mode: compiler error if handler is not implemented
```
The compiler enforces contract conformance; no drift between spec and code.

### Bad — Handwritten struct that mirrors the spec
```go
// DO NOT do this — written by hand, never checked against openapi.yaml
type PlaceOrderRequest struct {
    Items    []string `json:"items"`
    Currency string   `json:"currency"`
}
```
Spec and implementation drift silently. Breaking changes not caught in CI.

### Good — gRPC domain error mapping
```go
import (
    "google.golang.org/grpc/codes"
    "google.golang.org/grpc/status"
)

func mapDomainErr(err error) error {
    var e *domain.InsufficientFundsError
    if errors.As(err, &e) {
        return status.Errorf(codes.FailedPrecondition, "insufficient funds: %s", e.Detail)
    }
    return status.Errorf(codes.Internal, "internal error")
}
```
Every business error maps to a specific gRPC status code; `Unknown` is never returned for a business condition.

### Bad — Generic gRPC error
```go
return nil, status.Errorf(codes.Unknown, err.Error())
```
Client cannot distinguish a business error from an infrastructure failure.

### Good — Stable protobuf field numbers
```protobuf
message Order {
  string id = 1;
  string status = 2;
  // field 3 was `legacy_ref`, removed in v1.2; number is reserved
  reserved 3;
  reserved "legacy_ref";
  string currency = 4; // added in v1.3
}
```
Old clients parsing binary payloads ignore unknown fields safely; reserved prevents accidental reuse.

## Handoff

- Requirements behind the contract → `system-analyst` (`shared-api-contract-design`, System Analyst mode).
- Platform-wide API style guide → `tech-lead` / `system-architect`.
- Client-side contract consumption → `frontend-developer` / `mobile-developer`.
- Event/message schemas → `event-driven-integration`.
