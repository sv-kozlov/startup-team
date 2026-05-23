---
name: product-level-acceptance
description: Use when a Product Owner must define, sharpen, or apply acceptance criteria that express expected product value and observable behavior — without replacing QA test design or system specification.
family: method
profile_level: Senior+
---

# Product-Level Acceptance

## Purpose

Make acceptance conditions explicit enough that engineering, QA, and stakeholders share a single definition of done at the product level — what behavior confirms value is delivered — without the Product Owner absorbing test design or technical specification ownership.

## Use When

- Stories or epics lack acceptance criteria or have criteria that are vague, untestable, or scope-creeping.
- A release needs product-side acceptance signals before QA starts regression.
- Engineering, QA, or stakeholders disagree on what "done" means for a feature.
- An item is returning from development and PO must verify it meets product intent before QA.
- A Definition of Done (DoD) for the team or release needs product-level conditions.

## Do Not Use When

- Detailed test case design, regression scope, or QA strategy is required — route to QA.
- System-level behavior, API contracts, data contracts, or integration behavior must be specified — route to System Analyst.
- Product metrics, success criteria, or experiment design must be defined — route to Product Manager and Product Analyst.
- The product outcome itself is unclear — resolve with Product Manager before writing acceptance criteria for a misdirected feature.

## Inputs

- Story, epic, scope note, design mock, or requirement.
- User goal, business rule, product constraint, and expected observable behavior.
- Known edge cases, error states, and explicit exclusions.
- QA feedback on previous acceptance criteria gaps.

## Workflow

1. **Restate the product outcome.** One sentence: who does what and what changes for them. If the outcome is not clear, stop and resolve with Product Manager before writing criteria.
2. **Enumerate observable conditions.** List each condition that, when verified, confirms the feature works as intended. Use the format: "Given [context], when [action], then [observable result]."
3. **Add boundary conditions.** Include at least one error state, one limit case, and one explicit exclusion to prevent scope creep during development.
4. **Check testability.** Each criterion must be independently verifiable: QA or a stakeholder can confirm it without reading the code.
5. **Check coverage without over-specification.** Product AC covers what, not how. Implementation detail belongs in system specification.
6. **Hand off.** Send detailed test design to QA. Send system-level behavior questions to System Analyst. Send metric or experiment conditions to Product Analyst.

## Outputs

- Product-level acceptance criteria (Given/When/Then or checklist form).
- Boundary conditions: error states, limits, exclusions.
- Acceptance gaps: what is unknown or requires QA, SA, or PM input.
- Handoff tasks for QA (test design), System Analyst (system behavior), Product Manager / Analyst (metric conditions).

## Named Patterns

**Good — Acceptance criteria in Given/When/Then:**
```
Story: "Buyer can pay with saved bank card"

AC 1: Given the buyer has a saved card and the cart total > 0,
      when the buyer selects "Pay with saved card" and confirms,
      then payment is processed and order status changes to "Confirmed" within 10 seconds.

AC 2: Given the card has insufficient funds,
      when the buyer attempts payment,
      then an error "Insufficient funds — try another card" is shown; order is not created.

AC 3: Saved card number is masked (last 4 digits visible only) on all screens.

Explicit exclusion: Adding a new card at checkout is out of scope for this story (separate backlog item #512).
```

**Bad — Acceptance criteria as a feature description:**
```
AC: "User can pay with a saved card and it works correctly."
(Not testable; QA and engineering interpret "correctly" differently. Three defects reopened.)
```

---

**Good — DoD with product conditions:**
```
Definition of Done for "Notification preferences":
✓ User can toggle email / push / SMS independently.
✓ Preference saved and applied to next notification within 60 seconds.
✓ No notification sent for toggled-off channel (verified with test account).
✓ Preference survives logout-login cycle.
✓ Accessibility: toggle label readable by screen reader.
[QA to add: regression on notification service, load test for preference write endpoint.]
```

**Bad — DoD that is just a task checklist:**
```
DoD: "Code merged, tests green, deployed to staging."
(No product-level verification. Feature released with wrong default preference for 30% of users.)
```

---

**Good — Acceptance applied at review:**
```
PO review of "Admin export CSV":
  AC 1: ✓ Export includes all columns per spec.
  AC 2: ✓ Export completes within 5 seconds for ≤10,000 rows.
  AC 3: ✗ Encoding: special characters broken in Excel. → Defect logged. Not accepted.
  AC 4: ✓ Empty state handled ("No data to export" message shown).
Result: Feature returned with one blocking defect. Sprint goal at risk — flagged to Project Manager.
```

**Bad — Acceptance without criteria check:**
```
PO: "Looks good, ship it." → Admin export fails for 15% of users with non-ASCII data.
Support tickets: +40. Hotfix sprint consumed.
```

---

**Good — Acceptance criteria that respects QA boundary:**
```
PO writes: "Payment confirmation email sent within 2 minutes."
QA owns: test cases for email delivery, retry logic, spam folder, bounce handling.
(PO defines the observable product condition; QA designs how to verify it.)
```

**Bad — PO writes test cases instead of acceptance:**
```
PO writes: "Step 1: Create test account. Step 2: Place order. Step 3: Check inbox.
Step 4: Verify subject line. Step 5: Check link expiry."
(PO has crossed into QA territory; QA has no ownership. Regressions missed.)
```

---

**Good — Acceptance for an edge case:**
```
AC: If the session expires during form submission, the form data is preserved in browser
    localStorage; user sees "Session expired — your data is saved, please log in again."
```

**Bad — Edge case ignored in acceptance:**
```
No session-expiry AC. User loses filled mortgage application. Support escalation. GDPR question.
```

## Boundaries

- Does not own QA strategy, regression scope, or test case design.
- Does not own API, data, or integration specifications.
- Does not define product success metrics or experiment design — those belong to Product Manager and Product Analyst.
- Does not approve launch or release — launch decision belongs to Product Manager; release governance to Project Manager / Delivery Manager.

## Sources

**Priority 1 — Canonical method references:**
- Mike Cohn, "User Stories Applied" — acceptance criteria format and DoD patterns.
- Scrum Guide (Schwaber & Sutherland): https://scrumguides.org/scrum-guide.html
- Marty Cagan, "Inspired" (2nd ed.) — product acceptance and delivery feedback loop.

**Priority 2 — Practice guides:**
- Agile Alliance, User Stories: https://agilealliance.org/glossary/user-stories/
- Agile Alliance, Acceptance Testing: https://agilealliance.org/glossary/acceptance/
- Roman Pichler, "Agile Product Management with Scrum": https://www.romanpichler.com/books/

**Priority 3 — Supplementary reading:**
- SVPG Blog: https://www.svpg.com/articles/
- Scrum.org, Definition of Done: https://www.scrum.org/resources/blog/done-understanding-definition-done

## Handoff

```
To: qa-engineer
Task: Design test cases for [story/feature] based on these product-level acceptance criteria.
Context: AC defines what and why; QA owns how to verify, regression scope, and edge cases.
Inputs: AC list, story, scope note, known edge cases.
Expected artifact: Test plan or test case set covering the AC and QA-identified risks.
Acceptance criteria: All product-level AC covered; regression scope confirmed.
```

```
To: system-analyst
Task: Specify system behavior for [AC condition requiring technical detail].
Context: Product AC states observable outcome; system-level behavior (API, data, state) not yet specified.
Inputs: AC draft, product intent, known technical constraints.
Expected artifact: System specification covering the behavior.
Acceptance criteria: Developer can implement without additional clarification from PO.
```
