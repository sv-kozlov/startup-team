---
name: architecture-decision-records
description: Use when an architecturally significant decision must be recorded with context, alternatives, consequences, and constraints — covering ADR authoring, decision log maintenance, and exception tracking. Not for recording product, delivery, or operational decisions.
family: method
profile_level: Senior+
---

# Architecture Decision Records

## Purpose

Record architecturally significant decisions in a durable, reviewable format so context, alternatives, and consequences are not lost. Produce ADRs that a future engineer, reviewer, or architect can read and understand without asking the original decision-maker — and that can be audited, superseded, or revised with clear lineage.

## Use When

- A decision affects component boundaries, integration patterns, NFRs, core technology choice, or data ownership.
- Alternatives must be compared and trade-offs made explicit before the decision is made or ratified.
- An exception to an agreed architecture principle must be approved and tracked.
- A decision must remain auditable across delivery cycles or team changes.
- A recurring architecture debate must be closed with a binding record so the team can stop re-litigating it.
- A superseded decision must be marked and replaced with clear lineage.

## Do Not Use When

- The task is communicating the decision visually → `architecture-views-and-documentation`.
- The task is product, backlog, or delivery prioritization decisions → handoff to `product-manager` / `product-owner` / `project-manager`.
- The task is a code design choice within a single service → handoff to `tech-lead` (may use lightweight PR-level ADR).
- The task is a security audit finding → handoff to `security-engineer`.
- The decision is trivial, reversible, and low-impact → do not write an ADR; use PR description.

## Inputs

- Decision question and scope (which systems, components, or flows are affected).
- Context: requirements, constraints, current architecture, technical debt, regulatory requirements.
- Candidate options with known pros, cons, risks, and estimated effort.
- Stakeholders and approvers for this decision.
- Existing ADRs that this decision relates to or supersedes.

## Workflow

1. **Frame the decision question.** One decision, one ADR. "Should we use Kafka or RabbitMQ for order events?" — yes. "How should we handle all async messaging?" — split into separate decisions.
2. **Capture context, drivers, and constraints.** What is the problem? What are the non-negotiable constraints (regulatory, NFR targets, existing landscape)? What is the decision horizon (reversible in 6 months vs locked for 3 years)?
3. **List candidate options with consequences.** For each option: what it enables, what it costs, what risks it introduces, and what it makes harder later.
4. **Make and record the decision.** Name the chosen option. State the rationale tied to the specific context and constraints — not generic best practices. Include dissenting views if they were material.
5. **Record consequences, follow-up items, and revisit triggers.** What changes as a result? What follow-on decisions are unlocked or required? Under what conditions should this ADR be revisited (load threshold, regulatory change, team size, etc.)?
6. **Index and link.** Assign an ID (ADR-NNN). Link to related ADRs (supersedes, related to). Link to affected components or integration flows. Store in the architecture repository or decision log alongside the codebase.

## Outputs

- ADR entry following a stable template (see below).
- Decision log update with new ADR indexed.
- Linked follow-up items: open questions, handoff tasks, downstream ADR stubs.

## ADR Template

```markdown
# ADR-NNN: [Decision Title]

Status: Proposed | Accepted | Deprecated | Superseded by ADR-NNN

Date: YYYY-MM-DD
Deciders: [names or roles]
Reviewed by: [names or review body]

## Context

[What is the problem? What are the constraints, drivers, and non-negotiables?]

## Decision

[What was decided and why — tied to the specific context, not generic best practice.]

## Options Considered

| Option | Pros | Cons | Risk |
|---|---|---|---|
| Option A | ... | ... | ... |
| Option B | ... | ... | ... |

## Consequences

- Positive: [what this enables]
- Negative: [what this makes harder]
- Risks: [what could go wrong]
- Follow-on decisions: [what is now unlocked or required]

## Revisit Triggers

[Under what conditions should this ADR be reviewed: load threshold, regulatory change, team restructuring, etc.]

## Related ADRs

- Supersedes: ADR-NNN
- Related to: ADR-NNN
```

## Named Patterns

### Good — ADR with context, decision, consequences, and revisit trigger
```markdown
# ADR-012: Async order notification via Kafka

Status: Accepted | Date: 2026-04-01
Context: NotificationService SLA is best-effort (p99 < 5s). OrderService SLA is 99.9% at p99 < 200ms.
         Synchronous call would couple availability.
Decision: OrderService publishes OrderPlaced event to Kafka topic order.events.
          NotificationService consumes as independent consumer group.
Consequences: OrderService no longer blocked by NotificationService latency.
              Notification delivery is eventual (up to 30s). Accepted by Product on 2026-03-28.
Revisit trigger: If Kafka operational cost exceeds $X/month or if SLA requires synchronous confirmation.
```

### Bad — ADR without context or rationale
```markdown
# ADR-012: Use Kafka

Status: Accepted
Decision: Use Kafka for messaging.
```
No context, no alternatives, no trade-offs. A new engineer cannot understand why Kafka was chosen over RabbitMQ or a simple database queue. The decision cannot be audited or superseded with lineage.

### Good — Supersession with clear lineage
```markdown
# ADR-019: Replace Redis session store with database sessions

Status: Superseded by ADR-027
ADR-027 context: Redis cluster cost exceeded budget threshold defined in ADR-019 revisit trigger.
```

### Bad — Silent decision reversal
Engineers stop using Redis sessions and switch to database sessions without updating ADR-019. The ADR log says "Redis" but the code does something else. Future engineers are misled.

### Good — Exception ADR for deliberate deviation
```markdown
# ADR-021: Exception — shared database between OrderService and LegacyReportingService (temporary)

Status: Accepted, expires 2026-09-01
Context: LegacyReportingService cannot be refactored before Q3 release. Data must be shared temporarily.
Risk: Coupling violation. Accepted as time-bounded exception.
Revisit trigger: LegacyReportingService migration complete or 2026-09-01, whichever is earlier.
```

### Bad — Undocumented coupling exception
OrderService and LegacyReportingService share a database because "we'll fix it later." No ADR, no expiry, no owner. Three years later the coupling is invisible, undocumented, and unmovable.

## Boundaries

- Does not replace detailed system or API specification → `system-analyst`.
- Does not replace architecture views (diagrams communicate structure; ADRs record decisions) → `architecture-views-and-documentation`.
- Does not own product, backlog, or delivery decisions → `product-manager` / `project-manager`.
- Does not become a long design document — one decision per ADR, maximum 2 pages.

## Sources

### Priority 1 — Canonical References
- Michael Nygard — Documenting Architecture Decisions (original post): https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- ADR GitHub organization — templates and examples: https://adr.github.io/
- MADR template (Markdown Architectural Decision Records): https://adr.github.io/madr/

### Priority 2 — Practitioner Guidance
- ThoughtWorks Technology Radar — Lightweight Architecture Decision Records: https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records
- Microsoft Architecture Center — Architecture Decision Record guidance: https://learn.microsoft.com/azure/well-architected/architect-role/architecture-decision-record
- Mark Richards, Neal Ford — Fundamentals of Software Architecture (ch. on decisions): https://www.developertoarchitect.com/lessons/

### Priority 3 — Supplementary
- Joel Parker Henderson — ADR collection and examples: https://github.com/joelparkerhenderson/architecture-decision-record
- InfoQ — architecture decision practices: https://www.infoq.com/architecture-design/

## Handoff

- Visualization of the decided architecture → `architecture-views-and-documentation`.
- Conformance check of implementation against accepted ADRs → `architecture-review-and-governance`.
- Risk assessment implied by a decision → `architectural-risk-and-technical-debt`.
- Follow-on API or data spec authoring → `system-analyst`.
