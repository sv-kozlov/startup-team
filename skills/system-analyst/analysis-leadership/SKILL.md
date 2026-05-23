---
name: analysis-leadership
description: Use when a lead or principal analyst needs to review complex specifications written by the team, set team standards for analysis artefacts, mentor middle and junior analysts, or coordinate requirement alignment across multiple teams or components.
family: lead
profile_level: Senior+
---

# Analysis Leadership

## Purpose

Raise the quality ceiling of the analyst team by reviewing specifications before they reach engineering, establishing repeatable standards, mentoring analysts toward Senior-level independence, and coordinating requirement alignment across component or team boundaries. Distinct from writing individual specifications — this skill governs the quality of the specification layer as a whole.

## Use When

- A complex or high-risk specification needs a second review before handoff to engineering or QA.
- The team repeatedly produces similar specification gaps (missing error cases, untestable acceptance criteria, unresolved data ownership) — a standard or template is needed.
- A middle analyst is producing specs with recurring quality issues and needs structured feedback.
- Multiple teams or system components have conflicting or unaligned requirement sets that block engineering.
- A new analysis workflow, documentation standard, or artefact template is being introduced to the team.
- A senior analyst is being developed toward lead-level impact: cross-team coordination, standards authorship, mentoring.

## Do Not Use When

- The task is writing or improving a specific functional specification → `functional-specification`.
- The task is reviewing an API contract for backward compatibility → `api-contract-design`.
- The task is gathering requirements from stakeholders → `requirements-elicitation`.
- The discussion is about product prioritization, roadmap, or scope decisions → `product-manager` / `product-owner`.
- The discussion is about org-wide engineering standards beyond the analysis layer → `tech-lead`.

## Inputs

- Specification, SRS, or analytical artefact under review.
- Author's level and context (how much was known when they wrote it, what constraints they had).
- Team standards, artefact templates, or previous review feedback cycles.
- Cross-team dependency map and aligned requirement sets from adjacent analysts or teams.
- Mentee's recent work samples for pattern-level feedback.

## Workflow

1. **Review for structure and completeness.** Check that the artefact answers the key engineering question: is the system behavior, data shape, error handling, and acceptance criterion documented at implementation-ready detail? Flag missing sections, not just wrong ones.
2. **Review for testability.** Every functional requirement must have at least one testable condition. "Shall" / "must" statements without a verifiable outcome are not requirements — they are wishes. Mark these explicitly.
3. **Review for boundary discipline.** Check that the spec does not include architectural decisions (component topology, technology selection), engineering implementation choices (code structure, framework selection), or QA strategy (regression scope, test approach). Surface these as handoff items.
4. **Review for domain language consistency.** Check that the spec uses the agreed ubiquitous language throughout. Flag synonyms, ambiguous terms, or concepts from different bounded contexts used interchangeably.
5. **Give structured, intent-marked feedback.** Use explicit markers: `must` (blocks implementation), `should` (strong suggestion), `question` (asking for clarification), `nit` (low-priority style). The author must be able to distinguish what is blocking from what is optional.
6. **Build or update the team standard.** When the same gap appears in two or more specifications by different authors, convert the feedback into a team-level standard, template, or checklist. Recurring review comments that are not written down are tribal knowledge.
7. **Mentor through questions, not dictation.** "What happens when the external system returns a 503 here?" makes the analyst reason; "add error handling" gives them nothing to learn. Reserve dictation for hard blockers.
8. **Coordinate cross-team alignment.** When two teams' requirement sets conflict, drive a resolution session rather than letting engineering absorb the contradiction. Document the agreed boundary and the decision owner.
9. **Track mentee progress across artefacts.** Effective mentoring shows in the next spec, not just the current one. Track whether the recurring issue is resolved in subsequent work.

## Outputs

- Reviewed and annotated specification with intent-marked feedback.
- Approved specification cleared for engineering handoff.
- Team standard, artefact template, or specification checklist when a recurring gap is found.
- Cross-team alignment decision log when conflicting requirement sets are resolved.
- Structured mentoring notes with observable improvement criteria for the next review cycle.

## Named Patterns

### Good — Intent-marked specification review
```
must: Section 3.2 has no error case for the payment provider timeout.
      Engineering cannot implement idempotent retry without it.
      See the event-driven-integration skill for the retry/DLQ pattern.
should: The term "user" in section 4 should be replaced with "Registered Customer"
        (ubiquitous language, glossary entry 7).
question: Is the 200ms SLO in section 5 a P99 or P50 target?
          This affects whether the architect needs to add a cache.
nit: Section 6 has a duplicate sentence.
```
The author knows what to fix, what to consider, and what is optional.

### Bad — Unmarked taste as blocker
"Rewrite section 3. The structure is not clear. Also move the error table to the end."
The author cannot tell if section 3 is wrong or if the reviewer prefers a different layout. Blocks the merge on style.

### Good — Team standard from a recurring gap
```
Specification Checklist — Error Case Coverage
Every flow that calls an external system must document:
1. Timeout behavior and retry count.
2. HTTP 4xx and 5xx mapping to system behavior.
3. Idempotency rule for retried requests.
4. DLQ / fallback path if retries are exhausted.
Review will reject specs that skip any of these four points.
```
Converts three separate review cycles into one written standard.

### Bad — Tribal knowledge review
"You forgot error handling — again." Third time the same comment on the same analyst's spec. No standard was written; the next analyst will make the same mistake.

### Good — Mentoring through questions
"What state is the order in if the payment capture succeeds but the fulfillment event fails to publish?"
"Which team owns the idempotency key — the caller or the receiver?"
The analyst reasons through the problem; the answer becomes their knowledge.

### Bad — Mentoring through dictation
"Just copy the error handling from the checkout spec." The analyst copies without understanding the invariant. The next feature has the same gap.

### Good — Cross-team alignment decision
```
Conflict: Team A specifies OrderConfirmed as the trigger for fulfillment.
          Team B specifies PaymentCaptured as the trigger.
Decision (agreed by SA Team A, SA Team B, System Architect, 2026-05-20):
  PaymentCaptured triggers fulfillment. OrderConfirmed is an internal state change.
  OrderConfirmed event is deprecated from the fulfillment contract.
Owner: System Analyst Lead, Team A.
```
Engineering does not absorb a contradiction. The decision is traceable.

### Bad — Letting engineering absorb a conflict
"Both versions are in the spec; engineering will decide." Engineering picks one interpretation. QA tests the other. Integration defect in production.

## Boundaries

- Owns: specification review, team standards for analysis artefacts, analyst mentoring, cross-team requirement alignment.
- Does not own: org-wide engineering standards, technical design standards, code review → `tech-lead`.
- Does not own: product backlog governance or scope authority → `product-owner`.
- Does not own: writing individual specifications → specific method skills (`functional-specification`, `api-contract-design`, etc.).
- Does not own: QA strategy or test design standards → `qa-engineer`.
- Does not own: performance management of the analyst → role manager.

## Sources

### Priority 1 — Requirements quality and review practice
- IIBA BABOK v3, Knowledge Area: Requirements Life Cycle Management — https://www.iiba.org/career-resources/a-business-analysis-body-of-knowledge/babok/
- IEEE/ISO/IEC 29148:2018, Section 6: Requirements quality — https://standards.ieee.org/content/ieee-standards/en/standard/29148-2018.html
- Karl Wiegers, Joy Beatty: Software Requirements (3rd ed.), Part 4: Requirements Management — book reference

### Priority 2 — Mentoring and team standards
- Google Engineering Practices: Code Review — https://google.github.io/eng-practices/review/ (adapted for specification review)
- Gojko Adzic: Specification by Example, Part 2: Patterns — book reference
- Alistair Cockburn: Writing Effective Use Cases, Chapter 10: Writing style — book reference

### Priority 3 — Lead practice background
- Camille Fournier: The Manager's Path — book reference (chapters on technical leads and mentoring)
- ThoughtWorks Technology Radar — https://www.thoughtworks.com/radar

## Handoff

- Specification content issues that require domain knowledge → `requirements-elicitation`.
- Architectural decisions surfaced during review → `system-architect`.
- Engineering feasibility questions surfaced during review → `tech-lead`.
- QA testability concerns that require test-strategy decisions → `qa-engineer`.
- Org-wide engineering standards beyond the analysis layer → `tech-lead`.
