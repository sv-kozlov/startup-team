---
name: backlog-management
description: Use when a Product Owner must order, structure, clean up, or explain a product backlog — translating agreed product direction into a visible, prioritized, and actionable work queue for the team.
family: method
profile_level: Senior+
---

# Backlog Management

## Purpose

Keep the product backlog ordered, transparent, and connected to agreed product direction so the team always knows what to build next and why. This skill covers the full lifecycle of backlog items: intake, structuring, ordering, cleanup, and presentation to stakeholders.

## Use When

- A roadmap item or stakeholder request must become backlog epics and stories.
- The backlog has grown stale, unordered, or disconnected from the current product goal.
- Stakeholders or the engineering team need to understand why work is or is not in scope.
- Existing items need regrouping, splitting, or removal to reflect changed priorities.
- The team is entering sprint or release planning and the backlog is not ready.

## Do Not Use When

- Product strategy or roadmap priority decisions must be made — route to product-manager.
- Delivery dates, budget, staffing, or dependency governance are the main topic — route to project-manager.
- The work requires system specification, API contracts, or data model design — route to system-analyst.
- Metrics, experiment design, or analytics conclusions are needed — route to product-analyst.

## Inputs

- Agreed product goal, roadmap item, or initiative from Product Manager.
- Current backlog: epics, stories, defects, technical tasks, stakeholder requests.
- Value, risk, dependency, and readiness signals from team, analytics, QA, and design.
- Constraint signals: timeline, architecture, regulation, external dependency.

## Workflow

1. **Confirm product direction.** Identify the roadmap item or goal driving the current backlog update. If direction is unclear or missing, create a handoff to Product Manager before proceeding.
2. **Intake and triage.** Collect new requests through the defined intake channel. Classify each as: in-scope now, later, needs decision, or reject.
3. **Group by goal or outcome.** Cluster items under epics or themes that share a user outcome, delivery dependency, or product bet. Avoid grouping by team or component alone.
4. **Order using explicit signals.** Apply a consistent ordering method: value vs. effort, WSJF (Weighted Shortest Job First), cost of delay, or MoSCoW. Record the rationale for top-5 priorities.
5. **Identify DoR violations.** For each top-20 item, check: goal clear, acceptance criteria present, dependencies known, no open product decision blocking start.
6. **Remove or archive stale items.** Items with no clear value, no owner, or older than three sprints without movement should be archived or explicitly deprioritized with a note.
7. **Publish and communicate.** Make ordering and rationale visible to the team and stakeholders. Record changes that affect sprint or release expectations.

## Outputs

- Ordered, clean product backlog with intake/triage classification.
- Epics and stories grouped by user outcome or product goal.
- Priority rationale note (top-5 items with ordering logic).
- Backlog cleanup log (removed or archived items with reason).
- Open decisions and handoffs for blocked or unclear items.

## Named Patterns

**Good — Story with clear goal and outcome:**
```
Title: "As a logged-in buyer, I can save my delivery address so I do not re-enter it each order."
Goal: Reduce checkout friction for returning users.
Scope: Save / retrieve one default delivery address per user account.
Out of scope: Multiple addresses (later sprint).
Acceptance: User can save address; next checkout pre-fills it; address editable.
```

**Bad — Story without goal or acceptance:**
```
Title: "Delivery address."
(No goal, no scope boundary, no acceptance criteria — cannot be estimated or implemented.)
```

---

**Good — WSJF ordering with explicit rationale:**
```
Epic A: Cost of delay = high (blocks Q2 revenue milestone), job size = S → WSJF = 13.
Epic B: Cost of delay = medium (nice-to-have), job size = L → WSJF = 3.
Decision: Epic A first. Recorded in backlog ordering note dated 2026-05-10.
```

**Bad — Priority by loudest stakeholder:**
```
Epic B moved to top because VP asked. No rationale. Epic A missed Q2 milestone.
```

---

**Good — DoR check before sprint planning:**
```
Item "Payment retry logic":
✓ Goal clear (reduce failed payments > 3%)
✓ Acceptance criteria present (3 conditions, edge case noted)
✓ Dependency on PSP API: SA confirmed contract available
✓ No open product decision
→ Status: Ready
```

**Bad — Item enters sprint without DoR:**
```
Item "Payment retry logic" — no acceptance criteria, SA not consulted, PSP contract unknown.
Team spends day-1 of sprint clarifying basics. Sprint goal missed.
```

---

**Good — Epics grouped by user outcome:**
```
Epic: "Faster checkout for returning buyers"
  → Story: Save delivery address
  → Story: Pre-fill payment method
  → Story: One-click reorder
```

**Bad — Epics grouped by component:**
```
Epic: "Database changes"
  → Delivery address table
  → Payment method table
  (Team cannot explain value to stakeholder; acceptance is untestable.)
```

---

**Good — Intake triage with explicit rejection:**
```
Request from Sales: "Add PDF export to every screen."
Triage: No roadmap item, no user problem stated, Q2 scope frozen.
Decision: Reject for now. Recorded in intake log. Sales notified with reason.
```

**Bad — Intake without triage:**
```
Request added directly to top of backlog. Existing priorities displaced without discussion.
```

## Boundaries

- Does not decide product strategy or roadmap priority — those belong to Product Manager.
- Does not assign delivery dates, budget, or resource allocation — those belong to Project Manager / Delivery Manager.
- Does not write system specifications, API contracts, or data models — those belong to System Analyst.
- Does not replace analytics conclusions or experiment design — those belong to Product Analyst.
- Does not make QA or testing decisions for individual items.

## Sources

**Priority 1 — Canonical method references:**
- Scrum Guide (Schwaber & Sutherland): https://scrumguides.org/scrum-guide.html
- Roman Pichler, "Strategize": https://www.romanpichler.com/books/strategize/
- Marty Cagan, "Inspired" (2nd ed., SVPG Press, 2017) — backlog ownership chapter.

**Priority 2 — Practice guides:**
- Scrum.org, Introduction to Product Backlog: https://www.scrum.org/resources/introduction-product-backlog
- Agile Alliance, Product Backlog: https://agilealliance.org/glossary/backlog/
- Mike Cohn, "User Stories Applied" — story format and splitting heuristics.

**Priority 3 — Supplementary reading:**
- SVPG Blog (Silicon Valley Product Group): https://www.svpg.com/articles/
- ProductPlan, Backlog Management Guide: https://www.productplan.com/learn/product-backlog/

## Handoff

```
To: product-manager
Task: Confirm roadmap priority for [initiative] before backlog ordering.
Context: Backlog reorder affects sprint planning; need clear signal on top goal.
Inputs: Current backlog state, release timeline, open decisions.
Expected artifact: Priority ranking with brief rationale.
Acceptance criteria: Top-3 goals confirmed; trade-offs between them explicit.
```

```
To: system-analyst
Task: Clarify scope and technical constraints for [story or epic].
Context: Story cannot reach DoR without system-level detail on [dependency or integration].
Inputs: Product intent, stakeholder context, open questions.
Expected artifact: Functional scope note or system specification stub.
Acceptance criteria: Team can estimate and start implementation.
```
