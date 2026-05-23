---
name: code-review-and-mentoring
description: Use when reviewing someone else's React/TypeScript code, lifting a team frontend standard, writing an ADR for a frontend decision, or mentoring a Middle/Senior on idiomatic React. Covers review etiquette, the order of feedback, ADR shape for frontend, and the difference between "different" and "wrong" in TypeScript/React code.
family: lead
profile_level: Senior+
---

# Code Review and Mentoring

## Purpose

Make frontend code review move the code and the author forward, not just block the merge. Lift team React/TypeScript practice through ADRs and consistent feedback rather than personal preference. Distinguish "this is wrong" from "this is different from what I would write".

## Use When

- Reviewing a non-trivial React/TypeScript pull request.
- A pattern keeps reappearing in reviews — time to write it down.
- Onboarding a new frontend developer to the codebase.
- Mentoring a Middle toward Senior, or a Senior on team-level impact.
- A non-obvious frontend architecture decision is being made — write an ADR.

## Do Not Use When

- The review is about bundle size and performance → use `web-performance-and-bundling` for the substance.
- The review is about WCAG compliance → use `accessibility-and-i18n` for the checklist.
- The review is about performance management of a person → out of scope; that is the manager's job.

## Inputs

- Pull request with description, linked ticket, and tests.
- Existing team conventions, ADR log, style guide.
- Author's level and how much context they had.

## Workflow

1. Read the description and tests first. If they do not tell you what the change does and why, ask before reviewing the code. A PR without a description is incomplete, not just inconvenient.

2. Review in three passes:
   - **Pass 1 — Correctness**: does the code do what it claims? Are loading, error, and empty states handled? Are types sound? Are edge cases covered?
   - **Pass 2 — Shape**: component decomposition, hook extraction, data flow direction, state model. Is the component doing one thing?
   - **Pass 3 — Readability**: names, prop types, comments for non-obvious decisions, dead code.

3. Mark feedback intent explicitly:
   - `must` — blocker; merge-blocking issue.
   - `should` — strong suggestion; not a blocker but important.
   - `nit` — taste or style; author's call.
   - `question` — asking, not telling; may become a `must` after the answer.
   - `praise` — leave it; concrete praise teaches.

4. Separate "wrong" from "different". If the code works, is type-safe, and handles states correctly — your preferred React pattern is not a comment.

5. Reference standards, not feelings: link to the team style guide, React docs, TypeScript handbook, or an existing ADR. If no standard exists for the recurring pattern, write one.

6. When a pattern repeats across PRs, write an ADR. Light-weight format: context, decision, consequences. Get review on the ADR like on code.

7. Mentor by asking: "What happens when the API returns an empty array here?" "What does the TypeScript error mean if we remove this cast?" "Where would you add a test for this path?"

8. Praise concretely: "Good: the discriminated union here makes the loading/error/success branches exhaustive" is more useful than "nice types".

## Outputs

- Review with explicit intent tags and links to team standards or docs.
- ADRs in the repo's `docs/adr/` folder for recurring decisions.
- Style guide updates (rather than repeated PR-level comments).
- Authors who ship fewer review cycles on the next PR.

## Named Patterns

### Good — Marked-intent review
```
must: the error state is not rendered — if `useOrderList` fails, the component returns
      `undefined` and the user sees a blank area. Add an error branch.
      Ref: team convention ADR-FE-003.
should: extract the empty state to <OrderEmptyState /> — this pattern already exists
        in the Orders feature.
nit: `orderData` → `orders` is more idiomatic for an array. Up to you.
praise: the Zod schema here catches the backend shape mismatch we saw last sprint.
question: why is `staleTime: 0` set here? if the data does not change often,
          30 s would reduce redundant fetches. Curious about the intent.
```
The author knows what to act on, what is taste, and what needs clarification.

### Bad — Unmarked taste as blocker
"I would structure this differently."
"Move this hook to a separate file."
"Why didn't you use React.memo here?"
Reviewer blocks the merge; author cannot tell if the change is required.

### Good — Standard-anchored feedback
"Per [ADR-FE-007](link), we validate all API responses with Zod at the query boundary — cast `as Order` bypasses that. Please add `OrderSchema.parse()`."
Anchors the discussion outside personal preference.

### Bad — "Because I said so"
"This is not how we do it here." When the author asks where it is documented — silence.

### Good — Three-pass structure
Pass 1 leaves only correctness and safety blockers. Pass 2 addresses shape. Pass 3 addresses readability. Authors address blockers first and do not ship while open nits are unresolved.

### Bad — Mixed criticality
A `must: variable name` next to a `must: missing null check` — the author fixes the easy one first and submits.

### Good — ADR for a recurring frontend decision
```markdown
# ADR-FE-009: State management split — server vs client state
Status: Accepted
Context: We have mixed React Query data into Zustand store in 4 features,
         causing stale cache and over-fetching.
Decision: Server state goes into React Query. Zustand is for UI-only client state.
          No API data is duplicated into the store without explicit justification.
Consequences: One-time migration (issue #512). All future features follow this split.
```
The recurring review comment becomes a written decision.

### Bad — Tribal knowledge
The team "all knows" the convention. Every new hire learns it through three PR rounds.

### Good — Mentoring through questions
"What does the TypeScript error say if we remove the `as Order` cast?"
"What happens to this component if `data` is an empty array and not `undefined`?"
"Where is the test for the error branch?"
The author thinks through the problem; the answer becomes the lesson.

### Bad — Mentoring through dictation
"Just write it this way." The author copies without understanding; the next PR has the same issue.

### Good — Concrete praise
"Good: you put the query hook in the feature slice and exported from its index. That keeps the Orders feature self-contained."
Reinforces the structural rule concretely.

## Boundaries

- Owns frontend code review on this application/team and ADRs scoped to it.
- Does not own org-wide engineering standards → `tech-lead`.
- Does not own performance management of the author → the manager.
- Does not own technical hiring decisions, even when review is the signal.

## Sources

### Priority 1 — Review and React/TypeScript canon
- Google Engineering Practices: Code Review — https://google.github.io/eng-practices/review/
- React docs — https://react.dev/
- TypeScript handbook — https://www.typescriptlang.org/docs/

### Priority 2 — ADR and team practice
- Michael Nygard: Documenting Architecture Decisions — https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- ADR GitHub organization — https://adr.github.io/

### Priority 3 — Mentoring background
- Camille Fournier: The Manager's Path — book reference.
- ThoughtWorks Technology Radar — https://www.thoughtworks.com/radar

## Handoff

- Org-wide frontend direction and cross-team standards → `tech-lead`.
- Architectural decisions across frontend applications → `system-architect`.
- Career/performance management of the author → role manager.
- Substance of accessibility issues surfaced in review → `accessibility-and-i18n`.
- Substance of performance issues surfaced in review → `web-performance-and-bundling`.
