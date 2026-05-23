---
name: event-driven-integration
description: Use when specifying asynchronous event contracts, message schemas, topic/queue ownership, delivery semantics, idempotency, retry and DLQ behavior, consumer coordination, and observability requirements for event-driven or message-broker-based flows.
family: method
profile_level: Senior+
---

# Event-Driven Integration

## Purpose

Specify asynchronous event interactions so that producer, consumer, broker administration, and operations teams share an unambiguous understanding of event meaning, schema, delivery obligations, failure recovery, and ownership. Async systems fail silently when contracts are informal — this skill makes the contract explicit before implementation begins.

## Use When

- A feature uses Kafka, RabbitMQ, SQS, or another message broker to decouple producer from consumer.
- Event schema, topic/queue ownership, delivery semantics, or consumer coordination is unclear.
- Idempotency, retry strategy, DLQ handling, or replay requirements need to be specified.
- A feature requires asynchronous consistency, eventual state propagation, or event-driven saga behavior.
- An existing event contract is changing and consumer-impact and rollout must be assessed.

## Do Not Use When

- The integration is synchronous request-response — use `integration-analysis` or `api-contract-design`.
- The task is multi-system integration scenario covering multiple mechanisms — use `integration-analysis` for the overall scenario, then this skill for the async leg.
- The task is broker provisioning, topic/queue configuration, or cluster management — hand off to `devops-sre`.
- The task is building a data pipeline, streaming ETL, or DWH from the event stream — hand off to `data-engineer`.

## Inputs

- Business event: what domain occurrence the event represents (not a technical trigger — a business fact).
- Producer: service, team owner, and emission conditions (state transitions, commands, integration triggers).
- Consumers: services, team owners, and what each consumer does with the event.
- Broker type and configuration context: Kafka, RabbitMQ, SQS, or equivalent.
- Ordering requirements: global, per-partition, per-entity, or none.
- SLA: latency tolerance, delivery guarantee, and consumer processing budget.
- Known idempotency, replay, and retention requirements.

## Workflow

1. State the event's business meaning. Name it in past tense (OrderConfirmed, PaymentFailed, InventoryReserved). The name must be in the ubiquitous language — unambiguous to all teams. Confirm: is this a notification (fact broadcast), command (instruction to one consumer), or domain event (state change with multiple downstream consequences)?
2. Identify producer, consumers, topic/queue, and ownership. For each consumer: what does it do with the event, what is its SLA, and who owns it?
3. Specify the event schema. Use AsyncAPI 2.x format as the contract artifact:
   - Required fields: event type, event version, event ID (UUID for deduplication), aggregate ID, timestamp.
   - Payload fields: field name, type, required/optional, validation constraints, example values.
   - Header fields: correlation ID, trace ID, tenant ID if multi-tenant.
4. Define delivery semantics and their consequences:
   - At-most-once: events may be lost; acceptable for non-critical notifications only.
   - At-least-once: events may be duplicated; consumers must be idempotent.
   - Exactly-once: only when broker and consumer both support it (Kafka transactions); document the cost.
5. Specify idempotency: the consumer's idempotency key (event_id + aggregate_id combination), the deduplication window, and what happens on a detected duplicate (skip, log, alert).
6. Define retry policy: maximum retries, backoff strategy, maximum retry age. Define DLQ: topic/queue name, retention period, alert trigger, and the process for replaying or discarding DLQ messages.
7. Specify ordering requirements: global ordering is expensive — justify it. Per-partition ordering by entity ID is standard in Kafka. Unordered is safe for idempotent consumers.
8. Specify schema compatibility and evolution: backward-compatible additions only (new optional fields); breaking changes require a new event version and a consumer migration window. Reference the versioning policy in `api-contract-design` for consistency.
9. Specify observability: mandatory log events (produced, consumed, failed, retried, DLQ'd), consumer lag metric, alert thresholds, and trace ID propagation. Hand off implementation to `devops-sre`.
10. Document rollout: who deploys first (producer before consumer), compatibility window, and rollback procedure.

## Outputs

- Event contract: AsyncAPI 2.x schema outline or equivalent.
- Producer/consumer ownership table.
- Delivery semantics decision with rationale.
- Idempotency specification: key, deduplication window, duplicate behavior.
- Retry/DLQ policy: retries, backoff, DLQ name, replay process.
- Ordering requirements and partition key specification.
- Schema evolution and versioning policy.
- Observability requirements (metrics, logs, alerts) — for handoff to `devops-sre`.
- Rollout and migration plan.

## Named Patterns

### Good — Event named as business fact
```
Event: OrderConfirmed
Meaning: A customer order has been accepted, payment captured, and is now pending fulfillment.
Producer: Order Service
Consumers: Notification Service (send confirmation email), Inventory Service (reserve stock),
           Fulfillment Service (create shipment task), Data Platform (analytics stream)
Topic: order-events (Kafka), partitioned by tenant_id
```
Name, meaning, producer, all consumers, and routing — explicit before schema design begins.

### Bad — Event named as technical trigger
"order_updated" — consumers cannot tell what changed or why. Does this mean status changed? An address was corrected? A line item was added? Every consumer must read the diff.

### Good — AsyncAPI-style event schema outline
```yaml
asyncapi: "2.6.0"
channels:
  order-events:
    subscribe:
      message:
        name: OrderConfirmed
        payload:
          type: object
          required: [event_id, event_type, event_version, order_id, tenant_id, occurred_at]
          properties:
            event_id:      { type: string, format: uuid }
            event_type:    { type: string, const: "OrderConfirmed" }
            event_version: { type: integer, const: 1 }
            order_id:      { type: string, format: uuid }
            tenant_id:     { type: string }
            occurred_at:   { type: string, format: date-time }
            total_amount:  { type: number }
            currency:      { type: string }
```
Every consumer knows the exact schema; idempotency key is present; version is explicit.

### Bad — Event schema as "we'll figure it out in code"
Producer pushes raw domain object. Consumers receive internal implementation details; coupling is tight; any internal refactor breaks all consumers.

### Good — Idempotency key specification
```
Idempotency key: composite of (event_id, consumer_id)
Deduplication window: 24 hours (TTL in consumer's processed-events store)
Duplicate action: skip processing; log {event_id, consumer_id, detected_at} at INFO level.
Not-a-duplicate: any event not present in the processed-events store.
Consumer owns the deduplication store; broker delivery guarantee is at-least-once.
```
Consumer can implement correctly; QA can write a replay test.

### Bad — "Consumers should handle duplicates"
No key, no window, no log requirement. Each consumer implements a different strategy (or none). Duplicate orders, double notifications, incorrect inventory counts.

### Good — DLQ policy
```
DLQ topic: order-events-dlq
Trigger: event fails processing after 3 retries with exponential backoff (1s, 2s, 4s)
Retention: 7 days
Alert: PagerDuty P2 when DLQ depth > 0 for > 5 minutes
Replay process: Finance Ops reviews, approves, and triggers replay via ops-console UI
Auto-discard: events older than 7 days; logged before discard.
Owner of replay decision: Finance Ops; owner of replay tooling: Platform Engineering.
```
On-call knows what to do; operations has a clear process; no event silently disappears.

### Bad — DLQ exists but no process
Events accumulate in DLQ. Nobody owns replay. Six months later: DLQ has 10,000 events; nobody knows which are safe to replay or discard.

## Boundaries

- Owns: event contract specification, delivery semantics, idempotency, retry/DLQ, schema evolution.
- Does not own: broker provisioning, topic/queue configuration, cluster management — `devops-sre`.
- Does not own: data pipeline, streaming ETL, or analytical consumer implementation — `data-engineer`.
- Does not own: synchronous integration scenario — `integration-analysis`.
- Does not own: single REST/gRPC API contract — `api-contract-design`.
- Does not own: saga orchestration or distributed transaction architecture — `system-architect`.

## Sources

### Priority 1 — Protocol and broker canon
- AsyncAPI Specification 2.x — https://www.asyncapi.com/docs/reference/specification/v2.6.0
- Apache Kafka documentation — https://kafka.apache.org/40/design/design/
- RabbitMQ reliability guide — https://www.rabbitmq.com/docs/reliability
- RabbitMQ dead letter exchanges — https://www.rabbitmq.com/docs/next/dlx

### Priority 2 — Integration patterns
- Enterprise Integration Patterns — https://www.enterpriseintegrationpatterns.com/
- Martin Fowler: Event-driven architecture — https://martinfowler.com/articles/201701-event-driven.html

### Priority 3 — Background
- Vaughn Vernon: Implementing Domain-Driven Design — book reference (domain events chapter)
- ThoughtWorks Technology Radar — https://www.thoughtworks.com/radar

## Handoff

- Broker provisioning, topic/queue configuration, consumer lag alerting → `devops-sre`.
- Data pipeline or streaming ETL from the event stream → `data-engineer`.
- Synchronous integration scenario covering multiple systems → `integration-analysis`.
- REST/gRPC contract for the service that emits events → `api-contract-design`.
- Saga or distributed transaction architecture decision → `system-architect`.
