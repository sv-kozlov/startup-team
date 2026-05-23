---
name: system-context-analysis
description: Use when clarifying where a system sits in the landscape, what it depends on, who interacts with it, where boundaries lie, and which dependencies and ownership rules matter before detailed requirements can be written.
family: method
profile_level: Senior+
---

# System Context Analysis

## Purpose

Establish a shared, accurate picture of system boundaries, actors, external systems, integration points, and ownership responsibilities — before detailed requirements are written. Prevent scope creep, integration assumption errors, and cross-team ownership confusion. The context model is a prerequisite for integration, API, and data specifications.

## Use When

- A task spans multiple systems, teams, or components and boundary ownership is unclear.
- An integration or API contract requires knowing who owns each side and what each side does.
- A C4 context or container-level view is needed to frame the requirements conversation.
- A new feature requires discovery of which external systems it touches, who owns them, and what their contracts look like.
- Dependencies, shared components, or multi-team coordination risks must be surfaced early.

## Do Not Use When

- The system boundary is already clear and the task is specifying internal behavior — use `functional-specification`.
- The task is detailed component or sequence design inside a single system — hand off to `system-architect`.
- The task requires architectural decisions about decomposition or runtime topology — hand off to `system-architect`.
- The task is integration scenario specification for a known, bounded flow — use `integration-analysis`.

## Inputs

- System name, primary purpose, and team ownership.
- Known users, user roles, and external actor types.
- Known external systems, third-party services, and data stores that interact with the system.
- Existing architecture diagrams, wiki pages, or onboarding documents.
- Integration contracts, API lists, or message broker topics currently in use.
- Known constraints: data residency, security perimeter, regulated interfaces, SLA agreements.

## Workflow

1. Name the system in scope and state its primary purpose in one sentence. Agree on the canonical name to use in all downstream artifacts (ubiquitous language for the system itself).
2. Identify actors: people and systems that interact directly with the system in scope. For each actor, note: role, primary interaction type, data exchanged, frequency, and team/org ownership.
3. Map external systems: for each external system, record: name, owning team, interaction direction (outbound/inbound/bidirectional), protocol, known SLA, and data classification (PII, financial, regulated).
4. Draw the C4 context boundary: system in scope in the center; actors and external systems on the outside; interactions as labeled arrows (protocol, direction, key data). This is a requirements artifact — not an architecture diagram; defer component internals to `system-architect`.
5. Identify containers (C4 level 2) only where the container boundary is relevant to the requirements being written — for example, where different teams own different containers and need separate API contracts.
6. Record ownership and dependency risks: shared components, single points of failure, teams with release cycle dependencies, SLA mismatches. Flag each for handoff to `system-architect` or `tech-lead`.
7. Use the context model to scope downstream artifacts: reference it in `functional-specification`, `api-contract-design`, `integration-analysis`, and `data-modeling` so all specifications share the same landscape understanding.

## Outputs

- System context brief: system purpose, actor list, external system list, interaction summary.
- C4 Level 1 context diagram brief (textual or Mermaid sketch).
- C4 Level 2 container brief where container boundaries matter for requirements.
- Dependency and ownership map: who owns what, what must be negotiated, what is a cross-team risk.
- Boundary decisions: what is in scope, what is explicitly out of scope, and who decided.

## Named Patterns

### Good — System context statement
```
System: Order Management Service (OMS)
Purpose: Receives and manages customer orders from creation through fulfillment.
Owner: Order Platform team.
Actors:
  - Web Frontend (outbound, REST, order placement and status reads)
  - Mobile App (outbound, REST, same contract as web)
  - Payment Gateway [external, Stripe] (inbound webhook, payment events)
  - Warehouse System (inbound, REST, fulfillment status updates)
  - Notification Service [internal] (async, Kafka, order state change events)
  - Data Platform (async, Kafka, analytical event stream)
Out of scope: payment processing logic (Stripe), warehouse picking logic.
```
Every team knows exactly what OMS is responsible for and who talks to it.

### Bad — Implicit scope assumption
Team starts writing API specs assuming OMS owns refund processing. Three weeks later: Stripe owns refunds; OMS was never meant to initiate them. Specs redone.

### Good — Ownership and dependency risk entry
```
Dependency: Inventory Service
Owner: Catalog team (different release cadence — monthly releases)
Risk: OMS must remain functional when Inventory is degraded.
Impact on spec: order creation must not require a synchronous Inventory check;
  use async availability event instead.
Handoff: system-architect to decide fallback pattern (circuit breaker vs. read cache).
```
Risk is named, impact on requirements is clear, architectural decision is routed correctly.

### Bad — Dependency discovered during implementation
Developer calls Inventory Service synchronously; Inventory team deploys a breaking change; OMS goes down on release day.

### Good — C4 context boundary with protocol labels
```
[Web Client] → REST/HTTPS → [OMS]
[Mobile Client] → REST/HTTPS → [OMS]
[OMS] → Kafka → [Notification Service]
[OMS] → Kafka → [Data Platform]
[Stripe] → Webhook/HTTPS → [OMS]
[OMS] → REST/HTTPS → [Warehouse API]
Out of scope: [OMS] does not communicate directly with CRM or ERP.
```
Protocol and direction explicit; out-of-scope stated; downstream specs can reference this without repetition.

### Bad — Context captured in meeting notes only
Different stakeholders have different mental models. Spec authors invent integration points that do not exist; miss ones that do.

### Good — Scoping decision with authority
```
Decision: Reporting and analytics for order data are out of scope for OMS.
Owner of decision: VP Engineering + Product Manager (confirmed 2026-05-20 in kickoff).
Rationale: Data Platform team owns the analytical layer; OMS emits domain events.
Impact: OMS specs do not include reporting endpoints or BI schema requirements.
```
Decision is recorded with authority. No analyst will later add reporting specs "just in case".

### Bad — Scope left open
No explicit out-of-scope statement. Six months in, three teams add overlapping reporting features. Data Platform duplicates OMS data; OMS adds its own dashboard; product metrics are inconsistent.

## Boundaries

- Owns: system boundary definition, actor and dependency map, C4 context/container brief at the requirements level, ownership and risk documentation.
- Does not own: target architecture decisions (how components are deployed, what technology stack) — that is `system-architect`.
- Does not own: component design inside a container — that is `system-architect`.
- Does not own: integration scenario specification for a specific flow — that is `integration-analysis`.
- Does not own: deep NFR trade-off decisions — route via `non-functional-requirements` to `system-architect`.

## Sources

### Priority 1 — Modeling canon
- C4 model — https://c4model.com/
- C4 model diagrams reference — https://c4model.com/diagrams
- C4 model FAQ — https://c4model.com/faq

### Priority 2 — Context and integration
- Simon Brown: Software Architecture for Developers — https://leanpub.com/software-architecture-for-developers
- Enterprise Integration Patterns — https://www.enterpriseintegrationpatterns.com/

### Priority 3 — Background
- Martin Fowler: Strangler Fig and system boundary patterns — https://martinfowler.com/bliki/StranglerFigApplication.html
- ThoughtWorks Technology Radar — https://www.thoughtworks.com/radar

## Handoff

- Architecture decisions (component deployment, technology stack) → `system-architect`.
- Detailed integration scenario for a specific system-to-system flow → `integration-analysis`.
- NFR trade-offs surfaced from dependency risk → `non-functional-requirements` then `system-architect`.
- Ownership and release-cycle coordination → `tech-lead` / `system-architect`.
