---
name: integration-analysis
description: Use when analyzing and specifying system-to-system interaction — synchronous API calls, asynchronous message flows, data exchanges, field mappings, retry/error behavior, reconciliation, and cross-team ownership responsibilities for an integration scenario.
family: method
profile_level: Senior+
---

# Integration Analysis

## Purpose

Specify how systems interact and what each side must send, receive, validate, store, and recover from — completely enough that consuming and providing teams can implement, test, and operate the integration without recurring ambiguity. Surface cross-team ownership risks before implementation begins.

## Use When

- A feature requires two or more systems or teams to exchange data or coordinate behavior.
- The integration mechanism, data payload, error handling, or ownership boundary is unclear.
- A data flow, mapping, or transformation between systems must be documented.
- Retry, timeout, idempotency, or reconciliation requirements need to be specified.
- An existing integration is changing and the consumer-impact and rollout plan must be assessed.

## Do Not Use When

- The integration is a single API contract within one team — use `api-contract-design` for the contract spec.
- The integration is purely async event-based and requires deep delivery semantics, DLQ design, or broker-specific behavior — use `event-driven-integration`.
- Infrastructure implementation (broker provisioning, network policies, load balancers) — hand off to `devops-sre`.
- Data pipeline or ETL/ELT implementation — hand off to `data-engineer`.

## Inputs

- Business scenario: what business process or user journey triggers the integration.
- Participating systems: name, team owner, current SLA, known limitations.
- Data entities and field mappings from `data-modeling`.
- Existing contracts, API docs, or message schemas for the systems involved.
- Constraints: SLA, latency budget, security classification, regulatory rules.
- Known error conditions, retry expectations, and idempotency requirements.

## Workflow

1. Identify participating systems and their owners. For each system: who owns it, what team deploys it, what its documented SLA is, and what its failure modes are.
2. Determine interaction type: synchronous request-response, asynchronous message (event/command), batch/file exchange, or hybrid. Document the rationale for the choice.
3. Define the trigger: what event, user action, scheduled job, or upstream system action initiates this integration. State the exact trigger condition.
4. Specify the data payload for each direction of exchange: fields, types, required/optional, validation rules, allowed values, transformation rules, and examples. Use the ubiquitous language — no synonyms across systems.
5. Define error handling: list each error condition (source system failure, timeout, validation failure, business rule violation), the system response (retry, fallback, DLQ, alert), and the recovery path. State who owns each error response action.
6. Define idempotency: can the interaction be replayed safely? What is the correlation key? What is the duplicate detection window? If not idempotent, document the consequence and the safeguard.
7. Specify retry and timeout policy: maximum retries, backoff strategy (linear/exponential), timeout per attempt, circuit-breaker conditions. Align with the upstream SLA.
8. Define reconciliation: how does the system detect and resolve inconsistency between the two sides? Frequency, comparison key, action on mismatch, and owner of reconciliation logic.
9. Specify observability requirements for the integration path: correlation ID propagation, mandatory log events, latency metrics, and failure alerts. Hand off implementation to `devops-sre`.
10. Document rollout and compatibility: is this a new integration or a change to an existing one? Who must deploy first? What is the rollback plan? What backward compatibility obligation exists?

## Outputs

- Integration scenario: trigger, participating systems, interaction type, direction, and data payload.
- Data-flow and field mapping table: source field → target field, transform, validation, default.
- Error/retry/reconciliation requirements.
- Idempotency specification.
- Cross-team ownership and responsibility matrix.
- Rollout and compatibility notes.
- Observability and monitoring requirements handoff.

## Named Patterns

### Good — Integration scenario header
```
Integration: Order Confirmation → Notification Service
Trigger: OrderConfirmed event emitted by Order Service after payment capture.
Direction: Order Service (producer) → Notification Service (consumer).
Mechanism: Async, Kafka, topic order-events, partition by tenant_id.
Owner: Order Platform team (producer); Messaging team (consumer).
SLA dependency: Notification Service targets best-effort delivery < 5s; no delivery guarantee required.
```
Every team knows who owns what; no ambiguity about synchronous vs async.

### Bad — Integration described in one sentence
"Order Service calls Notification Service when an order is confirmed." Mechanism unknown; payload unknown; error handling unknown; owner unknown.

### Good — Field mapping table entry
```
Source: Payment Gateway webhook — "charge.captured" event
  Field: charge.id          → payments.external_reference (varchar 64, required, strip whitespace)
  Field: charge.amount      → payments.amount_cents (int64, required; value in smallest currency unit)
  Field: charge.currency    → payments.currency (ISO 4217, required, UPPERCASE)
  Field: charge.customer_id → payments.gateway_customer_id (varchar 128, optional)
  Field: charge.metadata.order_id → payments.order_id (UUID, required; validation: must exist in orders table)
Transformation: amount — no conversion; gateway already sends cents.
Missing order_id: reject with 422, code MISSING_ORDER_REFERENCE; log and alert.
```
Engineering can implement without asking questions; QA knows exactly what to test.

### Bad — "Map the fields"
"Map the payment gateway response to our payments table." No field list, no types, no transformation, no error handling for missing required fields.

### Good — Retry and timeout policy
```
Call: Order Service → Warehouse API (synchronous, order fulfillment request)
Timeout per attempt: 3000 ms
Retry: 3 attempts with exponential backoff (1s, 2s, 4s)
Circuit breaker: open after 5 consecutive failures in 30s; half-open after 60s
On circuit-open: order status set to PendingFulfillment; background retry job runs every 5 min
On final failure: alert on-call (P2); order remains Confirmed; do not cancel automatically.
Owner of retry logic: Order Service (Engineering).
Owner of fulfillment status: Warehouse team.
```
SRE knows what to alert on; Engineering knows what to implement; behavior on failure is explicit.

### Bad — "Handle errors gracefully"
No timeout, no retry count, no circuit-breaker condition, no failure behavior. Each developer interprets "gracefully" differently.

### Good — Reconciliation specification
```
Reconciliation: Payment status between OMS and Payment Gateway
Frequency: nightly at 02:00 UTC, full comparison for orders modified in past 48h
Key: payments.external_reference = charge.id
Mismatch action: log to reconciliation_errors table; send Slack alert to Finance Ops channel
Ownership: Data Platform team runs the reconciliation job; OMS provides the data endpoint.
Resolution SLA: Finance Ops resolves within 1 business day.
```
Finance Ops knows their obligation; Data Platform knows what to build; OMS knows what to expose.

### Bad — Reconciliation implied
"We can always check the gateway portal." Manual, unscalable, and untested. Discovered in production during a charge-order mismatch incident.

## Boundaries

- Owns: integration scenario specification, cross-system payload mapping, error/retry/reconciliation requirements, cross-team ownership matrix.
- Does not own: async delivery semantics, DLQ design, broker-specific configuration — `event-driven-integration`.
- Does not own: API wire contract (single interface) — `api-contract-design`.
- Does not own: infrastructure implementation, broker provisioning — `devops-sre`.
- Does not own: data pipeline and ETL/ELT construction — `data-engineer`.
- Does not own: architecture pattern decision (e.g., saga vs 2PC) — `system-architect`.

## Sources

### Priority 1 — Integration standards
- Enterprise Integration Patterns — https://www.enterpriseintegrationpatterns.com/
- Microsoft REST API design for microservices — https://learn.microsoft.com/en-us/azure/architecture/microservices/design/api-design
- Karl Wiegers, Joy Beatty: Software Requirements, 3rd ed. — book reference (integration requirements chapter)

### Priority 2 — Messaging and event systems
- Apache Kafka design — https://kafka.apache.org/40/design/design/
- RabbitMQ reliability guide — https://www.rabbitmq.com/docs/reliability
- AsyncAPI Specification 2.x — https://www.asyncapi.com/docs/reference/specification/v2.6.0

### Priority 3 — Pattern background
- microservices.io integration patterns — https://microservices.io/patterns/
- ThoughtWorks Technology Radar — https://www.thoughtworks.com/radar

## Handoff

- Async delivery semantics, DLQ policy, or broker-specific behavior → `event-driven-integration`.
- Single-interface API wire format → `api-contract-design`.
- Architecture pattern (saga, outbox, 2PC, circuit breaker design) → `system-architect`.
- Infrastructure, broker provisioning, or monitoring implementation → `devops-sre`.
- Data pipeline, ETL/ELT, or DWH construction → `data-engineer`.
- Cross-team release coordination → `tech-lead` / `system-architect`.
