---
name: shared-acceptance-criteria
description: Use when defining, reviewing, or splitting acceptance conditions for a requirement, user story, use case, rule set, or system behavior — covering observable outcome conditions, edge cases, UAT scope, testability signals, and sign-off readiness. Does not cover QA test design, regression strategy, or release readiness governance.
---

# Shared Acceptance Criteria

## Purpose

Make the conditions of satisfaction for a requirement, story, or specification explicit, observable, and owned. Acceptance criteria transform vague agreement ("should work correctly") into falsifiable, testable statements that each stakeholder and testing role can independently verify — eliminating integration surprises at handoff boundaries.

## Use When

- A requirement, story, or specification lacks observable outcome conditions and the team cannot tell whether it is satisfied.
- Business UAT expectations and system or QA test conditions are mixed together in the same item, creating ownership confusion.
- A rule, calculation, state transition, or edge case needs an explicit expected outcome before development starts.
- A feature is about to enter development and "definition of ready" requires testability review.
- A story or work item has passed through multiple roles and each has added conditions without separating ownership layers.
- An acceptance signal is tied to an experiment outcome, metric threshold, or rollout condition that must be stated explicitly.
- Criteria written earlier are found to be implementation-specific ("the button is blue") rather than behavior-specific ("the user can submit the form with valid data").

## Do Not Use When

- The task is authoring a QA test strategy, regression scope, or automation plan → QA Engineer owns those.
- The task is release readiness governance — go/no-go, stage-gate sign-off, or deployment approval → Product Owner or Delivery Manager owns release readiness.
- The task is defining product success metrics or experiment statistical thresholds → `product-metrics` skill or Product Analyst owns that.
- The criteria already exist and are testable; the task is writing test cases → QA Engineer.

## Inputs

- Requirements, user stories, use cases, process flows, business rules, or specifications being accepted.
- Stakeholder expectations, including known edge cases, exceptions, and data examples.
- Domain context: actors, user types, states, triggers, and expected outcomes.
- Known risk areas: data gaps, integration dependencies, performance expectations.
- Sign-off owner per criterion type (business, system, quality, measurement).

## Workflow

1. **Identify the acceptance owner per condition layer.** Separate business acceptance (was the business need met?), system acceptance (does the system behave correctly at boundaries, error paths, states?), and measurement acceptance (were the success signals observed?). Each layer has a different owner and different observable conditions.

2. **Decompose the story or requirement into named scenarios.** Use the Gherkin structure — Given / When / Then — as a thinking tool, not necessarily as a text format. Each scenario covers one path: happy path, exception path, boundary condition, or rule exception. Name each scenario explicitly.

3. **Apply the SMART-AC check per criterion.** Each criterion must be: Specific (one condition, not a bundle), Measurable (you can observe pass or fail), Agreed (an accountable owner confirmed it), Realistic (achievable in the iteration), and Testable (a test case can be written directly from it). Mark any criterion that fails one of these checks as a defect and rewrite it.

4. **Separate implementation details from behavioral outcomes.** Replace "the input field shows red border" with "the system prevents form submission and indicates which field is invalid". Replace "the API returns 200" with "the order is created and the confirmation number is returned to the caller". The how is implementation; the what and whether are acceptance.

5. **Identify missing coverage.** Walk the rule set or scenario for: negative inputs, null or empty values, permission boundaries, state preconditions, concurrent modification, and timeout or unavailability of dependencies. Capture gaps as open questions, not as silent omissions.

6. **Assign ownership and sign-off path.** Each criterion block must state who accepts it (business owner, system analyst, QA lead, product owner, product measurement signal). Criteria without an assigned owner are not ready for development.

7. **Hand off non-owned criteria.** If writing criteria surfaces system-level behavior decisions (API error shape, data validation rule details, idempotency), create a handoff to System Analyst. If it surfaces metric or experiment threshold definitions, create a handoff to the measurement owner.

## Outputs

- Acceptance criteria per story or requirement, split by layer (business, system, measurement).
- Named scenarios in Given / When / Then or equivalent structured format for each acceptance condition.
- UAT scope: which criteria are business-accepted versus system-tested versus measurement-observed.
- Edge-case and boundary-condition notes with explicit expected outcomes.
- Open questions and handoff tasks for conditions that require another role's decision.
- Sign-off assignment per criterion layer.

## Role Modes

### Business Analyst

Owns the business acceptance layer: the conditions under which the business stakeholder agrees the need is met. Defines UAT scope — which scenarios the business owner will verify manually, which rule exceptions require explicit business sign-off, and which conditions depend on real user behavior in a controlled rollout. Writes criteria in business vocabulary using domain examples; does not write system error codes, API response shapes, or test automation steps. Hands off system-level edge cases to System Analyst and measurement acceptance signals to the assigned metric owner.

### Product Owner

Owns the product-level acceptance gate: when does the increment satisfy the agreed scope for the iteration? Defines the "definition of done" at story level — which acceptance criteria must be verified by whom before the story closes. Reviews criteria written by Business Analyst and System Analyst for completeness and consistency with the agreed scope; does not rewrite them from scratch unless the story is a pure product-scope item without dedicated BA or SA coverage. Ensures that every story entering a sprint has criteria that pass the testability check; returns stories that fail the check to the authoring role for correction.

## Boundaries

- Does not own QA test strategy, test case design, regression scope selection, or automation plan. QA Engineer decides which acceptance criteria become automated tests, which are manual, and what the regression boundary is.
- Does not own release readiness governance. Product Owner or Delivery Manager owns the go/no-go decision.
- Does not own product success metric definitions or statistical experiment thresholds. Product Analyst or the product metric owner decides those.
- Does not decide system architecture, data model, or API error shape — those surface as handoff tasks when discovered during AC authoring.

## Named Patterns

### Good — Behavioral outcome criterion
```
Given the user has submitted a form with an invalid email address
When the form is validated on submission
Then the submission is rejected, the email field is marked as invalid,
     and the error message states "Enter a valid email address"
```
Describes observable behavior; independent of implementation color or framework. Any QA engineer can write a test case directly from this.

### Bad — Implementation-coupled criterion
```
The input field border turns red and the tooltip text color is #D32F2F.
```
Fails when the design system changes. The criterion tests implementation detail, not the behavior the business needs.

### Good — Rule boundary criterion with named exception
```
Discount applies when order total >= 5 000 RUB.
Exception: discount does not apply to orders marked as "gift card top-up".
Edge case: order of exactly 5 000 RUB qualifies.
```
Explicit threshold, named exception class, boundary value stated. No ambiguity at ±1 unit.

### Bad — Omnibus acceptance criterion
```
The checkout flow should work correctly for all user types including edge cases.
```
Not falsifiable. "Work correctly" and "all user types" are undefined. Fails the Specific and Measurable checks.

### Good — Separated ownership layers
```
Business acceptance: business owner verifies that the discount rule matches the
  approved promotion brief for Q2 (see BRD-44).
System acceptance: system analyst verifies error response when discount service
  is unavailable: HTTP 503 with code DISCOUNT_SERVICE_UNAVAILABLE.
QA acceptance: QA lead confirms regression suite passes for all affected
  checkout paths.
```
Each layer has a distinct owner, a distinct artifact, and a distinct check. No one role is responsible for everything.

### Bad — All conditions in one layer
All criteria assigned to "Development" with no owner distinction. UAT passes or fails at the last moment because business, system, and quality expectations were never separated.

### Good — Testability review before sprint
Acceptance criteria reviewed against the SMART-AC checklist before the story enters the sprint. Stories that fail the check are returned to the authoring role with specific gaps noted. Sprint contains only stories with criteria that pass.

### Bad — Acceptance criteria written after development
Developer interprets the story, builds a solution, then the team writes acceptance criteria post-hoc to match what was built. The criteria describe the implementation, not the business need, and UAT surprises accumulate.

### Good — Explicit sign-off assignment per criterion layer
```
Business AC 1: Finance Controller signs off that the loyalty discount rule matches BRD-44.
System AC 2: System Analyst confirms HTTP 503 response when discount service is unavailable.
Measurement AC 3: Product Analyst confirms conversion rate in cohort A meets +2% threshold
                  after 14-day observation window.
```
Each acceptance condition has exactly one sign-off owner. No criterion goes unverified because no one knew it was theirs to check.

### Bad — Criteria without sign-off assignment
All acceptance criteria listed as "QA verifies." Business-owner sign-off and measurement observation are never performed. Feature ships with unchecked business rules and no success measurement.

## Sources

### Priority 1 — Method canon

- ISO/IEC/IEEE 29148:2018 Systems and software engineering — Life cycle processes — Requirements engineering — https://standards.ieee.org/ieee/29148/6937/ (defines requirements quality attributes including verifiability and testability)
- Dan North, Introducing BDD (Behavior-Driven Development origin article) — https://dannorth.net/introducing-bdd/ (Gherkin Given/When/Then structure and its intent)
- Cucumber Documentation — BDD and Gherkin reference — https://cucumber.io/docs/gherkin/reference/ (canonical Gherkin syntax and scenario structure)
- Mike Cohn, "User Stories Applied: For Agile Software Development" (Addison-Wesley, 2004) — canonical reference on acceptance criteria as confirmation of user story intent

### Priority 2 — Orientation

- IIBA BABOK Guide v3 — Acceptance and Evaluation Criteria task — https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/ (defines acceptance criteria in business analysis context)
- Atlassian — How to write acceptance criteria — https://www.atlassian.com/agile/project-management/acceptance-criteria (practical guide; use as orientation, verify against ISO 29148 for canonical definition)
- Scrum.org — Definition of Done vs Acceptance Criteria — https://www.scrum.org/resources/blog/done-understanding-definition-done (separates story-level AC from team-level DoD)

### Priority 3 — Background

- IEEE 829-2008 Standard for Software and System Test Documentation — https://standards.ieee.org/ieee/829/3787/ (defines test documentation standards that acceptance criteria feed into)
- Gojko Adzic, "Specification by Example" (Manning, 2011) — illustrates AC-driven development as living documentation

## Handoff

- When authoring AC surfaces an undefined API error shape or response code → hand off to System Analyst via `shared-api-contract-design` or `functional-specification`.
- When authoring AC surfaces an undefined business rule or calculation → hand off to Business Analyst via `shared-business-rules`.
- When a measurement acceptance signal (metric threshold, experiment result) must be defined → hand off to the product metric owner or Product Analyst.
- When AC review finds a story not ready for the sprint → return to the authoring role with a gap list; do not let the story advance.
- When all criteria are verified and the feature is complete → trigger release readiness review with Product Owner or Delivery Manager.
