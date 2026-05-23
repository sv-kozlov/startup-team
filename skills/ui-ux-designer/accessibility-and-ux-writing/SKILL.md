---
name: accessibility-and-ux-writing
description: Use when checking or designing UI for accessibility risks — keyboard access, focus order, contrast, screen reader announcements, error accessibility — and when drafting or reviewing interface microcopy, labels, error messages, empty states, helper text, and button text to ensure copy is clear, actionable, and accessible.
family: method
profile_level: Senior+
---

# Accessibility and UX Writing

## Purpose

Reduce accessibility barriers in UX/UI artifacts and make interface text clear, actionable, consistent, and aligned with user intent. Accessibility and copy are addressed together because accessible copy is the primary intersection: labels, error messages, status messages, and focus announcements are both a copy problem and an accessibility problem simultaneously. Route technical implementation and compliance certification to the right owners.

## Use When

- A screen, prototype, component, or flow needs an accessibility risk review.
- Focus, keyboard access, contrast, status messages, errors, labels, or readability may be at risk.
- Labels, buttons, errors, empty states, onboarding copy, or helper text are unclear.
- UI copy affects task completion, error recovery, or user trust.
- A design needs microcopy before handoff or usability testing.
- A design must align with WCAG-aware product quality expectations.

## Do Not Use When

- WCAG compliance certification or formal accessibility audit is required — that is a QA and legal function, not a designer function.
- ARIA implementation, semantic HTML, or automated accessibility tests are needed — hand off to `frontend-developer` and `qa-engineer`.
- Brand voice, marketing copy, legal text, or editorial policy decisions are needed — hand off to Brand / Communication Design or Legal.
- Domain terminology validation is needed — hand off to `business-analyst` or domain owner.
- Comprehension testing or reading-level research is needed — hand off to `ux-researcher`.

## Inputs

**Accessibility:**
- UI mockup, prototype, components, states, target platform, and audience.
- Existing accessibility findings, design-system guidance, frontend constraints, or QA notes.
- WCAG target level (AA is the baseline; AAA for high-risk products).

**UX writing:**
- Screen goal, user context, state, business rule, system constraint, and tone guidance.
- Existing terminology, glossary, brand voice, legal constraints, or content owner feedback.
- Error codes and system states (from System Analyst) that need human-readable messages.

## Workflow

1. **Check the four WCAG principles: Perceivable, Operable, Understandable, Robust.** Work through them in order:
   - Perceivable: text alternatives, captions, contrast, no information conveyed by color alone.
   - Operable: keyboard access, no keyboard trap, focus visible, no timing without extension.
   - Understandable: labels, error identification, consistent navigation, predictable behavior.
   - Robust: name/role/value for custom components, status messages for screen readers.

2. **Check contrast.** For every text/background combination: normal text ≥ 4.5:1 (AA) or ≥ 7:1 (AAA). Large text (≥ 18pt regular or ≥ 14pt bold) ≥ 3:1. Non-text UI elements (focus rings, icons, chart lines) ≥ 3:1. Use the semantic token system, not raw hex — if a token fails contrast, flag it for `design-system-and-tokens` correction.

3. **Check focus order and keyboard path.** Focus must follow the reading order. On step transitions (modal opens, accordion expands, step advances), focus must move to the new content, not stay at the trigger. Trap keyboard focus inside modals and dialogs — escape must close. Custom interactive elements need keyboard event handling (space, enter, arrow keys by pattern type).

4. **Review labels and form copy.** Every input must have a visible `Label`, not only a placeholder. Placeholders disappear on input — they are not labels. Helper text appears below the label (always visible). Error messages: appear below the affected field, state what went wrong, and tell the user how to fix it.

5. **Draft and review interface copy.** Apply three rules: specific (say what it is, not 'something went wrong'), actionable (tell users what to do next), consistent (use the same term for the same thing throughout). Check: Is the button label a verb + object? Is the empty state helpful, not just decorative? Is the error message a recovery instruction, not an apology?

6. **Annotate aria-* intent for handoff.** The designer defines the intent; the developer implements:
   - Error messages: `aria-describedby` linking input to error text.
   - Status messages: `role="status"` for non-urgent announcements; `role="alert"` for errors.
   - Icon buttons without visible text: `aria-label` content agreed in the design.
   - Disabled states: `aria-disabled` vs `disabled` distinction noted.
   - Screen reader text for decorative vs. informative images.

7. **Separate design-level risks from implementation ownership.** Flag: what the designer can fix (contrast, label, copy, focus order in the design). Route: what requires implementation (ARIA attributes, semantic HTML, automated test, keyboard handler). Do not mark implementation concerns as design defects.

## Outputs

- Accessibility risk checklist organized by WCAG principle.
- Contrast audit table (token pairs + ratio + pass/fail).
- Focus order and keyboard path notes.
- aria-* intent annotations for handoff.
- Interface copy suggestions (labels, errors, empty states, helper text, button labels).
- Error and empty-state microcopy.
- Terminology questions and owner handoffs.
- Residual accessibility risks (what requires testing with real assistive technology).

## Named Patterns

**Good — Accessible error message:**
```
Label: Email address
[user tabs out of invalid field]
Error: "Enter a valid email address — for example, name@example.com"
— Specific (says what is wrong), actionable (shows the expected format), inline (below field)
— aria-describedby links input to this error text
— Error token uses --destructive; icon does not carry the error message alone
```

**Bad — Inaccessible error:**
```
[Red border around field]
[Small red asterisk next to label]
— Error conveyed by color alone (fails WCAG 1.4.1)
— No text error message
— Screen reader announces nothing about the error state
```

**Good — Visible label (not placeholder-as-label):**
```
<Label htmlFor="email">Email address</Label>
<Input id="email" placeholder="name@example.com" />
— Label is always visible; placeholder is an example, not a label
```

**Bad — Placeholder as label:**
```
<Input placeholder="Email address" />
— As soon as the user starts typing, the label disappears
— Screen reader may not announce the placeholder as a label
— Common pattern that fails WCAG 1.3.1
```

**Good — Button label is verb + object:**
> "Delete account" (specific, irreversible action clear)
> "Save changes" (what is saved is implied by context)
> "Continue to payment" (destination is named)

**Bad — Ambiguous button labels:**
> "OK" — OK to what? Close, confirm, submit, agree?
> "Click here" — no semantic meaning; screen reader announces "link: click here"
> "Submit" on a search form — the action is 'Search', not 'Submit'

**Good — Empty state with helpful guidance:**
> "No reports yet. Create your first report to start tracking performance."
> [Create report] button

**Bad — Empty state with no action:**
> "No data available." — User does not know if this is an error, a permission issue, or an empty state. No action is offered.

**Good — Focus moves to new content on modal open:**
> "Modal opens: focus moves to the modal title. User can tab through modal content. Escape closes modal and returns focus to the trigger button that opened it."

**Bad — Focus stays at trigger on modal open:**
> "Modal opens visually, but keyboard focus stays behind the modal. Screen reader user continues to interact with background content — 'keyboard trap' in the wrong direction. User cannot reach the modal."

## Boundaries

- Does not certify WCAG compliance alone — certification requires testing with real assistive technology and QA.
- Does not implement ARIA attributes, semantic HTML, or automated tests → `frontend-developer` + `qa-engineer`.
- Does not own brand voice, marketing copy, legal text, or editorial policy → Brand / Communication Design / Legal.
- Does not validate domain terminology without `business-analyst` or domain owner.
- Does not replace comprehension testing or accessibility user research → `ux-researcher`.

## Sources

**Priority 1:**
- W3C WCAG 2.2: https://www.w3.org/TR/WCAG22/
- WAI ARIA Authoring Practices Guide: https://www.w3.org/WAI/ARIA/apg/
- Ginny Redish, "Letting Go of the Words" (microcopy methodology): https://www.nngroup.com/books/letting-go-of-the-words/
- GOV.UK Design System, Error message: https://design-system.service.gov.uk/components/error-message/

**Priority 2:**
- GOV.UK Design System accessibility: https://design-system.service.gov.uk/accessibility/
- Apple Human Interface Guidelines, Accessibility: https://developer.apple.com/design/human-interface-guidelines/accessibility
- Material Design, Writing: https://m3.material.io/foundations/content-design/overview
- GOV.UK Service Manual, Writing for user interfaces: https://www.gov.uk/service-manual/design/writing-for-user-interfaces

**Priority 3:**
- Nielsen Norman Group, Error Message Guidelines: https://www.nngroup.com/articles/error-message-guidelines/
- Smashing Magazine, Writing Microcopy: https://www.smashingmagazine.com/2013/06/five-ways-prevent-bad-microcopy/
- A List Apart, Writing for Accessibility: https://alistapart.com/article/writing-for-accessibility/

## Handoff

```
To: frontend-developer
Task: Implement aria-* annotations from accessibility review
Context: Accessibility risk review identified ARIA intent for form errors, status messages, and icon buttons
Inputs: Accessibility annotation list (aria-describedby, role="alert", aria-label values per element)
Expected artifact: Implemented ARIA attributes confirmed in Storybook or dev environment
Acceptance criteria: All annotated elements have ARIA implemented; manual keyboard test passed
```

```
To: qa-engineer
Task: Run keyboard and screen reader test against accessibility checklist
Context: Design-level accessibility review complete; implementation risk remains for AT behavior
Inputs: Accessibility risk checklist, focus order notes, aria-* annotations
Expected artifact: Test results: passed / failed per checklist item; defect list for failures
Acceptance criteria: Tested with VoiceOver (iOS/macOS) and NVDA (Windows); keyboard-only test completed
```
