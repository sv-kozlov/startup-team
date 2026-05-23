---
name: code-review-and-mentoring
description: Use when reviewing a fullstack pull request (both frontend and backend sides), lifting a team standard that spans client and server code, writing an ADR for a feature-level technical decision, or mentoring a Middle fullstack developer toward Senior. Covers review etiquette, contract and type boundary feedback, and the difference between "wrong" and "different".
family: lead
profile_level: Senior+
---

# Code Review and Mentoring (Fullstack)

## Purpose

Make fullstack code review move both the code and the author forward. Lift the team's end-to-end quality through ADRs and consistent feedback on both ends of the stack, not just one. Distinguish "this is a bug" from "this is different from what I would write".

## Use When

- Reviewing a PR that changes both frontend and backend code.
- A pattern keeps re-appearing in reviews across both ends — time to write it down.
- Onboarding a new fullstack developer to the codebase conventions.
- Mentoring a Middle toward Senior on end-to-end feature ownership.
- A non-obvious technical decision spans both ends — write an ADR.

## Do Not Use When

- The review is about API contract evolution substance → use `api-contract-design` for the content.
- The review is about test coverage strategy → use `fullstack-testing` for the substance.
- The review is about migration safety → use `fullstack-release-and-migration` for the substance.
- The discussion is performance management of a person → out of scope; that is the manager's role.
- The review is for a specialized backend or frontend PR without fullstack scope → route to `backend-go-developer` or `frontend-developer`.

## Inputs

- Pull request with description, linked ticket, and tests on both ends.
- Existing team conventions, ADR log, API contract.
- Author's level and how much context they had when writing.

## Workflow

1. Read the description and the test plan first. If they do not tell you what the feature does, what changed in the contract, and what was tested — ask before reviewing the code.
2. Review in three passes:
   - **Pass 1 (correctness)**: does it do what it claims? Are the states correct? Is the migration safe? Leave blockers and questions only.
   - **Pass 2 (contract and boundaries)**: is the API contract consistent? Are types shared from the source of truth? Are layer boundaries (transport / service / repository, component / hook / API client) respected?
   - **Pass 3 (readability)**: names, comments, dead code, file organization.
3. Mark feedback intent explicitly: `must` (blocker), `should` (strong suggestion), `nit` (taste), `question` (asking, not asserting), `praise` (specific, not empty).
4. Separate "wrong" from "different". If the code works and is consistent with team conventions, your personal preference is not a comment.
5. Reference standards, not feelings. Link to the team ADR, OpenAPI spec, tsconfig rules, or Testing Library guide. If no standard exists for a recurring pattern — write one.
6. When a pattern repeats across PRs, write an ADR. Light-weight format: context, decision, consequences.
7. Mentor by asking: "What happens if the SSE connection drops?" "What state does the UI show if the migration step 2 fails?" "Where would you put a contract test for this endpoint?"
8. Praise concretely: "The outbox pattern in the same transaction is exactly the right call here — prevents the lost-event class of bugs."

## Outputs

- Review with explicit intent tags (`must`, `should`, `nit`, `question`, `praise`) and links to standards.
- ADRs in `docs/adr/` when a recurring decision needs writing down.
- Style guide or convention updates instead of repeating the same PR comment.
- Improved authors, visible across their next PRs.

## Named Patterns

### Good — Marked-intent fullstack review
```
must: the API error response uses { error: string } but the OpenAPI spec says RFC 7807.
      The frontend has three error parsers because of this. See docs/api/openapi.yaml line 42.

should: the React Query staleTime is 0 here, which means every mount refetches.
        Check if 30s would serve the UX — same as the other order queries.

nit: fetchOrderData → getOrder would match the naming in the rest of the file. Up to you.

question: why SSE here instead of polling? If update frequency is < 1/min, polling is simpler.
          If there's a latency requirement I missed, please add it to the PR description.

praise: the outbox insert inside the same transaction as the order save is exactly right.
        This prevents the "event published for a rolled-back order" class of bugs.
```
The author knows what to act on, what is a suggestion, and what is taste.

### Bad — Unmarked feedback as blocker
```
"Move this to a separate hook."
"I'd write this differently."
"Why are you using useEffect here?"
```
The author cannot tell whether these are blockers or taste. They either fix everything (slow) or nothing (unsafe).

### Good — Standard-anchored contract feedback
```
must: this endpoint returns { id, amount } but the OpenAPI spec defines
      { id, amountCents }. Run `npm run generate:api` and update the frontend type — 
      the discrepancy will cause a TypeScript error and a runtime bug for mobile clients.
      See docs/api/openapi.yaml line 87 and ADR-0014.
```
The comment links to the spec and the ADR. The author knows exactly what to fix and why.

### Bad — Opinion without anchor
```
"The response shape looks off to me."
```
The author does not know what "off" means or what the correct shape is.

### Good — Three-pass review
Pass 1 (correctness): leave blockers and questions about behavior. Do not comment on naming while the logic is wrong.
Pass 2 (contract/boundaries): check that API types are generated, not handwritten. Check that mutations invalidate the right query keys. Check that the migration follows expand/contract.
Pass 3 (readability): names, file structure, comments.

The author sees structured feedback and knows which issues are critical.

### Bad — Mixed-pass review
`must: variable name` alongside `must: the transaction is missing here`. The author fixes the variable name first because it is easy. The transaction bug ships.

### Good — ADR for a recurring fullstack decision
```
# ADR-0017: SSE over polling for live order status
Status: Accepted
Context: Three features tried polling intervals between 2s and 30s. Traffic grows with users.
Decision: Use SSE for any live status feed. Polling only when event frequency < 1/min.
Consequences: One SSE endpoint per resource type. Frontend uses the useOrderEvents hook pattern.
              Requires keep-alive proxy configuration (documented in ADR-0018).
```
The recurring review comment "why are you polling?" becomes a written, citable decision.

### Bad — Tribal knowledge
The team "always uses SSE for live data." Every new fullstack developer learns this through three PR rounds and one production incident.

### Good — Mentoring through questions
```
"What does the UI show if the SSE connection drops for 5 seconds?"
"What happens to the React Query cache if you navigate away and back before the mutation settles?"
"The expand step adds a nullable column. What is the minimum time before the contract step can run?"
```
The developer thinks through the edge case. The answer is the lesson.

### Bad — Mentoring through dictation
"Just write it this way." The developer copies the pattern without understanding. The next PR has the same gap.

## Boundaries

- Owns code review on fullstack PRs and ADRs scoped to the feature or team.
- Does not own org-wide engineering standards → `tech-lead`.
- Does not own performance management of the author → the manager.
- Does not own hiring decisions, even when review is the signal.
- Does not own deep backend idiom reviews (Go, Python) → `backend-go-developer` / `python-developer`.

## Sources

### Priority 1 — Review and quality canon
- Google Engineering Practices: Code Review — https://google.github.io/eng-practices/review/
- TypeScript Handbook — https://www.typescriptlang.org/docs/handbook/
- Testing Library Documentation — https://testing-library.com/docs/
- OpenAPI Specification 3.1 — https://spec.openapis.org/oas/v3.1.0

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
- Substance of API/contract decisions surfaced in review → `api-contract-design`.
- Deep Go or Python idiomatic review → `backend-go-developer` / `python-developer`.
- Deep frontend platform review → `frontend-developer`.
