---
name: service-observability
description: Use when laying in or improving observability of a Python service — structured logging via structlog, OpenTelemetry tracing with the Python SDK, Prometheus metrics via prometheus-client, correlation ID propagation via contextvars, and SLO/SLI definition on service paths.
family: method
profile_level: Senior+
---

# Service Observability

## Purpose

Make a Python service diagnosable in production without a debugger. Ensure every request leaves a trace, every error leaves a searchable log event, and every SLO-relevant path has a RED metric. Prevent cardinality explosions that crash the metrics backend.

## Use When

- A new Python service has no structured logs or metrics.
- An incident reveals missing trace context or unstructured log noise.
- Adding a new critical path that needs an SLI.
- Reviewing observability coverage before a production rollout.

## Do Not Use When

- The task is alerting rules or Grafana dashboards → handoff to `devops-sre`.
- The task is performance profiling for optimization → `python-testing` / `python-async-and-concurrency`.
- The task is API contract error shapes → `api-contract-design`.

## Inputs

- Service's critical user paths (from system analyst spec or product brief).
- Agreed log aggregation backend (ELK, Loki, Cloud Logging).
- Prometheus scrape endpoint requirement.
- SLO targets (e.g., p99 < 200 ms, error rate < 0.1%).

## Workflow

1. Add structured logging: configure `structlog` with JSON renderer for production, console renderer for local. Bind `request_id` (correlation ID) to context at the request entry point.
2. Propagate correlation ID via `contextvars.ContextVar`: set at middleware level; read by all downstream logger calls without explicit passing.
3. Add OpenTelemetry tracing: `opentelemetry-sdk`, `opentelemetry-instrumentation-fastapi` (or aiohttp), `opentelemetry-exporter-otlp`. Instrument DB calls with `opentelemetry-instrumentation-sqlalchemy`.
4. Instrument Prometheus metrics at `app/metrics.py`: one `Counter` for total requests and errors, one `Histogram` for response duration. Use labels: `endpoint`, `method`, `status_code`. Never use user IDs or request IDs as label values.
5. Define SLI per critical path: `error_rate = errors / total`, `latency_p99 = histogram_quantile(0.99, ...)`. Set SLO threshold and alerting rule in collaboration with `devops-sre`.
6. Expose `/metrics` endpoint with `prometheus-client`; expose `/health/live` and `/health/ready` probes.
7. Log at the right level: DEBUG for internal state, INFO for business events (`order_placed`, `payment_charged`), WARNING for recoverable issues, ERROR for exceptions that reach the boundary.

## Outputs

- `structlog` configuration in `app/logging.py`.
- Prometheus metric definitions in `app/metrics.py`.
- OpenTelemetry setup in `app/telemetry.py`.
- `/metrics`, `/health/live`, `/health/ready` endpoints.
- SLI/SLO definitions and alerting rules (handed off to `devops-sre`).

## Named Patterns

### Good — structlog with contextvars correlation ID
```python
# app/logging.py
import structlog
import logging
from contextvars import ContextVar

request_id_ctx: ContextVar[str] = ContextVar("request_id", default="")

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

# FastAPI middleware
@app.middleware("http")
async def set_request_id(request: Request, call_next):
    rid = request.headers.get("X-Request-Id", str(uuid4()))
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(request_id=rid)
    response = await call_next(request)
    response.headers["X-Request-Id"] = rid
    return response
```
Every log line in a request automatically carries `request_id`; no explicit passing needed.

### Bad — Unstructured logging with print or string interpolation
```python
import logging
logger = logging.getLogger(__name__)

async def place_order(order_id):
    logger.info(f"Processing order {order_id}")  # string, not structured
    print(f"DEBUG: order {order_id}")             # ungreppable in production
```
Cannot filter by `order_id` in log aggregator; correlation is manual.

### Good — Prometheus RED metrics with bounded cardinality
```python
# app/metrics.py
from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"],
)
REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration",
    ["method", "endpoint"],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5],
)

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    # Normalize path to avoid cardinality explosion
    endpoint = request.scope.get("path", "unknown")
    method = request.method
    with REQUEST_DURATION.labels(method=method, endpoint=endpoint).time():
        response = await call_next(request)
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, status_code=response.status_code).inc()
    return response
```
Labels are bounded; `endpoint` uses the route pattern, not the actual URL.

### Bad — User ID as metric label
```python
REQUEST_COUNT = Counter("requests", "Requests", ["user_id"])  # unbounded!
REQUEST_COUNT.labels(user_id=current_user.id).inc()
```
One label value per user; millions of label combinations; Prometheus memory explodes.

### Good — OpenTelemetry trace with custom span attributes
```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

async def place_order(cmd: PlaceOrderCommand) -> OrderID:
    with tracer.start_as_current_span("place_order") as span:
        span.set_attribute("order.currency", cmd.currency)
        span.set_attribute("order.item_count", len(cmd.items))
        order = Order.create(cmd.items)
        await repo.save(order)
        span.set_attribute("order.id", str(order.id))
        return order.id
```
Span carries business context; correlated with logs via `request_id`; visible in Jaeger/Tempo.

### Bad — No span context, only log-level tracing
```python
async def place_order(cmd):
    logger.info("place_order called")
    ...
    logger.info("place_order done")
```
No distributed trace; impossible to correlate across service boundaries; no duration measurement.

## Boundaries

- Owns service-level observability: logs, metrics, traces, health probes.
- Does not own alerting rules, Grafana dashboards, or on-call rotation → `devops-sre`.
- Does not own API error shapes (HTTP status mapping) → `api-contract-design`.
- Does not own performance profiling for code optimization → `python-testing`.

## Sources

### Priority 1 — Observability canon
- OpenTelemetry Python SDK — https://opentelemetry-python.readthedocs.io/
- OpenTelemetry Semantic Conventions — https://opentelemetry.io/docs/specs/semconv/
- prometheus-client (Python) — https://github.com/prometheus/client_python
- structlog documentation — https://www.structlog.org/
- FastAPI middleware — https://fastapi.tiangolo.com/tutorial/middleware/

### Priority 2 — SRE and metrics practice
- Google SRE Book — https://sre.google/sre-book/table-of-contents/
- Prometheus Best Practices — https://prometheus.io/docs/practices/
- OpenTelemetry Specification — https://opentelemetry.io/docs/specs/otel/

### Priority 3 — Background
- martinfowler.com on observability — https://martinfowler.com/articles/domain-oriented-observability.html

## Handoff

- Alerting rules, dashboards, on-call → `devops-sre`.
- API error shapes and HTTP status mapping → `api-contract-design`.
- Performance profiling and optimization → `python-async-and-concurrency`.
