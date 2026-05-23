---
name: go-concurrency-and-context
description: Use when adding or reviewing goroutines, propagating context.Context, designing request lifecycle, implementing graceful shutdown, or hunting data races. Covers goroutine ownership, cancellation, deadline propagation, sync primitives, and race detector use.
family: code
profile_level: Senior+
---

# Go Concurrency and Context

## Purpose

Make every goroutine accountable: it has an owner, a context with cancellation, a known termination point, and a draining strategy on shutdown. Make context propagation a first-class API choice, not an afterthought.

## Use When

- Spawning a goroutine in a handler, worker, or background job.
- Designing the lifecycle of a service from `main()` to graceful shutdown.
- Reviewing code that uses `sync`, channels, `errgroup`, or `context`.
- Diagnosing a data race, deadlock, goroutine leak, or shutdown hang.

## Do Not Use When

- The discussion is about error wrapping shape → `go-error-handling`.
- The discussion is about test concurrency primitives only → `go-testing`.
- The discussion is about cluster-level lifecycle (pod termination, drain) → handoff to `devops-sre`.

## Inputs

- Code path that introduces or consumes concurrency.
- Service entry point and shutdown signal handling.
- Race detector and `pprof` output if a defect is suspected.

## Workflow

1. For every `go` statement, name the owner. The owner is the function that started it and is responsible for its termination.
2. Pass `context.Context` as the first argument across every blocking call: I/O, channel receive, sleep, lock acquisition with timeout.
3. Use `errgroup.Group` with `WithContext` for parallel work that must fail together.
4. Bound the work: every external call has a deadline; every channel has a documented closer; every `select` has a `<-ctx.Done()` branch where relevant.
5. Shut down from the outside in: cancel the root context, stop accepting new work, drain in-flight work with a deadline, then return.
6. Run `go test -race` on any package that introduces concurrency. If the package has none, document why.

## Outputs

- Lifecycle diagram or short note describing owners, contexts, and shutdown order.
- Test coverage including `-race` for new concurrent code.
- ADR or PR note for any non-trivial channel topology (fan-out/fan-in, pipeline stages).

## Named Patterns

### Good — Owner-driven goroutine with cancellation
```go
func (s *Service) Run(ctx context.Context) error {
    g, gctx := errgroup.WithContext(ctx)
    g.Go(func() error { return s.consume(gctx) })
    g.Go(func() error { return s.publish(gctx) })
    return g.Wait()
}
```
The caller owns the goroutines via `errgroup`; one failure cancels the group; `Wait` reports the first non-nil error.

### Bad — Orphan goroutine
```go
func (s *Service) Handle(req Request) {
    go func() {
        s.expensiveAudit(req) // no ctx, no owner, no error path
    }()
}
```
On shutdown this goroutine keeps running; on panic it kills the process; on error it disappears.

### Good — Context propagation across layers
```go
func (h *Handler) Create(w http.ResponseWriter, r *http.Request) {
    ctx, cancel := context.WithTimeout(r.Context(), 2*time.Second)
    defer cancel()
    if err := h.svc.Create(ctx, parseBody(r)); err != nil { /* ... */ }
}
```
The request context flows from handler to service to repository, carrying deadline and cancellation.

### Bad — `context.Background()` in a request path
```go
func (s *Service) Create(_ context.Context, in Input) error {
    return s.repo.Insert(context.Background(), in) // drops deadline
}
```
The downstream call ignores the caller's deadline and cannot be cancelled when the client disconnects.

### Good — Graceful shutdown
```go
srv := &http.Server{ /* ... */ }
go func() { _ = srv.ListenAndServe() }()

<-sigCtx.Done() // SIGTERM
shutdownCtx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()
_ = srv.Shutdown(shutdownCtx)
workers.Drain(shutdownCtx)
```
Stop accepting new connections, then drain in-flight requests and workers with an explicit deadline.

### Bad — `os.Exit` on signal
A SIGTERM handler calls `os.Exit(0)` immediately. In-flight requests are cut, in-flight DB transactions are abandoned, the message broker thinks the consumer is alive.

### Good — `select` with cancellation branch
```go
select {
case msg := <-ch:
    return process(msg)
case <-ctx.Done():
    return ctx.Err()
}
```

### Bad — Unbounded `time.Sleep` in a loop
```go
for {
    work()
    time.Sleep(1 * time.Second) // not cancellable
}
```
Shutdown waits for the full sleep; a `time.NewTicker` plus `<-ctx.Done()` branch is the idiomatic shape.

## Boundaries

- Owns goroutine lifecycle and context propagation inside the service.
- Does not own pod lifecycle, preStop hooks, or cluster drain — that is `devops-sre`.
- Does not own cross-service backpressure design — that is `system-architect`.

## Sources

### Priority 1 — Go canon
- The Go Memory Model — https://go.dev/ref/mem
- Effective Go — https://go.dev/doc/effective_go
- `context` package — https://pkg.go.dev/context
- `golang.org/x/sync/errgroup` — https://pkg.go.dev/golang.org/x/sync/errgroup
- Go blog: Pipelines and cancellation — https://go.dev/blog/pipelines
- Go blog: Go Concurrency Patterns: Context — https://go.dev/blog/context

### Priority 2 — Reliability practice
- Google SRE Book — https://sre.google/sre-book/handling-overload/

### Priority 3 — Background
- Go Programming Language (Donovan, Kernighan), ch. 8–9 — book reference.

## Handoff

- Platform-level draining and PodDisruptionBudget → `devops-sre`.
- Backpressure across service boundaries → `system-architect`.
- Error propagation shape between goroutines → `go-error-handling`.
- Concurrency-aware testing → `go-testing`.
