---
name: forms-and-complex-workflows
description: Use when designing or reviewing forms, onboarding, checkout, multi-step workflows, dashboards, account areas, validation patterns, recovery paths, and complex task completion flows — including the full state matrix for all screens in a workflow.
family: method
profile_level: Senior+
---

# Forms and Complex Workflows

## Purpose

Design complex multi-step interfaces so users can complete high-stakes tasks (submit, purchase, register, configure, apply) with clear steps, predictable progress, recoverable errors, understandable validation, and visible checkpoints. This skill also covers the full interaction state matrix for any workflow: every screen in a flow must define all states, not just the happy path.

## Use When

- A product area contains forms, onboarding, checkout, profile setup, account flows, or multi-step decisions.
- Users must provide data, compare options, correct errors, or resume interrupted work.
- A workflow has many states, validations, permissions, or data dependencies.
- QA or frontend needs an explicit state matrix for a workflow's screens.
- System statuses, API failures, or permission states affect the user experience of a multi-step flow.

## Do Not Use When

- A single, self-contained screen without multi-step logic is the target — use `ui-composition-and-visual-hierarchy`.
- The goal is interaction state specification for a static view (not a workflow) — that belongs in `wireframing-and-prototyping` annotations.
- Business rules, eligibility logic, or field-level validation rules need to be defined — hand off to `business-analyst`.
- API behavior, validation implementation, or backend error taxonomy needs to be specified — hand off to `system-analyst`.
- Funnel metrics, drop-off analysis, or conversion experiment design is needed — hand off to `product-analyst`.

## Inputs

- User goal, flow, fields, rules, validations, system states, device context, and accessibility expectations.
- Business rules, API constraints, analytics signals, support feedback, or current defects.
- Known incidents: where users get stuck, where they abandon, where they call support.
- Step count, branching logic, and resume/save requirements.

## Workflow

1. **Identify the task outcome and all entry points.** State clearly: what does the user accomplish? What are all valid starting conditions? What are all stopping conditions (success, abandonment, timeout, error)?

2. **Group steps around user mental models, not data models.** Ask: "What does the user think they are doing at this step?" not "What data does the back end collect here?" Users mentally organize tasks by decision, not by field or entity. Reduce step count by grouping related decisions, not by cramming fields onto one screen.

3. **Define validation timing, error recovery, and progress model.** Validation timing: validate on blur (field loses focus), not on submit, for most fields. Validate on submit only for cross-field dependencies. Error recovery: inline error appears below the field, not only at the top of the page. Progress model: multi-step forms show where the user is (step 2 of 4) and allow backward navigation without losing progress.

4. **Build the full state matrix for each screen in the workflow.** For each screen, enumerate all states:
   - `default` — initial state, no user input yet
   - `in-progress` — user has started filling in data
   - `validation-error` — one or more fields have inline errors
   - `loading` — system processing (after submit, during real-time check)
   - `server-error` — API failure with recovery action
   - `success` — step or full task completed
   - `empty` — no data to show yet (dashboard with no records)
   - `permission-restricted` — user cannot access this step or field
   - `resume` — user returns to an interrupted flow
   - `timeout` — session or operation expired with a clear recovery path

5. **Check accessibility for the entire flow.** Focus management on step transitions: where does focus land after moving to step 2? Error announcements: are errors announced to screen readers (aria-live region or focus-to-error)? Form labels: every input has a visible label (not only a placeholder). Touch targets: all interactive elements meet platform minimum.

6. **Hand off business rules, API behavior, tracking, and test cases to owners.** Do not embed assumed business rules in the design — mark them as open questions and route to Business Analyst. Do not invent API error codes — mark all error states as "error from system, message TBD by SA." Create explicit handoff tasks.

## Outputs

- Workflow design brief (step structure, branching, progress model).
- Form or multi-step interaction model (annotated screens per step).
- Full state matrix for each screen in scope.
- Validation and recovery-state notes.
- Accessibility checklist for the flow.
- Handoff tasks for BA, SA, Product Analyst, Frontend, or QA.

## Named Patterns

**Good — Validation on blur, inline, actionable:**
```
Label: Email address
Helper: We'll send your confirmation here
[user types 'john@' and tabs away]
Error (on blur): Enter a valid email address (example@domain.com)
— Error appears below field immediately on blur
— Field gets error border color (semantic token: --destructive)
— aria-describedby links input to error message
```

**Bad — Validation only on submit, all errors at the top:**
```
[User fills 6 fields, clicks Submit]
Error banner: "Please correct the errors: Email is invalid, Phone number is required, Password too short"
— All errors appear at once, no visual link to the field
— User must scroll to find each problem
— Screen reader users hear a long list without field context
```

**Good — Multi-step with progress indicator and backward navigation:**
> "Step 2 of 4: 'Shipping address.' Progress bar shows step 2 active. 'Back' link returns to step 1 with all step-1 data preserved. Breadcrumb: Personal info → Shipping (active) → Payment → Review."

**Bad — No progress, no backward navigation:**
> "Form with no step indicator. 'Back' button navigates to the previous browser page, clearing all entered data. User abandons at step 3 because they cannot fix a step-1 error without starting over."

**Good — Save and resume for long workflows:**
> "Account application: 8 steps, ~15 minutes. After step 4, user sees 'Your progress is saved. Return at any time — your link: [email link].' On return: user lands at step 5 with all previous answers preserved."

**Bad — No save mechanism for long workflows:**
> "Application form with 8 steps and no save. User's session expires at step 7. All data lost. Support receives 40 complaints per day about lost applications." (Lack of resume is a design defect, not a technical limitation.)

**Good — Server error with recovery action:**
> "Payment declined state: 'Your card was declined. Check your card number or try a different card.' [Change card] button visible. Retry button available. Support contact link available. User is not left at a dead end."

**Bad — Generic error with no recovery path:**
> "'An error occurred. Please try again.' [OK button]. User clicks OK — same error. No guidance on what failed, what to do, or who to contact." (Error without recovery is a UX failure regardless of whose fault the error is.)

## Boundaries

- Does not own business rules, eligibility logic, or field-level validation rules → `business-analyst`.
- Does not own API, data model, or backend validation implementation → `system-analyst` + `frontend-developer`.
- Does not own checkout or funnel metrics interpretation → `product-analyst`.
- Does not own QA test-case design or regression → `qa-engineer`.
- Does not implement ARIA attributes or form semantics in code → `frontend-developer`.

## Sources

**Priority 1:**
- Caroline Jarrett & Gerry Gaffney, "Forms that Work: Designing Web Forms for Usability": https://www.formsthatwork.com/
- GOV.UK Design System, Question pages: https://design-system.service.gov.uk/patterns/question-pages/
- GOV.UK Design System, Error summary: https://design-system.service.gov.uk/components/error-summary/
- W3C WCAG 2.2: https://www.w3.org/TR/WCAG22/

**Priority 2:**
- Baymard Institute, Checkout usability research: https://baymard.com/research/checkout-usability
- Nielsen Norman Group, Prevent User Errors: https://www.nngroup.com/articles/slips/
- WAI ARIA Authoring Practices Guide, Forms: https://www.w3.org/WAI/ARIA/apg/patterns/

**Priority 3:**
- Smashing Magazine, Form Design Patterns: https://www.smashingmagazine.com/printed-books/form-design-patterns/
- Luke Wroblewski, "Web Form Design: Filling in the Blanks": https://www.lukew.com/resources/web_form_design.asp

## Handoff

```
To: system-analyst
Task: Specify API error taxonomy for all server-error states in the workflow
Context: Form design includes server-error states with placeholder messages; need actual error codes and recovery actions
Inputs: State matrix with all server-error states listed; current placeholder messages
Expected artifact: Error code list, human-readable error descriptions, recommended recovery actions per error type
Acceptance criteria: All state matrix server-error rows have a confirmed error code + message + recovery action
```

```
To: qa-engineer
Task: Build test cases from workflow state matrix
Context: Complete state matrix provided for all workflow screens
Inputs: Annotated wireframes, state matrix, validation rules, error states
Expected artifact: QA test case set covering all states (default, error, loading, success, empty, permission, timeout, resume)
Acceptance criteria: Each state row in the matrix has at least one test case with trigger, expected behavior, and pass/fail criteria
```
