---
name: cross-team-technical-alignment
description: Use when representing the team's technical constraints in cross-team forums, negotiating API contracts and shared dependencies with other tech leads or architects, escalating architectural conflicts that exceed the team's decision boundary, or coordinating a technical dependency that spans multiple teams.
family: method
profile_level: Senior+
---

# Cross-Team Technical Alignment

## Purpose

Prevent the team's technical decisions from creating invisible coupling or unresolved conflicts with adjacent teams. Surface constraints, negotiate dependencies, and escalate architectural conflicts to the right level before they block delivery or cause production incidents.

## Use When

- A feature requires an API change on a service owned by another team.
- A proposed design introduces a dependency on a shared platform component or library.
- Two teams are making conflicting assumptions about an event schema, a shared data model, or a protocol.
- A technical constraint from the team is blocking a dependency in another team's roadmap.
- An architectural conflict (service boundary, ownership of a shared component) cannot be resolved at the team level.
- The team is adopting a new technology and needs to align with org-wide standards or existing patterns.

## Do Not Use When

- The conflict is fully within the team's own service boundary → resolve internally using `architecture-decision-records`.
- The request is about defining system-wide architecture, platform NFR, or target-state HLD → handoff to `system-architect`.
- The request is about delivery schedule coordination with another team → `project-manager`.
- The request is about product feature alignment across teams → `product-manager`.

## Inputs

- Current team's technical constraints and non-negotiables: SLO requirements, deployment cadence, protocol choices.
- Proposed design or change that crosses the team boundary.
- Other team's constraints and contact: their tech lead or architect.
- Existing cross-team agreements (API contracts, shared schemas, platform standards).
- System-architect guidance on cross-cutting architectural principles.

## Workflow

1. Define the boundary of the conflict before entering the negotiation. What does the team own? What is shared? What does the other team own? A conflict about API contract evolution is different from a conflict about service ownership. Name the type of conflict explicitly.
2. Prepare the team's position. For the negotiation to be productive: what is the technical constraint and its evidence (why does this matter: latency, SLO, data integrity), what is the preferred resolution, what alternative approaches are acceptable, and what is non-negotiable and why?
3. Initiate the alignment conversation at the right level. Team-to-team for API and schema details. Tech Lead to Tech Lead for cross-cutting patterns. Escalate to system-architect only when the teams cannot converge after one or two working sessions. Do not escalate prematurely — most cross-team technical issues resolve at team level if prepared well.
4. Use a shared artifact as the anchor of the conversation. A draft ADR, a proposed schema, a sequence diagram, or a prototype endpoint. Conversations without artifacts drift. With an artifact, both sides can mark up the same document.
5. Identify the decision owner. Who has the authority to make the final call? For API contracts: typically the providing team, subject to consumer agreement. For shared schemas: the team that owns the data. For cross-cutting patterns: system-architect or a technical design authority forum. Clarify this before the conversation, not during.
6. Capture the agreed resolution in writing. Options: ADR owned by the relevant team, an API change documented in the spec, a schema version entry. A verbal agreement reached in a meeting and not written down is a future conflict.
7. Surface unresolved conflicts upward. If two working sessions produce no agreement, escalate to system-architect with: both teams' positions stated, the decision options and their trade-offs, and a requested resolution date. Do not let unresolved conflicts block delivery silently.
8. Monitor the dependency until it is delivered and verified. A cross-team agreement exists on paper; the integration test is the evidence.

## Outputs

- Cross-team agreement document or ADR: both parties named, decision recorded.
- Escalation memo if resolution requires system-architect: both positions, options, deadline.
- Integration test or contract test result as verification.

## Named Patterns

### Good — Prepared position
"We need the Order API to return the `currency` field on GET /orders/{id}. Our payment service requires it to calculate FX fees. Without it, we must make a second call to the Currency service, which adds 40ms to the checkout path and violates our p99 SLO of 200ms. We cannot make this second call in the hot path. We are open to: (a) add `currency` to the existing response, or (b) add a bulk currency endpoint that we call once and cache."
The other team has enough information to respond constructively.

### Bad — Underprepared request
"Can you add a currency field to the Order API?" No context, no constraint, no urgency. The other team deprioritizes. Three weeks later, delivery is blocked.

### Good — Conflict named and scoped
"We disagree on whether the Order event schema should include user PII for analytics. The conflict is: our analytics team needs user age for cohort analysis; our privacy team says PII must not appear in events without explicit consent. This is not an API design question — it is a data governance question. Escalating to the privacy officer and system-architect."
The conflict is scoped. The escalation path is clear.

### Bad — Conflict absorbed silently
Each team makes their own assumption. Order events include user age in one schema version, exclude it in another. Analytics queries break. No one knows which team's version is "correct."

### Good — Artifact-anchored negotiation
"Shared draft ADR: Order Event Schema v2. Section 3 — proposed fields: [list]. Section 4 — fields we removed: user_email (PII), user_age (PII). Both teams to mark up Section 3 by Friday."
Both teams react to the same document. Agreement is tracked in a single artifact.

### Bad — Agreement-by-meeting
Teams meet, verbally agree on the schema. Each team's engineer writes a different implementation. Integration breaks in staging. "But we agreed in the meeting."

### Good — Escalation memo
"Escalation: Order service team and Payment service team cannot agree on error response format after two working sessions. Option A (RFC 7807, proposed by Order team): consistent with platform standard but requires migration in Payment team. Option B (custom format, proposed by Payment team): no migration but diverges from standard. Requesting system-architect decision by 2026-06-01 to unblock Q3 delivery."
The escalation is specific, time-bound, and ready to decide.

### Bad — Silent escalation
The teams stop communicating. Delivery is blocked. The project manager discovers the conflict three weeks later during a status update. No options are prepared.

## Boundaries

- Owns cross-team negotiation for the team's APIs, schemas, and shared dependencies.
- Does not own system-wide architecture or platform NFR → `system-architect`.
- Does not own delivery schedule coordination with other teams → `project-manager`.
- Does not own product feature alignment across teams → `product-manager`.
- Does not own hiring or org structure decisions → `engineering-manager`.

## Sources

### Priority 1 — Leadership and alignment canon
- Will Larson: An Elegant Puzzle — Stripe Press, 2019. Cross-team dependency management and technical strategy.
- Tanya Reilly: The Staff Engineer's Path — O'Reilly, 2022. Cross-team influence and technical alignment.
- ADR GitHub organization — https://adr.github.io/

### Priority 2 — Practice orientation
- Martin Fowler: Bounded Context — https://martinfowler.com/bliki/BoundedContext.html
- Sam Newman: Building Microservices — O'Reilly, 2021. Service ownership and inter-team API management.
- Team Topologies: Matthew Skelton, Manuel Pais — IT Revolution, 2019. Team interaction modes.

### Priority 3 — Background
- LeadDev: Cross-team collaboration — https://leaddev.com/
- Increment Magazine: Coordination edition — https://increment.com/

## Handoff

- System-wide architectural decisions → `system-architect`.
- Delivery schedule and cross-team dependency governance → `project-manager`.
- Product feature alignment across teams → `product-manager`.
- Internal team-only architectural decisions → `architecture-decision-records`.
- Shared schema or API design substance → `system-analyst` for the requirements baseline.
