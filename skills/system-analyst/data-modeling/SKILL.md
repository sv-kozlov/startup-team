---
name: data-modeling
description: Use when specifying domain entities, attributes, relationships, ER diagrams, mapping tables, data constraints, reference and master data, data quality rules, lifecycle states, or data model change impact for a system feature.
family: method
profile_level: Senior+
---

# Data Modeling

## Purpose

Translate domain rules and system behavior into clear data structures, relationships, constraints, and mappings — at the requirements level. Give engineering and data roles an unambiguous model of what data the system stores, how it is structured, what constraints must be enforced, and what quality rules apply. Do not design physical database internals; describe what must be true of the data.

## Use When

- A feature introduces new entities, attributes, relationships, or reference data.
- ER diagram, schema requirements, or data dictionary is needed before or during implementation.
- A mapping between source systems, API payloads, UI states, and storage must be specified.
- Data constraints, lifecycle rules, quality thresholds, or retention policies must be explicit.
- A change to the data model requires impact analysis on API, events, tests, and migrations.

## Do Not Use When

- The task is physical database optimization, indexing strategy, or query tuning — hand off to Engineering.
- The task is DWH schema design, analytical modeling, or OLAP cubes — hand off to `data-engineer`.
- The task is data pipeline construction, ETL/ELT implementation — hand off to `data-engineer`.
- The task is specifying a wire-level API payload format — use `api-contract-design`.

## Inputs

- Domain entities and business rules from `requirements-elicitation` or stakeholders.
- Existing schemas, ERDs, API contracts, UI state descriptions.
- Source system descriptions, data dictionaries, integration payloads.
- Known constraints: privacy, retention, security classification, regulatory requirements.
- Data quality expectations from business: completeness, uniqueness, freshness, allowed values.

## Workflow

1. Define scope and entity grain. State which entities are in scope for this model and what their primary grain is (e.g., "one row per order, not per order line").
2. Identify entities, attributes, types, required/optional status, nullability, default values, and uniqueness constraints. Separate domain-meaningful nullability ("not captured yet") from technical nullability.
3. Define relationships: cardinality (1:1, 1:N, M:N), ownership (which side owns the relationship), and foreign key semantics. Note whether the relationship is enforced at the database level or application level.
4. Separate the conceptual model (domain entities and relationships) from the logical model (tables, columns, indices) and note which implementation decisions belong to Engineering.
5. Document reference data and master data: allowed values, value sets, ownership, update frequency, source of truth, and integration dependencies.
6. Define lifecycle and state transitions for stateful entities: which states exist, what triggers transitions, what invariants must hold at each state. Cross-reference the state model in `functional-specification`.
7. Specify data quality rules: completeness flags, validation constraints, uniqueness scope, value range checks, source-of-truth hierarchy, reconciliation rules. Note which rules are enforced by the system and which are monitored post-factum.
8. Build mapping tables between API payloads, UI fields, event schemas, source system fields, and storage columns. Note transformations, enrichments, and default-fill rules.
9. Assess migration and compatibility impact: new required fields, renamed entities, removed states, foreign key changes. Hand off migration script ownership to Engineering; document the data contract obligation.

## Outputs

- Conceptual ER brief: entities, relationships, cardinality, key constraints.
- Entity and attribute dictionary: name, type, required/optional, constraint, description, source.
- Reference and master data specification: allowed values, owner, update channel.
- Lifecycle and state model (cross-referenced to `functional-specification`).
- Mapping table: source → target field, transformation rule, default, validation.
- Data quality requirements: completeness, uniqueness, freshness thresholds, source-of-truth.
- Migration and compatibility impact notes.

## Named Patterns

### Good — Entity with explicit invariant
```
Entity: Order
Attributes:
  id:         UUID, required, immutable after creation
  status:     enum(Draft|Confirmed|Processing|Shipped|Delivered|Cancelled), required
  total:      decimal(12,2), required, > 0
  currency:   ISO 4217 code, required, immutable after Confirmed
Invariant: total must equal sum of line_items[].amount at Confirmed state.
Invariant: currency must not change after status reaches Confirmed.
```
Developer knows what the database must guarantee vs what the application must enforce.

### Bad — Anemic schema list
```
orders table: id, status, total, currency, created_at, updated_at
```
No types, no nullability, no constraints, no invariants. Every developer fills the gap differently.

### Good — Data quality rule with source-of-truth
```
Field: customer.email
Source of truth: CRM system
Allowed values: valid RFC 5322 address
Completeness: required for all customer records; null not permitted after registration
Uniqueness: unique per tenant scope
Reconciliation: nightly sync from CRM; system rejects orders for customers without a valid email
Freshness: email field updated within 24h of CRM change
```
Data engineer knows what to implement in the sync; QA knows what to validate; engineering knows what to enforce.

### Bad — Quality rule as prose wish
"Email should be valid and up to date." No scope, no reconciliation rule, no enforcement point.

### Good — Mapping table entry
```
Source: payment_gateway.response.charge_id (string, max 64)
Target: payments.external_reference (varchar(64), not null)
Transform: direct copy; strip leading/trailing whitespace
Default: none — field is required; reject if absent
Validation: must match pattern [A-Za-z0-9_-]{8,64}
Used in: POST /v1/payments response body, PaymentCompleted event
```
Engineering has everything needed to implement; QA knows how to test.

### Bad — Mapping by implication
"The charge ID from the payment gateway should be saved." Which field? Which format? What if absent?

### Good — Reference data specification
```
Reference: order_cancellation_reason
Owner: Business Operations team
Values: CUSTOMER_REQUEST | PAYMENT_FAILED | STOCK_UNAVAILABLE | FRAUD_DETECTED | ADMIN_ACTION
Update channel: configuration file; deployed via release; not editable at runtime
Used in: OrderCancelled event, refund eligibility rules
```
Engineering does not hard-code string literals; future value additions require a release.

### Bad — Enum embedded in code comments
Developer adds values as needed; inconsistency across services; no governance.

## Boundaries

- Owns: conceptual and logical data model at the requirements level, mappings, quality rules, lifecycle, reference data.
- Does not own: physical database optimization, indexing strategy, query tuning — that is Engineering.
- Does not own: DWH schema, analytical models, or data pipelines — that is `data-engineer`.
- Does not own: API wire payload format — that is `api-contract-design`.
- Does not own: data pipeline construction or ETL/ELT implementation — that is `data-engineer`.

## Sources

### Priority 1 — Modeling standards
- Karl Wiegers, Joy Beatty: Software Requirements, 3rd ed. — book reference, data modeling chapter
- Martin Fowler: Analysis Patterns — book reference, Addison-Wesley
- Eric Evans: Domain-Driven Design — book reference (entities, value objects, aggregates, invariants)

### Priority 2 — Reference and diagrams
- Lucidchart database design guide — https://www.lucidchart.com/pages/database-diagram/database-design
- Lucidchart ER diagrams — https://www.lucidchart.com/pages/er-diagrams
- IIBA BABOK Guide v3, Data Modeling section — https://www.iiba.org/career-resources/a-business-analysis-body-of-knowledge/babok/

### Priority 3 — Background
- Martin Fowler: Data Model Patterns — https://martinfowler.com/books/datapatterns.html
- ThoughtWorks Technology Radar — https://www.thoughtworks.com/radar

## Handoff

- Physical database optimization, indexing, query tuning → Engineering.
- DWH design, analytical modeling, data pipelines → `data-engineer`.
- API payload format for API endpoints referencing this model → `api-contract-design`.
- Event schema for events that carry model entities → `event-driven-integration`.
- Migration script authorship → Engineering (data model provides the contract obligation).
- Data quality monitoring implementation → `data-engineer`.
