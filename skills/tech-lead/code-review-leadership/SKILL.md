---
name: code-review-leadership
description: Use when establishing or improving code review culture at team scale — review conventions, intent-tagged feedback standards, ADR capture for recurring review patterns, reviewer guidelines, and onboarding new engineers to review expectations. Covers the system of conventions, not a single PR review.
family: method
profile_level: Senior+
---

# Code Review Leadership

## Purpose

Make code review a team-level practice that moves code and authors forward — consistently, predictably, and without creating a bottleneck on one reviewer. Build the conventions, feedback norms, and written standards that survive team changes.

## Use When

- The team has no written code review conventions and review quality varies by reviewer.
- Review comments are inconsistently tagged as blockers vs. suggestions, causing friction.
- The same review comment appears on multiple PRs and has never been captured as a standard.
- A new engineer joins and learns review expectations only through repeated PR rounds.
- Review cycle time is increasing and the bottleneck is unclear.
- The review process is blocking delivery without a clear quality justification.

## Do Not Use When

- The question is about a single PR's correctness → handle as a direct review.
- The question is about performance management of a developer → handoff to `line-manager`.
- The question is about system-level architectural standards → `cross-team-technical-alignment` or `system-architect`.
- The question is about individual developer growth → `mentoring-and-growth`.
- The question is about capturing a one-time architectural decision → `architecture-decision-records`.

## Inputs

- Current review conventions (if any): style guides, review checklists, linter configs.
- Review cycle time metrics: PR open-to-merge, time-to-first-review, review-round count.
- Recurring friction patterns from retrospectives and direct engineer feedback.
- Codebase maturity: test coverage, CI pass rate, existing ADRs.
- Team composition: number of reviewers, their levels, capacity for review work.

## Workflow

1. Audit the current review state. Ask: what fraction of PRs have a first review within 24 hours? What is the average number of review rounds? What are the top three recurring comment themes? Gather data before prescribing a change.
2. Define review intent levels. Adopt a written taxonomy for feedback weight. Example: `must` (merge blocker — correctness, security, data integrity), `should` (strong suggestion — maintainability, team convention), `nit` (taste — naming, formatting), `question` (asking, not telling), `praise` (explicit positive reinforcement). Publish it in the team handbook.
3. Separate "wrong" from "different". Establish the rule: a reviewer's personal style is not a `must`. If the standard is not written, the comment is a `question` until the standard exists.
4. Define review scope per level. What does a Senior review that a Junior does not? Correctness (all levels), architecture (Senior+), cross-service impact (Tech Lead). Scope prevents all-or-nothing review paralysis.
5. Set a review SLA. Example: first review within one business day for a PR under 400 lines; larger PRs get a review date agreed upfront. Post the SLA in the team handbook. Track it in weekly retrospectives.
6. Capture recurring decisions as standards. When the same comment appears on three PRs, write it down: as a linter rule, a style guide entry, or an ADR. Retire the review comment and link to the standard. Recurring comments that are not captured create tribal knowledge.
7. Onboard new engineers with an explicit review orientation. Walk them through one PR using intent tags. Explain what makes a comment a `must` vs. a `nit`. Show an example of a well-formed review. Set expectations within the first two weeks.
8. Review the review process itself quarterly. Are cycle times improving? Are blockers decreasing? Is the `must` rate stable (too many `must`s means quality problems upstream; too few means reviewers are rubber-stamping)? Adjust conventions based on data.

## Outputs

- Written review conventions document: intent taxonomy, scope per level, SLA.
- Recurring-decision log: patterns that have been converted to written standards.
- Onboarding checklist for review expectations.
- Quarterly review metrics: cycle time, round count, `must`-rate trend.

## Named Patterns

### Good — Intent-tagged review
```
must: nil pointer dereference on line 47 if response.Body is nil. See ADR-0011 for error-check pattern.
should: extract this into a helper; the same logic exists in OrderHandler.
nit: variable name `tmp2` does not convey intent.
question: why batch size 50? if not measured, 200 may reduce round trips.
praise: the table-driven test structure with named sub-cases is exactly what we want here.
```
The author knows what to fix before merging and what is optional.

### Bad — Unmarked feedback
"Rename this." "I wouldn't do it this way." "Move this to a separate file."
The author cannot distinguish a merge blocker from a naming preference. Friction without clarity.

### Good — Standard-anchored comment
"Per team style guide §error-wrapping: all errors from external calls must be wrapped with context. Use `fmt.Errorf('calling payment service: %w', err)`."
The feedback anchors to a written standard. The reviewer's taste is not in scope.

### Bad — "Because I said so"
"This is not how we do things here." The author asks where it is written down — silence. Tribal knowledge enforced through authority.

### Good — Review SLA in practice
PR opened Monday 09:00. Reviewer assigns themselves by 10:00 and leaves a first-pass comment with `question` and one `must` by 16:00. Author addresses it by Tuesday. Merges Tuesday afternoon.
Predictable flow. Author is not blocked. Reviewer is not surprised.

### Bad — Review lottery
PR sits for three days. One reviewer leaves 17 comments on day 4, 5 of which are `nit`. Author is demoralized and the team misses the sprint goal.

### Good — Recurring pattern captured as standard
"ADR-0015: Error wrapping in service boundary calls. Status: Accepted. Context: reviewers have left this comment 8 times in the last 6 weeks. Decision: all service boundary calls wrap errors with `fmt.Errorf`. Consequences: one-time refactor tracked in issue #502."
The comment is retired. The next PR cites the ADR.

### Bad — Recurring comment never captured
Same comment appears weekly for six months. Every new engineer learns it through a PR rejection. Senior engineers spend time leaving the same text repeatedly.

### Good — Scope definition
"Correctness review (all reviewers): does the code do what the PR description says? Senior review: does it fit the existing patterns, error handling, and test structure? Tech Lead review: does it cross service boundaries or introduce a new dependency?"
Each level knows its scope. Reviews are not bottlenecked on the tech lead.

### Bad — Tech Lead as single reviewer
Every PR needs the tech lead's approval. The team of five has one review queue, one bottleneck, and one point of failure for delivery pace.

## Boundaries

- Owns team-wide code review conventions, feedback norms, review SLA, and standard-capture practice.
- Does not own org-wide or cross-team engineering standards → `cross-team-technical-alignment` or `system-architect`.
- Does not own individual developer performance evaluation → `line-manager`.
- Does not own architectural decisions that span services → `architecture-decision-records` + `system-architect`.
- Does not own a single PR review's substance — this skill defines the system, not the content of any one review.

## Sources

### Priority 1 — Review canon
- Google Engineering Practices: Code Review — https://google.github.io/eng-practices/review/
- Google Engineering Practices: Reviewer Guide — https://google.github.io/eng-practices/review/reviewer/
- Michael Nygard: Documenting Architecture Decisions — https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions

### Priority 2 — Practice orientation
- Lara Hogan: Resilient Management — A Book Apart, 2019. Feedback delivery and norm-setting.
- Camille Fournier: The Manager's Path — O'Reilly, 2017. Review culture in growing engineering teams.
- Jeff Atwood: Code Reviews: Just Do It — https://blog.codinghorror.com/code-reviews-just-do-it/

### Priority 3 — Background
- ThoughtWorks Technology Radar: code review tooling — https://www.thoughtworks.com/radar
- LeadDev: Engineering culture articles — https://leaddev.com/

## Handoff

- Org-wide or cross-team engineering standards → `system-architect` or `cross-team-technical-alignment`.
- Individual growth beyond review feedback → `mentoring-and-growth`.
- Performance management of a specific developer → `line-manager`.
- Capturing a system-level architectural decision surfaced in review → `architecture-decision-records`.
- Team-level engineering quality standards (DoD, test requirements) → `engineering-quality-and-standards`.
