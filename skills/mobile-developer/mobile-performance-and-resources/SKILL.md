---
name: mobile-performance-and-resources
description: Use when investigating or improving mobile application startup time, frame rate (jank/ANR), memory consumption (heap, Bitmap leaks), battery drain (wake locks, GPS, BLE usage), or download size (R8/thinning/AAB splits). Covers profiling tools (Android Studio Profiler, Instruments) and named decision points for optimizing constrained mobile hardware.
family: method
profile_level: Senior+
---

# Mobile Performance and Resources

## Purpose

Identify and eliminate performance bottlenecks that degrade the user experience: slow startup, dropped frames, app crashes due to OOM, excessive battery drain, and oversized download. Measure before optimizing; profile to confirm the bottleneck; verify the fix with a before/after comparison. Never optimize without data.

## Use When

- App startup time (Time to First Frame / Time to Interactive) exceeds acceptable thresholds.
- Frame rate drops below 60 fps on target devices; jank is visible in scrolling or transitions.
- ANR dialogs appear in crash reports or Play Console.
- Memory grows monotonically over a session (leak) or crashes with OOM on low-RAM devices.
- Battery usage report shows excessive background wakeups, GPS, or BLE scanning.
- App download size exceeds the threshold triggering the "Large app" warning or exceeds store limits.
- CI performance budget baseline is violated by a new change.

## Do Not Use When

- The task is about functional correctness or test coverage → `mobile-testing`.
- The task is about crash analytics and event tracking → `mobile-observability`.
- The task is about backend API response time → handoff to `backend-developers`.
- The task is about server-side infrastructure capacity → handoff to `devops-sre`.

## Inputs

- Profiler trace or baseline report: Android Studio Profiler, Instruments, or Firebase Performance.
- Affected device model, RAM, and OS version.
- Reproduction scenario: cold start vs warm start, specific screen or user action.
- Current binary size report (AAB / IPA).

## Workflow

1. **Baseline first**: record the metric before any change. For startup: `adb shell am start -W` or Instruments → Time Profiler. For frames: Android Studio Profiler → CPU → System Trace; Instruments → Core Animation.
2. **Identify the bottleneck category**: startup initialization, layout/render, memory allocation, blocking I/O on main thread, background wakeup, or binary size.
3. **Startup optimization**: move heavy initialization (SDKs, DB open, network warm-up) off the main thread. Use lazy initialization for non-critical dependencies. Measure with `reportFullyDrawn()` (Android) or MetricKit (iOS).
4. **Frame rate**: verify no I/O, serialization, or lock acquisition on the main thread. In Compose: reduce recomposition scope with `remember`, stable lambdas, and `key`. In SwiftUI: profile with Instruments → SwiftUI.
5. **Memory**: use LeakCanary (Android) or Instruments → Allocations to find retained references. Check Bitmap/UIImage loading: use `BitmapFactory.Options.inSampleSize` / `resizable()`. Remove static references to Activities or ViewControllers.
6. **Battery**: audit wake locks with `adb shell dumpsys battery`. Replace periodic polling with `WorkManager` (Android) / `BGAppRefreshTask` (iOS). Use geofencing instead of continuous GPS; set BLE scan interval explicitly.
7. **App size**: enable R8 (Android) with proguard rules; use AAB with split APKs by ABI and screen density. iOS: verify App Thinning is enabled (no Bitcode since Xcode 14); check asset catalog compression.
8. **Verify and commit**: record the after metric; ensure CI tracks the metric baseline; add a regression test or performance test if the CI system supports it.

## Outputs

- Profiler trace with annotated bottleneck and root cause.
- Before/after metric comparison documented in PR description.
- Performance ADR for non-obvious trade-offs (lazy init, pre-warming).
- Size report delta.

## Named Patterns

### Good — Startup: lazy SDK initialization
```kotlin
// Android: move non-critical SDK init to background after first frame
class MyApp : Application() {
    override fun onCreate() {
        super.onCreate()
        initCritical()           // Firebase, Crashlytics — needed immediately
        doAfterFirstDraw {
            initAnalytics()      // analytics SDK — not needed before first frame
            initImageLoader()    // Glide/Coil — not needed before first frame
        }
    }
}

private fun doAfterFirstDraw(block: () -> Unit) {
    ProcessLifecycleOwner.get().lifecycle.addObserver(object : DefaultLifecycleObserver {
        override fun onStart(owner: LifecycleOwner) { lifecycleScope.launch { block() } }
    })
}
```

### Bad — All SDKs initialized in Application.onCreate synchronously
```kotlin
override fun onCreate() {
    super.onCreate()
    ThirdPartyAnalytics.init(this)  // 80 ms
    AnotherSdk.init(this)           // 60 ms
    MapsSdk.init(this)              // 120 ms
    // User sees blank screen for 260+ ms
}
```

### Good — Compose recomposition scope reduction
```kotlin
// Extract stable lambda to limit recomposition to item level
@Composable
fun OrderList(items: List<Order>, onItemClick: (String) -> Unit) {
    LazyColumn {
        items(items, key = { it.id }) { order ->
            val onClick = remember(order.id) { { onItemClick(order.id) } }
            OrderItem(order, onClick)
        }
    }
}
```

### Bad — Recomposing entire list on one item change
```kotlin
@Composable
fun OrderList(vm: OrderViewModel) {
    val orders = vm.orders // observing the whole list without stable keys
    Column { orders.forEach { OrderItem(it, onClick = { vm.select(it.id) }) } }
}
```
Every item change triggers recomposition of the whole Column.

### Good — LeakCanary integration in debug build
```kotlin
// app/build.gradle.kts
dependencies {
    debugImplementation("com.squareup.leakcanary:leakcanary-android:2.x")
}
// No other setup needed; LeakCanary auto-installs in debug builds
```

### Bad — Holding Activity context in a singleton
```kotlin
object ImageCache {
    lateinit var context: Context  // Activity context stored statically → memory leak
    fun load(url: String) = Glide.with(context).load(url)
}
```

## Boundaries

- Owns client-side performance measurement, profiling, and optimization.
- Does not own server-side response time or infrastructure capacity → `backend-developers` / `devops-sre`.
- Does not own crash analytics and error reporting → `mobile-observability`.
- Does not own CI/CD performance gating infrastructure → `devops-sre`.

## Sources

### Priority 1 — Platform canon
- Android Performance (developer.android.com) — https://developer.android.com/topic/performance
- Android App Startup — https://developer.android.com/topic/libraries/app-startup
- Compose performance — https://developer.android.com/jetpack/compose/performance
- Xcode Instruments — https://developer.apple.com/instruments/
- MetricKit (Apple) — https://developer.apple.com/documentation/metrickit
- Firebase Performance Monitoring — https://firebase.google.com/docs/perf-mon

### Priority 2 — Tools
- LeakCanary — https://square.github.io/leakcanary/
- Android R8 / ProGuard — https://developer.android.com/build/shrink-code
- App Thinning (Apple) — https://help.apple.com/xcode/mac/current/#/devbbdc5ce4f

### Priority 3 — Community
- ThoughtWorks Technology Radar — https://www.thoughtworks.com/radar

## Handoff

- Backend API response time optimization → `backend-developers`.
- CI/CD performance gating infrastructure → `devops-sre`.
- Crash analytics and error monitoring → `mobile-observability`.
- Testing strategy for performance regression → `mobile-testing`.
