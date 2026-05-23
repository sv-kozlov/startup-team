---
name: exploratory-and-session-based-testing
description: Use when running a structured discovery session to find defects that scripted tests miss — using a charter, applying SFDPOT or CRUSPIC heuristics, conducting a tour, and producing a session report with findings and coverage notes.
family: method
profile_level: Senior+
---

# Exploratory and Session-Based Testing

## Purpose

Find defects that scripted tests do not find, through structured unscripted investigation guided by charters
and heuristics. Exploratory testing is not ad-hoc clicking: it has a scope (charter), a time limit (session),
a method (heuristic or tour), and a deliverable (session report). It is the primary technique for discovering
unknown-unknowns and validating product behavior in the presence of ambiguous or evolving requirements.

## Use When

- A new feature is deployed and scripted tests cover known behavior but not undiscovered edge cases.
- A complex workflow has many state combinations that decision tables do not fully capture.
- A recent release had an escaped defect and targeted risk-based exploration is needed.
- Requirements are vague, evolving, or under rapid change — scripted tests cannot keep pace.
- Reviewing a product area for testability, observability, or behavior consistency.
- Time-boxed verification when a full scripted regression is not feasible.

## Do Not Use When

- Verifying specific documented acceptance criteria -> use `test-design-and-coverage`.
- Automated regression must be designed -> use `test-automation-framework`.
- A performance anomaly needs load measurement -> use `performance-and-load-testing`.

## Inputs

- Feature description, user story, or area of the product under exploration.
- Risk list (from `test-strategy-and-planning` or recent defect history).
- Time budget for the session (typical: 60-90 minutes per charter).
- Known heuristics or areas of concern from system-analyst or tech-lead.
- Access to the product under test, test environment, logs, and diagnostic tools.

## Workflow

1. Write the charter before the session. A charter answers: what is the target area, what is the main
   test idea, and what risks are being explored? Charter format:
   ```
   Explore [area of the product]
   With [approach or technique]
   To discover [risks or information sought]
   ```
   One charter per session. If the scope is too large for one session, split into multiple charters.

2. Choose a heuristic to guide the session. Two canonical models:

   SFDPOT (James Bach, Structure/Function/Data/Platform/Operations/Time):
   - Structure: what are the components and their relationships?
   - Function: what does it do? what should it not do?
   - Data: what data does it handle, transform, or produce?
   - Platform: what environments, browsers, devices, OS versions, configurations?
   - Operations: how is it used, by whom, in what sequence?
   - Time: what happens at startup, shutdown, under sustained use, with time-sensitive inputs?

   CRUSPIC (Coupling/Reliability/Usability/Security/Performance/Installability/Compatibility):
   Use when the focus is quality attribute discovery rather than functional discovery.

3. Conduct the session. Time-box strictly. Use a timer. During the session:
   - Follow the charter but allow brief detours when something surprising appears (note the detour).
   - Document findings as you go (not after): what you did, what you found, questions raised.
   - Classify findings: defect, question, risk note, or testability problem.
   - Note setup and teardown time separately from test execution time (charter coverage metric).

4. Apply tour techniques for systematic coverage of a complex area:
   - Intellectual tour: follow the most complex paths.
   - Saboteur tour: try to break the feature with invalid, boundary, or unexpected inputs.
   - Money tour: test the paths most critical to business value.
   - Landmark tour: visit every significant UI component or API endpoint in the area.
   - Garbage tour: feed the system trash data, wrong types, empty strings, very large values.

5. Write the session report immediately after the session. Delay degrades accuracy.
   Session report structure:
   - Charter text.
   - Duration (setup time / test time / investigation time).
   - Coverage notes: what was explored, what was not reached.
   - Findings: defects (filed), risks (noted), questions (for SA or PO), testability issues.
   - Metrics: charter completion (%), bugs found, risks identified.
   - Recommendations: which findings need follow-up scripts or automation.

6. Debrief with a developer or tech lead when findings are complex or ambiguous. A 15-minute
   debrief after a session is more valuable than a long written report no one reads.

7. Convert significant findings to scripted tests or regression cases. Exploratory sessions
   that produce reproducible defects should result in regression cases to prevent re-occurrence.

## Outputs

- Test charter (before the session).
- Session report with findings classified by type.
- Defect reports for all filed bugs (link to defect tracker).
- Risk notes for uncovered areas or unexpected behavior that needs investigation.
- Recommended scripted test cases or regression additions.

## Named Patterns

### Good — Focused charter with clear scope

```
Charter: Explore the discount code application flow at checkout
With: SFDPOT heuristic, focusing on Data and Time dimensions
To discover: edge cases in expired codes, stacked codes, codes applied to ineligible items,
             and timing issues when codes expire during checkout

Session time: 75 minutes
Tester: [name]
Date: 2026-05-23
Environment: Staging v3.42
```

The charter is specific. Another tester can read it and understand what was explored.

### Bad — Undefined exploration

"Testing the checkout." No charter, no heuristic, no time limit.
After 3 hours: "I tested checkout. Found some stuff."
Coverage is unknown. Findings are not reproducible. No session report.

### Good — SFDPOT application to a discount feature

```
S (Structure): tested single service boundary (API + cache), no multi-service scenarios possible in staging
F (Function): applied valid code, expired code, code with zero remaining uses, code for wrong region
D (Data): tested strings: 0-length, max-length (50), unicode, SQL injection attempt, whitespace padding
P (Platform): Chrome 124 (desktop), mobile web Safari (iOS 17)
O (Operations): applied code before and after adding items to cart; applied same code twice
T (Time): set system time to 1 minute before code expiry; checked behavior at exact expiry boundary
```

Systematic coverage across all SFDPOT dimensions. Coverage note shows what was not reached (no multi-browser
desktop coverage; noted as risk).

### Bad — Random clicking with no heuristic

Tester opens the feature and clicks around. Files two obvious defects. Reports "tested discount."
Time dimension (code expiry boundary) is not explored. Expiry boundary defect escapes to production.

### Good — Session report with metrics

```
Session Report: Discount code checkout
Charter: [as above]
Duration: 75 min total (setup 10 min, testing 55 min, reporting 10 min)

Coverage: 70% of charter completed. Time dimension explored partially; clock manipulation
in staging environment blocked by environment config (noted as environment issue, not product defect).

Findings:
  BUG-0342: 500 error when applying expired code (filed, Critical/High)
  BUG-0343: No error message when discount doesn't apply to item category (filed, Minor/Medium)
  RISK: stacked discount behavior when two valid codes are entered simultaneously — not in spec,
        not tested; recommend SA to clarify
  TESTABILITY: no feature flag available to force code into expired state without system clock change

Recommendations:
  - Add scripted test: TC-347 (expired code -> 422)
  - Add to regression: discount with ineligible item category
  - Ask SA: stacked discount spec
```

### Bad — Session report with no structure

"Found 2 bugs. Discount is mostly OK. There might be edge cases with stacking."
No metrics, no charter completion rate, no testability notes, no action items.

### Good — Saboteur tour on payment input

```
Saboteur tour: payment form field resilience
Target: payment amount field, currency field, card number field

Attempts:
  - amount: -1 (negative) -> received 200 with negative total (BUG-0344)
  - amount: 0 -> received 422 with clear error (OK)
  - amount: 9999999999999.99 (overflow) -> received 500 (BUG-0345)
  - currency: "FAKE" -> received 422 (OK)
  - card number: 15-digit (Amex format) -> validation failed with wrong message (cosmetic, noted)
  - card number: 100 spaces -> trimmed server-side, processed (OK, but logged as potential data leak)
```

Saboteur tour systematically tries to break the feature. Two bugs found that scripted tests missed.

### Bad — Scripted tests only for payment form

Scripted tests cover valid card and one invalid card. Negative amount and overflow are not
in the requirements and are not tested. Defects escape.

### Good — Detour policy during session

```
During SFDPOT exploration of discount codes, noticed that the session timer component
in the checkout flow was not in my charter. Observed it briefly (5 minutes) and noted:
RISK: session timer does not pause when payment dialog is open.
Returned to charter. Detour noted in session report with time spent.
```

Brief, noted detour. Does not become a 3-hour rabbit hole.

### Bad — Uncontrolled detour

Session starts with discount codes. Tester finds a timer issue and spends the rest of the session
on the timer. Charter is not completed. Session report is never written.

## Boundaries

- Owns charter authoring, heuristic application, session execution, and session report.
- Does not own scripted test design -> `test-design-and-coverage`.
- Does not own defect registration (findings go to `defect-management-and-triage`).
- Does not own requirements authorship (questions go to `system-analyst`).
- Does not own regression design for found defects -> `test-design-and-coverage` + `test-automation-framework`.

## Sources

### Priority 1 — Exploratory testing canon

- James Bach: Heuristic Test Strategy Model — https://www.satisfice.com/download/heuristic-test-strategy-model
- James Bach and Michael Bolton: Rapid Software Testing methodology — https://www.satisfice.com/rapid-software-testing
- Jon Bach: Session-Based Test Management — https://www.satisfice.com/download/session-based-test-management
- Cem Kaner: Exploratory Testing (writings) — https://kaner.com/
- ISTQB CTFL v4.0: Exploratory Testing section — https://www.istqb.org/certifications/certified-tester-foundation-level

### Priority 2 — Orientation

- Elisabeth Hendrickson: Explore It! — book reference (Pragmatic Programmers, 2013)
- Lisa Crispin and Janet Gregory: Agile Testing (exploratory testing chapter) — book reference
- Google Testing Blog — https://testing.googleblog.com/

### Priority 3 — Background

- ISTQB Advanced Level Test Analyst: Exploratory testing section — https://www.istqb.org/certifications/advanced-level-test-analyst
- ThoughtWorks Technology Radar — https://www.thoughtworks.com/radar

## Handoff

- Defects found in the session -> `defect-management-and-triage` for structured reporting.
- Requirements questions raised in the session -> `system-analyst` with specific question list.
- Recurring testability problems (no feature flags, no log access) -> `tech-lead` with testability requirements.
- Findings that need regression scripted coverage -> `test-design-and-coverage`.
- Broader risk areas identified -> update `test-strategy-and-planning` for the relevant feature.
