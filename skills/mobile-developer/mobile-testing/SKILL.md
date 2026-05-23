---
name: mobile-testing
description: Use when writing unit tests for ViewModels and repositories, UI tests with Espresso or XCUITest, snapshot tests, or designing a device matrix for mobile regression. Covers test doubles, coroutine test dispatchers, fake repositories, and the strategy for real device vs emulator testing.
family: code
profile_level: Senior+
---

# Mobile Testing

## Purpose

Cover mobile application code with a layered test suite that catches regressions before they reach production. Unit tests verify business logic independently of the platform; UI tests verify user-visible flows on the actual rendering engine; snapshot tests catch unintended visual regressions. The suite runs in CI on every merge.

## Use When

- Writing unit tests for a ViewModel, use case, or repository.
- Writing Espresso or XCUITest UI tests for a user flow.
- Setting up a Compose UI test or SwiftUI preview test.
- Choosing which test level covers a given scenario (unit vs integration vs UI).
- Designing a device matrix for a release regression pass.
- Replacing a live dependency with a test double.

## Do Not Use When

- The task is about QA test strategy or release-level regression ownership → handoff to `qa-engineer`.
- The task is about performance profiling with benchmarks → `mobile-performance-and-resources`.
- The task is about crash analytics → `mobile-observability`.
- The task is about defining acceptance criteria from the business side → handoff to `system-analyst`.

## Inputs

- Existing ViewModel, repository, or use case to test.
- Test double requirements: fake, stub, or mock.
- CI platform and target device list.
- Platform: Android (JUnit 5, Turbine, kotlinx-coroutines-test) or iOS (XCTest, async/await testing).

## Workflow

1. Start with the unit layer. ViewModel tests use `TestCoroutineDispatcher` (Android) or `MainActor` isolation (iOS); inject fake repositories; test each state transition.
2. Define the device matrix: ≥2 API levels (min supported + current stable), ≥2 screen sizes. UI tests run on emulators in CI; real device smoke test before each release.
3. Write UI tests for critical user flows only: authentication, checkout, primary navigation. Avoid UI-testing utility screens; they are slow and brittle.
4. Use `ComposeTestRule` (Android) or `XCUIApplication` (iOS) to control test lifecycle. Launch the app in a test-clean state; do not rely on data left from a previous test.
5. Implement snapshot tests for design system components only (not full screens). Use Paparazzi (Android) or swift-snapshot-testing (iOS). Record snapshots in CI; review diffs in PR.
6. Mock the network layer at the repository level, not at OkHttp/URLSession level, to keep tests fast and platform-independent.
7. Gate CI: unit tests on every push; UI tests on PR merge to main; device farm on release candidate.

## Outputs

- Unit tests for ViewModel and repository with ≥80% branch coverage on business logic.
- UI test suite for critical flows (Espresso / XCUITest / Detox).
- Snapshot test suite for design system components.
- Device matrix documented in the release checklist.

## Named Patterns

### Good — ViewModel unit test with Turbine and fake
```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
class OrderViewModelTest {
    private val testDispatcher = UnconfinedTestDispatcher()
    private val fakeRepo = FakeOrderRepository()
    private lateinit var vm: OrderViewModel

    @BeforeEach fun setUp() {
        Dispatchers.setMain(testDispatcher)
        vm = OrderViewModel(fakeRepo)
    }
    @AfterEach fun tearDown() { Dispatchers.resetMain() }

    @Test fun `initial load emits items`() = runTest {
        fakeRepo.emit(listOf(Order("1", "Coffee")))
        vm.state.test {
            val loading = awaitItem()
            assertTrue(loading.isLoading)
            vm.load()
            val ready = awaitItem()
            assertEquals(1, ready.items.size)
            cancelAndIgnoreRemainingEvents()
        }
    }
}

class FakeOrderRepository : OrderRepository {
    private val flow = MutableSharedFlow<List<Order>>(replay = 1)
    suspend fun emit(orders: List<Order>) = flow.emit(orders)
    override fun observeOrders(): Flow<List<Order>> = flow
    override suspend fun sync() = Unit
}
```

### Bad — ViewModel test with real coroutine dispatcher
```kotlin
@Test fun `loads orders`() = runBlocking {
    val vm = OrderViewModel(RealOrderRepository(db, api)) // real DB + network
    vm.load()
    delay(500) // flaky timing
    assertEquals(1, vm.state.value.items.size)
}
```
Test depends on real network and DB; flaky and slow; not portable to CI.

### Good — Compose UI test with semantic queries
```kotlin
@get:Rule val composeRule = createComposeRule()

@Test fun `shows order list after load`() {
    composeRule.setContent {
        OrderScreen(
            state = OrderUiState(items = listOf(Order("1", "Coffee")), isLoading = false),
            onRetry = {}, onItemClick = {}
        )
    }
    composeRule.onNodeWithText("Coffee").assertIsDisplayed()
}
```

### Bad — UI test that depends on live backend
```kotlin
@Test fun `order screen shows items`() {
    ActivityScenario.launch(OrderActivity::class.java) // hits real API
    onView(withId(R.id.order_list)).check(matches(isDisplayed()))
    // passes on dev network, fails in CI
}
```

### Good — XCUITest flow test
```swift
func testOrderFlowAddsItemToCart() throws {
    let app = XCUIApplication()
    app.launchArguments = ["--uitesting", "--stub-orders"]
    app.launch()
    app.tables.cells.firstMatch.tap()
    XCTAssertTrue(app.navigationBars["Order Detail"].exists)
    app.buttons["Add to Cart"].tap()
    XCTAssertTrue(app.staticTexts["1 item"].waitForExistence(timeout: 2))
}
```

### Bad — Hard-coded sleep in UI test
```swift
app.buttons["Load"].tap()
sleep(3) // arbitrary; fails on slow CI; passes on fast local
XCTAssertTrue(app.tables.cells.firstMatch.exists)
```

## Boundaries

- Owns developer-level tests: unit, UI, and snapshot.
- Does not own QA test strategy, acceptance test plans, or release-level regression ownership → `qa-engineer`.
- Does not own performance benchmarks and profiling → `mobile-performance-and-resources`.
- Does not own crash analytics → `mobile-observability`.

## Sources

### Priority 1 — Platform canon
- Android testing documentation — https://developer.android.com/training/testing
- Jetpack Compose testing — https://developer.android.com/jetpack/compose/testing
- XCTest (Apple) — https://developer.apple.com/documentation/xctest
- Turbine (Flow testing) — https://github.com/cashapp/turbine
- kotlinx-coroutines-test — https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-test/

### Priority 2 — Device and snapshot
- Paparazzi (Android snapshot) — https://github.com/cashapp/paparazzi
- swift-snapshot-testing — https://github.com/pointfreeco/swift-snapshot-testing
- Detox (React Native E2E) — https://wix.github.io/Detox/

### Priority 3 — Community practice
- Google Engineering Practices: Testing — https://google.github.io/eng-practices/

## Handoff

- QA strategy and release-level regression → `qa-engineer`.
- Performance benchmarks and profiling → `mobile-performance-and-resources`.
- Crash analytics setup → `mobile-observability`.
- Acceptance criteria from requirements → `system-analyst`.
