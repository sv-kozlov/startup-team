---
name: code-review-and-mentoring
description: Use when reviewing someone else's Go code, lifting a team standard, writing an ADR, or mentoring a Middle/Senior on idiomatic Go. Covers review etiquette, the order of feedback, ADR shape, and the difference between "different" and "wrong".
family: lead
profile_level: Senior+
---

# Code Review and Mentoring

## Purpose

Make code review move the code and the author forward, not just block the merge. Lift team practice through ADRs and consistent feedback rather than personal preference. Distinguish "this is wrong" from "this is different from what I would write".

## Use When

- Reviewing a non-trivial Go pull request.
- A pattern keeps re-appearing in reviews — time to write it down.
- Onboarding a new Go developer to the codebase.
- Mentoring a Middle toward Senior, or a Senior on team-level impact.
- A non-obvious technical decision is being made — write an ADR.

## Do Not Use When

- The review is about API contract evolution → use `api-contract-design` for the substance.
- The review is about performance hot paths → use `go-testing` benchmarks for evidence.
- The discussion is performance management of a person → out of scope; that is the manager's job.

## Inputs

- Pull request with description, linked ticket, and tests.
- Existing team conventions, ADR log, style guide.
- Author's level and how much context they had.

## Workflow

1. Read the description and tests first. If they don't tell you what the change does and why, ask before reviewing the code.
2. Review in three passes: correctness (does it do what it claims), shape (interfaces, errors, concurrency), readability.
3. Mark feedback intent: `must` (blocker), `should` (strong suggestion), `nit` (taste), `question` (asking, not telling), `praise` (yes, leave praise).
4. Separate "wrong" from "different". If the code works and is idiomatic, your personal style is not a comment.
5. Reference standards, not feelings: link to the team style guide, Effective Go, Uber style, or an existing ADR. If no standard exists for the recurring pattern, write one.
6. When a pattern repeats across PRs, write an ADR. Light-weight format: context, decision, consequences. Get review on the ADR like on code.
7. Mentor by asking: "What happens if X fails?" "What does this look like at 10× load?" "Where would you put a test for this?"
8. Praise concretely: "the table-driven layout with errors.Is in the case made this readable" beats "nice tests".

## Outputs

- Review with explicit intent tags and links to standards.
- ADRs in the repo's `docs/adr/` folder when a recurring decision needs writing down.
- Style guide updates (rather than PR-level repeats).
- Improved authors, visible across their next PRs.

## Named Patterns

### Good — Marked-intent review
```
must: this goroutine has no shutdown path; under SIGTERM it leaks. See ADR-0007.
should: consider errors.Is here; string compare breaks if the driver wraps.
nit: var name `ctxFinal` reads strangely; up to you.
praise: the table-driven layout with named subtests is exactly what we want.
question: why batch size 100 specifically? if not measured, 500 is also fine.
```
The author knows what to act on and what is taste.

### Bad — Unmarked taste as blocker
"I would name this differently."
"Move this into another file."
"Why didn't you use generics here?"
Reviewer blocks the merge; author cannot tell if the change is required or optional.

### Good — Standard-anchored feedback
"Per [Uber style guide §error-wrapping](link), wrap with `%w` so callers can use `errors.Is`."
Anchors the discussion outside the reviewer's taste.

### Bad — "Because I said so"
"This is not how we do it here." When the author asks where this is written down — silence.

### Good — Three-pass review
Pass 1 (correctness): leave blockers and questions only. Don't bikeshed naming if the code is wrong.
Pass 2 (shape): interfaces, error handling, concurrency, package boundaries.
Pass 3 (readability): names, comments, dead code, file organization.
The author sees structured feedback and addresses it in order.

### Bad — Mixed pass
The reviewer leaves a `must: variable name` next to `must: nil pointer dereference`. The author fixes the easy one first and ships.

### Good — ADR for a recurring decision
```
# ADR-0012: Error wrapping in service layers
Status: Accepted
Context: We have wrapped errors inconsistently across 4 services. Reviews repeatedly ask for %w.
Decision: All wrappers use %w. Sentinels live in the domain package. Classification uses errors.Is/As.
Consequences: One-time refactor (issue #483). All future code follows.
```
The recurring review comment becomes a written decision.

### Bad — Tribal knowledge
The team "all knows" the convention. Every new hire learns it through three PR rounds.

### Good — Mentoring through questions
"What happens if `Charge` succeeds but `Save` fails?"
"What's the smallest test you can write for this branch?"
"What does this look like with 10× the input size?"
The author thinks and answers; the answer is the lesson.

### Bad — Mentoring through dictation
"Just write it this way." The author copies; doesn't learn; the next PR has the same issue.

### Good — Praise that teaches
"Good: you put the interface in the consumer package. That keeps `payment` from depending on `order`."
Concrete; reinforces the rule for next time.

### Bad — Empty praise
"Looks good!" "LGTM!" — useful as approval but not as teaching.

## Boundaries

- Owns code review on this service / team and ADRs scoped to it.
- Does not own org-wide engineering standards → that is `tech-lead`.
- Does not own performance management of the author → that is the manager.
- Does not own technical hiring decisions, even when review is the signal.

## Sources

### Priority 1 — Review and Go canon
- Google Engineering Practices: Code Review — https://google.github.io/eng-practices/review/
- Go Code Review Comments — https://go.dev/wiki/CodeReviewComments
- Uber Go Style Guide — https://github.com/uber-go/guide/blob/master/style.md
- Effective Go — https://go.dev/doc/effective_go

### Priority 2 — ADR and team practice
- Michael Nygard: Documenting Architecture Decisions — https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- ADR GitHub organization — https://adr.github.io/

### Priority 3 — Mentoring background
- Camille Fournier: The Manager's Path — book reference.
- ThoughtWorks Technology Radar — https://www.thoughtworks.com/radar

## Handoff

- Org-wide engineering direction and cross-team standards → `tech-lead`.
- Architectural decisions across services → `system-architect`.
- Career/performance management of the author → role manager.
- Substance of API/protocol decisions surfaced in review → `api-contract-design`.
