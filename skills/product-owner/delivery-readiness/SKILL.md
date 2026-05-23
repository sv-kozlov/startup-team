---
name: delivery-readiness
description: Use when a Product Owner must assess whether a story, epic, or release scope is ready for development, QA, and delivery — producing a readiness checklist, classifying blockers by owner, and generating handoffs without taking over delivery governance.
family: method
profile_level: Senior+
---

# Delivery Readiness

## Purpose

Determine whether product-side work is ready enough for delivery to proceed. Readiness means the team can start, progress, and complete work without stopping for missing product decisions, unclear acceptance, or unresolved dependencies. This skill is the gate between product ownership and delivery execution — it does not govern the delivery plan itself.

## Use When

- Sprint planning is approaching and the team asks whether stories are ready.
- An epic or release scope needs a product-side go / no-go assessment.
- Dependencies, unclear acceptance, or missing product decisions are blocking planning.
- Product, system analysis, design, QA, and delivery need a shared view of what is blocking and who owns each blocker.
- A release candidate must be reviewed from the product side before QA sign-off.

## Do Not Use When

- Delivery schedule, resource allocation, budget, or governance decisions are the primary question → `project-manager`.
- Technical architecture or implementation decisions are blocking readiness → `tech-lead` or `system-architect`.
- QA test readiness (test coverage, regression scope, environment state) is the concern → `qa-engineer`.
- The product scope itself is unclear → resolve product direction with `product-manager` first, then assess readiness.

## Inputs

- Backlog items, epics, or release scope with current readiness state.
- Acceptance criteria drafts for each item under review.
- Known dependencies: system analysis notes, design files, QA input, infrastructure readiness, external services.
- Delivery timing context (sprint goal, release window, milestone date) from Project Manager.
- Open questions and blocker log from previous refinement.

## Workflow

1. **Frame the readiness scope.** Define which items are being assessed (sprint backlog, release candidate, or epic). Do not assess readiness in the abstract — tie it to a specific delivery event.
2. **Run the product-side DoR check.** For each item, verify:
   - Goal and user outcome stated.
   - Scope bounded with explicit exclusions.
   - Product-level acceptance criteria present and testable.
   - Dependencies identified and either resolved or explicitly accepted as risk.
   - No open product decision that blocks the start of work.
3. **Classify blockers by owner.** For each blocker: identify whether it is a product, system analysis, design, QA, engineering, or delivery governance blocker. Route, do not absorb.
4. **Produce readiness verdict per item.** Use: `Ready`, `Ready with risk` (noted), `Needs refinement` (specific gap), `Blocked` (external dependency), `Needs decision` (product or business).
5. **Generate handoffs for each blocker.** One handoff per owner; include the specific question, context, and expected artifact.
6. **Communicate status.** Prepare a readiness summary for the team and delivery owner. Do not promise delivery dates — that belongs to Project Manager / Delivery Manager.

## Outputs

- Delivery readiness checklist per item (DoR verdict and gap list).
- Blocker list classified by owner (product, SA, design, QA, engineering, delivery).
- Handoff tasks for each blocker owner.
- Readiness summary for sprint planning or release review.
- Risk register for items accepted as `Ready with risk`.

## Named Patterns

### Good — Readiness checklist per item
```
Story: "Display carbon offset label on product page"
DoR check:
  ✓ Goal: Increase eco-conscious purchase rate (PM confirmed, metric from PA)
  ✓ Scope: Label shown for products with verified offset data; hidden otherwise
  ✓ AC: 3 conditions — label visible, correct value, tooltip on hover
  ✓ Dependency: SA confirmed product data schema; design mockup attached
  ✗ Open: offset verification rule unclear — who sets the threshold?
  → Status: Needs decision | Owner: Product Manager | Due: 2026-05-26
```
Benefit: team knows exactly what is missing and who must resolve it.

### Bad — "Looks ready to me" verdict with no check
```
PO: "This story has been in the backlog for 3 weeks — let's just pull it in."
Team starts; day 2 blocked by missing verification rule. Sprint goal missed.
```

### Good — Blocker classified by owner
```
Blocker: "Payment service SLA for retry flow unknown"
Owner: System Analyst (confirm with PSP)
Action: SA to clarify SLA from PSP contract by 2026-05-28
Story status: Blocked until SA delivers answer
```

### Bad — Blocker absorbed by PO
```
PO attempts to read PSP API docs, writes own interpretation.
Incorrect SLA assumed; implementation does not match contract.
Post-release incident.
```

### Good — Ready-with-risk verdict for accepted dependency
```
Story: "Push notifications for order status"
Risk: iOS push certificate renewal pending (DevOps, ETA 2026-05-25)
Decision: Accept risk — certificate renewal independent of story; fallback = in-app alert.
Status: Ready with risk. Risk owner: DevOps.
```

### Bad — Ignoring dependency and accepting story as simply "Ready"
```
Story: "Push notifications" — Ready (no mention of certificate dependency)
iOS push fails on release day. Hotfix needed.
```

### Good — Readiness summary for sprint planning
```
Sprint 14 Readiness Review:
  Ready: 7 stories (42 points)
  Ready with risk: 2 stories (noted risks assigned)
  Blocked: 1 story (PSP SLA pending — excluded from sprint)
  Needs decision: 1 story (PM escalated — expected answer 2026-05-26)
  Team advised: do not plan blocked story; escalation in progress.
```

### Bad — Sprint planning starts without readiness review
```
All 11 stories pulled into sprint planning. 3 hours spent in planning clarifying gaps.
Sprint goal set but 3 stories immediately blocked on day 1.
```

## Boundaries

- Does not own delivery schedule, sprint commitment, resource plan, or budget → `project-manager`.
- Does not approve technical architecture or implementation feasibility → `tech-lead` or `system-architect`.
- Does not own QA readiness — test coverage, regression scope, and environment readiness belong to `qa-engineer`.
- Does not own system specifications, API contracts, or data models → `system-analyst`.
- Does not promise release dates or sprint capacity — that is a delivery team and PM decision.

## Sources

**Priority 1 — Canonical method references:**
- Scrum Guide (Schwaber & Sutherland): https://scrumguides.org/scrum-guide.html — Definition of Ready and Sprint Planning.
- Mike Cohn, "Succeeding with Agile" — readiness criteria and team agreement.
- Roman Pichler, "Agile Product Management with Scrum": https://www.romanpichler.com/books/

**Priority 2 — Practice guides:**
- Scrum.org, Definition of Ready: https://www.scrum.org/resources/blog/definition-ready
- Agile Alliance, Definition of Ready: https://agilealliance.org/glossary/definition-of-ready/
- Atlassian, Backlog Refinement: https://www.atlassian.com/agile/scrum/backlog-refinement

**Priority 3 — Supplementary reading:**
- SAFe, Team Backlog: https://scaledagileframework.com/team-backlog/
- SVPG Blog: https://www.svpg.com/articles/

## Handoff

```
To: system-analyst
Task: Clarify [specific system behavior or constraint] for [story].
Context: Story cannot pass DoR — system-level detail needed for AC to be testable.
Inputs: Product intent, open questions, dependency map.
Expected artifact: Functional scope note or system specification stub.
Acceptance criteria: Engineering team can estimate and start without further clarification.
```

```
To: project-manager
Task: Confirm delivery timeline constraints for [sprint or release].
Context: Readiness assessment needs delivery date to classify risks correctly.
Inputs: Release window, dependency list, blocked story list.
Expected artifact: Delivery timeline and escalation path for blocked items.
Acceptance criteria: PO can communicate readiness status to the team with correct date context.
```
