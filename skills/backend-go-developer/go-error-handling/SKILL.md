---
name: go-error-handling
description: Use when introducing or unifying error handling across Go service layers — wrapping with %w, classifying with errors.Is/As, choosing between sentinel and typed errors, mapping internal errors to API error shapes, and deciding when to use panic.
family: code
profile_level: Senior+
---

# Go Error Handling

## Purpose

Make errors carry enough information to diagnose and classify, without leaking implementation details to clients. Treat error type and chain as part of the contract, not as accident.

## Use When

- Introducing error handling conventions in a new service.
- Refactoring layers where errors are stringified, swallowed, or untyped.
- Mapping internal errors to API responses (HTTP status, gRPC code, error code).
- Reviewing code that uses `panic`, `recover`, or returns `error` with no classification.

## Do Not Use When

- The discussion is logging and tracing format only → `service-observability`.
- The discussion is API error contract shape (RFC 7807, gRPC status details) at the protocol level → `api-contract-design` for the contract; this skill covers the mapping.
- The discussion is test assertions on errors → `go-testing`.

## Inputs

- Layer responsibilities (handler / service / repository / external client).
- Current error types and where they originate.
- Target API error contract (HTTP/gRPC/event).

## Workflow

1. Decide error classification per layer: domain errors (`ErrNotFound`, `ErrConflict`), infrastructure errors (DB, network), input validation errors.
2. Wrap with `%w` when adding context; never use `%v` or string concatenation if the caller needs to classify.
3. Classify with `errors.Is` for sentinel errors and `errors.As` for typed errors. Never `strings.Contains` on `err.Error()`.
4. Define typed errors as exported structs in the domain package, not in the handler.
5. Map domain errors to transport errors at one well-known boundary — typically the handler — and nowhere else.
6. Use `panic` only for programmer errors (nil map write, invariant violation in `init`). Never for expected failure paths.
7. Log the error once, at the boundary that decides the response. Earlier layers wrap and return.

## Outputs

- Error type catalogue: domain sentinels, typed errors, validation error shape.
- Mapping table: domain error → HTTP status / gRPC code / API error code.
- Logging convention: who logs, with what fields, at what level.

## Named Patterns

### Good — Wrap with `%w`, classify with `errors.Is`
```go
// repository
func (r *Repo) Get(ctx context.Context, id ID) (Order, error) {
    var o Order
    err := r.db.QueryRowContext(ctx, q, id).Scan(&o.ID, &o.Total)
    if errors.Is(err, sql.ErrNoRows) {
        return Order{}, fmt.Errorf("order %s: %w", id, ErrNotFound)
    }
    if err != nil {
        return Order{}, fmt.Errorf("order %s: %w", id, err)
    }
    return o, nil
}
```
```go
// handler
if errors.Is(err, order.ErrNotFound) {
    http.Error(w, "not found", http.StatusNotFound)
    return
}
```

### Bad — String compare on `err.Error()`
```go
if strings.Contains(err.Error(), "no rows") { /* ... */ }
```
Brittle: changes when the driver updates, when the error is wrapped, when locale changes.

### Good — Typed error with `errors.As`
```go
type ValidationError struct {
    Field string
    Reason string
}
func (e *ValidationError) Error() string { return e.Field + ": " + e.Reason }

// classify
var ve *ValidationError
if errors.As(err, &ve) {
    respondValidation(w, ve)
}
```

### Bad — Untyped errors with magic strings
```go
return errors.New("validation: email is invalid")
// caller: if err.Error() == "validation: email is invalid" { ... }
```
No structured field access; cannot localize; cannot machine-route.

### Good — Mapping at one boundary
```go
// handler/error.go — the only place that knows transport
func writeErr(w http.ResponseWriter, err error) {
    switch {
    case errors.Is(err, order.ErrNotFound):
        http.Error(w, "not found", 404)
    case errors.Is(err, order.ErrConflict):
        http.Error(w, "conflict", 409)
    default:
        log.Error(err)
        http.Error(w, "internal", 500)
    }
}
```

### Bad — Transport leak in service layer
```go
func (s *Service) Create(ctx context.Context, in In) error {
    if !in.Valid() {
        return errors.New(`{"code": 400, "msg": "bad"}`) // HTTP knowledge in service
    }
}
```

### Good — Sentinel vs typed selection
Use a sentinel error when the only thing callers need to know is "this kind happened" (`ErrNotFound`, `ErrConflict`, `io.EOF`). Use a typed error when callers need structured data (`ValidationError{Field, Reason}`, `RateLimitError{RetryAfter}`).

### Bad — `panic` on expected failure
```go
func mustParse(s string) int {
    n, err := strconv.Atoi(s)
    if err != nil { panic(err) } // user input is not a programmer error
    return n
}
```

### Good — `panic` for programmer errors only
```go
func (c *Config) MustGet(key string) string {
    v, ok := c.values[key]
    if !ok { panic("config: missing key " + key) } // invariant in startup
    return v
}
```

## Boundaries

- Owns error type design and classification inside the service.
- Does not own the wire-level error contract (HTTP problem details, gRPC status details) — that is `api-contract-design`.
- Does not own log routing or alerting on errors — that is `service-observability` / `devops-sre`.

## Sources

### Priority 1 — Go canon
- `errors` package — https://pkg.go.dev/errors
- Go 1.13 error handling — https://go.dev/blog/go1.13-errors
- Effective Go: Errors — https://go.dev/doc/effective_go#errors
- Go Code Review Comments: Error Strings — https://go.dev/wiki/CodeReviewComments#error-strings
- Uber Go Style Guide: errors — https://github.com/uber-go/guide/blob/master/style.md#errors

### Priority 2 — API error contracts
- RFC 7807 Problem Details for HTTP APIs — https://www.rfc-editor.org/rfc/rfc7807
- gRPC error model — https://grpc.io/docs/guides/error/

### Priority 3 — Background
- Dave Cheney: Don't just check errors, handle them gracefully — https://dave.cheney.net/2016/04/27/dont-just-check-errors-handle-them-gracefully

## Handoff

- Wire-level error contract design → `api-contract-design`.
- Log format and trace correlation for errors → `service-observability`.
- Alert routing on error rate → `devops-sre`.
