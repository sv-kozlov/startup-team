---
name: defect-management-and-triage
description: Use when writing, triaging, escalating, or analyzing defect reports — applying the severity vs priority matrix, localizing the defect to the layer of origin, assessing regression risk, and tracking defects from registration through retest to closure.
family: method
profile_level: Senior+
---

# Defect Management and Triage

## Purpose

Make defects actionable: each defect report contains enough information to reproduce, understand, prioritize,
and fix the problem without back-and-forth. Triage separates critical blockers from cosmetic issues, product
defects from environment failures, and real bugs from test data problems. Tracking ensures nothing falls
through cracks between discovery and verification.

## Use When

- Reporting a newly found defect.
- Triaging a batch of defects before a sprint review or release.
- Assessing whether a defect blocks release or can be deferred.
- Analyzing repeated defects to find systemic causes.
- Determining whether a defect is in the product, the test, the test data, or the environment.
- Assessing regression risk of a defect fix.

## Do Not Use When

- Test design to discover defects is the goal -> `test-design-and-coverage`.
- Root cause is a production incident requiring on-call response -> `devops-sre`.
- A defect points to a security vulnerability requiring pen-test follow-up -> `security-engineer`.

## Inputs

- Observed behavior (actual result).
- Test case or scenario that revealed the behavior.
- Environment details: version, build, environment name, OS, browser, device.
- Logs, screenshots, HAR traces, or API response dumps relevant to the defect.
- Expected behavior per specification or acceptance criteria.
- Steps to reproduce.

## Workflow

1. Classify before logging. Is it a product defect (application behaves contrary to spec), a test defect
   (the test is wrong), a data problem (bad test data), or an environment issue (broken environment, not the app)?
   Only product defects go into the defect tracker. Others go into the relevant fix track.

2. Write the defect report. Mandatory fields:
   - Title: what fails, in what context (verb + object + condition).
   - Environment: version/build, environment name, OS, browser/device.
   - Precondition: required system state before reproduction.
   - Steps to reproduce: numbered, minimal, complete.
   - Actual result: exact observed behavior (text, status code, screenshot, log excerpt).
   - Expected result: exact expected behavior per specification (cite the spec or AC, not intuition).
   - Severity: impact on system functionality (Critical/Major/Minor/Trivial).
   - Priority: urgency of fix relative to business needs (High/Medium/Low).
   - Attachments: screenshot, log, HAR, API response.

3. Apply the severity vs priority matrix:

   ```
   | Severity \ Priority | High          | Medium        | Low           |
   |---------------------|---------------|---------------|---------------|
   | Critical            | Release blocker: fix now | Release blocker: fix this sprint | Rare; escalate |
   | Major               | Fix this sprint | Fix next sprint | Defer with risk note |
   | Minor               | Fix this sprint | Defer | Backlog |
   | Trivial             | Cosmetic; backlog | Backlog | Won't fix or design decision |
   ```

   Severity = functional impact. Priority = business urgency. They can differ:
   - High severity / Low priority: a crash in a rarely used admin panel.
   - Low severity / High priority: a typo on the login screen visible to all users.

4. Localize to the layer of origin. State in the defect which layer is suspected:
   UI presentation, API response, backend logic, data store, integration, or environment.
   Localization helps the developer triage faster and prevents sending a frontend defect to a backend team.

5. Assess regression risk. Before marking a fix as ready for retest, assess which other features
   could be affected by the change. Flag related test cases for retest.

6. Retest the fix. Verify the original steps no longer reproduce the defect. Verify related
   regression cases. Update the defect status: Passed (fixed), Failed (not fixed), or
   Partially Fixed (fixed but a new defect introduced).

7. Analyze defect clusters. After a release or sprint, review the defect distribution:
   - Which components had the most defects?
   - Were defects found late (after test execution started) or early?
   - Are there repeated root causes (missing validation, race condition, untested edge case)?
   Document findings and recommend process or test coverage changes.

8. Maintain the defect register. Ensure no open defect is "forgotten": every open defect has
   a current status, an owner, and a resolution plan or an explicit deferral decision.

## Outputs

- Defect report with all mandatory fields.
- Triage decision: severity, priority, layer, release impact.
- Regression risk assessment for the affected area.
- Retest result: fixed / not fixed / partially fixed.
- Defect cluster analysis report (per sprint or release).
- Deferred defect register with rationale.

## Named Patterns

### Good — Complete, reproducible defect report

```
Title: Checkout fails with 500 when applying expired discount code

Environment: Build 3.42.1, Staging, Chrome 124, macOS 14

Precondition:
  - User is authenticated
  - Cart contains at least one item
  - Discount code "SAVE10" exists and is expired (expiry: 2024-01-01)

Steps to reproduce:
  1. Add product P-001 to cart
  2. Navigate to checkout
  3. Enter discount code "SAVE10" in the coupon field
  4. Click "Apply"

Actual result:
  HTTP 500, response body: {"error": "unexpected nil pointer in discount service"}
  Server log: NullPointerException at DiscountService.validate:87

Expected result:
  HTTP 422, response body: {"code": "DISCOUNT_EXPIRED", "detail": "This code has expired"}
  (per AC-17 in the payment spec)

Severity: Major (core checkout flow broken for any expired code)
Priority: High (coupon field is in the active marketing campaign)

Attachments: screenshot_checkout_error.png, server.log (lines 120-145)
```

The developer can reproduce in under 2 minutes. Spec reference removes ambiguity.

### Bad — Incomplete defect report

```
Title: Discount doesn't work
Steps: I tried to use a coupon
Actual: error
Expected: should work
Severity: Critical
```

Developer cannot reproduce. Requests more info. Two days lost. Defect is rejected as "cannot reproduce."

### Good — Severity vs priority correctly distinguished

```
Defect: Company logo is pixelated on the login screen on 4K displays.
Severity: Trivial (no functional impact; purely cosmetic).
Priority: High (login screen is the brand face; CMO reported it; sprint demo is Monday).
Decision: Fix in current sprint. Not a release blocker but business priority overrides.
```

### Bad — Severity = Priority as a default

"This is a Critical issue" with no distinction between functional impact and business urgency.
Every defect becomes Critical. Triage is meaningless. Developers lose trust in the severity rating.

### Good — Defect localized to layer

```
Layer: API (backend)
The UI sends a valid request. The API returns 500.
The client-side code is correct per the network trace (HAR attached).
The error originates in the order service at the discount validation step.
Route to: backend team, order service.
```

### Bad — No layer localization

"The checkout is broken." Sent to both frontend and backend teams simultaneously.
Both spend two hours investigating before determining it is a backend issue.

### Good — Regression risk assessment before retest

```
Fix: Discount code validation logic refactored in DiscountService.validate()

Regression risk areas:
  - All valid discount code flows (REG-TC-42, REG-TC-43)
  - Zero-value cart with discount (REG-TC-44)
  - Stacked discount behavior (REG-TC-45) — low risk but include
  - Anonymous checkout flow — no discount code feature; exclude

Retest plan: run TC-112 (original defect) + regression set REG-TC-42 to REG-TC-45.
```

### Bad — Retest without regression check

"The specific bug is fixed. Closing." Three weeks later, stacked discounts stop working.
The fix broke a neighbor case. Nobody checked.

### Good — Defect cluster analysis

```
Post-sprint defect analysis (Sprint 23):

Total: 18 defects
By component: Order service 7, Payment 4, Discount 5, UI 2
By root cause:
  - Missing input validation: 6 defects (33%) — recommendation: add validation review to DoD
  - Untested edge case (expired/null data): 5 defects (28%) — recommendation: add data boundary cases to test design guide
  - Environment issue (not product defects): 3 — excluded from count
  - Regression from previous sprint: 4 — recommendation: expand regression set for order service
```

Systemic action follows data. Not just "we found 18 bugs."

### Bad — No defect analysis

Defects are filed and closed. No one tracks which components are defect-prone. The same
root causes repeat sprint after sprint. The team fixes symptoms, not the process.

## Boundaries

- Owns defect registration, triage, retest, and regression risk assessment.
- Does not own bug fixing -> `developer`.
- Does not own production incident response -> `devops-sre`.
- Does not own product priority decisions (only informs them) -> `product-owner` / `product-manager`.
- Does not own requirements authorship even when defects reveal gaps -> `system-analyst`.

## Sources

### Priority 1 — Testing standards

- ISTQB CTFL v4.0 Syllabus: Defect Management section — https://www.istqb.org/certifications/certified-tester-foundation-level
- ISO/IEC/IEEE 29119-3: Software Testing Documentation (defect reports) — https://www.iso.org/standard/56737.html
- Cem Kaner: Lessons Learned in Software Testing (Chapter: Bug Reports) — book reference

### Priority 2 — Orientation

- Atlassian Jira bug tracking guide — https://www.atlassian.com/software/jira/guides/issues/overview
- ISTQB Advanced Level Test Analyst: Defect taxonomy — https://www.istqb.org/certifications/advanced-level-test-analyst
- James Bach: Heuristic Test Strategy Model (defect analysis section) — https://www.satisfice.com/download/heuristic-test-strategy-model

### Priority 3 — Background

- Google Testing Blog — https://testing.googleblog.com/
- Software Engineering at Google: Testing chapter — https://abseil.io/resources/swe-book

## Handoff

- Bug fix implementation -> `developer` with the defect report.
- Production incident root cause beyond testing scope -> `devops-sre`.
- Security vulnerability found during testing -> `security-engineer` with OWASP classification.
- Requirements gap revealed by a defect -> `system-analyst` with specific gap description.
- Release go/no-go decision on open defects -> `product-owner` / `product-manager` with severity/priority context.
