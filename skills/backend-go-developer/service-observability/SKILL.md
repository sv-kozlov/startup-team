---
name: service-observability
description: Use when laying in or improving observability of a Go service — structured logs, OpenTelemetry tracing, Prometheus metrics, SLO/SLI/error budget on service paths. Covers cardinality control, log levels, trace propagation, and signal-to-noise discipline.
family: method
profile_level: Senior+
---

# Service Observability

## Purpose

Make the service answerable from production: every signal earns its place, cardinality is a budget, and SLOs are reasoned about rather than declared. Stop log-noise and metric-bloat at the service boundary.

## Use When

- Starting observability on a new service or hardening an existing one.
- Diagnosing a production incident that "the logs don't show".
- Defining or reviewing SLO/SLI for a service path.
- Adding metrics or trace spans during code review.

## Do Not Use When

- The discussion is the alerting/paging routing layer → handoff to `devops-sre`.
- The discussion is data lake/warehouse analytics on logs → handoff to `data-engineer`.
- The discussion is error type design → `go-error-handling`.

## Inputs

- Service paths and their business criticality.
- Existing logging library, metric backend, tracing backend.
- Known incidents and what data was missing.
- NFR targets: latency p95/p99, availability, error rate.

## Workflow

1. Define the SLI per critical path: availability, latency, correctness. Pick one or two, not all.
2. Set SLO targets that reflect business intent, not technical reach. Derive an error budget. Decide what the team does when the budget burns.
3. Choose log levels with intent: `ERROR` for actionable failures, `WARN` for degraded but recovered, `INFO` for state transitions, `DEBUG` off in prod.
4. Make logs structured (JSON or logfmt). Every log has request ID and trace ID; every business log has the aggregate ID.
5. Instrument with OpenTelemetry: spans on inbound handlers, outbound clients, broker producers/consumers, and meaningful business operations. Follow semantic conventions.
6. Metrics with controlled cardinality. Label budget: per metric, ≤10 stable labels; never user ID, never request path with IDs.
7. Use the RED method (Rate, Errors, Duration) for service paths; USE (Utilization, Saturation, Errors) for resources.
8. Cross-reference signals: log → trace ID → trace → spans → exemplar on metric.
9. Document where each signal lives, what it answers, and who owns the dashboard.

## Outputs

- SLO document with SLI, target, window, error budget, burn policy.
- Logging conventions and example.
- Metric catalogue with name, labels, cardinality budget, owner.
- Trace coverage map.
- Dashboards as code (Grafana JSON, etc.) under version control.

## Named Patterns

### Good — Structured log with trace correlation
```go
logger.InfoContext(ctx, "order created",
    slog.String("order_id", o.ID),
    slog.String("user_id", o.UserID),
    slog.Int64("amount_cents", o.AmountCents),
)
```
With an OTel-aware handler the trace and span ID land on the line automatically. Logs and traces are linkable.

### Bad — Stringly-typed log
```go
log.Printf("order %s created for user %s at amount %d", o.ID, o.UserID, o.AmountCents)
```
Not parseable. Cannot filter by `order_id` in Kibana. Cannot link to a trace.

### Good — RED metric with bounded labels
```go
reqDuration := promauto.NewHistogramVec(
    prometheus.HistogramOpts{
        Name: "http_request_duration_seconds",
        Buckets: prometheus.DefBuckets,
    },
    []string{"method", "route", "status_class"}, // 3 stable labels
)
```
`route` is the routing pattern (`/orders/:id`), not the URL with IDs. `status_class` is `2xx`/`4xx`/`5xx`, not every code.

### Bad — Unbounded label cardinality
```go
metric.WithLabelValues(r.URL.Path, userID, requestID).Inc()
```
Each user ID and request ID becomes a separate time series. Prometheus chokes. The dashboard goes blank.

### Good — Span with semantic attributes
```go
ctx, span := tracer.Start(ctx, "OrderService.Create",
    trace.WithAttributes(
        attribute.String("order.id", o.ID),
        attribute.Int64("order.amount_cents", o.AmountCents),
    ),
)
defer span.End()
if err != nil {
    span.RecordError(err)
    span.SetStatus(codes.Error, err.Error())
}
```
Attributes follow OTel semantic conventions where they exist.

### Bad — Trace without context propagation
The HTTP client used by the service does not inject the trace context header. Downstream spans live in a separate trace. The trace tree is broken.

### Good — SLO with error budget policy
- SLI: `availability = 1 - errors_5xx / requests` over 30 days.
- SLO: 99.5%.
- Error budget: 0.5% × monthly request count.
- Burn policy: when 50% of the budget is gone before week 3, the team freezes feature work and prioritizes reliability.

### Bad — "Five nines" by aspiration
The team writes "99.999%" in the README. No measurement, no budget, no policy. When incidents happen, "we'll do better".

### Good — Log level discipline
- `ERROR`: actionable failure; on-call should care.
- `WARN`: degraded but recovered (retry succeeded, fallback used).
- `INFO`: state transition (order placed, batch finished).
- `DEBUG`: off in prod, on in dev/sample.

### Bad — Everything is `INFO`
Or everything is `ERROR`. The level conveys no meaning; alerts are tuned by message content.

### Good — Sampling tail-based for traces
Head-based for performance, tail-based for "keep traces with errors or high latency". Sampler config lives next to the SLO.

### Bad — 100% trace sampling at scale
Storage costs explode; traces are kept for a day; debugging an incident from yesterday is impossible.

## Boundaries

- Owns service-level signals and SLO/SLI design for the service.
- Does not own the alerting/paging routing layer or platform telemetry pipeline → `devops-sre`.
- Does not own organization-wide observability platform choice → `system-architect` / `tech-lead`.

## Sources

### Priority 1 — Standards
- OpenTelemetry Specification — https://opentelemetry.io/docs/specs/otel/
- OpenTelemetry Semantic Conventions — https://opentelemetry.io/docs/specs/semconv/
- Prometheus Best Practices — https://prometheus.io/docs/practices/
- `log/slog` — https://pkg.go.dev/log/slog

### Priority 2 — Reliability practice
- Google SRE Book — https://sre.google/sre-book/table-of-contents/
- Google SRE Workbook — https://sre.google/workbook/table-of-contents/
- The RED method (Tom Wilkie) — https://thenewstack.io/monitoring-microservices-red-method/
- The USE method (Brendan Gregg) — https://www.brendangregg.com/usemethod.html

### Priority 3 — Background
- Honeycomb engineering blog — https://www.honeycomb.io/blog/
- Charity Majors writings on observability — https://charity.wtf/

## Handoff

- Alert routing, paging, incident response → `devops-sre`.
- Cross-service observability platform decisions → `system-architect` / `tech-lead`.
- Log analytics for product/business questions → `product-analyst` / `data-engineer`.
- Error type and classification → `go-error-handling`.
