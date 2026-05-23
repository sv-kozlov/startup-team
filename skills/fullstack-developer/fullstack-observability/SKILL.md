---
name: fullstack-observability
description: Use when adding or improving observability across both ends of a fullstack feature — Web Vitals (LCP, CLS, INP) and JavaScript error tracking on the frontend, structured logs and OpenTelemetry traces on the backend, and a single request/trace ID flowing through the full stack. Covers SLI definition at the feature level and the signal-to-noise discipline on both ends.
family: method
profile_level: Senior+
---

# Fullstack Observability

## Purpose

Make the feature answerable from production on both ends: the browser signals a slow interaction, the trace finds the slow query, and both are linked by the same request ID. Stop log noise and undefined metrics at the feature boundary.

## Use When

- Launching a new feature and defining what to measure on both ends.
- Diagnosing a production issue where "the logs don't show what happened on the client".
- Adding request ID propagation so frontend and backend logs can be correlated.
- Defining the SLI for a feature path: which latency and error rate targets matter to users?
- Reviewing observability coverage in a PR: are UI error states tracked? Are backend errors structured?

## Do Not Use When

- The discussion is the alerting/paging routing layer → `devops-sre`.
- The discussion is the observability platform choice (which APM vendor, which log aggregation) → `system-architect` / `tech-lead`.
- The discussion is data lake or BI analytics on event data → `product-analyst` / `data-engineer`.
- The discussion is backend-only observability without any frontend signal → `service-observability` (backend specialist skill).

## Inputs

- Feature's critical user paths and their business value.
- Existing frontend error tracking setup (Sentry or equivalent) and backend OTel configuration.
- Current Web Vitals baseline from Lighthouse or CrUX.
- Known incidents where data was missing.

## Workflow

1. Define the SLI for the feature: which user action has a latency and an error rate that users notice? Define one or two, not ten.
2. Set the SLO targets from business intent: "checkout completes in < 2s at p95 for 99% of users". Derive an error budget.
3. Add a request ID to every HTTP request from the frontend. Propagate it as a response header. Include it in every backend log line.
4. Instrument the backend with OpenTelemetry spans on: inbound handler, outbound API calls, database queries on the critical path. Attach request ID as a span attribute.
5. Configure frontend error tracking (Sentry) to capture unhandled errors, rejected promises, and React error boundaries — with the request ID in the context.
6. Track Web Vitals (LCP, CLS, INP) for the feature's key pages. Report to your analytics backend. Use a performance budget: alert when LCP > 2.5s.
7. Define log levels for the feature: ERROR for actionable failures, WARN for recovered degradation, INFO for state transitions, DEBUG off in production.
8. Document where each signal lives (dashboard, log query, trace view) and who owns it.

## Outputs

- SLO document: SLI, target, window, error budget, burn policy.
- Request ID propagation from frontend HTTP headers to backend trace spans.
- OpenTelemetry spans on critical backend paths with semantic attributes.
- Web Vitals measurement for the feature's key pages with a budget.
- Sentry (or equivalent) capturing frontend errors with request context.
- Log level convention for the feature.

## Named Patterns

### Good — Request ID from frontend to backend log
```typescript
// Frontend: attach a request ID to every fetch
const requestId = crypto.randomUUID();
const res = await fetch('/v1/orders', {
  headers: { 'X-Request-Id': requestId },
});

// Backend (Express middleware): read and forward
app.use((req, res, next) => {
  const reqId = req.headers['x-request-id'] ?? crypto.randomUUID();
  res.setHeader('X-Request-Id', reqId);
  req.locals.requestId = reqId;
  next();
});

// Backend structured log
logger.info('order placed', {
  requestId: req.locals.requestId,
  orderId: order.id,
  durationMs: Date.now() - start,
});
```
User reports an error. Support team reads `X-Request-Id` from the browser. Finds the log line instantly.

### Bad — No correlation between client and server
Frontend logs `"Request failed"`. Backend logs `"Order placed"` and `"Validation error"`. Support team searches logs by time window and approximate user ID. Finds nothing.

### Good — OpenTelemetry span on critical path
```typescript
import { trace, SpanStatusCode } from '@opentelemetry/api';

const tracer = trace.getTracer('order-service');

const placeOrder = async (input: PlaceOrderInput): Promise<Order> => {
  const span = tracer.startSpan('OrderService.place', {
    attributes: {
      'order.user_id': input.userId,
      'request.id': input.requestId,
    },
  });
  try {
    const order = await orderRepo.save(input);
    span.setStatus({ code: SpanStatusCode.OK });
    return order;
  } catch (err) {
    span.recordException(err as Error);
    span.setStatus({ code: SpanStatusCode.ERROR });
    throw err;
  } finally {
    span.end();
  }
};
```
Trace shows exactly where time is spent. Error is recorded on the span — visible in the trace viewer.

### Bad — Untraced critical path
`placeOrder` takes 3 seconds in production. Nobody knows if it's the database, the outbox, or the downstream payment call. There are no spans to look at.

### Good — Web Vitals with performance budget
```typescript
// Next.js: report Web Vitals to your analytics
export function reportWebVitals({ id, name, value }: NextWebVitalsMetric) {
  analytics.track('web_vitals', {
    metric: name,     // LCP, CLS, INP, FCP, TTFB
    value: Math.round(name === 'CLS' ? value * 1000 : value),
    id,
    page: window.location.pathname,
  });
}

// Performance budget (Lighthouse CI)
// .lighthouserc.json
{
  "ci": {
    "assert": {
      "assertions": {
        "largest-contentful-paint": ["warn", { "maxNumericValue": 2500 }],
        "cumulative-layout-shift": ["error", { "maxNumericValue": 0.1 }]
      }
    }
  }
}
```
Automated budget enforcement. LCP regression fails CI before it reaches users.

### Bad — "We'll check vitals after launch"
The feature ships. After two weeks, a data analyst notices bounce rate doubled on the checkout page. LCP is 7 seconds. The root cause was a blocking third-party script nobody tracked.

### Good — Sentry with request context
```typescript
// Frontend: set request ID on every Sentry error
import * as Sentry from '@sentry/react';

const fetchWithTracking = async (url: string, init: RequestInit = {}) => {
  const requestId = crypto.randomUUID();
  Sentry.setContext('request', { requestId });
  const res = await fetch(url, {
    ...init,
    headers: { ...init.headers, 'X-Request-Id': requestId },
  });
  if (!res.ok) {
    Sentry.captureMessage(`API error ${res.status}`, { extra: { requestId, url } });
  }
  return res;
};
```
Every Sentry error has a `requestId` that links to the backend trace.

### Bad — Generic error tracking
```typescript
window.onerror = (msg) => Sentry.captureMessage(String(msg));
// No URL, no request ID, no component context. Sentry inbox fills with "Script error."
```

## Boundaries

- Owns feature-level signals: SLI/SLO definition, request ID propagation, frontend error tracking, backend OTel spans, Web Vitals budget.
- Does not own the alerting/paging routing layer → `devops-sre`.
- Does not own the observability platform choice (APM vendor, log aggregation) → `system-architect` / `tech-lead`.
- Does not own organization-wide SLO governance → `devops-sre` / `tech-lead`.
- Does not own BI/analytics dashboards on user behavior → `product-analyst`.

## Sources

### Priority 1 — Standards
- Web Vitals — https://web.dev/vitals/
- OpenTelemetry Specification — https://opentelemetry.io/docs/specs/otel/
- OpenTelemetry Semantic Conventions — https://opentelemetry.io/docs/specs/semconv/
- Sentry Documentation — https://docs.sentry.io/

### Priority 2 — Reliability practice
- Google SRE Book — https://sre.google/sre-book/table-of-contents/
- Google SRE Workbook — https://sre.google/workbook/table-of-contents/
- Lighthouse Performance Auditing — https://developer.chrome.com/docs/lighthouse/

### Priority 3 — Background
- Honeycomb engineering blog — https://www.honeycomb.io/blog/
- web.dev — https://web.dev/

## Handoff

- Alerting, paging, incident response → `devops-sre`.
- Observability platform choice across the organization → `system-architect` / `tech-lead`.
- BI analytics and product metrics dashboards → `product-analyst`.
- Deep backend error classification and structured log design → `backend-go-developer` / `python-developer`.
