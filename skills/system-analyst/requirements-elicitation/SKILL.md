---
name: requirements-elicitation
description: Use when gathering, refining, and validating requirements through stakeholder interviews, workshops, document analysis, AS IS/TO BE investigation, or DDD-aligned domain exploration. This is the entry skill before specification work begins.
family: method
profile_level: Senior+
---

# Requirements Elicitation

## Purpose

Acquire enough accurate, validated information from stakeholders, domain experts, existing systems, and documentation to make specification work possible. Separate fact from assumption, resolve contradictions early, and establish the ubiquitous language that will carry through all downstream artifacts.

## Use When

- Starting a new feature, product area, or integration with unclear or incomplete requirements.
- Stakeholders hold domain knowledge that has not been formalized or is contradictory.
- A change request requires understanding the AS IS process before specifying the TO BE system.
- The team needs a shared domain vocabulary, business rules, or event map before writing specs.
- Existing documentation is stale, incomplete, or conflicts with system behavior.

## Do Not Use When

- Requirements are already gathered and validated — proceed to `functional-specification` or `api-contract-design`.
- The task is writing or improving a specification from known inputs — that is `functional-specification`.
- Business process ownership or business value case decisions are needed — hand off to `business-analyst`.
- Product strategy, priority, or MVP scope decisions are needed — hand off to `product-manager`.

## Inputs

- Feature or change request: description, business goal, expected outcome.
- Stakeholder list: roles, availability, domain expertise, decision authority.
- Existing artifacts: process diagrams, current system documentation, data dictionaries, past requirements, defect history.
- Known constraints: regulatory, architectural, technical, timeline, team capacity.
- Context: system landscape, adjacent teams, integration points.

## Workflow

1. Plan the elicitation: identify stakeholder roles, knowledge gaps, contradictions to resolve, and the artifact the session must produce. Choose the method — interview, structured workshop, document analysis, observation, or a combination.
2. Prepare targeted questions for each stakeholder type. For domain experts: focus on rules, exceptions, edge cases, and terminology. For tech leads: focus on constraints, existing behavior, and known deviations. For end users: focus on goals, pain points, and workarounds.
3. Conduct elicitation sessions. Take structured notes: capture statements verbatim where precision matters. Separate facts, opinions, constraints, and open questions.
4. Build or extend the ubiquitous language: list domain terms, entities, roles, events, commands, and invariants. Resolve synonyms and contradictions with a naming decision.
5. Model AS IS: describe the current process, system behavior, data flow, and actors using plain text, BPMN sketch, or UML activity/sequence fragment. Mark gaps and deviations from documented behavior.
6. Define TO BE boundary: what changes, what stays the same, what is out of scope. Record each scoping decision with the stakeholder who made it.
7. Classify gathered requirements: business, user, functional, non-functional, integration, data, security, regulatory. Separate confirmed from assumed.
8. Validate with stakeholders: walk through a summary of findings, confirm interpretations, surface conflicts, and close open questions. Document remaining assumptions.
9. Hand off to specification: produce a requirements brief suitable as input for `functional-specification`, `api-contract-design`, `data-modeling`, or `integration-analysis`.

## Outputs

- Requirements brief: classified, conflict-free requirements with source stakeholder noted.
- Ubiquitous language glossary: terms, definitions, entity names, agreed synonyms, excluded alternatives.
- AS IS / TO BE delta description.
- Open questions log with owner and resolution status.
- Assumption register.
- Scoping decision log.

## Named Patterns

### Good — Requirement with testable "shall"
```
The system shall reject a payment initiation request
when the account balance is below the requested amount,
returning HTTP 422 with error code INSUFFICIENT_FUNDS
and the current available balance in the response body.
```
Stakeholder, condition, behavior, observable outcome, and error detail — all present.

### Bad — Vague stakeholder wording copied verbatim
```
The system should handle payment errors properly.
```
"Handle properly" has no test criterion. Cannot be implemented, estimated, or accepted.

### Good — Ubiquitous language entry
```
Term: Order
Definition: A confirmed intent to purchase one or more products.
Distinct from: Cart (unconfirmed intent), Invoice (billing document).
Lifecycle: Draft → Confirmed → Processing → Shipped → Delivered | Cancelled.
```
Every downstream artifact uses "Order" with this precise meaning. Ambiguity surfaced and resolved.

### Bad — Unresolved synonym used in specs
Specification says "order" in section 2, "purchase" in section 5, "request" in section 8 — all referring to the same entity. Developers implement three concepts; QA writes tests against two; defect emerges in integration.

### Good — Structured AS IS / TO BE delta
```
AS IS: Refund approval requires email from the finance manager.
Gap: Process takes 3–5 days; no audit trail in the system.
TO BE: System records refund requests with status and approver;
       finance manager approves in-app; audit log is mandatory.
Out of scope: Payment gateway integration (handled by separate project).
```
Scope boundary is explicit; engineering does not over-implement.

### Bad — Scope inflation without a decision
AS IS is documented. The team adds features that "seem logical" without a scoping decision. Engineering builds them; product never asked for them; they delay launch.

### Good — Open question with owner
```
OQ-14: Does the cancellation policy apply to B2B orders as well as B2C?
Owner: Maria K. (Head of Sales)
Due: 2026-05-30
Status: Open
Impact: Affects business rules in functional-specification section 4.3.
```
The question is tracked; it blocks nothing until the deadline; the impact is visible.

### Bad — Open question embedded in spec prose
"Note: clarify whether cancellation applies to B2B." Three weeks later, nobody remembers; the spec ships with a gap; QA finds a defect in UAT.

### Good — DDD-aligned elicitation output
```
Domain event: OrderCancelled
Trigger: Customer requests cancellation and refund window is open.
Preconditions: Order.status == Confirmed | Processing; elapsed < 24h.
Invariant: RefundAmount <= OriginalPaymentAmount.
Producers: Order service.
Consumers: Inventory service (restore stock), Notification service (email), Finance service (refund).
```
Event storming output that directly drives API, data model, and integration specs.

### Bad — Events listed without meaning
"Events: order_created, order_updated, order_cancelled." No trigger, no precondition, no consumer, no invariant. Each consuming team will interpret the event differently.

## Boundaries

- Owns: requirement gathering, classification, conflict resolution, ubiquitous language, AS IS/TO BE, scoping decisions.
- Does not own: functional specification authorship → `functional-specification`.
- Does not own: business process ownership or business value decisions → `business-analyst`.
- Does not own: product scope authority, roadmap, or priority → `product-manager` / `product-owner`.
- Does not own: architecture or engineering decisions that emerge during elicitation → `system-architect` / `tech-lead`.

## Sources

### Priority 1 — Canon
- IIBA BABOK Guide v3, Knowledge Area: Elicitation and Collaboration — https://www.iiba.org/career-resources/a-business-analysis-body-of-knowledge/babok/
- IREB CPRE Requirements Elicitation Handbook v2.1 — https://cockpit.ireb.org/media/pages/downloads/cpre-requirements-elicitation-handbook/adc3d55045-1733311667/advanced_level_elicitation_handbook_en_v2.1.pdf
- IEEE/ISO/IEC 29148:2018 Requirements Engineering — https://standards.ieee.org/content/ieee-standards/en/standard/29148-2018.html
- Karl Wiegers, Joy Beatty: Software Requirements, 3rd ed. — book reference, Microsoft Press

### Priority 2 — Method and DDD
- Alistair Cockburn: Writing Effective Use Cases — book reference, Addison-Wesley
- Eric Evans: Domain-Driven Design — book reference, Addison-Wesley (chapters on Ubiquitous Language and Bounded Contexts)
- Martin Fowler: Ubiquitous Language — https://martinfowler.com/bliki/UbiquitousLanguage.html

### Priority 3 — Practice background
- Gojko Adzic: Specification by Example — book reference, Manning
- ThoughtWorks Technology Radar — https://www.thoughtworks.com/radar

## Handoff

- Functional specification authorship from gathered requirements → `functional-specification`.
- Business process ownership or value case decisions → `business-analyst`.
- Product scope, roadmap, or priority decisions → `product-manager` / `product-owner`.
- Architecture option decisions surfaced during elicitation → `system-architect`.
- Feasibility and implementation risk questions → `tech-lead`.
