---
name: mobile-data-and-offline
description: Use when implementing local storage (Room/CoreData/SQLite), offline-first behavior, background synchronization, conflict resolution, push notification handling, or deep link processing in a mobile application. Covers the pattern where local storage is the source of truth and the network is the sync channel.
family: code
profile_level: Senior+
---

# Mobile Data and Offline

## Purpose

Make the application usable without a network connection and resilient to intermittent connectivity. The local database is the source of truth; the UI always reads from it; the network refreshes it in the background. Users see cached data immediately and are never left with an empty screen because of a failed request.

## Use When

- Implementing local persistent storage for entities that must survive app restart.
- Designing offline-first behavior: the app must work with no network and sync when reconnected.
- Implementing a background sync queue: mutations accumulate locally and drain when network is available.
- Handling push notification payload and updating local state without a full network round-trip.
- Processing deep links and routing to the correct screen on cold and warm start.

## Do Not Use When

- The task is about remote API client implementation → `api-integration-mobile`.
- The task is about app architecture pattern → `mobile-app-architecture`.
- The task is about server-side data storage or sync orchestration → handoff to `backend-developers`.
- The task is about crash or performance observability → `mobile-observability`.

## Inputs

- Entity schemas and relationships (from requirements or system-analyst spec).
- API response shapes and update frequency.
- Offline tolerance requirement: read-only cache vs full offline mutations.
- Platform target: Android (Room) or iOS (CoreData / SwiftData) or cross-platform (SQLDelight / drift).

## Workflow

1. Choose storage engine: Room (Android, Kotlin, Flow-native), CoreData (iOS, complex relationships), SwiftData (iOS 17+, simpler syntax), SQLDelight (KMP), Hive/Drift (Flutter).
2. Design the local schema separately from the API response shape. Use a `toEntity()` / `toDomain()` mapping layer. Never store raw JSON blobs as the primary persistence format.
3. Wire the repository to expose a reactive stream from the local DB: `Flow<List<Entity>>` (Room) or `@FetchRequest` / `@Query` (SwiftData). The UI collects from the stream; sync writes to DB; UI updates automatically.
4. Implement the sync path: call the API, map the response to entities, upsert into the DB. On success, the reactive stream delivers the updated data to the UI.
5. Build the offline mutation queue: write local first, mark as pending, drain queue on connectivity restored. Implement idempotency key or use a timestamp for conflict resolution.
6. Handle push notifications: extract payload, update local entity, notify the reactive stream. Avoid triggering a full network re-fetch from the notification handler.
7. Handle deep links: on cold start, defer routing until the navigation graph is initialized. Capture the URL in `SceneDelegate`/`Activity.onNewIntent`, store it, and process after initialization is complete.

## Outputs

- Local database schema (Room entities / CoreData model / SwiftData schema).
- Repository implementation with reactive stream and sync method.
- Offline mutation queue (if mutations required offline).
- Push notification handler updating local state.
- Deep link router with cold-start support.

## Named Patterns

### Good — Room + Flow: local DB as source of truth
```kotlin
@Entity(tableName = "orders")
data class OrderEntity(@PrimaryKey val id: String, val title: String, val syncedAt: Long)

@Dao
interface OrderDao {
    @Query("SELECT * FROM orders ORDER BY syncedAt DESC")
    fun observeAll(): Flow<List<OrderEntity>>

    @Upsert
    suspend fun upsert(orders: List<OrderEntity>)
}

// Repository: UI reads from DB; sync writes to DB
class OrderRepositoryImpl(private val dao: OrderDao, private val api: OrderApi) : OrderRepository {
    override fun observeOrders(): Flow<List<Order>> =
        dao.observeAll().map { entities -> entities.map(OrderEntity::toDomain) }

    override suspend fun sync() {
        val remote = api.fetchOrders()
        dao.upsert(remote.map(OrderApiModel::toEntity))
    }
}
```

### Bad — Fetching from network inside reactive stream
```kotlin
// Anti-pattern: ViewModel fetches directly and replaces list
class OrderViewModel(private val api: OrderApi) : ViewModel() {
    private val _orders = MutableStateFlow<List<Order>>(emptyList())
    fun load() = viewModelScope.launch {
        _orders.value = api.fetchOrders() // UI shows empty on network error; no local cache
    }
}
```

### Good — SwiftData reactive query (iOS 17+)
```swift
@Model
class OrderModel {
    @Attribute(.unique) var id: String
    var title: String
    var syncedAt: Date
    init(id: String, title: String, syncedAt: Date) {
        self.id = id; self.title = title; self.syncedAt = syncedAt
    }
}

struct OrderListView: View {
    @Query(sort: \OrderModel.syncedAt, order: .reverse) private var orders: [OrderModel]
    var body: some View { List(orders, id: \.id) { Text($0.title) } }
}
```

### Bad — UserDefaults for list data
```swift
// Anti-pattern: array of codable models stored in UserDefaults
UserDefaults.standard.set(try! JSONEncoder().encode(orders), forKey: "orders")
```
UserDefaults is not designed for relational or list data; no reactive updates; no query capability.

### Good — Deep link cold-start deferred routing
```kotlin
// Android: Activity stores the intent, processes after NavHost is ready
class MainActivity : ComponentActivity() {
    private var pendingDeepLink: Uri? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        pendingDeepLink = intent.data
        setContent {
            AppNavHost(
                onNavControllerReady = { navController ->
                    pendingDeepLink?.let { navController.handle(it); pendingDeepLink = null }
                }
            )
        }
    }
}
```

### Bad — Deep link handled in Application.onCreate
```kotlin
class MyApp : Application() {
    override fun onCreate() {
        super.onCreate()
        // NavController doesn't exist yet — NPE or silently lost link
        if (intent?.data != null) navigate(intent.data!!)
    }
}
```

## Boundaries

- Owns local storage schema, offline-first queue, background sync, push payload handling, and deep link routing on the client.
- Does not own server-side sync orchestration → `backend-developers`.
- Does not own the remote API client layer → `api-integration-mobile`.
- Does not own analytics event schema → `mobile-observability`.

## Sources

### Priority 1 — Platform canon
- Room persistence library — https://developer.android.com/training/data-storage/room
- Android data and file storage — https://developer.android.com/training/data-storage
- WorkManager (background sync) — https://developer.android.com/topic/libraries/architecture/workmanager
- Core Data (Apple) — https://developer.apple.com/documentation/coredata
- SwiftData — https://developer.apple.com/documentation/swiftdata
- Apple: Push Notifications — https://developer.apple.com/documentation/usernotifications
- Android: Firebase Cloud Messaging — https://firebase.google.com/docs/cloud-messaging/android/client

### Priority 2 — Patterns and security
- OWASP MASVS — https://mas.owasp.org/MASVS/
- Android App Links — https://developer.android.com/training/app-links
- iOS Universal Links — https://developer.apple.com/documentation/xcode/supporting-universal-links-in-your-app

### Priority 3 — Community
- SQLDelight — https://cashapp.github.io/sqldelight/
- drift (Flutter/Dart) — https://drift.simonbinder.eu/

## Handoff

- Server-side sync strategy and API contract → `backend-developers`.
- Remote API client implementation → `api-integration-mobile`.
- Analytics event schema and observability → `mobile-observability`.
- Architecture and layer separation → `mobile-app-architecture`.
