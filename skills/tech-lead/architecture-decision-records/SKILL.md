---
name: architecture-decision-records
description: Use when initiating, writing, reviewing, or maintaining an Architecture Decision Record — capturing a non-obvious technical decision with its context, alternatives, chosen option, and consequences. Covers the full ADR lifecycle from trigger to maintenance.
family: method
profile_level: Senior+
---

# Architecture Decision Records

## Purpose

Make technical decisions discoverable, reviewable, and permanent — so they survive team changes and do not become tribal knowledge or repeated arguments. An ADR is the written evidence that a decision was made deliberately, not by default.

## Use When

- A technical decision is non-obvious and involves trade-offs that are not visible from the code.
- The same question has been raised in three or more PR reviews without a written answer.
- A significant technology, pattern, or architectural choice is being introduced for the first time.
- An existing decision is being reversed or superseded and the reasons need to be documented.
- A decision has cross-team impact and the other team needs a shareable artifact, not a meeting summary.
- Onboarding a new engineer and they ask "why do we do X this way?" — the answer should be an ADR link, not a verbal explanation.

## Do Not Use When

- The decision is fully reversible and low-stakes — a PR description is sufficient.
- The decision is system-wide and crosses multiple domains → involve `system-architect` before writing.
- The request is about a recurring code review pattern that needs a style guide entry, not an ADR → `code-review-leadership`.
- The request is about team-level technical direction, not a single decision → `tech-strategy-and-roadmap`.

## Inputs

- The decision to be captured: what is being decided and why now.
- Context: the forces, constraints, and requirements that make this decision necessary.
- Alternatives considered: at least two, including the option of doing nothing.
- Chosen option and its rationale: why this option over the alternatives.
- Consequences: what becomes easier, what becomes harder, what new problems are introduced.

## Workflow

1. Decide whether an ADR is warranted. Apply the three tests: (a) is the decision non-obvious from the code? (b) will someone ask "why?" in the next 12 months? (c) would reversing this decision be costly? If yes to two of three, write the ADR.
2. Choose the format. Lightweight ADR (Michael Nygard format) is sufficient for most decisions: Title, Status, Context, Decision, Consequences. Extended format adds: Alternatives Considered, Pros/Cons per alternative, Decision Drivers. Use the extended format when the decision has significant cross-team impact or reverses a previous decision.
3. Write the context first. Context is not an introduction — it is the set of forces that make the decision necessary. Include: constraints (latency budget, team size, existing tech stack), events (incident that revealed a problem, new compliance requirement, scaling target), and the problem that will persist if no decision is made.
4. List the alternatives. A minimum of two: the proposed option and at least one other, including "do nothing / continue with the current approach." For each alternative: what it solves, what it does not solve, what it introduces. Write this before the Decision section — the alternatives make the decision legible.
5. State the decision explicitly. "We will use X for Y." Not "we are considering X" or "X might be better." The decision field records what was decided, not what was discussed.
6. Write the consequences. Three categories: positive (what becomes easier or safer), negative (what becomes harder or more expensive), and risks (what might go wrong if the decision turns out to be wrong). Honest consequences build trust in the ADR log.
7. Assign status and get it reviewed. Draft → Proposed (open for comment) → Accepted (decided) → Superseded (replaced by another ADR, with a link). Review an ADR like code: at least one other Senior or the Tech Lead, and any team whose work is affected.
8. Maintain the log. ADRs live in a discoverable location (repo `docs/adr/`, Confluence, or Notion). Each ADR has a sequential number and a short title. When a decision is superseded, update the old ADR's status with a link to the new one. Do not delete old ADRs — historical decisions are valuable context.

## Outputs

- ADR document: Title, Status, Context, Decision, Consequences (and Alternatives if extended format).
- Updated ADR log or index in the team's documentation system.
- Link from PR, ticket, or code comment to the ADR when the decision is implemented.

## Named Patterns

### Good — Nygard-format ADR
```markdown
# ADR-0023: Use cursor-based pagination for Order API

Status: Accepted

Context:
The Order API currently uses offset pagination. At scale (>100k orders per user), offset queries
degrade: P99 latency for page 500 exceeds 800ms, violating our 200ms SLO. Inserts and deletes
cause page drift. The payment team reports duplicate items in their reconciliation runs.

Decision:
Adopt cursor-based pagination for all Order API list endpoints. The cursor encodes the last
seen order ID and timestamp, is opaque to the client, and is stable under inserts and deletes.
Existing offset endpoints remain for 90 days with a deprecation notice.

Consequences:
+ Stable pages under concurrent inserts/deletes.
+ P99 latency for list queries drops to <50ms at current scale.
- Clients cannot jump to an arbitrary page number.
- 90-day migration window required for existing consumers.
- Cursor format must be versioned if the schema changes.
```
Complete, reviewable, and useful to a future engineer who asks "why cursor pagination?"

### Bad — Decision captured in a PR description
"Switched to cursor pagination — offset was slow."
The context, alternatives, and consequences are invisible. Six months later: "Why cursor? Can we go back to offset?"

### Good — Three-test trigger applied
"Question: should we write an ADR for switching from REST to gRPC on the internal Auth service?
Test 1: non-obvious from code? Yes — the wire protocol is not visible in business logic.
Test 2: someone will ask why in 12 months? Yes — every new engineer will ask.
Test 3: costly to reverse? Yes — client code in 4 services must change.
Decision: write the ADR."

### Bad — ADR for every decision
"ADR-0015: Use snake_case for variable names." A linter rule covers this. ADRs for low-stakes decisions create noise and dilute the signal of the important ones.

### Good — Alternatives section
```
## Alternatives Considered

### Option A: Offset pagination (current state)
+ No client changes required.
- Page drift under concurrent writes.
- P99 > 800ms at scale. Violates SLO.

### Option B: Cursor pagination (chosen)
+ Stable under concurrent writes. P99 < 50ms.
- No arbitrary page jump.
- 90-day migration window.

### Option C: Do nothing
- P99 SLO violation continues. Payment team reconciliation errors continue.
```
The decision is legible because the alternatives are explicit.

### Bad — Decision without alternatives
"We decided to use cursor pagination." Why not offset? Why not keyset? What was the trade-off? The reader cannot evaluate the decision.

### Good — Superseded ADR
```
# ADR-0007: Use Redis for session storage

Status: Superseded by ADR-0031 (2026-03-15)
Reason: Redis dependency added operational overhead; sessions moved to JWT after stateless auth adoption.
```
The history is preserved. The current state is discoverable.

### Bad — ADR deleted when superseded
Future engineers find a gap in the ADR sequence and cannot reconstruct the reasoning. Or they re-introduce the old decision because they do not know it was tried.

## Boundaries

- Owns ADR authoring, review, and maintenance for decisions within the team or domain.
- Does not own system-wide or cross-org architectural decisions → involve `system-architect`.
- Does not own code style or convention capture → `code-review-leadership` or style guide.
- Does not own team-level technical direction → `tech-strategy-and-roadmap`.
- Does not own cross-team alignment negotiations → `cross-team-technical-alignment`.

## Sources

### Priority 1 — ADR canon
- Michael Nygard: Documenting Architecture Decisions — https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- ADR GitHub organization and templates — https://adr.github.io/
- MADR (Markdown Architectural Decision Records) — https://adr.github.io/madr/

### Priority 2 — Architecture documentation practice
- Will Larson: Staff Engineer — Larson, 2021. Technical writing and decision records for staff+ impact.
- arc42 documentation framework — https://arc42.org/
- C4 Model for architecture diagrams — https://c4model.com/

### Priority 3 — Background
- ThoughtWorks Technology Radar: ADR entry — https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records
- LeadDev: Technical documentation — https://leaddev.com/

## Handoff

- System-wide or cross-org architectural decisions → `system-architect`.
- Cross-team alignment on decisions that affect other teams → `cross-team-technical-alignment`.
- Style and convention capture for recurring review patterns → `code-review-leadership`.
- Team-level technical direction and roadmap → `tech-strategy-and-roadmap`.
