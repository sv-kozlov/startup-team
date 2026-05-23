---
name: go-testing
description: Use when designing or reviewing Go tests — unit, integration, contract, benchmarks. Covers table-driven tests, fakes vs mocks, testcontainers for integration, race detector, fuzzing, and pprof-driven performance work.
family: code
profile_level: Senior+
---

# Go Testing

## Purpose

Build a test suite that catches regressions, runs fast enough to be used, and isolates the unit under test from the rest of the system. Choose the testing level by the question being answered, not by reflex.

## Use When

- Writing tests for new Go code.
- Adding integration coverage for DB, broker, or HTTP client.
- Reviewing tests that are slow, flaky, or duplicate.
- Investigating performance with benchmarks and `pprof`.

## Do Not Use When

- The discussion is QA strategy or release-level regression → handoff to `qa-engineer`.
- The discussion is CI infrastructure → handoff to `devops-sre`.
- The discussion is concurrency design itself → `go-concurrency-and-context`.

## Inputs

- Code path under test and its dependencies.
- Existing test pyramid shape and current pain (slow, flaky, missing coverage).
- NFR for test runtime in CI.

## Workflow

1. Pick the level: unit (no I/O), integration (real DB/broker via testcontainers), contract (against schema), end-to-end (rare, owned by QA).
2. Default to table-driven tests. One `t.Run(tt.name)` per case; subtests give isolation and parallelism.
3. Use fakes over mocks when behavior is checked, not interaction. Generate mocks (`gomock`, `mockery`) only when interaction matters and reduces hand-rolled boilerplate.
4. For integration tests, use `testcontainers-go` to start real Postgres/Kafka/Redis. Share a container across tests in the same package via `TestMain`.
5. Run `go test -race` on any concurrent code. Required, not optional.
6. Write benchmarks for hot paths before optimizing. Use `b.ReportAllocs()` and `testing.Benchmark` results, not stopwatches.
7. Use `go test -fuzz` for parsers, decoders, and any function with a string/bytes input boundary.
8. Keep tests deterministic: inject clock, random seed, IDs.

## Outputs

- Tests at the appropriate level, runnable with `go test ./...`.
- Benchmarks for hot paths with documented baselines.
- CI runtime budget respected; no flaky tests in main.

## Named Patterns

### Good — Table-driven test
```go
func TestParse(t *testing.T) {
    tests := []struct {
        name    string
        in      string
        want    Order
        wantErr error
    }{
        {"empty", "", Order{}, ErrEmpty},
        {"valid", `{"id":"a"}`, Order{ID: "a"}, nil},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := Parse(tt.in)
            if !errors.Is(err, tt.wantErr) {
                t.Fatalf("err = %v, want %v", err, tt.wantErr)
            }
            if got != tt.want {
                t.Errorf("got %+v, want %+v", got, tt.want)
            }
        })
    }
}
```

### Bad — Sequential assertions in one `Test*` function
A 200-line function that exercises 12 scenarios. One failure aborts the rest. Adding a case means scrolling and copy-pasting.

### Good — Fake over mock for behavior checks
```go
type fakeRepo struct {
    orders map[string]Order
}
func (f *fakeRepo) Get(_ context.Context, id string) (Order, error) {
    o, ok := f.orders[id]
    if !ok { return Order{}, ErrNotFound }
    return o, nil
}
```
Tests assert on state via the fake; no `EXPECT().Get(...).Return(...)` ceremony.

### Bad — Mock for trivial behavior
```go
m := NewMockRepo(ctrl)
m.EXPECT().Get(gomock.Any(), "a").Return(Order{ID: "a"}, nil)
m.EXPECT().Save(gomock.Any(), gomock.Any()).Return(nil)
// ...
```
Brittle, hard to read, couples the test to call order.

### Good — Integration with testcontainers
```go
func TestMain(m *testing.M) {
    ctx := context.Background()
    pg, _ := postgres.Run(ctx, "postgres:16-alpine",
        postgres.WithDatabase("test"),
        postgres.WithUsername("test"),
        postgres.WithPassword("test"),
    )
    defer pg.Terminate(ctx)
    dsn, _ := pg.ConnectionString(ctx, "sslmode=disable")
    os.Setenv("DB_DSN", dsn)
    os.Exit(m.Run())
}
```
Real Postgres, lifecycle-managed by the test binary.

### Bad — Shared dev database
Tests connect to a shared `dev` DB. Parallel runs collide. Flakes blamed on "the network".

### Good — Deterministic time
```go
type Clock interface { Now() time.Time }
type realClock struct{}
func (realClock) Now() time.Time { return time.Now() }

type fakeClock struct{ t time.Time }
func (f *fakeClock) Now() time.Time { return f.t }
```
Tests inject `fakeClock`; production injects `realClock`.

### Bad — `time.Sleep` in tests
`time.Sleep(100*time.Millisecond)` to "wait for the goroutine". Flakes on slow CI; wastes time on fast CI.

### Good — Benchmark with allocations
```go
func BenchmarkParse(b *testing.B) {
    b.ReportAllocs()
    in := load("testdata/large.json")
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        _, _ = Parse(in)
    }
}
```
Optimize against the benchmark, not against a feeling.

### Bad — Optimize without baseline
"This loop looks slow" → rewrite → no measurement before or after. Sometimes faster, sometimes slower, no one can tell.

## Boundaries

- Owns service-level Go test design.
- Does not own QA strategy or release regression — that is `qa-engineer`.
- Does not own CI runners and platform-level test infrastructure — that is `devops-sre`.

## Sources

### Priority 1 — Go canon
- `testing` package — https://pkg.go.dev/testing
- Go blog: subtests and sub-benchmarks — https://go.dev/blog/subtests
- Go blog: fuzzing — https://go.dev/security/fuzz/
- Effective Go: testing — https://go.dev/doc/effective_go

### Priority 2 — Tooling
- testcontainers-go — https://golang.testcontainers.org/
- gomock — https://github.com/uber-go/mock
- mockery — https://github.com/vektra/mockery
- `pprof` — https://pkg.go.dev/runtime/pprof

### Priority 3 — Background
- Google Testing on the Toilet (test pyramid) — https://testing.googleblog.com/
- Martin Fowler: Test Pyramid — https://martinfowler.com/articles/practical-test-pyramid.html

## Handoff

- QA strategy, release regression, exploratory testing → `qa-engineer`.
- CI runners, test parallelism at platform level → `devops-sre`.
- Concurrency-specific test design → `go-concurrency-and-context`.
- Contract testing against API schema → `api-contract-design`.
