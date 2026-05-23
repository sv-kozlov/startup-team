---
name: backlog-refinement
description: Use when backlog items must be split, clarified, dependency-mapped, and prepared to a Definition of Ready before team sprint or release planning.
family: method
profile_level: Senior+
---

# Backlog Refinement

## Purpose

Prepare backlog items for team planning by raising clarity, reducing size, surfacing dependencies, and confirming readiness so the team can estimate and start work without spending planning time on clarification.

## Use When

- Items are too large, vague, duplicated, or blocked to enter sprint planning.
- A team needs refinement notes and a DoR check before the next sprint.
- Open questions (business rules, edge cases, dependencies) prevent estimation or discussion.
- Acceptance criteria are missing, ambiguous, or untestable.
- A large epic must be broken into deliverable increments before roadmap planning.

## Do Not Use When

- The product direction itself is unclear — resolve with Product Manager first; refinement of misdirected items wastes team time.
- Technical architecture or system design must be decided — route to Tech Lead or System Analyst; PO can facilitate but does not own the answer.
- Items require QA test design detail beyond product acceptance — route to QA.
- Business process modeling (AS IS / TO BE) is needed — route to Business Analyst.

## Inputs

- Backlog items, epics, user stories, defects, or stakeholder requests.
- Product intent, goal, and constraints from Product Manager or product brief.
- Acceptance criteria drafts, design notes, system analysis notes, QA feedback.
- Team estimates or capacity signals from previous sprints.
- Dependency map from Project Manager / Delivery Manager or Tech Lead.

## Workflow

1. **Select items for refinement.** Pick items from the top of the ordered backlog that are likely to enter planning in the next 1–2 sprints. Include blockers that hold up other items.
2. **Check DoR gate.** For each item, verify: goal stated, user/actor named, scope bounded, acceptance criteria present, dependencies listed, no open product decision blocking start.
3. **Split oversized items.** Use splitting heuristics: by workflow step, by user type, by data variant, by acceptance condition, by dependency boundary, or by happy-path vs. edge case.
4. **Clarify acceptance criteria.** Write or sharpen acceptance conditions: observable behavior, boundary cases, explicit exclusions. Each criterion must be independently testable.
5. **Surface and assign open questions.** For each unanswered question, identify the owner (Product Manager, System Analyst, Business Analyst, UX/UI, QA) and create a handoff or action.
6. **Update readiness state.** Mark each item: Ready (all DoR criteria met), Needs refinement (specific gap noted), Blocked (external dependency), or Needs decision (product or business decision required).
7. **Confirm with the team.** Run or pass refinement notes to the team. Collect and record any new questions or blockers that emerge from engineering perspective.

## Outputs

- Refined backlog items with updated acceptance criteria and scope notes.
- Split recommendations with rationale (why split at this boundary).
- DoR status per item (Ready / Needs refinement / Blocked / Needs decision).
- Open questions log with owner and due date.
- Handoff tasks for System Analyst, QA, UX/UI, and Product Manager.

## Named Patterns

**Good — Story with explicit DoD/DoR:**
```
Story: "Filter job listings by remote/hybrid/onsite"
Goal: Reduce irrelevant results for remote-first candidates.
Scope: Filter UI, query parameter, result count update.
Out of scope: Saving filter preference (later story).
Acceptance:
  1. Filter visible on search page.
  2. Result list updates without full page reload.
  3. Empty state shown when no results match filter.
  4. Filter state preserved on browser back.
DoR: ✓ goal, ✓ scope, ✓ AC, ✓ design mockup attached, ✓ API field confirmed by SA.
```

**Bad — Story without DoR:**
```
Story: "Filter by remote"
(No scope, no acceptance, no design, no API confirmation.
Team spends half of planning discussing basics. Sprint delayed.)
```

---

**Good — Split by happy path vs. edge case:**
```
Epic: "Mortgage application form"
Story 1 (sprint N): Happy path — applicant submits complete form, application created.
Story 2 (sprint N+1): Edge cases — incomplete form validation, duplicate application guard.
Story 3 (sprint N+2): Error states — service timeout, partial save, resume flow.
```

**Bad — Monolithic story that cannot be tested or demoed incrementally:**
```
Story: "Build full mortgage application form with all validations, error states, and retries."
(Cannot demo in one sprint; acceptance is impossible to verify end-to-end.)
```

---

**Good — Acceptance criteria testable and bounded:**
```
AC for "Send booking confirmation email":
  1. Email sent within 30 seconds of booking creation.
  2. Email contains: booking ID, date/time, address, cancellation link.
  3. If email delivery fails, booking is still created; error logged; retry in 5 min.
  4. No email sent for cancelled bookings.
```

**Bad — Acceptance criteria that is a feature description:**
```
AC: "User gets a nice confirmation email with all booking details."
(Not independently testable; no timing, no failure handling, no boundary defined.)
```

---

**Good — Open question with owner assigned:**
```
Open question: "What happens when the user's KYC check is pending at payment time?"
Owner: Business Analyst (business rule) + System Analyst (technical flow).
Due: before next refinement session (2026-05-27).
Action: BA to confirm rule; SA to model flow; PO to incorporate in AC.
```

**Bad — Open question left undocumented:**
```
Team discusses KYC edge case in refinement. No decision recorded.
Same question resurfaces at sprint planning. Team loses 40 min. Story delayed.
```

---

**Good — Refinement session output note:**
```
Refinement 2026-05-20:
  - "Payment retry logic" → Ready (AC sharpened, 3 ACs added, SA confirmed PSP contract)
  - "Admin export" → Split into export-trigger (sprint 12) + scheduling (sprint 13)
  - "Fraud alert banner" → Blocked pending InfoSec approval (owner: BA, due 2026-05-25)
```

**Bad — No refinement record:**
```
Team had a refinement call. Stories "good enough." Planning starts with same questions.
```

## Boundaries

- Does not own delivery schedule, resource plan, or sprint commitment — those belong to Project Manager / Delivery Manager and the engineering team.
- Does not make engineering estimates — the engineering team owns estimation.
- Does not own product strategy — if an item's direction is wrong, stop refinement and route to Product Manager.
- Does not replace System Analyst functional specification — AC is product-level, not system-level.
- Does not replace QA test design — acceptance criteria are product intent, not test cases.

## Sources

**Priority 1 — Canonical method references:**
- Scrum Guide (Schwaber & Sutherland): https://scrumguides.org/scrum-guide.html
- Mike Cohn, "User Stories Applied" — splitting heuristics and AC patterns.
- Roman Pichler, "Agile Product Management with Scrum": https://www.romanpichler.com/books/

**Priority 2 — Practice guides:**
- Agile Alliance, Backlog Refinement: https://agilealliance.org/glossary/backlog-refinement/
- Scrum.org, Product Backlog: https://www.scrum.org/resources/introduction-product-backlog
- Richard Lawrence, story splitting patterns: https://www.humanizingwork.com/the-humanizing-work-guide-to-splitting-user-stories/

**Priority 3 — Supplementary reading:**
- SVPG Blog: https://www.svpg.com/articles/
- Scrum.org Blog on Definition of Ready: https://www.scrum.org/resources/blog/definition-ready

## Handoff

```
To: system-analyst
Task: Define functional behavior and system constraints for [story].
Context: Story at DoR gate; system-level detail needed for AC to be testable.
Inputs: Product intent, AC draft, open technical questions.
Expected artifact: Functional scope note or system specification stub.
Acceptance criteria: Engineering team can estimate and start implementation.
```

```
To: product-manager
Task: Confirm product direction for [epic or initiative] before refinement continues.
Context: Refinement reveals direction mismatch with current roadmap item.
Inputs: Current epic, stakeholder input, roadmap reference.
Expected artifact: Clear go/no-go and priority signal.
Acceptance criteria: PO can confidently set DoR target and resume refinement.
```
