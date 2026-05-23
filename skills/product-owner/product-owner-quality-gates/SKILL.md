---
name: product-owner-quality-gates
description: Use when Product Owner backlog items, scope briefs, acceptance criteria, or readiness artifacts need a structured review for clarity, boundary compliance, and correct ownership before handoff to delivery teams or stakeholders.
family: lead
profile_level: Senior+
---

# Product Owner Quality Gates

## Purpose

Review Product Owner artifacts — backlog items, scope briefs, acceptance criteria, readiness checklists — against a structured quality rubric to catch scope creep, boundary violations, vague or untestable criteria, and missing handoffs before those artifacts drive delivery work. This is a lead skill: it audits the PO's own output and the output of less experienced POs in adjacent teams.

## Use When

- A backlog slice, sprint scope, or release scope is about to be handed to the engineering team for planning.
- Acceptance criteria may be vague, untestable, scope-creeping, or absorbing adjacent-role ownership (QA, System Analyst, Project Manager, BI).
- A less experienced PO on an adjacent team needs a peer review of their artifacts before delivery.
- A cross-team release requires a consistent standard of readiness across multiple backlog owners.
- The team is experiencing repeated sprint failures and a root-cause check of PO artifact quality is needed.

## Do Not Use When

- Product strategy or roadmap quality review is needed — that belongs to Product Manager.
- QA test plan quality review is needed — that belongs to QA.
- System specification quality review is needed — that belongs to System Analyst.
- Delivery governance review (plan, timeline, resource) is needed — that belongs to Project Manager / Delivery Manager.

## Inputs

- Backlog items, scope briefs, acceptance criteria, readiness checklists.
- Role boundaries reference (who owns what at PO boundary with PM, SA, QA, UX/UI, BA).
- Expected receiving team and delivery event (sprint planning, release, stakeholder review).
- Decision log entries for scope changes under review.

## Workflow

1. **Frame the review scope.** Name the artifact set under review, the delivery event it feeds, and the expected audience.
2. **Run the goal and value check.** Each backlog item must have: a stated user or business goal, a named actor, and a connection to an agreed product outcome. Items with no goal trigger a rewrite or deferral.
3. **Run the scope and AC quality check.** For each acceptance criterion: is it observable, independently testable, and free of implementation detail? Does it state what, not how? Does it include at least one boundary condition?
4. **Run the boundary violation check.** Flag any artifact that absorbs: QA test case design, system API specification, business process modeling, delivery planning, analytics methodology, or product strategy. Each violation gets a named fix and a handoff recommendation.
5. **Run the DoR compliance check.** For items claiming "Ready" status: verify all DoR conditions are met. Downgrade to "Needs refinement" if any condition fails.
6. **Produce an ordered findings list.** Classify each finding: Blocker (cannot proceed), Major (likely to cause sprint failure), Minor (quality issue, proceed with fix). Assign owner and recommended action.
7. **Communicate findings and route fixes.** Present findings to the artifact owner. Do not rewrite adjacent-role artifacts — recommend the handoff instead.

## Outputs

- Quality gate review with findings ordered by severity (Blocker / Major / Minor).
- Required fixes per finding with owner and recommended action.
- Boundary violation flags with handoff recommendations.
- DoR compliance summary per item.
- Approved or conditionally approved artifact set for handoff.

## Named Patterns

**Good — AC flagged as untestable with fix recommendation:**
```
Finding: "User gets a great onboarding experience" — not testable.
Severity: Blocker.
Fix: Rewrite as observable conditions.
Example: 
  AC 1: User completes onboarding wizard (5 steps) and lands on dashboard.
  AC 2: Each step shows progress indicator (1 of 5 … 5 of 5).
  AC 3: User can skip optional step 4 without error.
Owner: PO. Action: Rewrite before sprint planning.
```

**Bad — Vague AC approved without review:**
```
"User gets a great experience" accepted at planning.
Team interprets differently. Sprint produces feature that stakeholder rejects at review.
```

---

**Good — Boundary violation flagged with handoff:**
```
Finding: Story "Payment retry" includes: "SA should implement exponential backoff with 3 retries."
Severity: Major boundary violation — implementation detail in product AC.
Fix: Remove implementation detail. Replace with product-level condition:
  "If payment fails, user is offered a retry option; the system retries up to [n] times (SA to specify n and strategy)."
Handoff: System Analyst to specify retry policy in system specification.
Owner: PO to revise AC; SA to add spec.
```

**Bad — PO writes implementation spec in acceptance criteria:**
```
AC: "Backend to implement exponential backoff: 1s, 2s, 4s, max 3 retries using RabbitMQ."
Engineering follows PO spec. SA later provides conflicting contract. Conflict mid-sprint.
```

---

**Good — DoR downgrade with reason:**
```
Story: "Referral program invite flow"
DoR check:
  ✓ Goal stated.
  ✓ Scope bounded.
  ✗ AC: only 1 condition (happy path only; no error or limit case).
  ✗ Dependency: referral engine API contract not confirmed by SA.
Verdict: Needs refinement. Cannot enter sprint planning.
Actions: PO adds 2 AC conditions; SA confirms API by 2026-05-26.
```

**Bad — Item accepted as Ready with incomplete DoR:**
```
Story enters sprint with 1 AC and no SA confirmation.
Day 2: engineering asks about error states. Day 3: SA confirms different API shape.
Story pulled from sprint. Sprint velocity drops.
```

---

**Good — Peer review of adjacent PO artifact:**
```
Review of PO (team B) sprint scope for Release 3.2:
Finding 1 (Minor): 3 stories missing explicit exclusions — recommend adding "Out of scope" line.
Finding 2 (Major): "Admin report" AC contains SQL query — implementation detail; route to SA.
Finding 3 (Blocker): "Real-time alerts" story: no dependency status on WebSocket service (DevOps).
Recommendation: Resolve blocker before planning; fix minor/major in refinement.
```

**Bad — No peer review for cross-team release:**
```
Team B artifacts merged into release without review.
Release contains 2 stories with untestable AC and 1 story blocked by undiscovered dependency.
Release delayed 2 weeks.
```

---

**Good — Quality gate output for sprint planning:**
```
Sprint 17 artifact quality gate:
  Approved (no changes needed): 6 stories.
  Conditionally approved (minor fix before planning): 2 stories — AC boundary condition missing.
  Requires refinement (major): 1 story — SA dependency not confirmed.
  Blocked: 1 story — product decision pending PM.
Action: Planning proceeds with 6 approved + 2 conditionally approved; 2 stories excluded.
```

**Bad — Planning proceeds with all items regardless of quality:**
```
11 stories in planning. 4h session. 3 stories pulled mid-discussion.
Sprint goal set for 7 stories. Morale impact. Repeated sprint after sprint.
```

## Boundaries

- Does not approve product strategy, roadmap priority, or commercial decisions.
- Does not rewrite adjacent-role artifacts (SA spec, QA test plan, PM strategy brief) — recommends handoff.
- Does not approve delivery plan, release calendar, or resource allocation.
- Does not make final go/no-go for release — that belongs to Product Manager; does inform PO readiness position.
- Does not own analytics methodology or experiment design quality review.

## Sources

**Priority 1 — Canonical method references:**
- Scrum Guide (Schwaber & Sutherland): https://scrumguides.org/scrum-guide.html — Sprint Review, DoD, transparency.
- Mike Cohn, "User Stories Applied" — AC quality and DoR patterns.
- Roman Pichler, "Agile Product Management with Scrum": https://www.romanpichler.com/books/

**Priority 2 — Practice guides:**
- Scrum.org, Definition of Done: https://www.scrum.org/resources/blog/done-understanding-definition-done
- Agile Alliance, Acceptance Testing: https://agilealliance.org/glossary/acceptance/
- SAFe, Team Backlog Quality: https://scaledagileframework.com/team-backlog/

**Priority 3 — Supplementary reading:**
- SVPG Blog: https://www.svpg.com/articles/
- ProductPlan, Product Backlog Refinement: https://www.productplan.com/learn/product-backlog/

## Handoff

```
To: system-analyst
Task: Remove implementation detail from [story] AC and provide system-level specification.
Context: PO quality gate found implementation detail in product-level AC — boundary violation.
Inputs: Current AC with flagged violation, product intent.
Expected artifact: System specification covering the technical behavior.
Acceptance criteria: Product AC rewritten as observable conditions only; tech detail in SA spec.
```

```
To: qa-engineer
Task: Review [story] acceptance criteria for testability and QA coverage gaps.
Context: Quality gate found AC that may be incomplete from a QA perspective.
Inputs: AC list, story scope, known edge cases.
Expected artifact: QA assessment — which AC are testable, which need additional test design.
Acceptance criteria: PO can finalize AC knowing QA coverage is confirmed.
```
