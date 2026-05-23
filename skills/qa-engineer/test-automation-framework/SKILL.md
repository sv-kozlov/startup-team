---
name: test-automation-framework
description: Use when designing, building, or improving a test automation framework — page object model, fixture lifecycle, data setup and teardown, parallel execution, test isolation, and flakiness diagnosis. Tool-stack neutral structural patterns for API, UI, and e2e suites.
family: code
profile_level: Senior+
---

# Test Automation Framework

## Purpose

Make automated tests a trusted engineering asset: readable, stable, diagnosable, and maintainable. A framework
that developers and QA can change without breaking each other, where a failing test tells you what broke and
where, and where flakiness is tracked and fixed rather than tolerated.

## Use When

- Starting a new automation project and choosing structural patterns before writing the first test.
- Existing tests are unstable: flaky, slow, environment-dependent, or unreadable.
- Tests pass locally but fail in CI due to data state or timing issues.
- The suite is growing without a consistent pattern and becomes hard to maintain.
- Test data setup is coupled to test logic and causes interference between tests.

## Do Not Use When

- Designing which scenarios to automate -> `test-design-and-coverage` first.
- Wiring tests into a CI pipeline -> `ci-cd-test-integration`.
- Designing API contract tests with schema validation -> `api-testing`.

## Inputs

- Technology stack of the product under test (browser-based, API, mobile, or mixed).
- Existing test code (if any) to audit for structural problems.
- CI/CD toolchain (for parallel execution and reporting constraints).
- Team conventions: language, dependency management, code style.

## Workflow

1. Choose the automation layer for each test type. UI tests: Playwright or Selenium for browser.
   API tests: HTTP client (requests, REST Assured, httpx) with assertion library.
   Do not write UI tests for scenarios that can be covered at the API layer.

2. Apply Page Object Model (POM) for UI tests. Each page or significant component has an object
   that encapsulates locators and actions. Tests call page methods, not raw DOM selectors.
   Locators live in one place; when the UI changes, only the page object changes.

3. Design the fixture lifecycle. Fixtures provide the precondition state for a test. Each fixture
   is responsible for its own setup and teardown. Teardown runs even when the test fails.
   Fixtures are composable: a test requiring an authenticated user with a seeded order composes
   auth-fixture and order-fixture, not a god-fixture that does everything.

4. Isolate test data. Each test owns its data and cleans it up. Tests must not share mutable state.
   Use unique identifiers (UUIDs, timestamps) for test-created entities to avoid collision.
   Prefer database teardown or scoped transactions over snapshot restore for speed.

5. Write assertion-first tests. Structure: Arrange (set up state), Act (trigger behavior),
   Assert (verify outcome). One logical assertion per test. Multiple technical assertions
   (e.g., status code + body + header) are acceptable when they test one behavior.

6. Handle async behavior explicitly. Use wait conditions, not sleeps. For UI: wait for element
   state (visible, enabled, value). For API: poll with timeout and assertion. Never use
   `time.sleep(2)` or `await page.waitForTimeout(3000)` as the primary synchronization strategy.

7. Diagnose and track flakiness. Classify flaky failures:
   - Timing: insufficient or hardcoded waits -> replace with state-based waits.
   - Data: shared mutable state -> isolate test data.
   - Environment: external dependency instability -> mock or skip in CI.
   - Test order dependency: teardown missing or incomplete -> fix fixture.
   Flakiness rate = flaky failures / total runs. Target: below 1%. Above 5% is a trust problem.

8. Structure the project for maintainability:
   - Tests separate from framework utilities.
   - Configuration (base URLs, credentials) via environment variables, not hardcoded.
   - Page objects and test data factories in dedicated modules.
   - No business logic in tests; tests are declarative.

## Outputs

- Automation framework skeleton with clear layer separation.
- Page object or service-client layer.
- Fixture library with setup/teardown contracts.
- Test data factory or builder pattern.
- Flakiness tracking report (slug/failure type/frequency).
- Configuration guide for local and CI execution.

## Named Patterns

### Good — Page Object Model separating locators from logic

```python
# page_objects/checkout_page.py
class CheckoutPage:
    def __init__(self, page):
        self.page = page
        self._submit_button = page.locator('[data-testid="checkout-submit"]')
        self._total_amount = page.locator('[data-testid="order-total"]')

    def submit(self):
        self._submit_button.click()

    def total_text(self):
        return self._total_amount.inner_text()

# test_checkout.py
def test_checkout_shows_correct_total(page, seeded_cart):
    checkout = CheckoutPage(page)
    checkout.navigate()
    assert checkout.total_text() == "$49.99"
```

When the `data-testid` changes, only `CheckoutPage` changes. Tests remain unchanged.

### Bad — Raw locators in tests

```python
def test_checkout(page):
    page.click('#submit-btn-v2')
    assert page.inner_text('.order-total-display') == "$49.99"
```

The locator is in the test. When the designer renames the class, 20 tests break.

### Good — Composable fixture with teardown guarantee

```python
# conftest.py (pytest style)
@pytest.fixture
def authenticated_user(api_client):
    user = api_client.create_user(email=f"test_{uuid4()}@example.com")
    yield user
    api_client.delete_user(user.id)   # teardown always runs

@pytest.fixture
def order_for_user(api_client, authenticated_user):
    order = api_client.create_order(user_id=authenticated_user.id, items=[...])
    yield order
    api_client.cancel_order(order.id)  # teardown always runs
```

Tests compose fixtures. Teardown is guaranteed. No leftover data between runs.

### Bad — God fixture with no teardown

```python
@pytest.fixture(scope="session")
def shared_test_user():
    # Creates one user for ALL tests, never deleted
    return {"id": 42, "email": "shared@example.com"}
```

Tests modify the shared user. Test order determines outcome. CI passes; local fails.
Deleting the fixture after the session causes cascade failures.

### Good — State-based wait replacing sleep

```python
# Playwright
page.locator('[data-testid="success-toast"]').wait_for(state="visible", timeout=5000)

# pytest with polling
import time
def wait_for_status(api_client, order_id, target_status, timeout=10):
    deadline = time.time() + timeout
    while time.time() < deadline:
        status = api_client.get_order(order_id).status
        if status == target_status:
            return
        time.sleep(0.5)
    raise TimeoutError(f"Order {order_id} did not reach {target_status}")
```

### Bad — Hardcoded sleep

```python
time.sleep(3)  # "wait for the page to load"
assert page.locator('.result').inner_text() == "done"
```

Fragile: fails on slow CI, wastes time on fast machines. Does not adapt to actual state.

### Good — Configuration from environment variables

```python
BASE_URL = os.environ.get("TEST_BASE_URL", "http://localhost:8080")
API_KEY  = os.environ.get("TEST_API_KEY")    # no default; fail fast if missing
```

The same test code runs locally (with .env) and in CI (with injected secrets).

### Bad — Hardcoded base URL and credentials

```python
BASE_URL = "https://staging.myapp.internal"
API_KEY  = "sk-live-abc123"
```

The test suite only runs against one environment. Credentials leak in version control.

### Good — Flakiness tracking table

```
| Test | Failure type | Frequency | Root cause | Fix status |
|------|-------------|-----------|------------|------------|
| test_payment_webhook | Timing | 8% | Missing wait for webhook delivery | Fixed: state-based poll |
| test_search_results  | Data   | 3% | Shared search index, test writes conflict | In progress: isolated index per test |
| test_pdf_export      | Env    | 5% | Font service unavailable in CI | Mocked: stub PDF service |
```

### Bad — Marking flaky tests as skipped without tracking

Tests annotated `@pytest.mark.skip("flaky")`. No tracking. The suite grows "green"
but coverage is silently decreasing. Escaped defects follow.

## Boundaries

- Owns test automation framework architecture and fixture lifecycle.
- Does not own CI/CD pipeline configuration -> `ci-cd-test-integration`.
- Does not own which scenarios to automate -> `test-design-and-coverage`.
- Does not own API contract design or schema validation logic -> `api-testing`.
- Does not own product feature code or business logic -> `developer`.

## Sources

### Priority 1 — Testing standards and tool documentation

- ISTQB Advanced Level Test Automation Engineer Syllabus — https://www.istqb.org/certifications/advanced-test-automation-engineer
- Playwright documentation — https://playwright.dev/docs/intro
- pytest documentation (fixtures, conftest, parametrize) — https://docs.pytest.org/
- Selenium documentation — https://www.selenium.dev/documentation/
- REST Assured documentation — https://rest-assured.io/

### Priority 2 — Orientation and patterns

- Martin Fowler: Page Object pattern — https://martinfowler.com/bliki/PageObject.html
- Martin Fowler: TestDouble — https://martinfowler.com/bliki/TestDouble.html
- Google Testing Blog: Test Isolation — https://testing.googleblog.com/
- Lisa Crispin and Janet Gregory: Agile Testing (Part IV: Automating) — book reference

### Priority 3 — Background

- Software Engineering at Google: Testing chapters — https://abseil.io/resources/swe-book
- ThoughtWorks Technology Radar (test automation) — https://www.thoughtworks.com/radar

## Handoff

- Which scenarios to automate -> `test-design-and-coverage`.
- Wiring automated tests into CI/CD -> `ci-cd-test-integration`.
- API contract test logic and schema validation -> `api-testing`.
- Framework code quality review against team engineering standards -> `tech-lead` or `code-review-and-mentoring` (if applicable).
- Test environment stability issues -> `devops-sre`.
