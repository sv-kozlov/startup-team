---
name: python-service-design
description: Use when starting a new Python backend service, restructuring package layout, deciding where interfaces live, or evaluating whether to introduce layered/clean/hexagonal architecture. Covers Protocol-based interfaces, dependency injection, package boundaries, and proportionality of architectural choice to problem size.
family: code
profile_level: Senior+
---

# Python Service Design

## Purpose

Shape a Python backend service so it is easy to read, easy to change, and pays for every architectural layer it carries. Optimize for clear package boundaries, explicit dependency injection, typed interfaces via `Protocol`, and a code shape a new Senior can navigate without a guide.

## Use When

- Bootstrapping a new Python service or module.
- Adding a feature that does not cleanly fit the current package layout.
- Reviewing a design where layers, interfaces, or dependency direction are unclear.
- The team is considering hexagonal/clean/DDD tactical patterns and the cost of the layer is not obvious.

## Do Not Use When

- The task is purely about async lifecycle or event loop → `python-async-and-concurrency`.
- The task is API contract shape (REST/gRPC/OpenAPI/protobuf) → `api-contract-design`.
- The task is the data access layer specifically → `data-layer-python`.
- The task is platform topology across services → handoff to `system-architect`.

## Inputs

- Current module tree, import graph, and known pain points.
- Business capability and expected change axes.
- Visible load profile and team size.
- Framework choice: FastAPI, Django, aiohttp, or plain Python package.

## Workflow

1. State the capability and the change axis. Name what is most likely to change (HTTP transport, storage, business rule, ML integration, external API).
2. Draft the minimum package layout around domains: `orders/`, `payments/`, `notifications/` — not `models/`, `views/`, `utils/`.
3. Define layer boundaries: `transport/` (routers, serializers) → `application/` (use-case services) → `domain/` (entities, value objects, domain services) → `infrastructure/` (repositories, adapters, clients).
4. Place interfaces on the consumer side using `Protocol`. The application service defines `OrderRepository(Protocol)`, not the infrastructure adapter.
5. Verify dependency direction: domain depends on nothing outside itself; infrastructure depends on domain, not vice versa.
6. Check for circular imports and god-modules. A module named `utils.py` or `helpers.py` is a smell.
7. Decide layer count by problem size: start with router → service → repository. Add hexagonal ports only when ≥2 transports or ≥2 storages are in scope.

## Outputs

- Package tree with explicit dependency arrows.
- ADR or PR description naming the chosen architectural shape and the trade-off paid.
- List of `Protocol`-based interfaces with their consumer-side owners.

## Named Patterns

### Good — Protocol-based interface at the consumer
```python
# application/orders/ports.py — consumer defines what it needs
from typing import Protocol
from domain.orders.models import Order, OrderID

class OrderRepository(Protocol):
    async def get(self, order_id: OrderID) -> Order | None: ...
    async def save(self, order: Order) -> None: ...

class PaymentCharger(Protocol):
    async def charge(self, amount: Money, idempotency_key: str) -> TransactionID: ...
```
```python
# application/orders/service.py — depends only on Protocol, not on SQLAlchemy or Stripe
class OrderService:
    def __init__(self, repo: OrderRepository, payment: PaymentCharger) -> None:
        self._repo = repo
        self._payment = payment
```
Consumer owns the abstraction; infrastructure implements it. No inheritance required; `mypy` checks structural compatibility.

### Bad — Infrastructure dependency in application layer
```python
# application/orders/service.py
from infrastructure.db import SessionLocal  # infrastructure in application
from sqlalchemy.orm import Session

class OrderService:
    def __init__(self) -> None:
        self._session = SessionLocal()  # global session, not injectable
```
Tight coupling to SQLAlchemy; testing requires a real database; layer boundary is broken.

### Good — Domain package around domains, not layers
```
src/
  orders/
    domain.py       # Order, OrderID, OrderPlaced event
    service.py      # application use-cases
    repository.py   # Protocol definition
    router.py       # FastAPI router
  payments/
    ...
  shared/
    money.py        # Money value object shared across domains
```
Cohesion by feature; a new developer finds everything about orders in one place.

### Bad — Technical layer packaging
```
src/
  models/           # all ORM models for all domains
  views/            # all routers for all domains
  services/         # all business logic for all domains
  utils/            # miscellaneous helpers
```
Adding a feature requires touching 4 directories; cross-domain contamination is hard to prevent.

### Good — Proportional layering
A small CRUD service ships with router → service → repository. No ports, no adapters, no domain/application split until a second transport or integration appears.

### Bad — Premature hexagonal
A single REST endpoint over a single Postgres table sits behind `ports/inbound/`, `ports/outbound/`, `application/commands/`, `domain/aggregates/`, `infrastructure/persistence/`. Six files to change one field.

### Good — Explicit DI via constructor, not service locator
```python
def create_app() -> FastAPI:
    db_pool = create_async_engine(settings.DATABASE_URL)
    session_factory = async_sessionmaker(db_pool)
    order_repo = PostgresOrderRepository(session_factory)
    payment = StripePaymentAdapter(settings.STRIPE_KEY)
    order_service = OrderService(repo=order_repo, payment=payment)
    router = OrderRouter(service=order_service)
    app = FastAPI()
    app.include_router(router.router)
    return app
```
Dependency graph is explicit and visible at startup; swapping implementations requires changing one line.

### Bad — Service locator or global imports
```python
# service.py
from app.db import get_session  # hidden import from global
import stripe  # module-level singleton

async def place_order(items: list) -> dict:
    async with get_session() as session:
        stripe.charge(...)
```
Hidden dependencies; impossible to unit-test without patching globals.

## Boundaries

- Owns service-internal package shape and dependency direction.
- Does not own cross-service architecture, bounded contexts, or platform topology → `system-architect`.
- Does not own team-wide layout standards across multiple services → `tech-lead`.

## Sources

### Priority 1 — Python canon
- Python 3 Language Reference — https://docs.python.org/3/reference/
- PEP 544 Protocols: Structural subtyping — https://peps.python.org/pep-0544/
- FastAPI documentation: Bigger Applications — https://fastapi.tiangolo.com/tutorial/bigger-applications/
- Pydantic v2 documentation — https://docs.pydantic.dev/

### Priority 2 — Architectural orientation
- The Twelve-Factor App — https://12factor.net/
- Hexagonal Architecture (Alistair Cockburn) — https://alistair.cockburn.us/hexagonal-architecture/

### Priority 3 — Pattern background
- martinfowler.com on layered architecture — https://martinfowler.com/bliki/PresentationDomainDataLayering.html
- microservices.io patterns catalog — https://microservices.io/patterns/

## Handoff

- Cross-service contracts and bounded contexts → `system-architect`.
- Team-wide standards across multiple Python services → `tech-lead`.
- Async lifecycle within the chosen shape → `python-async-and-concurrency`.
- Data layer specifics inside the chosen shape → `data-layer-python`.
- API contract shape → `api-contract-design`.
