---
name: test-strategy-and-planning
description: Use when defining the test approach for a feature, release, or product area — choosing test levels, allocating the pyramid, mapping environments, and setting entry and exit criteria so the team knows what is covered, what is not, and what risk is accepted.
family: method
profile_level: Senior+
---

# Test Strategy and Planning

## Purpose

Translate product requirements and system risks into a coherent test approach that is proportionate to criticality,
defensible to stakeholders, and executable within the available time and environment. Prevent coverage drift where
tests accumulate without a rationale, and prevent under-testing where the team ships without knowing what risk
remains.

## Use When

- Starting a new feature, epic, or release and the team needs a shared understanding of test scope.
- The current regression suite is growing without clear prioritization or rationale.
- Environments are not defined and testing is uncoordinated across team members.
- The team lacks agreed entry and exit criteria, causing ambiguous readiness signals.
- After an incident or escaped defect where the test strategy clearly missed a risk category.
- Agreeing what will not be tested and making that decision explicit.

## Do Not Use When

- Designing individual test cases for specific scenarios -> use `test-design-and-coverage`.
- Running an exploratory session to discover unknown risks -> use `exploratory-and-session-based-testing`.
- Setting up test automation framework architecture -> use `test-automation-framework`.

## Inputs

- Requirements, user stories, or specification documents.
- Architecture diagram or service dependency map.
- Risk register or known defect history (if available).
- Constraints: timeline, environment availability, team capacity.
- Existing test suite inventory and coverage gaps.

## Workflow

1. Identify the risk surface: which behaviors, if broken, cause the highest business or user impact? Classify
   risks as critical (must test), important (should test), and low (may skip or automate later).

2. Map test levels to the pyramid. Decide the target distribution:
   - Unit tests: owned by developers; QA confirms they exist for business logic.
   - Component/API tests: QA and developers share; contract and integration behavior.
   - E2E/UI tests: QA owns; only for critical user journeys where lower-level coverage is insufficient.
   Do not invert the pyramid by writing e2e tests for scenarios that belong at the API or unit level.

3. Define test types needed: functional, regression, smoke, sanity, integration, contract, performance,
   exploratory, security-adjacent. Not every type is needed for every feature.

4. Plan environments: which test environment is needed for each phase (development, integration, staging,
   pre-prod)? What data state is required? Who sets it up?

5. Set entry criteria: what must be true before QA testing begins? (e.g., dev tests passing, build deployed
   to test environment, test data seeded, API documentation available).

6. Set exit criteria: what must be true before the feature is declared ready? (e.g., all critical test cases
   passed, no open blockers, regression suite green, performance NFR validated, known residual risks documented).

7. Write the test plan or strategy note: scope, out-of-scope, risk-based rationale, level allocation,
   environment, entry/exit criteria, coverage matrix skeleton. Length proportionate to feature size.

8. Review the strategy with system analyst (to confirm requirements are testable) and with tech lead or
   product owner (to confirm risk prioritization matches business priorities).

## Outputs

- Test strategy document or test plan (length proportionate to feature scope).
- Risk-based coverage matrix (requirements -> test levels -> coverage rationale).
- Entry and exit criteria checklist.
- Out-of-scope list with rationale.
- Environment and test data plan.
- Open questions for system analyst or product owner.

## Named Patterns

### Good — Risk-stratified coverage with explicit out-of-scope

```
Feature: Payment gateway integration

CRITICAL (must test):
  - Successful charge: e2e + API contract test
  - Charge failure (card declined): API test + UI error state
  - Duplicate charge prevention: API idempotency test
  - Refund: API test + e2e

IMPORTANT (should test):
  - Partial refund: API test
  - Webhook delivery retry: integration test

LOW / OUT OF SCOPE for this release:
  - Currency conversion edge cases: covered by gateway provider's own tests
  - Fraud scoring: separate QA track in security sprint

Rationale: Out-of-scope decisions reviewed with PM and SA.
```

Stakeholders see what is covered, what is not, and why. No guessing after a release.

### Bad — Test everything, no rationale

```
Test plan: Test all payment functionality.
Scope: All scenarios.
Exit criteria: Testing complete.
```

"Testing complete" is not an exit criterion. "All scenarios" is not a scope. The team ships
without knowing what residual risk exists.

### Good — Pyramid allocation statement

```
Unit: developers own unit tests for payment service logic.
API: QA authors 12 API contract tests covering all documented error codes.
E2E: QA authors 3 e2e tests covering the checkout critical path only.
Reason: e2e tests are slow and brittle; critical path is the only justified investment.
```

### Bad — Inverted pyramid

The QA team writes 40 e2e tests for every form field variation because "e2e tests are most realistic."
API tests are skipped. Regression takes 2 hours; flaky tests block every deployment.

### Good — Explicit entry criteria preventing premature testing

```
Entry criteria for QA:
  [x] Feature branch merged to integration environment
  [x] Developer smoke test passed (no 500 errors on main flows)
  [x] API documentation updated with new endpoints
  [x] Test data seed script reviewed and applied
  [ ] OPEN: performance environment not yet available -> performance testing blocked, noted in plan
```

QA does not start testing a broken environment and mistake environment failures for product defects.

### Bad — No entry criteria

QA begins testing on an environment where the feature is half-deployed. Defects filed against
a broken build. Developer rejects all bugs as "environment issues." Trust erodes.

### Good — Exit criteria with residual risk statement

```
Exit criteria:
  [x] 100% critical test cases executed, 98% passed (2 known cosmetic defects, accepted by PM)
  [x] Regression suite green
  [x] NFR validated: p95 checkout latency < 300ms under 50 concurrent users
  [ ] RESIDUAL RISK: error message text on declined card not localized -> accepted, logged in backlog
```

The team and stakeholders have a factual basis for the release decision.

### Bad — Binary "all tests passed"

Exit criterion is "100% pass rate." Team skips or marks-as-passed failing tests to hit the metric.
Quality gate becomes a formality.

### Good — Living strategy updated after incidents

After an escaped defect in data migration, QA updates the strategy to add a migration
verification step in the entry criteria and a data integrity check in exit criteria.
The strategy reflects what the team learned.

### Bad — Strategy written once, never revisited

The test plan from 18 months ago still defines the test scope for a product that has
doubled in complexity. New risk areas are untested because no one updated the plan.

## Boundaries

- Owns the test strategy and plan for a feature, release, or product area.
- Does not own requirements authorship or API contract design -> `system-analyst`.
- Does not own the release go/no-go decision -> `product-owner` / `product-manager`.
- Does not own delivery schedule or resource planning -> `project-manager`.
- Does not own individual test case design -> `test-design-and-coverage`.

## Sources

### Priority 1 — Testing standards and canonical practice

- ISTQB CTFL v4.0 Syllabus: Test Planning section — https://www.istqb.org/certifications/certified-tester-foundation-level
- ISO/IEC/IEEE 29119-2 Software Testing Processes — https://www.iso.org/standard/81228.html
- ISO/IEC/IEEE 29119-3 Software Testing Documentation (test plan structure) — https://www.iso.org/standard/56737.html
- James Bach: Heuristic Test Strategy Model — https://www.satisfice.com/download/heuristic-test-strategy-model

### Priority 2 — Orientation

- Martin Fowler: Test Pyramid — https://martinfowler.com/articles/practical-test-pyramid.html
- Lisa Crispin and Janet Gregory: Agile Testing (Part II: Quadrants) — book reference
- Google Testing Blog: Just Say No to More End-to-End Tests — https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html

### Priority 3 — Background

- ThoughtWorks Technology Radar (test automation entries) — https://www.thoughtworks.com/radar
- Software Engineering at Google: Testing chapters — https://abseil.io/resources/swe-book

## Handoff

- Requirements testability gaps found during planning -> `system-analyst` with specific questions.
- Risk prioritization disagreement -> `product-owner` / `product-manager` for business priority decision.
- Environment provisioning needs -> `devops-sre` with environment spec.
- Performance or load test scope -> escalate to `performance-and-load-testing` skill.
- Detailed test case design -> `test-design-and-coverage` skill.
