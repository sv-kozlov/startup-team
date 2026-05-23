---
name: accessibility-and-i18n
description: Use when auditing or improving WCAG 2.2 compliance, fixing keyboard navigation, adding ARIA semantics, managing focus, conducting screen reader testing, or designing the internationalization and localization architecture (i18n-lib, plurals, bidirectional text). Covers semantic HTML, ARIA best practices, and multi-locale support.
family: method
profile_level: Senior+
---

# Accessibility and Internationalization

## Purpose

Make the interface usable by people with disabilities (WCAG 2.2 AA minimum) and usable across languages and locales. Accessibility is structural: semantic HTML first, ARIA only when native semantics are insufficient. i18n is architectural: translations are data, not code; locale-specific behavior (dates, numbers, plurals) is handled by the platform, not hand-rolled.

## Use When

- Auditing a new feature or page for WCAG 2.2 AA compliance.
- Fixing keyboard navigation, focus trapping in modals, or focus restoration after routing.
- Adding ARIA roles, labels, or live regions to custom interactive components.
- Conducting a screen reader test pass on critical user flows.
- Designing i18n architecture for a new application: choosing the library, setting up the message format, handling plurals and locale switching.
- Adding a new language/locale to an existing i18n setup.

## Do Not Use When

- The task is automated component testing including accessibility assertions → `frontend-testing`.
- The task is visual performance and bundle size → `web-performance-and-bundling`.
- The task is translation content review or copy editing → handoff to content/UX team.

## Inputs

- WCAG 2.2 AA conformance target (or project-specific accessibility SLA).
- Screen reader environment: NVDA/Firefox, JAWS/Chrome, VoiceOver/Safari.
- Supported locales and languages.
- Existing i18n library and message format (ICU, gettext, or custom).

## Workflow

### Accessibility pass

1. **Structural audit first.** Walk the component tree for: missing `<label>` on inputs, `<button>` vs `<div onClick>`, `<img>` without `alt`, decorative images with non-empty `alt`, heading hierarchy gaps (`h1` → `h3` skip).
2. **Keyboard navigation.** Every interactive element must be reachable by `Tab`, operable by `Enter`/`Space`, and dismissible by `Escape` for overlays. Custom widgets (dropdown, combobox, date picker) must follow the ARIA APG keyboard patterns for their role.
3. **Focus management.** When a modal opens, focus moves to the first interactive element inside it. When the modal closes, focus returns to the trigger element. Do not use `outline: none` without a visible focus style replacement.
4. **ARIA scoped to genuine need.** Use `role`, `aria-label`, `aria-labelledby`, `aria-describedby`, and `aria-live` only when native HTML semantics are insufficient. A `<button>` needs no `role="button"`; a custom combobox does.
5. **Color and contrast.** Text: ≥4.5:1 (AA) or ≥7:1 (AAA). Large text: ≥3:1. Interactive components and state indicators: ≥3:1.
6. **Screen reader test.** Test the critical user flow (login, main task, form submission) with at least one screen reader. Verify announcements of dynamic content (`aria-live="polite"` for status, `aria-live="assertive"` only for urgent interruptions).

### i18n architecture

1. Choose a library that supports ICU message format: `react-intl` or `i18next` with the ICU plugin. Avoid string concatenation for translated text.
2. Externalize all user-visible strings from day one. No hard-coded English strings in component code.
3. Handle plurals through the library's plural rules, not `count === 1 ? 'item' : 'items'`.
4. Handle dates, times, numbers, and currencies through `Intl.*` APIs or the library's formatters — never hand-format locale-specific values.
5. Support RTL: use logical CSS properties (`margin-inline-start` instead of `margin-left`). Test the layout with an RTL locale before declaring RTL support.
6. Lazy-load locale message bundles by language code to avoid shipping all translations in the main bundle.

## Outputs

- WCAG 2.2 AA audit checklist per feature.
- Fixed semantic HTML, ARIA attributes, and focus management.
- Screen reader test report for critical user flows.
- i18n setup with ICU messages, plural rules, and locale bundle splitting.
- RTL layout verified for supported RTL locales.

## Named Patterns

### Good — Native button for interactivity
```tsx
<button
  type="button"
  onClick={handleCancel}
  aria-label="Cancel order"
>
  <XIcon aria-hidden="true" />
</button>
```
Native `<button>` is focusable, activatable by keyboard, and announced correctly by screen readers.

### Bad — Click on a `div`
```tsx
<div onClick={handleCancel} className="btn">
  <XIcon />
</div>
```
Not focusable by keyboard; not announced as interactive by screen readers; no keyboard activation without manual `onKeyDown`.

### Good — Focus trap in modal
```tsx
import FocusTrap from 'focus-trap-react';

export function ConfirmDialog({ onConfirm, onCancel }: Props) {
  return (
    <FocusTrap>
      <div role="dialog" aria-modal="true" aria-labelledby="dialog-title">
        <h2 id="dialog-title">Confirm cancellation</h2>
        <button onClick={onConfirm}>Yes, cancel</button>
        <button onClick={onCancel}>No, keep order</button>
      </div>
    </FocusTrap>
  );
}
```
Focus stays inside the dialog until it is dismissed; `role="dialog"` and `aria-modal` are announced correctly.

### Bad — Modal without focus trap
```tsx
// Keyboard user can Tab out of the modal to background content
// Screen reader user does not know a dialog is open
```

### Good — ICU plural message
```ts
// en.json
{
  "cart.items": "{count, plural, one {# item} other {# items}}"
}

// usage
intl.formatMessage({ id: 'cart.items' }, { count: ordersCount })
```

### Bad — Manual ternary
```tsx
`${count} ${count === 1 ? 'item' : 'items'}`
// Fails for languages with complex plural rules (Russian, Polish, Arabic)
```

### Good — RTL-safe layout
```css
.card {
  margin-inline-start: 16px;  /* left in LTR, right in RTL */
  padding-inline: 12px 8px;
}
```

### Bad — Directional CSS
```css
.card {
  margin-left: 16px; /* flips incorrectly in RTL without mirroring */
}
```

## Boundaries

- Owns WCAG compliance, focus management, ARIA, and i18n architecture within the frontend.
- Does not own content authoring or translation review → content/UX team.
- Does not own infrastructure-level locale routing → `devops-sre` / `system-architect`.
- Does not own automated accessibility assertions in test suites → `frontend-testing`.

## Sources

### Priority 1 — Accessibility and i18n canon
- WCAG 2.2 — https://www.w3.org/TR/WCAG22/
- WAI-ARIA Authoring Practices 1.2 — https://www.w3.org/WAI/ARIA/apg/
- MDN: Accessibility — https://developer.mozilla.org/en-US/docs/Web/Accessibility
- MDN: Intl API — https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl

### Priority 2 — Orientation
- react-intl docs — https://formatjs.io/docs/react-intl/
- i18next docs — https://www.i18next.com/
- Google web.dev: Accessibility — https://web.dev/accessibility/

### Priority 3 — Pattern background
- Inclusive Components (Heydon Pickering) — https://inclusive-components.design/
- ARIA in HTML (W3C Note) — https://www.w3.org/TR/html-aria/

## Handoff

- Content authoring and translation → content/UX team.
- Locale routing and server-side locale detection → `devops-sre` / `system-architect`.
- Automated accessibility assertions in tests → `frontend-testing`.
- UX decisions on information hierarchy and interaction design → `ui-ux-designer`.
