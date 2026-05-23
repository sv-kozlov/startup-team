---
name: shared-cross-functional-alignment
description: Use when work that spans multiple roles, teams, or systems requires explicit ownership mapping, dependency resolution, decision routing, or a coordinated handoff payload — so that each role can proceed without absorbing adjacent ownership.
---

# Shared Cross-Functional Alignment

## Purpose

Make ownership, dependencies, and decision routing explicit across role boundaries so that work can proceed without role overlap, silent assumptions, or ownership gaps. The method produces structured alignment artifacts — ownership maps, dependency logs, handoff payloads, and decision records — rather than soft agreements that dissolve at the next context switch.

## Use When

- A change, initiative, or decision touches artifacts, systems, or user groups owned by two or more roles, and no single role can move forward without input from the others.
- Ownership of a decision, artifact, or open question is unclear or contested between roles.
- A handoff is imminent and the receiving role needs explicit context, inputs, expected artifact, and acceptance criteria — not an informal verbal brief.
- A dependency between teams creates a scheduling or sequencing constraint that must be tracked and communicated.
- A cross-role working session has produced decisions, assumptions, and actions that must be captured before they are lost.
- A shared product goal requires multiple functions (product, engineering, design, QA, data, operations) to align on their respective contributions without each role attempting to own the whole.

## Do Not Use When

- The task is deciding product priority, roadmap sequencing, or strategic bets → Product Manager owns product prioritization; this skill carries the decision, not makes it.
- The task is delivery governance — milestone tracking, budget, resource allocation, or risk escalation → Project Manager / Delivery Manager owns delivery governance.
- The task is single-role artifact authoring where no cross-role dependency exists; use the relevant role-local skill.
- The task is restructuring teams or reporting lines → organizational design is outside scope; escalate to leadership.

## Inputs

- Description of the shared goal, change, or decision that requires multi-role participation.
- Current state of the affected artifacts and who owns them.
- Known open questions, assumptions, and conflicts between roles.
- Role boundaries for all participating roles (consult boundary files or role contracts).
- Target decision date or handoff deadline.

## Workflow

1. **Identify the shared decision or dependency.** State in one sentence: what must be resolved, and why no single role can resolve it alone. If the dependency is one-sided (one role needs input from another), model it as a handoff request, not as an alignment session.

2. **Map ownership by role and artifact.** List every artifact or decision in scope and assign an owner role. Use a simple table: artifact / decision, owner role, consumer roles, current status. Mark cells where ownership is contested or absent.

3. **Apply a decision routing model.** Use DACI (Driver, Approver, Contributor, Informed) or RACI to assign accountability for each decision:
   - *Driver*: who coordinates the decision process.
   - *Approver*: who makes the final call.
   - *Contributors*: who provides input.
   - *Informed*: who must know the outcome.
   Only one Approver per decision. If no Approver is named, the decision is blocked — record it as blocked with an escalation path.

4. **Define handoff payloads.** For each role-to-role dependency, write a compact handoff block:
   - *To*: receiving role.
   - *Context*: what the receiving role needs to know to proceed.
   - *Inputs*: artifacts being transferred.
   - *Expected artifact*: what the receiving role must produce.
   - *Acceptance criteria*: how the sending role will know the handoff is complete.
   - *Deadline or trigger*: when the handoff should occur.

5. **Surface and record open items.** For each unresolved point, classify it as: decision needed (DACI approver must decide), assumption (recorded with a risk note), dependency (another role must produce something before this can proceed), or risk (a condition that may affect the shared outcome). No open item should be left unlabeled.

6. **Agree on a follow-up cadence or resolution path.** State how each open item will be resolved: async written answer, synchronous session, escalation path. Assign an owner and a date to each. Alignment without a follow-up path is a conversation, not an artifact.

## Outputs

- Ownership and artifact map: table of artifact/decision, owner, consumers, and status.
- DACI or RACI matrix for the shared decision set.
- Handoff payload blocks: one per role-to-role dependency.
- Decision and dependency log: open items with type, owner, deadline, and resolution path.
- Alignment note or session summary capturing what was decided, what was deferred, and what actions were taken.

## Role Modes

### Business Analyst

Aligns business stakeholders, Product Manager, System Analyst, UX/UI, QA, Data/BI, and Delivery around business scope, business rules, process boundaries, and UAT readiness. Uses this skill to make explicit which business requirements have been signed off, which cross-role questions remain open, and which handoff payloads are ready for System Analyst or QA. Does not absorb product prioritization, system specification, or delivery scheduling — those surface as handoff tasks.

### Product Owner

Aligns the delivery team (engineering, QA, design, operations) around the sprint-level scope, acceptance criteria, and readiness conditions. Uses this skill to surface and resolve cross-team blockers before the sprint begins and to confirm that each team has the inputs they need. Does not own product strategy alignment (Product Manager) or delivery plan governance (Project Manager).

### Product Manager

Aligns product, engineering, design, data, and business stakeholders around the product outcome goal — ensuring each function understands its contribution to the shared bet without collapsing ownership. Uses DACI to make product-level decisions explicit: who approves scope changes, who contributes evidence, who must be informed. Does not own sprint backlog alignment (Product Owner) or delivery governance (Project Manager).

### Project Manager

Aligns all participating teams, vendors, and stakeholders around delivery milestones, dependencies, risks, and escalation paths. Uses this skill to produce dependency logs, cross-team handoff schedules, and decision records for governance forums. Does not own product priority, scope definition, system specification, or QA strategy — surfaces those as handoff tasks to the respective owners.

## Boundaries

- Does not override role ownership. Alignment maps and DACI matrices describe ownership; they do not transfer it.
- Does not make product priority decisions, architecture choices, QA release decisions, or engineering estimates. Those belong to the respective roles; this skill routes decisions to the right approver.
- Does not duplicate artifacts owned by adjacent roles. The alignment note references artifacts, not replaces them.
- Does not substitute for delivery governance ceremonies (sprint planning, standup, retrospective) when a specific ceremony role owns facilitation.

## Named Patterns

### Good — DACI matrix for a product scope decision
```
Decision: Which payment methods to support in v1.
Driver: Product Manager
Approver: Head of Product (if strategic) or Product Manager (if tactical)
Contributors: Business Analyst (business rules), System Analyst (integration feasibility),
              Engineering Lead (effort estimate)
Informed: QA Lead, Finance Controller, Marketing
Decision date: 2025-06-03
```
One Approver, explicit contributors, deadline set. No role absorbs another's ownership.

### Bad — Consensus-required approval
Decision: "The team agrees on the payment methods." No named Approver. Result: the decision is re-opened at every retro; contributors become blockers; the sprint starts with scope uncertainty.

### Good — Structured handoff payload
```
To: System Analyst
Context: Business Analyst has completed business rules for the discount engine (BR-041 to BR-055).
         Rules have been validated by Finance Controller (2025-05-15).
Inputs: rule-catalog-v1.1.md, decision-table-discounts.xlsx
Expected artifact: Functional specification for discount calculation with API contract draft.
Acceptance criteria: spec covers all rule types (BR-041 to BR-055); edge cases from
                     conflict log resolved; API error shapes included.
Deadline: 2025-06-05
```
The receiving role knows exactly what it receives, what it must produce, and how success is measured.

### Bad — Verbal handoff
"I sent you the business rules, can you spec it out?" No context, no explicit inputs, no expected artifact, no acceptance criteria. System Analyst starts work on a different scope or produces an artifact that misses key rules.

### Good — Dependency log entry
```
Dependency: Frontend development depends on API contract for discount calculation.
Owner: System Analyst (contract) → Backend Go Developer (implementation) → Frontend (integration).
Status: Contract draft due 2025-06-05. Frontend blocked until contract is merged.
Risk: If contract slips, Frontend sprint goal is at risk. Escalation path: Product Manager.
```
Sequence, ownership, blocking status, and escalation path in one entry.

### Bad — Undocumented assumption
Frontend starts development using a guessed API shape. Contract is published two weeks later with a different response structure. Integration requires rework affecting both backend and frontend.

### Good — Open-item classification
```
[DECISION NEEDED] Which error handling strategy for unavailable discount service?
  Options: (a) block checkout, (b) apply no discount, (c) retry with timeout.
  Approver: Product Manager. Input needed from: Engineering Lead (feasibility).
  Due: 2025-05-28.
```
Type is explicit (decision needed vs assumption vs risk). Approver named. Due date set.

### Bad — Open item as assumption
"Discount service unavailability is rare, so we'll handle it gracefully." No approver, no decision record. Team discovers in UAT that "gracefully" means different things to product, engineering, and QA.

### Good — Alignment note as a lightweight artifact
```
Alignment note: Payment methods for v1 — 2025-05-28
Attendees: PM, BA, SA, Engineering Lead
Decided: Support card, SBP, and e-wallet for v1. Bank transfer deferred to v2.
Owner of rule catalog update: BA (due 2025-06-02).
Owner of integration spec: SA (due 2025-06-05).
Owner of v2 scope note in roadmap: PM (due 2025-05-30).
Open: Partner payment method — DACI in progress. Approver: Head of Product.
```
Session produces a written artifact, not a memory. Every role leaves knowing exactly what it owns.

### Bad — Alignment by meeting summary in chat
Session decisions posted in a team chat message. No owner assignments, no document, no due dates. Two weeks later, Engineering asks "what was decided about bank transfer?" No one can find the original message.

## Sources

### Priority 1 — Method canon

- IIBA BABOK Guide v3, Chapter 5: Strategy Analysis (stakeholder needs, change context, alignment) and Chapter 7: Requirements Life Cycle Management (trace, maintain, prioritize) — https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/
- Marty Cagan, "EMPOWERED: Ordinary People, Extraordinary Products" (Wiley, 2020) — coalition model for cross-functional product teams and ownership without bureaucracy
- Patrick Lencioni, "The Advantage" (Jossey-Bass, 2012) — organizational clarity as an alignment enabler; clarity of ownership is the prerequisite, not an output, of alignment

### Priority 2 — Orientation

- LeanKit / Planview — DACI Decision-Making Framework — https://leankit.com/learn/project-management/daci-decision-making-framework/ (practical DACI structure and template)
- ThoughtWorks Technology Radar — team interaction modes — https://www.thoughtworks.com/radar (orientation on cross-team interaction models)
- Google re:Work — Guide: Understand team effectiveness — https://rework.withgoogle.com/guides/understanding-team-effectiveness/steps/introduction/ (evidence base for what makes cross-functional collaboration reliable)

### Priority 3 — Background

- Wikipedia — RACI matrix — https://en.wikipedia.org/wiki/Responsibility_assignment_matrix
- Scrum Guide 2020 — cross-functional team definition — https://scrumguides.org/scrum-guide.html

## Handoff

- When a shared decision requires final approval from a role not in the current conversation → create a DACI record and route to the named Approver.
- When alignment surfaces product prioritization conflicts → hand off to Product Manager.
- When alignment surfaces delivery schedule or resource conflicts → hand off to Project Manager.
- When alignment surfaces system architecture or API contract conflicts → hand off to System Analyst or System Architect.
- When an open item has no named owner after the session → escalate to the shared team lead or Product Manager before the next sprint begins.
