---
name: test-design-and-coverage
description: Use when designing test cases for a feature, API, or data flow — selecting the right technique (equivalence partitioning, boundary analysis, decision tables, state transition, pairwise) to achieve minimum sufficient coverage with maximum defect detection power.
family: method
profile_level: Senior+
---

# Test Design and Coverage

## Purpose

Convert requirements, acceptance criteria, state models, and data specifications into a precise set of test cases
that detect real defects with minimum redundancy. Avoid two failure modes: a bloated suite with hundreds of
redundant cases, and a thin suite that misses critical combinations and boundaries.

## Use When

- Designing test cases for a new feature, changed behavior, or API endpoint.
- Reviewing whether existing test cases cover the stated requirements and acceptance criteria.
- Choosing the right technique for a given input space (discrete values, ranges, states, conditions).
- Building a coverage matrix that links requirements to tests to execution results.
- A regression suite is growing without rationale and needs pruning and restructuring.

## Do Not Use When

- The test approach and pyramid allocation are not yet defined -> use `test-strategy-and-planning` first.
- Discovery of unknown behavior is needed, not verification of known behavior -> use `exploratory-and-session-based-testing`.
- Designing automated framework structure -> use `test-automation-framework`.

## Inputs

- Requirements, user stories, or specification with acceptance criteria.
- API specification (OpenAPI, protobuf schema, or similar).
- State diagrams or state transition tables (if applicable).
- Known defect history or risk areas.
- Existing test cases (for pruning and gap analysis).

## Workflow

1. Identify the input space: what are the variables, conditions, and states being tested? Separate
   independent from dependent variables.

2. Apply equivalence partitioning: group inputs into classes where all values in the class are expected
   to behave identically. Test one representative from each valid class and one from each invalid class.

3. Apply boundary value analysis: test the minimum, maximum, just-below-minimum, and just-above-maximum
   of every numeric or ordered input. Most defects cluster at boundaries.

4. Apply decision table testing where multiple conditions combine to produce distinct outcomes.
   Columns are rules (combinations); rows are conditions and expected actions.

5. Apply state transition testing when a system has distinct states and transitions triggered by events.
   Map: states, events, valid transitions, invalid transitions (negative paths).

6. Apply pairwise (all-pairs) testing when there are many independent parameters and combinatorial
   explosion makes full coverage impractical. Use a pairwise tool to generate the minimum set.

7. Write test cases in structured form. Each test case has: ID, precondition, input, action, expected
   result, actual result (blank at design time), and traceability to the requirement.

8. Build a coverage matrix: requirements or acceptance criteria (rows) vs test cases (columns).
   Cells show which test cases cover which requirement. Identify uncovered requirements as gaps.

## Outputs

- Test case suite in structured format (table or Given/When/Then).
- Coverage matrix: requirements x test cases.
- Gap analysis: requirements or scenarios with no covering test.
- Technique justification note (why this technique for this input space).

## Named Patterns

### Good — Equivalence partitioning with invalid classes

```
Input: User age (valid: 18-120)

Valid partitions:
  EP1: 18-120 -> representative value: 25 -> test case TC-01: expect success
  
Invalid partitions:
  EP2: < 18 -> representative value: 17 -> test case TC-02: expect validation error
  EP3: > 120 -> representative value: 121 -> test case TC-03: expect validation error
  EP4: non-integer (e.g., "abc") -> test case TC-04: expect validation error
  EP5: empty / null -> test case TC-05: expect validation error

Total: 5 test cases cover the entire input space. Not one case per age value.
```

### Bad — Testing every value in the range

Writing 103 test cases for ages 18 through 120. Each test is a separate row in a spreadsheet.
200 test cases for a single field. Redundant. Equivalent to 2 test cases in terms of defect detection.

### Good — Boundary value analysis

```
Input: discount percentage (valid: 0-100)

Boundary cases:
  TC-B1: -1 -> invalid (just below minimum)
  TC-B2: 0  -> valid minimum
  TC-B3: 1  -> valid just above minimum
  TC-B4: 99 -> valid just below maximum
  TC-B5: 100 -> valid maximum
  TC-B6: 101 -> invalid (just above maximum)
```

Most off-by-one defects in boundary handling are caught by this set.

### Bad — Testing only the "happy path" with middle values

A single test with discount = 50. Passes in development. Ships with a bug where 100% discount
crashes the calculation engine due to a division-by-zero at the boundary.

### Good — Decision table for complex business rules

```
| Condition: account type = premium | Y | Y | N | N |
| Condition: balance >= 1000        | Y | N | Y | N |
| Action: waive fee                 | Y | N | N | N |
| Action: apply 50% discount        | N | Y | N | N |
| Action: apply standard fee        | N | N | Y | Y |

4 rules = 4 test cases, each covering a distinct combination.
```

### Bad — Verbal rule with no table

"Premium accounts with sufficient balance don't pay fees, otherwise they get a discount." QA writes
one test (premium + sufficient balance). Edge case of premium + insufficient balance is missed.
Defect escapes to production.

### Good — State transition test covering invalid transitions

```
States: Draft -> Submitted -> Approved / Rejected -> Archived

Invalid transitions to test:
  - Approve a Draft directly (skip Submitted) -> expect error
  - Resubmit an Approved item -> expect error or prompt
  - Archive a Submitted item without approval -> expect error

Valid transitions:
  - Draft -> Submit -> Approve -> Archive: TC-S1 (happy path)
  - Draft -> Submit -> Reject -> Resubmit -> Approve: TC-S2 (reject and resubmit)
```

### Bad — Only testing the happy-path state sequence

Only TC-S1 exists. The application allows approving a Draft directly in production because
no one tested the invalid transition.

### Good — Coverage matrix showing gaps

```
| Requirement         | TC-01 | TC-02 | TC-03 | TC-04 | Gap? |
|---------------------|-------|-------|-------|-------|------|
| R-12: Valid login   |   X   |       |       |       |  No  |
| R-13: Invalid pwd   |       |   X   |       |       |  No  |
| R-14: Locked account|       |       |   X   |       |  No  |
| R-15: MFA flow      |       |       |       |       | YES  |
```

R-15 has no covering test. Gap is visible and can be addressed before release.

### Bad — Test cases written without traceability

A list of 200 test cases with no link to requirements. No one can tell if R-15 is covered.
After a defect in MFA, the team discovers the test suite never covered it.

### Good — Pairwise reduction for config matrix

```
Parameters: OS (Win/Mac/Linux), Browser (Chrome/Firefox/Safari), Screen (Desktop/Mobile)
Full matrix: 3 x 3 x 2 = 18 combinations
Pairwise set (using PICT or similar): 9 combinations covering all pairs
Defect detection efficiency is preserved; execution time halved.
```

### Bad — Full combinatorial matrix without pairwise

A team writes 18 test cases for all OS x Browser x Screen combinations. Adding a fourth parameter
(language: EN/FR/DE) makes it 54 cases. The test matrix grows quadratically with no benefit.

## Boundaries

- Owns test case design and coverage matrix for a given feature or component.
- Does not own test automation framework structure -> `test-automation-framework`.
- Does not own requirements authorship -> `system-analyst`.
- Does not own test strategy and pyramid allocation -> `test-strategy-and-planning`.
- Does not own exploratory charters or unscripted discovery sessions -> `exploratory-and-session-based-testing`.

## Sources

### Priority 1 — Technique canon

- ISTQB CTFL v4.0 Syllabus: Black-Box Test Techniques — https://www.istqb.org/certifications/certified-tester-foundation-level
- ISO/IEC/IEEE 29119-4 Software Testing Techniques — https://www.iso.org/standard/81229.html
- BS 7925-2 Software Component Testing Standard — https://www.bcs.org/
- Cem Kaner: Lessons Learned in Software Testing (Chapters on test design) — book reference

### Priority 2 — Orientation

- ISTQB Advanced Level Test Analyst Syllabus: Techniques section — https://www.istqb.org/certifications/advanced-level-test-analyst
- Microsoft PICT (Pairwise Independent Combinatorial Testing) — https://github.com/microsoft/pict
- Glenford Myers: The Art of Software Testing — book reference (Wiley, 3rd ed. 2011)

### Priority 3 — Background

- Software Engineering at Google: Testing chapters — https://abseil.io/resources/swe-book
- Google Testing Blog — https://testing.googleblog.com/

## Handoff

- Requirements or acceptance criteria that are not testable -> `system-analyst` with specific ambiguity list.
- Test strategy and pyramid allocation questions -> `test-strategy-and-planning`.
- Automation of the designed test cases -> `test-automation-framework`.
- Complex state models requiring business validation -> `system-analyst` for state diagram review.
