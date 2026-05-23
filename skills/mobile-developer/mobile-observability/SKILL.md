---
name: mobile-observability
description: Use when connecting crash analytics (Firebase Crashlytics, Sentry), setting up ANR and performance monitoring, designing an analytics event schema, instrumenting A/B experiments, or building crash-free and performance dashboards for a mobile application.
family: method
profile_level: Senior+
---

# Mobile Observability

## Purpose

Make the mobile application's health visible in production: who crashes, how often, on which devices, and under which conditions. Define and instrument analytics events so product, data, and engineering share a single source of truth about user behavior. Connect crash data and performance metrics before the first public release, not after.

## Use When

- Connecting Crashlytics, Sentry, or another crash SDK to a new or existing application.
- Designing an analytics event taxonomy: event names, properties, and naming conventions.
- Instrumenting an A/B experiment: control vs variant assignment, conversion event, guardrail metric.
- Building a crash-free rate dashboard or setting alert thresholds.
- Investigating a production crash from a symbolicated stack trace.
- Reviewing analytics event quality: missing events, duplicate fires, wrong properties.

## Do Not Use When

- The task is about server-side observability (logs, metrics, tracing) → handoff to `backend-developers` / `devops-sre`.
- The task is about experiment design and statistical analysis → handoff to `product-analyst`.
- The task is about app performance profiling (startup, memory, battery) → `mobile-performance-and-resources`.
- The task is about release pipeline → `mobile-release-and-distribution`.

## Inputs

- Crash SDK credentials (Crashlytics project, Sentry DSN).
- Analytics schema requirements from product-analyst or product-manager.
- Existing event naming conventions or analytics system (Amplitude, Segment, custom).
- A/B framework in use: Firebase A/B Testing, LaunchDarkly, Optimizely.

## Workflow

1. **Integrate crash SDK**: add Crashlytics or Sentry to the build. Verify that symbolication is configured (upload dSYMs for iOS; R8 mapping file for Android). Confirm a test crash appears in the dashboard before merging.
2. **Set crash-free rate baseline**: record the crash-free rate for the current version before the release. Define a pausing threshold (e.g., crash-free rate drops by > 0.5 pp triggers a release pause).
3. **Design the event taxonomy**: agree on naming conventions before instrumentation (noun_verb: `checkout_started`, `payment_completed`). Define required properties per event (user_id, session_id, platform, app_version). Document in a schema registry.
4. **Instrument events**: fire events at the boundary of a user action or a state transition, not in UI callbacks deep inside rendering. Each event fires exactly once per action; use a deduplication key if needed.
5. **Instrument experiments**: log an `experiment_viewed` event with `experiment_id` and `variant` when the user is assigned. Log the conversion event. Verify both fire in the expected order before launching the experiment.
6. **ANR and performance**: configure Firebase Performance custom traces for critical paths (checkout, image load). Set alerts for p75 and p95 exceeding thresholds. Review ANR traces in Play Console.
7. **Dashboard and alerting**: build a crash-free rate + ANR rate widget per version. Set PagerDuty / Slack alerts on threshold breach. Review after each staged rollout step.

## Outputs

- Integrated crash SDK with symbolication verified.
- Analytics event schema document (event name, required properties, trigger condition).
- A/B instrumentation with experiment_viewed + conversion events.
- Performance monitoring traces for critical paths.
- Crash-free rate dashboard with alert thresholds.

## Named Patterns

### Good — Crash SDK with user context (no PII)
```kotlin
// Android: set non-PII context before any crash-prone code
FirebaseCrashlytics.getInstance().apply {
    setUserId(user.anonymizedId)         // hashed; no email/phone
    setCustomKey("app_version", BuildConfig.VERSION_NAME)
    setCustomKey("experiment_variant", featureFlags.checkoutVariant)
}
```

### Bad — PII in crash logs
```kotlin
Crashlytics.setCustomKey("user_email", user.email)  // GDPR violation; App Store rejection risk
Crashlytics.log("User ${user.fullName} triggered checkout") // PII in crash log
```

### Good — Event naming convention (noun_verb)
```kotlin
// Consistent naming: <screen>_<action> or <entity>_<state>
analytics.track("checkout_started", mapOf(
    "cart_value" to cart.total,
    "item_count" to cart.items.size,
    "payment_method" to paymentMethod.type,
    "experiment_variant" to featureFlags.checkoutVariant
))
```

### Bad — Event fired in UI render
```kotlin
@Composable
fun CheckoutScreen(state: CheckoutUiState) {
    // Anti-pattern: analytics fired during composition; fires on every recomposition
    analytics.track("checkout_viewed")
    // ...
}
```
Fire once per navigation event, not per recomposition. Use `LaunchedEffect(Unit)` or fire in ViewModel.

### Good — A/B experiment instrumentation
```kotlin
class CheckoutViewModel(
    private val analytics: Analytics,
    private val flags: FeatureFlagService
) : ViewModel() {

    private val variant = flags.getString("checkout_v2", default = "control")

    fun onScreenVisible() {
        analytics.track("experiment_viewed", mapOf(
            "experiment_id" to "checkout_v2",
            "variant" to variant
        ))
    }

    fun onPaymentCompleted(orderId: String) {
        analytics.track("payment_completed", mapOf(
            "order_id" to orderId,
            "experiment_id" to "checkout_v2",
            "variant" to variant
        ))
    }
}
```

### Bad — Conversion event without experiment context
```kotlin
analytics.track("payment_completed", mapOf("order_id" to orderId))
// experiment_id and variant missing → cannot attribute conversion to the experiment
```

## Boundaries

- Owns client-side crash analytics, performance monitoring, and analytics event instrumentation.
- Does not own server-side observability (logs, metrics, tracing) → `backend-developers` / `devops-sre`.
- Does not own experiment design and statistical significance analysis → `product-analyst`.
- Does not own release rollout decision → `mobile-release-and-distribution`.

## Sources

### Priority 1 — Platform canon
- Firebase Crashlytics — https://firebase.google.com/docs/crashlytics
- Firebase Performance Monitoring — https://firebase.google.com/docs/perf-mon
- Firebase Analytics — https://firebase.google.com/docs/analytics
- Sentry for Android — https://docs.sentry.io/platforms/android/
- Sentry for iOS — https://docs.sentry.io/platforms/apple/

### Priority 2 — Standards and policies
- App Store Review Guidelines (privacy) — https://developer.apple.com/app-store/review/guidelines/#privacy
- Google Play data safety — https://support.google.com/googleplay/android-developer/answer/10787469
- OWASP MASVS — https://mas.owasp.org/MASVS/

### Priority 3 — Community
- Segment analytics spec — https://segment.com/docs/connections/spec/
- ThoughtWorks Technology Radar — https://www.thoughtworks.com/radar

## Handoff

- Server-side observability and alerting → `backend-developers` / `devops-sre`.
- Experiment design and statistical analysis → `product-analyst`.
- Release rollout decisions based on crash data → `mobile-release-and-distribution`.
- Performance profiling root cause → `mobile-performance-and-resources`.
