---
name: event-driven-integration
description: Use when integrating a Go service via Kafka, RabbitMQ, NATS, or similar — designing event schemas, choosing delivery semantics, implementing outbox/saga, building idempotent consumers, handling poison messages and DLQ.
family: method
profile_level: Senior+
---

# Event-Driven Integration

## Purpose

Make asynchronous integration reliable and reasoned-about: explicit delivery semantics, schema discipline, idempotent consumers, observable backlogs. Treat the broker as part of the contract, not an implementation detail.

## Use When

- Adding a producer or consumer of events on a Go service.
- Designing the outbox or saga to keep state and events consistent.
- Reviewing a consumer for idempotency, error handling, and DLQ behavior.
- Sizing a topic/partition layout for known load.

## Do Not Use When

- The discussion is synchronous REST/gRPC contract — that is `api-contract-design`.
- The discussion is broker cluster operation — handoff to `devops-sre`.
- The discussion is data warehouse ingestion — handoff to `data-engineer`.

## Inputs

- Business event being modeled, its trigger, and downstream consumers.
- Required delivery semantics: at-most-once, at-least-once, effectively-once.
- Existing schema registry, broker, and operational tooling.
- Throughput, latency, ordering, and retention requirements.

## Workflow

1. Name the event in past tense (`OrderPlaced`, `PaymentRefunded`). The producer publishes facts, not commands.
2. Choose delivery semantics. Default to at-least-once + idempotent consumer. Effectively-once is a property of the consumer, not the broker.
3. Define the schema in a registry (Avro, JSON Schema, protobuf). Pin a `schema_id` or `event_version`. Additive evolution only.
4. Use the transactional outbox when the same transaction must change DB state and publish an event. Never publish from inside the request transaction directly to the broker.
5. Make consumers idempotent on the event key (event ID, aggregate ID + version). Store a processed-ID set with a TTL aligned with the broker retention.
6. Define DLQ policy: max retry attempts, backoff, what counts as poison, who owns the DLQ drain runbook.
7. Document ordering guarantees per topic: partition key, ordering scope (per-key, none).
8. Instrument: consumer lag, processing duration, retry rate, DLQ depth.

## Outputs

- Event catalogue with schema, version, owner, retention, ordering scope.
- Outbox table + dispatcher implementation, or explicit ADR if not used.
- Consumer idempotency key strategy.
- DLQ runbook.
- Dashboards: lag, throughput, error rate.

## Named Patterns

### Good — Transactional outbox
```sql
CREATE TABLE outbox (
    id UUID PRIMARY KEY,
    aggregate_id UUID NOT NULL,
    event_type TEXT NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    published_at TIMESTAMPTZ
);
```
```go
// Same DB transaction commits state and outbox row.
tx, _ := db.BeginTx(ctx, nil)
_, _ = tx.ExecContext(ctx, updateOrderSQL, ...)
_, _ = tx.ExecContext(ctx, insertOutboxSQL, ...)
_ = tx.Commit()
// A separate dispatcher reads unpublished rows and sends to Kafka.
```
State and event are atomically persisted; the dispatcher provides at-least-once delivery.

### Bad — Publish-then-commit
```go
producer.Send(ctx, event)        // succeeds
_ = tx.Commit()                  // fails → event without state
```
The world saw an event the database does not reflect. Reconciliation is manual.

### Good — Idempotent consumer keyed by event ID
```go
func (c *Consumer) Handle(ctx context.Context, msg Message) error {
    if seen, _ := c.store.Seen(ctx, msg.EventID); seen {
        return nil // duplicate; ack
    }
    if err := c.apply(ctx, msg); err != nil {
        return err // will be retried
    }
    return c.store.MarkSeen(ctx, msg.EventID, c.retentionTTL)
}
```

### Bad — Idempotency by "we don't expect duplicates"
The consumer code assumes the broker delivers exactly once. The first duplicate (broker rebalance, retry, replay) corrupts state.

### Good — Schema evolution
```protobuf
message OrderPlaced {
  string order_id = 1;
  int64 amount_cents = 2;
  // v2: added — optional
  string currency = 3;
}
```
Old consumers ignore the new field; new consumers handle absence.

### Bad — Breaking schema in place
The producer changes `amount_cents` from `int64` to `string` "for precision". Every consumer breaks on the next message.

### Good — DLQ with intent
- After N retries with exponential backoff → DLQ.
- DLQ has its own dashboard and an owner.
- Drain runbook covers: inspect, fix root cause, replay or discard.

### Bad — Silent retry forever
A consumer retries a poisoned message every 5 seconds for 14 days. Lag grows. The dashboard is green because the consumer is "running".

### Good — Ordering scope documented
"Topic `orders.events`: partitioned by `order_id`. Ordering guaranteed per-`order_id` only. Consumers must not assume cross-order ordering."

### Bad — Implicit global ordering
The team assumes events arrive in commit order across all aggregates. Multi-partition topology breaks this; debugging takes weeks.

### Good — Saga over distributed transaction
For a cross-service workflow (place order → reserve inventory → charge payment), use a saga with compensating actions. Each step is a local transaction + event. No 2PC.

### Bad — Distributed two-phase commit across HTTP services
Coordinator timeouts, in-doubt transactions, locked resources. The pattern that "feels safe" fails under partition.

## Boundaries

- Owns service-side production and consumption of events.
- Does not own the broker cluster, partitioning at the cluster level, retention policy at the platform level → `devops-sre`.
- Does not own the data lake/warehouse ingestion of these events → `data-engineer`.
- Schemas may be co-owned with `system-analyst` for business semantics.

## Sources

### Priority 1 — Protocol and platform canon
- Apache Kafka documentation — https://kafka.apache.org/documentation/
- NATS documentation — https://docs.nats.io/
- RabbitMQ documentation — https://www.rabbitmq.com/docs
- CloudEvents Specification — https://cloudevents.io/

### Priority 2 — Pattern canon
- Enterprise Integration Patterns — https://www.enterpriseintegrationpatterns.com/
- microservices.io — Saga, Outbox, Transactional Outbox — https://microservices.io/patterns/data/transactional-outbox.html
- Martin Kleppmann: Designing Data-Intensive Applications — book reference.

### Priority 3 — Background
- Confluent blog (schema evolution, exactly-once) — https://www.confluent.io/blog/
- Chris Richardson: Microservices Patterns — book reference.

## Handoff

- Broker cluster operation, retention, scaling → `devops-sre`.
- Data lake/warehouse ingestion → `data-engineer`.
- Business semantics of events → `system-analyst`.
- Synchronous contract surface → `api-contract-design`.
