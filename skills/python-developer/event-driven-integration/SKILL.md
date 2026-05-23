---
name: event-driven-integration
description: Use when integrating a Python service via a message broker (Kafka, RabbitMQ, Celery), designing an async event flow, or making a consumer idempotent. Covers transactional outbox, saga/process manager, delivery semantics, DLQ strategy, and schema evolution for events.
family: method
profile_level: Senior+
---

# Event-Driven Integration

## Purpose

Design and implement async integration between services so that messages are delivered reliably, processed exactly once (or idempotently), and failures are observable and recoverable — without creating tightly coupled synchronous chains.

## Use When

- A Python service needs to publish or consume events via Kafka, RabbitMQ, or Celery.
- Designing a distributed transaction that spans multiple services.
- An existing consumer is causing duplicate processing or silent data loss.
- Reviewing an async integration for delivery guarantees or DLQ coverage.

## Do Not Use When

- The integration is synchronous REST or gRPC → `api-contract-design`.
- The task is async task lifecycle (asyncio TaskGroup) → `python-async-and-concurrency`.
- The task is broker cluster configuration or Kafka topic management → handoff to `devops-sre`.

## Inputs

- Business event that triggers the integration (e.g., `OrderPlaced`).
- Producer and consumer service boundaries.
- Required delivery semantics: at-least-once, at-most-once, effectively-once.
- Schema registry or agreed schema format (Avro, Protobuf, JSON Schema).

## Workflow

1. Name the event in past tense from the domain perspective: `OrderPlaced`, `PaymentFailed`, `UserCreated`.
2. Choose delivery semantics: at-least-once is the default for Kafka and RabbitMQ. Design consumers to be idempotent; avoid at-most-once unless data loss is acceptable.
3. Use the transactional outbox pattern when the producer must atomically persist a domain change and emit an event. Insert the event into an outbox table within the same DB transaction; a relay process polls and publishes.
4. For multi-service distributed flows, model the coordination as a saga: choreography (events trigger reactions) for simple flows; orchestration (process manager holds state) for complex or compensatable flows.
5. Make every consumer idempotent: check a deduplication key before processing; store the key in the same transaction that applies the effect.
6. Design a DLQ strategy: after N retries, route to a DLQ topic/queue; add alerting on DLQ depth.
7. Version event schemas additively; never remove or rename a field without a deprecation window.

## Outputs

- Event schema (Pydantic model, protobuf, or JSON Schema) in a versioned location.
- Outbox table migration (if transactional outbox is used).
- Consumer with idempotency check.
- DLQ configuration and alerting rule.

## Named Patterns

### Good — Transactional outbox with SQLAlchemy
```python
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from datetime import datetime, timezone
import json

class OutboxEvent(Base):
    __tablename__ = "outbox_events"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    event_type: Mapped[str]
    payload: Mapped[str]  # JSON
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    published_at: Mapped[datetime | None] = mapped_column(default=None)

async def place_order_and_enqueue(
    cmd: PlaceOrderCommand,
    session: AsyncSession,
) -> OrderID:
    order = Order.create(cmd.items)
    session.add(order.to_orm())
    session.add(OutboxEvent(
        event_type="OrderPlaced",
        payload=json.dumps({"order_id": str(order.id), "total": str(cmd.total)}),
    ))
    await session.commit()  # atomic: order + event in one transaction
    return order.id
```
Domain change and event emission are atomic; no two-phase commit; relay polls and publishes.

### Bad — Direct publish inside domain transaction
```python
async def place_order(cmd, session, kafka_producer):
    order = Order.create(cmd.items)
    session.add(order.to_orm())
    await session.commit()
    await kafka_producer.send("orders", OrderPlaced(order.id))  # NOT atomic
```
If Kafka publish fails after DB commit, event is lost. If commit fails after Kafka send, duplicate event.

### Good — Idempotent consumer with deduplication key
```python
async def handle_payment_completed(event: PaymentCompleted, session: AsyncSession) -> None:
    exists = await session.execute(
        select(ProcessedEvent).where(ProcessedEvent.event_id == event.event_id)
    )
    if exists.scalar_one_or_none():
        return  # already processed; safe to skip

    order = await session.get(Order, event.order_id)
    order.mark_paid(event.transaction_id)
    session.add(ProcessedEvent(event_id=event.event_id))
    await session.commit()  # dedup key stored in same transaction
```
Replay of the same event is a no-op; dedup key committed atomically with the state change.

### Bad — Non-idempotent consumer
```python
async def handle_payment_completed(event):
    order = await get_order(event.order_id)
    order.mark_paid(event.transaction_id)
    await save(order)
    # No dedup check; broker retries cause duplicate charges
```

### Good — Choreography saga for simple flow
```
OrderPlaced → PaymentService: charge
PaymentCharged → OrderService: confirm
PaymentFailed → OrderService: cancel (compensating)
```
Each service reacts to events; no central coordinator; each step is idempotent.

### Bad — Distributed synchronous chain disguised as events
```python
async def on_order_placed(event):
    payment_result = await payment_service.charge(...)  # sync RPC inside event handler
    await order_service.confirm(...)  # another sync RPC
```
Loses all benefits of async; both services must be available simultaneously; error propagation is synchronous.

## Boundaries

- Owns event schema, producer/consumer lifecycle, and idempotency within the Python service.
- Does not own broker cluster configuration, topic creation, or Kafka Connect → `devops-sre`.
- Does not own data warehouse ingestion from events → `data-engineer`.
- Does not own synchronous API contracts → `api-contract-design`.

## Sources

### Priority 1 — Broker and pattern canon
- Apache Kafka documentation — https://kafka.apache.org/documentation/
- RabbitMQ documentation — https://www.rabbitmq.com/documentation.html
- Celery documentation — https://docs.celeryq.dev/
- aiokafka documentation — https://aiokafka.readthedocs.io/

### Priority 2 — Distributed systems patterns
- microservices.io: Transactional Outbox — https://microservices.io/patterns/data/transactional-outbox.html
- microservices.io: Saga — https://microservices.io/patterns/data/saga.html
- Google SRE Book — https://sre.google/sre-book/table-of-contents/

### Priority 3 — Background
- martinfowler.com on event-driven architecture — https://martinfowler.com/articles/201701-event-driven.html

## Handoff

- Broker cluster and topic management → `devops-sre`.
- Data warehouse ingestion from events → `data-engineer`.
- Synchronous API contracts → `api-contract-design`.
- Async task lifecycle (TaskGroup, CancelledError) → `python-async-and-concurrency`.
