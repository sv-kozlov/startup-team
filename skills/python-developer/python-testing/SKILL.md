---
name: python-testing
description: Use when covering Python service code with unit, integration, or contract tests. Covers pytest fixture scoping, testcontainers for real database/broker integration tests, AsyncMock and Protocol-based fakes, httpx.AsyncClient for FastAPI endpoint tests, and a mock strategy that avoids patching global state.
family: code
profile_level: Senior+
---

# Python Testing

## Purpose

Build a test suite that catches real bugs at the lowest cost: fast unit tests for domain logic, integration tests with real infrastructure (via testcontainers), and contract tests for API boundaries. Avoid a testing strategy that patches global state and produces tests that pass locally but are meaningless.

## Use When

- Adding tests to new or modified domain/service/repository code.
- Setting up the integration test baseline with testcontainers.
- Testing async FastAPI endpoints without a running server.
- Reviewing a PR for test coverage on critical paths and error branches.
- Choosing between a mock, a fake, and testcontainers for a test scenario.

## Do Not Use When

- The task is QA strategy or release-level regression planning → handoff to `qa-engineer`.
- The task is performance benchmarking and profiling → `service-observability`.
- The task is typing or static analysis → `python-typing-and-quality`.

## Inputs

- Functions or classes under test with their dependency graph.
- Infrastructure dependencies: Postgres, Redis, Kafka, external HTTP services.
- Desired coverage target (typically ≥80% on service layer for new code).

## Workflow

1. Classify the unit: domain logic (pure function / dataclass) → unit test with no infrastructure. Application service (use-case) → unit test with Protocol-based fakes. Repository → integration test with testcontainers. FastAPI router → `httpx.AsyncClient` test.
2. Scope fixtures correctly: `session`-scope for expensive resources (Postgres container, applied migrations); `function`-scope for per-test data; `module`-scope only when teardown is cheap.
3. For database tests: start container in `session`-scope conftest, apply Alembic migrations once, use transaction rollback per test to avoid table truncation.
4. For async tests: use `pytest-anyio` or `pytest-asyncio` with `asyncio_mode = "auto"` in `pyproject.toml`. Do not mix sync and async fixtures without explicit handling.
5. For FastAPI endpoints: use `httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test")` — no real network, full ASGI stack.
6. For external HTTP dependencies: use `respx` (for httpx) or `aioresponses` (for aiohttp) to mock outbound HTTP calls.
7. Assert on behavior: check return values, state changes, emitted events. Avoid asserting on internal implementation details.

## Outputs

- Unit tests for domain entities and use-cases.
- Integration tests for repositories against a real database container.
- Endpoint tests using `httpx.AsyncClient`.
- `conftest.py` with scoped fixtures documented by their scope and teardown strategy.

## Named Patterns

### Good — Protocol-based fake in unit test (no patching)
```python
# tests/orders/test_place_order.py
import pytest
from decimal import Decimal
from uuid import uuid4
from orders.application.service import OrderService
from orders.domain.models import OrderID, Order

class FakeOrderRepository:
    def __init__(self) -> None:
        self._store: dict[OrderID, Order] = {}
    async def get(self, order_id: OrderID) -> Order | None:
        return self._store.get(order_id)
    async def save(self, order: Order) -> None:
        self._store[order.id] = order

class FakePaymentCharger:
    async def charge(self, amount: Decimal, idempotency_key: str) -> str:
        return f"tx_{uuid4()}"

@pytest.mark.anyio
async def test_place_order_saves_and_returns_id() -> None:
    service = OrderService(repo=FakeOrderRepository(), payment=FakePaymentCharger())
    order_id = await service.place(items=["item-1"], currency="USD", total=Decimal("9.99"))
    assert order_id is not None
```
No monkeypatching; fakes are explicit; test is fast and deterministic.

### Bad — Patching global dependency
```python
@pytest.mark.anyio
@patch("orders.application.service.stripe")  # patches global import
async def test_place_order(mock_stripe) -> None:
    mock_stripe.charge.return_value = "tx_123"
    result = await place_order({"items": ["item-1"]})
    assert result["status"] == "placed"
```
Test is coupled to import path; refactoring breaks test names; behavior hidden inside patch.

### Good — Integration test with testcontainers and Alembic migrations
```python
# tests/conftest.py
import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from alembic import command
from alembic.config import Config

@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:16") as pg:
        yield pg

@pytest.fixture(scope="session")
def engine(postgres_container):
    url = postgres_container.get_connection_url().replace("postgresql://", "postgresql+asyncpg://")
    eng = create_async_engine(url)
    # run migrations once per session
    cfg = Config("alembic.ini")
    cfg.set_main_option("sqlalchemy.url", url.replace("+asyncpg", ""))
    command.upgrade(cfg, "head")
    yield eng

@pytest.fixture
async def session(engine):
    async with engine.begin() as conn:
        await conn.execute(text("BEGIN"))
        yield async_sessionmaker(bind=conn)()
        await conn.execute(text("ROLLBACK"))
```
Container starts once per session; migrations run once; each test rolls back without truncation.

### Bad — Re-creating database schema in every test
```python
@pytest.fixture
async def db():
    await engine.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
    Base.metadata.create_all(engine)
    yield engine
```
Schema recreation per test is 10–100× slower than rollback; does not test real migration paths.

### Good — FastAPI endpoint test with httpx.AsyncClient
```python
import pytest
import httpx
from fastapi.testclient import TestClient  # sync alternative
from httpx import AsyncClient, ASGITransport

@pytest.mark.anyio
async def test_place_order_returns_201(app, fake_order_service) -> None:
    app.dependency_overrides[get_order_service] = lambda: fake_order_service
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post(
            "/v1/orders/",
            json={"items": ["item-1"], "currency": "USD", "total": "9.99"},
            headers={"Idempotency-Key": "test-key-1"},
        )
    assert resp.status_code == 201
    assert "id" in resp.json()
```
No real server; full ASGI stack; dependency_overrides for service injection.

### Bad — TestClient in async test
```python
def test_place_order():
    client = TestClient(app)
    response = client.post("/v1/orders/", ...)
```
Sync `TestClient` blocks; async database calls inside handlers fail silently; event loop conflicts in complex fixtures.

## Boundaries

- Owns service-level unit and integration tests.
- Does not own QA strategy, release-level regression, or acceptance test planning → `qa-engineer`.
- Does not own performance benchmarks and profiling → `service-observability`.

## Sources

### Priority 1 — Testing canon
- pytest documentation — https://docs.pytest.org/
- pytest-anyio / anyio documentation — https://anyio.readthedocs.io/
- httpx documentation — https://www.python-httpx.org/
- testcontainers-python — https://testcontainers-python.readthedocs.io/
- FastAPI testing guide — https://fastapi.tiangolo.com/tutorial/testing/

### Priority 2 — Quality standards
- Google Engineering Practices: Writing Good Tests — https://google.github.io/eng-practices/
- ISO/IEC 25010 — https://iso25000.com/index.php/en/iso-25000-standards/iso-25010

### Priority 3 — Practice background
- martinfowler.com on test doubles — https://martinfowler.com/bliki/TestDouble.html

## Handoff

- QA strategy and release-level regression → `qa-engineer`.
- Performance benchmarking and SLI definition → `service-observability`.
- Static type checking → `python-typing-and-quality`.
