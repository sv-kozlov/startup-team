---
name: code-review-and-mentoring
description: Use when reviewing mobile code (Kotlin/Swift/Dart/TypeScript) for platform idiomaticity, writing an ADR for a recurring mobile architectural decision, setting a team standard, or mentoring a Middle → Senior mobile developer. Covers review etiquette, feedback intent tagging, ADR format, and the difference between "wrong" and "different".
family: lead
profile_level: Senior+
---

# Code Review and Mentoring

## Purpose

Make code review move the code and the author forward, not just block the merge. Lift team practice through ADRs and consistent feedback rather than personal preference. Distinguish "this is wrong and unsafe" from "this is different from what I would write". Apply the same review discipline whether the language is Kotlin, Swift, or Dart.

## Use When

- Reviewing a non-trivial mobile pull request (new screen, architectural change, SDK integration).
- A pattern keeps re-appearing in reviews — time to write it down as an ADR or team convention.
- Onboarding a new mobile developer to the codebase or platform.
- Mentoring a Middle toward Senior on platform idiomaticity, lifecycle, or testability.
- A non-obvious technical decision is being made (native vs cross-platform, storage engine, auth flow) — write an ADR.

## Do Not Use When

- The review is about API contract evolution → involve `backend-developers` or `system-analyst` for the substance.
- The review is about performance hot paths → use `mobile-performance-and-resources` for profiling evidence.
- The review is about QA test strategy → handoff to `qa-engineer`.
- The discussion is performance management of a person → out of scope; that is the manager's job.

## Inputs

- Pull request with description, linked ticket, and tests.
- Existing team conventions, ADR log, or platform style guides.
- Author's level and platform experience.

## Workflow

1. Read the description and tests first. If they do not tell you what the change does and why, ask before reviewing the code.
2. Review in three passes: (1) correctness — lifecycle, threading, error handling; (2) shape — architecture layers, dependency direction, testability; (3) readability — naming, dead code, comments.
3. Mark feedback intent: `must` (blocker, safety/correctness), `should` (strong suggestion), `nit` (taste, optional), `question` (asking, not telling), `praise` (leave praise explicitly).
4. Separate "wrong" from "different". If the code works correctly and is platform-idiomatic, your personal style is not a blocker comment.
5. Reference standards, not feelings: link to Android Architecture Guide, Swift API Design Guidelines, the team ADR, or Effective Kotlin. If no standard exists for a recurring pattern, write one.
6. When a pattern repeats across PRs (e.g., every team member puts business logic in Composables), write an ADR. Light-weight format: context, decision, consequences. Review the ADR like code.
7. Mentor by asking: "What happens if the ViewModel is destroyed here?", "How would you test this branch?", "What does this look like on a low-RAM device?"
8. Praise concretely: "the state hoisting here keeps the Composable stateless and the ViewModel testable" beats "nice code".

## Outputs

- Review with explicit intent tags and links to standards or ADRs.
- ADRs in `docs/adr/` when a recurring mobile decision needs writing down.
- Team convention updates (rather than repeating the same PR comment).
- Improved authors visible across their next PRs.

## Named Patterns

### Good — Marked-intent review comment
```
must: this coroutine is launched in GlobalScope; it will leak after the ViewModel is cleared.
      Use viewModelScope.launch { } instead. See ADR-0003.

should: extract this mapping to a toDomain() extension function; repository returns
        domain models, not API models.

nit: variable name `tempList` — up to you, but `pending` reads closer to the intent.

praise: the fake repository pattern here makes the ViewModel test fast and reliable.

question: why is this retry hardcoded to 3? if not measured, exponential backoff to 5 is also fine.
```
The author knows what to act on and what is taste.

### Bad — Unmarked taste as blocker
```
"I would have named this differently."
"Move this logic to the ViewModel."
"Why didn't you use a sealed class here?"
```
Author cannot tell if the change is required or optional; review blocks without teaching.

### Good — Standard-anchored feedback (Kotlin)
```kotlin
// must: per Android Architecture Guide, the data layer must not expose LiveData to the
// domain layer. Replace with Flow<List<Order>> and let the UI collect it.
// Reference: https://developer.android.com/topic/architecture/data-layer
```

### Bad — "Because I said so"
```
"We don't do it like this." Author asks where it's written — silence.
```

### Good — ADR for a recurring mobile decision
```markdown
# ADR-0007: ViewModel state model — single sealed state vs separate fields

Status: Accepted
Context: PRs alternate between a single `UiState` sealed class and multiple LiveData/StateFlow fields.
         Reviews consistently ask for consistency.
Decision: All ViewModels expose a single `data class UiState(...)` as a StateFlow.
          Side-effects (navigation, toasts) are exposed as a SharedFlow<UiEffect>.
Consequences: One-time refactor (issue #312). All new ViewModels follow this pattern.
              Tests become predictable: one state object, not multiple observable fields.
```

### Bad — Tribal knowledge
```
"Everyone on the team knows we use single state." A new hire learns through five PR rounds.
```

### Good — Mentoring through questions (iOS/Swift)
```
"What happens to this Task if the view is dismissed before it completes?"
"How would you test this path without a real URLSession?"
"What does this look like when the user has a low-memory warning while on this screen?"
```
Author thinks; the answer is the lesson.

### Bad — Mentoring through dictation
"Just write it like this." Copy-paste; no understanding; same issue in the next PR.

## Boundaries

- Owns code review on this mobile codebase or team scope and ADRs scoped to it.
- Does not own org-wide engineering standards across all platforms → `tech-lead`.
- Does not own performance management of the author → role manager.
- Does not own QA test strategy or release sign-off → `qa-engineer`.

## Sources

### Priority 1 — Review canon and platform style
- Google Engineering Practices: Code Review — https://google.github.io/eng-practices/review/
- Android Architecture Guide (review reference) — https://developer.android.com/topic/architecture
- Swift API Design Guidelines — https://www.swift.org/documentation/api-design-guidelines/
- Effective Kotlin — https://leanpub.com/effectivekotlin (reference; cite specific items in comments)

### Priority 2 — ADR practice
- Michael Nygard: Documenting Architecture Decisions — https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- ADR GitHub organization — https://adr.github.io/

### Priority 3 — Mentoring background
- Camille Fournier: The Manager's Path — book reference.
- ThoughtWorks Technology Radar — https://www.thoughtworks.com/radar

## Handoff

- Org-wide engineering direction and cross-team standards → `tech-lead`.
- API contract decisions surfaced in review → `backend-developers` / `system-analyst`.
- QA test strategy issues surfaced in review → `qa-engineer`.
- Performance bottleneck evidence needed → `mobile-performance-and-resources`.
