---
name: mobile-app-architecture
description: Use when starting a new mobile application, restructuring module layout, choosing an architecture pattern (MVVM/MVI), managing screen lifecycle, or evaluating whether to introduce Clean Architecture or Kotlin Multiplatform. Covers dependency direction, layer separation, and proportionality of architectural choice to problem size.
family: code
profile_level: Senior+
---

# Mobile App Architecture

## Purpose

Shape a mobile application so it is easy to read, easy to test, and survives platform lifecycle events (configuration changes, process death, background eviction) without data loss or UI inconsistency. Optimize for clear layer boundaries, unidirectional data flow, and a structure a new Senior can navigate without a guide.

## Use When

- Bootstrapping a new Android or iOS application or adding a significant new module.
- Adding a feature that does not cleanly fit the current module structure.
- Reviewing a design where layers, state ownership, or dependency direction are unclear.
- The team is considering Clean Architecture, Kotlin Multiplatform, or cross-platform migration and the cost is not obvious.
- Screen state is lost on rotation or process death and no clear owner exists.

## Do Not Use When

- The task is purely about UI component implementation → `mobile-ui-and-navigation`.
- The task is local storage or offline sync specifically → `mobile-data-and-offline`.
- The task is cross-service platform topology → handoff to `system-architect`.
- The task is team-wide mobile standards → handoff to `tech-lead`.

## Inputs

- Current module graph, package tree, and known pain points.
- Business capability and expected change axes (which layer changes most often).
- Platform target: Android-only, iOS-only, or cross-platform (KMP / Flutter / React Native).
- Team size and platform maturity.

## Workflow

1. State the capability and its change axis. Name what is most likely to change: UI design, business rules, backend API shape, or storage engine.
2. Choose the architecture pattern proportional to complexity: MVVM for most screens; MVI when side-effects need strict control; Clean Architecture only when domain logic is complex and independently testable.
3. Define the layer boundary: UI layer (Composable / SwiftUI View) observes state; ViewModel/Presenter transforms domain data; Repository abstracts data sources; data sources (remote/local) are replaceable.
4. Place interfaces on the consumer side. ViewModel owns the Repository interface; the concrete implementation lives in the data layer.
5. Verify dependency direction: UI → ViewModel → domain/use-case → repository interface; data layer implements the interface; domain depends on nothing platform-specific.
6. Handle lifecycle explicitly: Android ViewModel survives rotation; iOS @StateObject owns the reference. State that must survive process death uses SavedStateHandle (Android) or AppStorage/SceneStorage (iOS).
7. Decide module count by team size and build time: start with a single app module; split into feature modules when build time exceeds 2 min or teams step on each other.

## Outputs

- Module/package diagram with explicit dependency arrows.
- ADR or PR description naming the chosen architecture pattern and the trade-off.
- List of interfaces with their consumer-side owners.
- ViewModel state class and event/effect definitions (for MVI).

## Named Patterns

### Good — Unidirectional data flow with StateFlow (Android/Kotlin)
```kotlin
// ViewModel: single state + events only from UI
data class OrderUiState(
    val items: List<Order> = emptyList(),
    val isLoading: Boolean = true,
    val error: String? = null
)

class OrderViewModel(private val repo: OrderRepository) : ViewModel() {
    private val _state = MutableStateFlow(OrderUiState())
    val state: StateFlow<OrderUiState> = _state.asStateFlow()

    fun load() {
        viewModelScope.launch {
            repo.observeOrders()
                .catch { e -> _state.update { it.copy(isLoading = false, error = e.message) } }
                .collect { orders -> _state.update { it.copy(items = orders, isLoading = false) } }
        }
    }
}
```

### Bad — Mutable state scattered across Composables
```kotlin
// Anti-pattern: each Composable manages its own network state
@Composable
fun OrderList() {
    var orders by remember { mutableStateOf<List<Order>>(emptyList()) }
    LaunchedEffect(Unit) { orders = ApiClient.fetchOrders() } // network in composable
}
```
State is duplicated, inconsistent after rotation, untestable without the UI.

### Good — Lifecycle-safe state on iOS (SwiftUI)
```swift
// @StateObject owns the lifecycle; @ObservedObject observes without owning
@MainActor
class OrderViewModel: ObservableObject {
    @Published private(set) var orders: [Order] = []
    @Published private(set) var isLoading = true

    private let repo: OrderRepository

    init(repo: OrderRepository = DefaultOrderRepository()) { self.repo = repo }

    func load() async {
        defer { isLoading = false }
        do { orders = try await repo.fetchOrders() }
        catch { /* map to error state */ }
    }
}

struct OrderListView: View {
    @StateObject private var vm = OrderViewModel()
    var body: some View {
        List(vm.orders, id: \.id) { Text($0.title) }
            .task { await vm.load() }
    }
}
```

### Bad — Logic inside SwiftUI View body
```swift
struct OrderListView: View {
    @State private var orders: [Order] = []
    var body: some View {
        List(orders, id: \.id) { Text($0.title) }
            .onAppear {
                Task { orders = try! await URLSession.shared.decode([Order].self, from: url) }
            }
    }
}
```
Business logic in the view body is untestable; try! crashes in production.

### Good — Consumer-side repository interface
```kotlin
// Domain layer owns the abstraction; data layer implements
interface OrderRepository {
    fun observeOrders(): Flow<List<Order>>
    suspend fun sync()
}

class DefaultOrderRepository(
    private val dao: OrderDao,
    private val api: OrderApi
) : OrderRepository {
    override fun observeOrders(): Flow<List<Order>> = dao.observeAll().map { it.map(::toDomain) }
    override suspend fun sync() { dao.upsert(api.fetchOrders().map(::toEntity)) }
}
```

### Bad — ViewModel calling API directly
```kotlin
class OrderViewModel(private val api: OrderApi) : ViewModel() {
    fun load() = viewModelScope.launch {
        val orders = api.fetchOrders() // data source skips repository; untestable; can't swap to local
    }
}
```

## Boundaries

- Owns mobile application module structure, layer separation, and lifecycle management.
- Does not own cross-service architecture or bounded contexts → `system-architect`.
- Does not own team-wide layout standards across multiple applications → `tech-lead`.
- Does not own specific UI component implementation → `mobile-ui-and-navigation`.
- Does not own storage engine selection or sync strategy → `mobile-data-and-offline`.

## Sources

### Priority 1 — Platform canon
- Android Guide to App Architecture — https://developer.android.com/topic/architecture
- Android Architecture: UI Layer — https://developer.android.com/topic/architecture/ui-layer
- Android Architecture: Data Layer — https://developer.android.com/topic/architecture/data-layer
- Apple: Model-View-ViewModel (SwiftUI) — https://developer.apple.com/tutorials/app-dev-training/managing-data-flow-between-views
- Swift.org — https://www.swift.org/documentation/

### Priority 2 — Architectural orientation
- The Twelve-Factor App — https://12factor.net/
- Kotlin Multiplatform — https://www.jetbrains.com/kotlin-multiplatform/

### Priority 3 — Community samples
- Now in Android (Google reference app) — https://github.com/android/nowinandroid
- Android Architecture Samples — https://github.com/android/architecture-samples

## Handoff

- Cross-service contracts and platform topology → `system-architect`.
- Team-wide architectural standards → `tech-lead`.
- UI component and navigation implementation → `mobile-ui-and-navigation`.
- Local storage and offline sync specifics → `mobile-data-and-offline`.
