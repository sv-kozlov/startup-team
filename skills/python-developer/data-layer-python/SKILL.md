---
name: data-layer-python
description: Use when designing or changing the data access layer of a Python service — SQLAlchemy 2.x async, asyncpg, Alembic forward-compatible migrations, transaction boundary discipline, N+1 query protection, and Redis async cache or queue access. Does not own the database cluster or schema outside the service boundary.
family: code
profile_level: Senior+
---

# Data Layer Python

## Purpose

Design the data access layer of a Python service so it is correct by transaction boundary, safe to evolve with forward-compatible migrations, observable under load, and decoupled from business logic.

## Use When

- Designing or reviewing the repository layer of a Python service.
- Writing or reviewing an Alembic migration.
- Diagnosing N+1 query patterns or slow query plans.
- Adding Redis caching or rate-limiting to a service.
- Reviewing transaction boundaries across use-case operations.

## Do Not Use When

- The task is database cluster configuration, index creation in production, or DBA-level tuning → handoff to `devops-sre`.
- The task is a data warehouse ETL or data pipeline → handoff to `data-engineer`.
- The task is service package and DI wiring → `python-service-design`.

## Inputs

- Domain model being persisted (entities, value objects, aggregates).
- Target database: Postgres (primary), Redis (cache/queue), or NoSQL.
- Migration history: existing Alembic revision chain.
- Query load profile: read-heavy, write-heavy, or mixed.

## Workflow

1. Map domain entities to ORM models using SQLAlchemy 2.x mapped classes (`Mapped`, `mapped_column`). Keep ORM models in `infrastructure/`; convert to/from domain objects at the repository boundary.
2. Use `async_sessionmaker` with `expire_on_commit=False` (avoids lazy loads after commit in async context).
3. Apply transactions at the use-case boundary, not the repository boundary. A use-case either commits or raises; the repository never commits autonomously.
4. Write Alembic migrations with the expand/migrate/contract pattern for zero-downtime deploys: (1) add nullable column, (2) backfill, (3) add NOT NULL constraint.
5. Identify N+1 risks: any `relationship()` without `lazy="selectin"` or explicit `selectinload`/`joinedload` in queries is a potential N+1.
6. Add query plan review for new queries touching large tables: `EXPLAIN ANALYZE` output in PR description; confirm index is used.
7. For Redis: use `redis.asyncio` (redis-py async); set TTL explicitly on every key; never use unbounded `KEYS *`; use `SCAN` for iteration.

## Outputs

- Repository classes implementing domain `Protocol` interfaces.
- Alembic migration files with up and down scripts.
- Query plan snippet in PR description for expensive queries.
- Redis key naming convention and TTL policy documented in ADR or `README.md`.

## Named Patterns

### Good — SQLAlchemy 2.x mapped class with domain conversion
```python
# infrastructure/persistence/order_orm.py
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Numeric
from uuid import UUID
from decimal import Decimal

class Base(DeclarativeBase):
    pass

class OrderModel(Base):
    __tablename__ = "orders"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(String(32))
    total: Mapped[Decimal] = mapped_column(Numeric(12, 2))

    def to_domain(self) -> Order:
        return Order(id=self.id, status=OrderStatus(self.status), total=self.total)

    @classmethod
    def from_domain(cls, order: Order) -> "OrderModel":
        return cls(id=order.id, status=order.status.value, total=order.total)
```
ORM model stays in infrastructure; domain is a pure Python dataclass; no SQLAlchemy in domain layer.

### Bad — SQLAlchemy model as domain entity
```python
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Order(Base):  # domain entity is also the ORM model
    __tablename__ = "orders"
    id = Column(String, primary_key=True)
    status = Column(String)
    # business methods mixed with ORM concerns
    def place(self): ...
```
Domain imports SQLAlchemy; unit tests require a database; swapping ORM requires domain rewrite.

### Good — Transaction at use-case boundary
```python
async def place_order(
    cmd: PlaceOrderCommand,
    session: AsyncSession,
    repo: OrderRepository,
    payment: PaymentCharger,
) -> OrderID:
    async with session.begin():  # transaction wraps the whole use-case
        order = Order.create(cmd.items)
        tx_id = await payment.charge(order.total, cmd.idempotency_key)
        order.confirm(tx_id)
        await repo.save(order)
    return order.id
    # commit happens on __aexit__; exception triggers rollback
```
Transaction boundary matches the unit of work; repository never commits.

### Bad — Transaction inside repository
```python
class OrderRepository:
    async def save(self, order: Order) -> None:
        async with self._session.begin():  # repo commits!
            self._session.add(OrderModel.from_domain(order))
```
Two repositories in one use-case open two transactions; cannot atomically save order + outbox event.

### Good — Alembic expand/migrate/contract for zero-downtime column rename
```python
# Migration step 1 — expand: add new column
def upgrade():
    op.add_column("orders", sa.Column("currency_code", sa.String(3), nullable=True))

# Migration step 2 — migrate: backfill (run separately)
# UPDATE orders SET currency_code = currency WHERE currency_code IS NULL;

# Migration step 3 — contract: make NOT NULL, drop old column (separate deploy)
def upgrade():
    op.alter_column("orders", "currency_code", nullable=False)
    op.drop_column("orders", "currency")
```
Each migration is deployed independently; old app version and new app version coexist safely during rollout.

### Bad — Immediate NOT NULL on large table
```python
def upgrade():
    op.add_column("orders", sa.Column("currency_code", sa.String(3), nullable=False))
```
Table lock on Postgres during migration; migration fails if any existing row has no value; downtime on large tables.

### Good — N+1 protection with selectinload
```python
stmt = select(OrderModel).options(selectinload(OrderModel.items))
result = await session.execute(stmt)
orders = result.scalars().all()
# items are loaded in one additional query, not N queries
```

### Bad — Implicit lazy load (N+1)
```python
orders = (await session.execute(select(OrderModel))).scalars().all()
for order in orders:
    print(order.items)  # triggers N separate SELECT queries in async context → DetachedInstanceError or N+1
```

## Boundaries

- Owns service-level data access: repositories, migrations, query optimization within the service.
- Does not own database cluster, connection pool max_connections, or backup strategy → `devops-sre`.
- Does not own shared database schemas accessed by multiple services → `system-architect`.
- Does not own data warehouse ETL → `data-engineer`.

## Sources

### Priority 1 — Data layer canon
- SQLAlchemy 2.x documentation — https://docs.sqlalchemy.org/
- asyncpg documentation — https://magicstack.github.io/asyncpg/
- Alembic documentation — https://alembic.sqlalchemy.org/
- redis-py async documentation — https://redis-py.readthedocs.io/

### Priority 2 — Reliability and migration practice
- The Twelve-Factor App (backing services) — https://12factor.net/backing-services
- Google SRE Book — https://sre.google/sre-book/table-of-contents/

### Priority 3 — Pattern background
- microservices.io: Shared Database anti-pattern — https://microservices.io/patterns/data/shared-database.html
- martinfowler.com on Repository pattern — https://martinfowler.com/eaaCatalog/repository.html

## Handoff

- Database cluster, connection pool, backup strategy → `devops-sre`.
- Shared database schema across services → `system-architect`.
- Data warehouse ETL and pipelines → `data-engineer`.
- Transaction boundary across services (saga) → `event-driven-integration`.
