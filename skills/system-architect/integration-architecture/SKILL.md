---
name: integration-architecture
description: Use when an integration approach between components or systems must be chosen at the architectural level — selecting synchronous vs asynchronous, API-first or contract-first, event-driven patterns, messaging topology, cross-cutting delivery properties, or gateway and broker governance. Not for writing detailed API contracts or operating brokers.
family: method
profile_level: Senior+
---

# Integration Architecture

## Purpose

Define how systems and components interact: synchronous APIs, asynchronous events, messaging, contracts, and integration patterns at the architectural level. Produce integration decisions that are explicit, measurable against NFRs, and traceable to ADRs — without absorbing detailed specification or platform operation work.

## Use When

- An integration approach between components or systems must be chosen (REST, gRPC, events, queues, CDC, file, batch).
- API-first or contract-first must be applied across component boundaries.
- Asynchronous patterns — events, sagas, outbox, CDC, competing consumers — must be evaluated.
- Cross-system flows need an architectural map, protocol selection, and contract governance decision.
- Delivery guarantee, idempotency, retry, ordering, and backpressure rules must be set at the architectural level.
- An integration ADR must be authored for a significant flow or topology change.

## Do Not Use When

- The task is writing detailed OpenAPI, AsyncAPI, or protobuf specs → handoff to `system-analyst`.
- The task is operating, sizing, or configuring message brokers or API gateways → handoff to `devops-sre`.
- The task is choosing integration patterns within a single bounded context (internal module calls) → `component-and-service-decomposition`.
- The task is data platform ingestion, lake pipelines, or streaming analytics → handoff to data-engineer / data-architect.
- The task is setting NFR targets (latency SLO, throughput) rather than choosing the pattern that meets them → `non-functional-architecture`.

## Inputs

- Functional flows and business processes crossing component or system boundaries.
- NFRs per flow: latency, throughput, consistency model (strong / eventual / causal), availability, ordering, retry semantics, idempotency requirement.
- Existing integration landscape: brokers, gateways, contracts, and legacy protocols.
- Constraints: vendor systems, regulatory rules (GDPR, PCI-DSS data flows), security, network topology, organizational boundary.
- Bounded context map from `component-and-service-decomposition`.

## Workflow

1. **Map cross-boundary flows.** For each flow: source, sink, payload type, frequency (sync request / async event / batch), criticality, and SLO.
2. **Choose integration style per flow.** Decision tree: Can the caller wait? → synchronous (REST/gRPC). Can the caller fire-and-forget or tolerate eventual delivery? → asynchronous event or queue. Does volume or schedule require batching? → batch/file. Apply the simplest style that satisfies NFRs.
3. **Choose protocol and contract approach.** Synchronous: REST (HTTP/2, resource-oriented, OpenAPI) or gRPC (protobuf, streaming, strong typing). Asynchronous: event schema (AsyncAPI, Avro, protobuf), broker choice (Kafka for ordered durability, RabbitMQ for flexible routing, NATS for low-latency). Record rationale in an ADR.
4. **Define cross-cutting integration properties.** Per flow: idempotency key strategy, retry policy (exponential backoff + jitter, dead-letter queue), ordering guarantee (partition key, sequencing), delivery guarantee (at-least-once with consumer idempotency vs exactly-once via transactional outbox).
5. **Define gateway and broker governance.** API gateway: authentication, rate limiting, request routing, versioning policy. Broker: schema registry, topic naming convention, retention, consumer group ownership.
6. **Assess synchronous coupling risk.** Chains of synchronous calls create latency multiplication and availability coupling. Convert to async where the downstream SLA is looser than the caller's SLA; record the boundary in the integration ADR.
7. **Record integration ADRs.** One ADR per significant flow type change or topology decision. Link to bounded context map and NFR catalog.
8. **Hand off contract detail.** Integration architecture defines the protocol, pattern, and cross-cutting rules. API contract authoring (OpenAPI, AsyncAPI schema) goes to `system-analyst`.

## Outputs

- Integration architecture brief with flow map, pattern choice per flow, and rationale.
- Cross-cutting integration rules: idempotency strategy, retry policy, ordering, delivery guarantees, backpressure.
- Gateway and broker governance note.
- Integration ADRs.
- Handoff items for `system-analyst` (contract authoring), `devops-sre` (broker/gateway operation), `security-and-observability-by-design` (trust boundaries on integration flows).

## Named Patterns

### Good — Async choice justified by NFR mismatch
```
OrderService SLA: 99.9% at p99 < 200ms.
NotificationService SLA: best-effort, p99 < 5s.
Decision: OrderService publishes OrderPlaced event to Kafka; NotificationService consumes.
OrderService availability is not coupled to NotificationService availability.
ADR-012: Event-driven notification decoupling.
```

### Bad — Default REST everywhere
All 12 service-to-service calls are synchronous REST. PaymentService calls FraudService calls ProfileService. A 200ms spike in ProfileService causes p99 > 600ms on payment checkout. No delivery guarantee, retry propagates load.

### Good — Transactional outbox for exactly-once event publishing
```sql
-- Same transaction: update order state AND insert outbox row
INSERT INTO outbox (aggregate_id, event_type, payload, created_at)
VALUES (:order_id, 'OrderPlaced', :payload, now());
```
Relay process polls outbox and publishes to Kafka. Consumer deduplicates by event ID. No dual-write inconsistency.

### Bad — Dual write (database + broker)
```
db.save(order);          // succeeds
broker.publish(event);   // fails silently
```
Downstream consumers never see the event. State diverges. No dead-letter queue, no replay.

### Good — Schema evolution with backward compatibility
Producer adds an optional field to the Avro schema. Old consumers ignore the field. New consumers use it. Schema registry enforces compatibility rules. No coordination deployment required.

### Bad — Breaking schema change in shared contract
Producer renames a required field. Three consumers fail on startup after deployment. Schema registry not used; compatibility not checked. Rollback requires coordinated multi-service redeploy.

### Good — Idempotency key on sync API
```
POST /payments
Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000
```
Server stores result keyed by idempotency key; duplicate requests return cached response. Network retry is safe.

### Bad — Non-idempotent mutation with retry
POST /payments with auto-retry on 5xx. No idempotency key. Each retry creates a new charge. Customer is billed three times.

## Boundaries

- Does not write detailed API contracts, OpenAPI files, AsyncAPI schemas, or message schemas → `system-analyst`.
- Does not own broker, gateway, or platform operation — sizing, deployment, runbooks → `devops-sre`.
- Does not own data platform integration contracts as a separate platform → data-engineer / data-architect.
- Does not own security implementation on integration flows → `security-and-observability-by-design` for design, `security-engineer` for audit.

## Sources

### Priority 1 — Canonical References
- Gregor Hohpe — Enterprise Integration Patterns: https://www.enterpriseintegrationpatterns.com/
- AsyncAPI specification: https://www.asyncapi.com/docs/reference/specification/v3.0.0
- OpenAPI Specification: https://spec.openapis.org/oas/v3.1.0
- microservices.io — communication patterns: https://microservices.io/patterns/communication-style/index.html
- Martin Kleppmann — Designing Data-Intensive Applications (ch. 11, streaming): https://dataintensive.net/

### Priority 2 — Practitioner Guidance
- Microsoft Azure Architecture Center — messaging patterns: https://learn.microsoft.com/azure/architecture/patterns/category/messaging
- AWS Well-Architected Framework — event-driven architectures: https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html
- Sam Newman — Building Microservices, ch. 4 (integration): https://samnewman.io/books/building_microservices/
- Confluent — Kafka design patterns and schema registry: https://docs.confluent.io/platform/current/schema-registry/index.html

### Priority 3 — Supplementary
- InfoQ — event-driven architecture articles: https://www.infoq.com/event-driven-architecture/
- NATS documentation — messaging patterns: https://docs.nats.io/

## Handoff

- Detailed API contract authoring (OpenAPI, AsyncAPI, protobuf files) → `system-analyst`.
- Broker and gateway operation, sizing, runbook, monitoring → `devops-sre`.
- Trust boundary and AuthN/AuthZ design on integration flows → `security-and-observability-by-design`.
- NFR target-setting for the chosen integration pattern → `non-functional-architecture`.
- Recording the integration topology decision → `architecture-decision-records`.
