---
name: mobile-ui-and-navigation
description: Use when implementing a screen, navigation flow, or UI component on Android (Jetpack Compose) or iOS (SwiftUI), ensuring platform guideline compliance (Material Design 3, HIG), correct state hoisting, accessibility, and adaptive layout. Covers state management in UI layer, gesture handling, and design handoff.
family: code
profile_level: Senior+
---

# Mobile UI and Navigation

## Purpose

Implement mobile screens that faithfully translate design intent into platform-idiomatic UI, handle all visible states (loading, empty, error, success), adapt to device sizes and OS versions, and meet platform accessibility standards. Keep UI logic thin: screens observe state; they do not compute it.

## Use When

- Implementing a new screen or flow in Compose or SwiftUI.
- Migrating a screen from XML/UIKit to Compose/SwiftUI.
- Implementing multi-screen navigation with back-stack management and deep link handling from the UI side.
- Reviewing a screen for state hoisting, recomposition correctness, or HIG/Material compliance.
- Adding accessibility labels, semantic roles, or keyboard navigation.

## Do Not Use When

- The task is about architecture pattern selection or module boundaries → `mobile-app-architecture`.
- The task is about implementing local data storage → `mobile-data-and-offline`.
- The task is about UX research, wireframes, or design decisions → handoff to `ui-ux-designer`.
- The task is about accessibility audit strategy beyond implementation → handoff to `qa-engineer`.

## Inputs

- Design specs (Figma or equivalent) with states, transitions, and component variants.
- Platform target: Android (Compose) or iOS (SwiftUI) or cross-platform (Flutter / React Native).
- Navigation graph or routing plan.
- Existing design system or component library.

## Workflow

1. Identify all screen states from the design spec: loading, success, empty, error, offline. Each state must be reachable and visually distinct.
2. Hoist state to the ViewModel. Composable / View receives immutable state; it emits events up. Never compute business state inside a Composable or View body.
3. Implement the navigation graph. Android: NavHost with typed routes (Compose Navigation). iOS: NavigationStack with NavigationPath or NavigationLink. Avoid global singletons for routing.
4. Apply platform guidelines: Material Design 3 on Android (dynamic color, elevation, typography scale); HIG on iOS (SF Symbols, native controls, safe area insets).
5. Test recomposition scope: in Compose, extract stable lambdas and use `remember` + `key` to limit recomposition to the changed subtree. Profile with Layout Inspector.
6. Add accessibility: `contentDescription` / `accessibilityLabel`, `semantics { role }`, focus order, minimum touch target 48 dp / 44 pt.
7. Validate adaptive layout: foldables (WindowSizeClass), iPad (NavigationSplitView), landscape orientation.

## Outputs

- Screen Composable or SwiftUI View with explicit state parameter.
- Navigation graph definition or routing module.
- Component extracted to the design system (if reusable).
- Accessibility annotations and semantic roles.

## Named Patterns

### Good — State hoisting in Compose
```kotlin
// Stateless composable receives state + callbacks
@Composable
fun OrderScreen(
    state: OrderUiState,
    onRetry: () -> Unit,
    onItemClick: (String) -> Unit
) {
    when {
        state.isLoading -> CircularProgressIndicator()
        state.error != null -> ErrorView(state.error, onRetry)
        state.items.isEmpty() -> EmptyView()
        else -> LazyColumn { items(state.items) { OrderItem(it, onItemClick) } }
    }
}

// Stateful entry point wires ViewModel
@Composable
fun OrderRoute(vm: OrderViewModel = hiltViewModel()) {
    val state by vm.state.collectAsStateWithLifecycle()
    OrderScreen(state, onRetry = vm::load, onItemClick = vm::selectOrder)
}
```

### Bad — State computed inside Composable
```kotlin
@Composable
fun OrderScreen(repo: OrderRepository) { // repo injected into composable!
    var orders by remember { mutableStateOf<List<Order>>(emptyList()) }
    LaunchedEffect(Unit) { orders = repo.fetchOrders() }
    LazyColumn { items(orders) { Text(it.title) } }
}
```
Composable owns state, bypasses ViewModel; rotation loses data; impossible to test without UI.

### Good — NavigationStack on iOS
```swift
struct AppView: View {
    @StateObject private var router = AppRouter()

    var body: some View {
        NavigationStack(path: $router.path) {
            OrderListView()
                .navigationDestination(for: OrderRoute.self) { route in
                    switch route {
                    case .detail(let id): OrderDetailView(id: id)
                    }
                }
        }
        .environmentObject(router)
    }
}
```

### Bad — Dismiss + present chaining without NavigationStack
```swift
// Anti-pattern: pushViewController chained in callbacks
orderListVC.onItemTap = { id in
    let detailVC = OrderDetailVC(id: id)
    self.navigationController?.pushViewController(detailVC, animated: true)
}
```
Navigation logic scattered across ViewControllers; deep links and testing are hard.

### Good — Recomposition scope control
```kotlin
// Extract stable lambda to prevent recomposition of the parent
@Composable
fun OrderList(items: List<Order>, onItemClick: (String) -> Unit) {
    LazyColumn {
        items(items, key = { it.id }) { order ->
            OrderItem(order, onItemClick = { onItemClick(order.id) })
        }
    }
}
```

### Bad — Inline lambdas causing full recomposition
```kotlin
LazyColumn {
    items(orders) { order ->
        OrderItem(order, onItemClick = { vm.select(order.id) }) // new lambda every recomposition
    }
}
```

## Boundaries

- Owns screen implementation, state rendering, and navigation within the mobile application.
- Does not own UX research, wireframes, design decisions, or visual identity → `ui-ux-designer`.
- Does not own ViewModel business logic or repository layer → `mobile-app-architecture`.
- Does not own accessibility audit strategy → `qa-engineer`.

## Sources

### Priority 1 — Platform canon
- Jetpack Compose state management — https://developer.android.com/jetpack/compose/state
- Jetpack Compose Navigation — https://developer.android.com/jetpack/compose/navigation
- Compose performance — https://developer.android.com/jetpack/compose/performance
- SwiftUI — https://developer.apple.com/xcode/swiftui/
- Human Interface Guidelines — https://developer.apple.com/design/human-interface-guidelines/
- Material Design 3 — https://m3.material.io/

### Priority 2 — Accessibility and adaptive
- Android Accessibility — https://developer.android.com/guide/topics/ui/accessibility
- iOS Accessibility — https://developer.apple.com/accessibility/

### Priority 3 — Community
- Now in Android (Google reference app) — https://github.com/android/nowinandroid

## Handoff

- UX flow design, wireframes, and design system decisions → `ui-ux-designer`.
- Architecture pattern and module structure → `mobile-app-architecture`.
- Local data binding specifics → `mobile-data-and-offline`.
- Accessibility audit → `qa-engineer`.
