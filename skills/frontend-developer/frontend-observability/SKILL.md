---
name: frontend-observability
description: Use when setting up or improving client-side error monitoring, adding error boundaries with structured metadata, instrumenting critical user paths with Real User Monitoring (RUM), or creating custom spans for frontend performance tracing. Covers Sentry integration, error context enrichment, RUM setup, and the principle of separating signal from noise in frontend error streams.
family: method
profile_level: Senior+
---

# Frontend Observability

## Purpose

Make the frontend's health measurable and its failures diagnosable without requiring reproduction. Every client-side error that reaches a user should be captured with enough context to reproduce and fix it; every critical user path should have a latency signal so regressions are detected before users report them.

## Use When

- Setting up client-side error monitoring for the first time (Sentry, Datadog RUM, or equivalent).
- Adding error boundaries with structured metadata to a feature or page.
- Instrumenting a critical user journey (checkout, onboarding, form submission) with RUM or custom spans.
- Reviewing error monitoring configuration that produces too much noise (unhandled promise rejections from browser extensions, irrelevant third-party errors).
- Configuring source maps for readable production error stacks.

## Do Not Use When

- The task is server-side observability (traces, metrics, SLO) → `backend-go-developer` / `devops-sre`.
- The task is frontend performance optimization (bundle, LCP) → `web-performance-and-bundling`.
- The task is e2e test coverage of user flows → `frontend-testing`.

## Inputs

- Monitoring platform (Sentry, Datadog RUM, New Relic, or custom).
- Source map pipeline (built and uploaded to the monitoring platform).
- List of critical user journeys to instrument.
- Current noise level in the error stream: what percentage of events is actionable.

## Workflow

1. **Source maps first.** Without source maps, production errors show minified call stacks. Configure the build to upload source maps to the monitoring platform at deploy time. Keep source map files off the public CDN.

2. **Error boundary hierarchy.** Add an error boundary at the application root as a last resort. Add feature-level boundaries at each major route or isolated UI region. Each boundary captures the error with:
   - Component name or boundary identifier.
   - Current URL and user action context.
   - Relevant state snapshot (sanitized of PII).

3. **Sentry/RUM initialization.** Configure:
   - `tracesSampleRate` and `replaysSessionSampleRate` at production-safe levels (do not send 100% of traces in high-traffic apps).
   - `ignoreErrors` list: filter known browser extension errors, network errors from third-party scripts, and cancelled requests.
   - `beforeSend` hook: strip PII from error breadcrumbs and events before they leave the browser.

4. **Enrich error context.** Set user context (non-PII identifier, role), release version, and environment on initialization. Set feature context in error boundaries so the platform groups errors by feature, not only by component name.

5. **Custom performance spans for critical paths.** For each critical user journey (login, checkout, form submission):
   - Start a transaction or span at the user action trigger.
   - Add child spans for API calls, heavy computations, or animations.
   - Finish the transaction on success or failure with a clear outcome label.
   - Set a latency budget; alert when p95 exceeds the budget.

6. **Signal-to-noise discipline.** Review the error stream weekly for the first month after setup. Errors that fire on every page load without being user-visible belong in `ignoreErrors`. Errors that appear frequently with the same stack but cannot be fixed immediately get a suppression comment and a linked ticket — not silence without tracking.

## Outputs

- Sentry (or equivalent) initialized with environment, release, user context, sample rates, and `beforeSend` PII filter.
- Error boundaries at app and feature level with structured metadata capture.
- Source maps uploaded to monitoring platform at each deploy.
- Custom transaction/span instrumentation for ≥3 critical user journeys.
- Alert rules on error rate threshold and p95 latency for critical paths.
- `ignoreErrors` list with documented rationale per suppressed pattern.

## Named Patterns

### Good — Error boundary with structured metadata
```tsx
import * as Sentry from '@sentry/react';

export function OrdersFeature() {
  return (
    <Sentry.ErrorBoundary
      fallback={({ error, resetError }) => (
        <FeatureErrorFallback error={error} onRetry={resetError} />
      )}
      beforeCapture={(scope) => {
        scope.setTag('feature', 'orders');
        scope.setContext('page', { url: window.location.href });
      }}
    >
      <OrderList />
    </Sentry.ErrorBoundary>
  );
}
```
Every error from the Orders feature is tagged and grouped separately in the monitoring platform.

### Bad — Global error boundary without context
```tsx
<ErrorBoundary fallback={<GenericError />}>
  <App />
</ErrorBoundary>
// All errors from all features arrive as a single unnamed group
```

### Good — Custom performance transaction
```ts
import * as Sentry from '@sentry/react';

async function handleCheckout(cart: Cart) {
  const transaction = Sentry.startTransaction({ name: 'checkout.submit' });
  Sentry.getCurrentHub().configureScope(s => s.setSpan(transaction));

  try {
    const apiSpan = transaction.startChild({ op: 'http', description: 'POST /orders' });
    const order = await ordersApi.create(cart);
    apiSpan.finish();

    transaction.setStatus('ok');
    return order;
  } catch (err) {
    transaction.setStatus('internal_error');
    throw err;
  } finally {
    transaction.finish();
  }
}
```
Checkout latency is measured end-to-end; p95 regressions are detectable.

### Bad — No performance instrumentation on critical paths
```ts
async function handleCheckout(cart: Cart) {
  return ordersApi.create(cart); // no timing; regressions invisible until user complaints
}
```

### Good — Filtered initialization
```ts
Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  release: process.env.APP_VERSION,
  tracesSampleRate: 0.1,        // 10% of sessions
  ignoreErrors: [
    /ResizeObserver loop limit/,
    /Non-Error exception captured/,
    /ChunkLoadError/,            // handled by reload logic separately
  ],
  beforeSend(event) {
    // Strip email from breadcrumbs
    event.breadcrumbs?.values?.forEach(b => {
      if (b.data?.email) b.data.email = '[filtered]';
    });
    return event;
  },
});
```

### Bad — 100% trace rate without PII filtering
```ts
Sentry.init({ dsn: '…', tracesSampleRate: 1.0 });
// High volume, high cost; user PII in breadcrumbs; noise drowns signal
```

## Boundaries

- Owns client-side error capture, context enrichment, RUM, and critical path instrumentation.
- Does not own server-side traces, metrics, or SLO → `backend-go-developer` / `devops-sre`.
- Does not own monitoring infrastructure setup or alerting routing → `devops-sre`.
- Does not own error handling UX (what the user sees) → `api-integration-frontend`.

## Sources

### Priority 1 — Observability tooling
- Sentry React docs — https://docs.sentry.io/platforms/javascript/guides/react/
- MDN: Performance API — https://developer.mozilla.org/en-US/docs/Web/API/Performance_API
- Web Vitals (RUM) — https://web.dev/vitals/

### Priority 2 — Orientation
- OpenTelemetry JS — https://opentelemetry.io/docs/languages/js/
- Google web.dev: Measure performance — https://web.dev/measure/

### Priority 3 — Pattern background
- martinfowler.com: Observability — https://martinfowler.com/

## Handoff

- Server-side traces and backend SLO → `backend-go-developer` / `devops-sre`.
- Monitoring infrastructure and alerting rules → `devops-sre`.
- Error handling UI (fallbacks, retry buttons) → `api-integration-frontend`.
- Performance measurement and optimization → `web-performance-and-bundling`.
