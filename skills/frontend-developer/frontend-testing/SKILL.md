---
name: frontend-testing
description: Use when covering React/TypeScript code with unit, component, or e2e tests; designing component APIs for testability; setting up Testing Library conventions; or writing Playwright e2e flows. Covers test strategy for critical user paths, visual regression, and the distinction between testing behavior versus implementation.
family: code
profile_level: Senior+
---

# Frontend Testing

## Purpose

Cover the risk that the interface breaks for users — not the risk that implementation details change. Write tests that exercise real behavior from the user's perspective, catch regressions reliably, and run fast enough to stay in the developer's inner loop.

## Use When

- Adding tests to a new component, hook, or user flow.
- Reviewing existing tests that mock implementation internals rather than behavior.
- Setting up a test pyramid for a new frontend module: deciding the split between unit, component, and e2e.
- Writing a Playwright e2e for a critical purchase, auth, or checkout flow.
- Evaluating component API design for testability (render props vs compound components vs direct hook tests).

## Do Not Use When

- The task is performance benchmarking of rendering → `web-performance-and-bundling`.
- The task is accessibility auditing as a separate pass → `accessibility-and-i18n`.
- The task is QA strategy and release-level regression planning → handoff to `qa-engineer`.
- The task is visual design review → handoff to `ui-ux-designer`.

## Inputs

- Component or user flow to cover.
- Existing test setup (Vitest/Jest config, Testing Library version, Playwright config).
- Known risk areas: critical purchase paths, auth flows, data mutation flows.
- Accessibility of test IDs or ARIA roles in the component.

## Workflow

1. Choose the test level by value:
   - **Unit** (hook logic, utility functions): fast, no DOM, Vitest or Jest.
   - **Component** (rendered UI, user interactions): Testing Library — render → act → assert by visible text/role.
   - **E2e** (critical multi-step flows): Playwright — browser, real routing, real or mocked API.

2. Query elements by role, label, or accessible name, not by CSS class or `data-testid` as first resort. Tests that find a button by `.btn-primary` break on style change; tests that find it by `role="button", name="Cancel"` survive.

3. Use `data-testid` only when no accessible query is possible (e.g., a chart data point without a label). Avoid `data-testid` as the default strategy — it hides accessibility gaps.

4. Test behavior, not implementation: do not assert the internal state of a hook or the order of `useState` calls. Assert what the user sees and can interact with.

5. For async components: use `await screen.findByRole(…)` instead of `waitFor`. Avoid arbitrary `setTimeout(fn, 100)` waits.

6. For Playwright e2e:
   - Define critical user journeys (login → browse → add to cart → checkout → success) as separate test files.
   - Use `page.getByRole()` and `page.getByLabel()` as primary locators; avoid `page.$('#some-id')`.
   - Isolate test data: use fixtures or API mocking so tests do not depend on shared live state.

7. Keep the test pyramid proportional: component tests are the majority; e2e tests cover only the flows that must not break in production. Avoid 90% e2e — they are slow and flaky.

## Outputs

- Component tests using Testing Library that query by role/label.
- Hook unit tests (via `renderHook` or standalone test doubles).
- Playwright e2e suite for critical user journeys.
- Visual regression baseline (if the project uses Chromatic or Percy).
- PR description noting which risk the tests address.

## Named Patterns

### Good — Query by accessible role
```tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { OrderForm } from './OrderForm';

test('submits order and shows confirmation', async () => {
  render(<OrderForm />);

  fireEvent.change(screen.getByRole('spinbutton', { name: /quantity/i }), {
    target: { value: '2' },
  });
  fireEvent.click(screen.getByRole('button', { name: /place order/i }));

  expect(await screen.findByText(/order placed/i)).toBeInTheDocument();
});
```
The test exercises a real user interaction path and fails only when the behavior changes.

### Bad — Query by CSS class
```tsx
const btn = container.querySelector('.btn-primary.submit');
fireEvent.click(btn!);
```
Passes when the class name matches; fails when the class is refactored even if the button still works.

### Good — Async query with `findBy`
```tsx
test('displays orders after loading', async () => {
  render(<OrderList filter={defaultFilter} />);
  expect(screen.getByRole('status', { name: /loading/i })).toBeInTheDocument();
  expect(await screen.findByRole('list')).toBeInTheDocument();
});
```
`findByRole` waits for the element; no arbitrary timeouts.

### Bad — `waitFor` with timeout
```tsx
await waitFor(() => expect(screen.getByRole('list')).toBeInTheDocument(), {
  timeout: 2000,
});
```
Adds 2 seconds to every run. Flaky under CI load. `findBy` is the idiomatic replacement.

### Good — Playwright with accessible locators
```ts
// e2e/checkout.spec.ts
test('user completes checkout', async ({ page }) => {
  await page.goto('/cart');
  await page.getByRole('button', { name: 'Proceed to checkout' }).click();
  await page.getByLabel('Card number').fill('4242424242424242');
  await page.getByRole('button', { name: 'Pay now' }).click();
  await expect(page.getByRole('heading', { name: /order confirmed/i })).toBeVisible();
});
```

### Bad — Playwright with CSS selectors
```ts
await page.click('#checkout-btn');
await page.fill('input[data-id="card-input"]', '4242...');
```
Breaks on any DOM refactor; does not verify accessibility role or text.

### Good — Hook test via `renderHook`
```ts
import { renderHook, act } from '@testing-library/react';
import { useCounter } from './useCounter';

test('increments count', () => {
  const { result } = renderHook(() => useCounter(0));
  act(() => result.current.increment());
  expect(result.current.count).toBe(1);
});
```

### Bad — Testing React internal state
```ts
// Asserting useState value directly via jest.spyOn(React, 'useState')
// Implementation test — breaks on any refactor, gives no user-facing confidence
```

## Boundaries

- Owns developer-level tests: unit, component, and e2e for user flows owned by the frontend.
- Does not own QA strategy, release-level regression, or exploratory testing → `qa-engineer`.
- Does not own performance benchmarking of rendered output → `web-performance-and-bundling`.
- Does not own accessibility auditing as a formal WCAG pass → `accessibility-and-i18n`.

## Sources

### Priority 1 — Testing canon
- Testing Library docs — https://testing-library.com/
- Playwright docs — https://playwright.dev/
- React Testing Library: Which query to use — https://testing-library.com/docs/queries/about

### Priority 2 — Orientation
- Kent C. Dodds: Testing Implementation Details — https://kentcdodds.com/blog/testing-implementation-details
- Google Testing Blog — https://testing.googleblog.com/

### Priority 3 — Pattern background
- martinfowler.com: Testing Pyramid — https://martinfowler.com/bliki/TestPyramid.html

## Handoff

- QA strategy and release regression → `qa-engineer`.
- Accessibility audit and WCAG compliance → `accessibility-and-i18n`.
- Performance profiling of renders → `web-performance-and-bundling`.
- E2e environment and CI test runner setup → `devops-sre`.
