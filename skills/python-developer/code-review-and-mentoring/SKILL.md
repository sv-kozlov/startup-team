---
name: code-review-and-mentoring
description: Use when reviewing someone else's Python code, lifting a team standard, writing an ADR, or mentoring a Middle/Senior on idiomatic Python. Covers review etiquette, the order of feedback, ADR shape, and the difference between "different" and "wrong".
family: lead
profile_level: Senior+
---

# Code Review and Mentoring

## Purpose

Make code review move the code and the author forward, not just block the merge. Lift team practice through ADRs and consistent feedback rather than personal preference. Distinguish "this is wrong" from "this is different from what I would write".

## Use When

- Reviewing a non-trivial Python pull request.
- A pattern keeps re-appearing in reviews — time to write it down.
- Onboarding a new Python developer to the codebase.
- Mentoring a Middle toward Senior, or a Senior on team-level impact.
- A non-obvious technical decision is being made — write an ADR.

## Do Not Use When

- The review is about API contract evolution → use `api-contract-design` for the substance.
- The review is about performance hot paths → use `python-testing` and `service-observability` for evidence.
- The discussion is performance management of a person → out of scope; that is the manager's job.

## Inputs

- Pull request with description, linked ticket, and tests.
- Existing team conventions, ADR log, style guide (`pyproject.toml` with ruff/mypy config).
- Author's level and how much context they had.

## Workflow

1. Read the description and tests first. If they don't tell you what the change does and why, ask before reviewing the code.
2. Review in three passes: correctness (does it do what it claims?), shape (typing, error handling, async safety, DI), readability.
3. Mark feedback intent: `must` (blocker), `should` (strong suggestion), `nit` (taste), `question` (asking, not telling), `praise` (yes, leave praise).
4. Separate "wrong" from "different". If the code works, is typed, and is idiomatic, your personal style is not a comment.
5. Reference standards, not feelings: link to `pyproject.toml` rules, PEP 8, mypy docs, or an existing ADR. If no standard exists for the recurring pattern, write one.
6. When a pattern repeats across PRs, write an ADR. Light-weight format: context, decision, consequences. Get review on the ADR like on code.
7. Mentor by asking: "What happens if the DB is unavailable here?" "What does this look like at 10× the input size?" "How would you test this without patching globals?"
8. Praise concretely: "the Protocol-based fake instead of monkeypatching made this test readable" beats "nice tests".

## Outputs

- Review with explicit intent tags and links to standards.
- ADRs in the repo's `docs/adr/` folder when a recurring decision needs writing down.
- Style guide updates (rather than PR-level repeats).
- Improved authors, visible across their next PRs.

## Named Patterns

### Good — Marked-intent review
```
must: this async function calls requests.get() — that blocks the event loop. See ADR-0004 on async HTTP.
should: use Protocol here instead of importing the concrete SQLAlchemy repo; keeps this test from needing a DB.
nit: variable name `res` is ambiguous; `order_response` or `response` is clearer. Up to you.
praise: the contextvars propagation for correlation ID is exactly right.
question: why retry 3 times specifically here? if not measured, 5 might be safer.
```
The author knows what to act on and what is taste.

### Bad — Unmarked taste as blocker
"I would name this differently."
"Move this to another module."
"Why aren't you using a dataclass here?"
Reviewer blocks the merge; author cannot tell if the change is required or optional.

### Good — Standard-anchored feedback
"Per `pyproject.toml` ruff rule B008: do not call mutable defaults in function signatures. Use `default_factory` instead."
Anchors the discussion to a configured rule, not the reviewer's preference.

### Bad — "Because I said so"
"This is not how we do it here." When the author asks where this is written down — silence.

### Good — Three-pass review
Pass 1 (correctness): leave blockers and questions only. Don't bikeshed naming if the async code is wrong.
Pass 2 (shape): Protocol interfaces, error hierarchy, `CancelledError` handling, missing `mypy` annotations.
Pass 3 (readability): names, comments, dead code, file organization.
The author sees structured feedback and addresses it in order.

### Bad — Mixed pass
The reviewer leaves `must: variable name` next to `must: swallowed CancelledError`. The author fixes the easy one first and ships.

### Good — ADR for a recurring Python decision
```
# ADR-0007: Dependency injection strategy
Status: Accepted
Context: We mixed global singletons, service locators, and constructor injection across 5 services.
  Tests required extensive monkeypatching; changes to one global broke unrelated tests.
Decision: Use constructor injection everywhere. Composition root wires dependencies at startup.
  No import of concrete implementations inside service methods.
Consequences: One-time refactor (issue #241). All new code follows. mypy enforces Protocol types.
```
The recurring review comment becomes a written decision.

### Bad — Tribal knowledge
The team "all knows" to use Protocol-based fakes. Every new hire learns it through three PR rounds.

### Good — Mentoring through questions
"What happens if `session.commit()` succeeds but the Kafka publish fails?"
"Can you write a test for this branch without patching globals?"
"What's the `mypy` output if you remove the type annotation here?"
The author thinks and answers; the answer is the lesson.

### Bad — Mentoring through dictation
"Just write it this way." The author copies; doesn't learn; the next PR has the same issue.

### Good — Praise that teaches
"Good: you put the `Protocol` in the application package, not in infrastructure. That keeps SQLAlchemy out of the use-case tests."
Concrete; reinforces the design rule for next time.

### Bad — Empty praise
"Looks good!" "LGTM!" — useful as approval but not as teaching.

## Boundaries

- Owns code review on this service / team and ADRs scoped to it.
- Does not own org-wide engineering standards → that is `tech-lead`.
- Does not own performance management of the author → that is the manager.
- Does not own technical hiring decisions, even when review is the signal.

## Sources

### Priority 1 — Review and Python canon
- Google Engineering Practices: Code Review — https://google.github.io/eng-practices/review/
- PEP 8 — https://peps.python.org/pep-0008/
- mypy documentation — https://mypy.readthedocs.io/
- ruff documentation — https://docs.astral.sh/ruff/

### Priority 2 — ADR and team practice
- Michael Nygard: Documenting Architecture Decisions — https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- ADR GitHub organization — https://adr.github.io/

### Priority 3 — Mentoring background
- Google Engineering Practices (reviewer guide) — https://google.github.io/eng-practices/review/reviewer/
- ThoughtWorks Technology Radar — https://www.thoughtworks.com/radar

## Handoff

- Org-wide engineering direction and cross-team standards → `tech-lead`.
- Architectural decisions across services → `system-architect`.
- Career/performance management of the author → role manager.
- Substance of API/protocol decisions surfaced in review → `api-contract-design`.
