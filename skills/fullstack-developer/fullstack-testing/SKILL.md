---
name: fullstack-testing
description: Use when defining or implementing the test strategy for a fullstack feature — choosing the right test type per layer (unit, integration, component, contract, e2e), setting up MSW for API mocking, writing Testing Library component tests, backend integration tests with a real database, and deciding the minimum coverage to ship with confidence. Covers both frontend and backend test layers as one coherent strategy.
family: method
profile_level: Senior+
---

# Fullstack Testing

## Purpose

Cover the critical user path through both ends of the stack with the minimum tests that give confidence to ship and refactor safely. Focus test investment on the contract boundary (API shape), the service boundary (integration), and the user-visible behaviour (e2e) — not on mocking implementation details.

## Use When

- Starting a new feature and deciding what tests to write before implementation.
- Reviewing a PR where tests cover only one end of the stack.
- Adding confidence to a refactor that touches backend and frontend simultaneously.
- Setting up the test toolchain for a new fullstack project (MSW, Testing Library, Vitest/Jest, integration tests against real DB).
- Deciding which layer owns which test and why.

## Do Not Use When

- The discussion is QA strategy at the release or team level → handoff to `qa-engineer`.
- The discussion is load testing or performance benchmarks → backend specialist skill.
- The discussion is test infrastructure setup (CI parallelization, container orchestration) → `devops-sre`.
- The discussion is e2e platform ownership (Playwright grid, reporting) → `qa-engineer`.

## Inputs

- User scenario for the feature: what user action, what outcome, what failure paths.
- Existing test toolchain: frameworks, mocking libraries, CI setup.
- API contract (OpenAPI spec or TypeScript types).
- Risk profile: what breaks if this is wrong? How fast must you know?

## Workflow

1. Map the risk levels: identify the two or three critical paths where a bug costs the most. Write tests for those first, not for every function.
2. Choose the layer for each test:
   - **Unit**: pure functions, business logic with no I/O — fast, no setup.
   - **Component**: React component renders correct UI for each API state (loading, success, error, empty) — use Testing Library + MSW.
   - **Contract**: does the frontend receive what the API schema promises? — use MSW with OpenAPI-validated handlers.
   - **Integration**: does the backend write to and read from the real database correctly? — use a real test DB (testcontainers or local instance).
   - **E2e**: does the critical user path work from browser to server? — use Playwright on the happy path + the top two error paths.
3. Mock at the boundary, not inside the boundary. For frontend: mock the HTTP layer with MSW (not fetch directly). For backend: use a real database in integration tests (not the repository mock).
4. Write component tests for every distinct UI state a component can be in. A component with three states needs three tests.
5. Write backend integration tests for: create, read, update, and the two most important constraint violations. Use a real database, reset state between tests.
6. Write one e2e test per critical user flow. Keep e2e tests narrow: one action, one assertion. Long e2e tests are expensive and fragile.
7. Add a contract test or OpenAPI validation snapshot to CI. It fails when the API shape changes without updating the frontend types.

## Outputs

- Test strategy documented in the PR description or ADR: which layer, which test, which tool.
- Component tests for every distinct UI state (Testing Library + MSW).
- Backend integration tests against a real database for critical writes and reads.
- One e2e test per critical user path (Playwright or Cypress).
- CI step that validates OpenAPI → TypeScript type generation on every contract change.

## Named Patterns

### Good — Component test per UI state with MSW
```typescript
import { render, screen, waitFor } from '@testing-library/react';
import { http, HttpResponse } from 'msw';
import { server } from '@/mocks/server'; // MSW server setup
import { OrderPage } from './OrderPage';

test('shows skeleton while loading', () => {
  server.use(
    http.get('/v1/orders/:id', () => new Promise(() => {})) // never resolves
  );
  render(<OrderPage orderId="123" />);
  expect(screen.getByRole('progressbar')).toBeInTheDocument();
});

test('shows order data on success', async () => {
  server.use(
    http.get('/v1/orders/:id', () =>
      HttpResponse.json({ id: '123', status: 'placed', total: 4200 })
    )
  );
  render(<OrderPage orderId="123" />);
  await waitFor(() => expect(screen.getByText('4200')).toBeInTheDocument());
});

test('shows error with retry on server failure', async () => {
  server.use(
    http.get('/v1/orders/:id', () => HttpResponse.json({}, { status: 500 }))
  );
  render(<OrderPage orderId="123" />);
  await waitFor(() => expect(screen.getByRole('button', { name: /retry/i })).toBeInTheDocument());
});
```
Three tests, three states. MSW intercepts at the HTTP layer — no React Query mocking, no module mocking.

### Bad — Mocking React Query internals
```typescript
jest.mock('@tanstack/react-query', () => ({
  useQuery: () => ({ data: mockOrder, isLoading: false }),
}));
```
The mock bypasses the actual fetch. The test passes even if the component does not call the API at all.

### Good — Backend integration test with real database
```typescript
// Uses testcontainers or a test DB connection
describe('OrderRepository', () => {
  let repo: OrderRepository;

  beforeEach(async () => {
    await db.migrate.latest(); // run migrations
    await db('orders').truncate();
    repo = new OrderRepository(db);
  });

  it('saves and retrieves an order', async () => {
    const input = { userId: 'u1', total: 4200, status: 'placed' };
    const saved = await repo.save(input);
    const found = await repo.getById(saved.id);
    expect(found).toMatchObject(input);
  });

  it('throws on duplicate idempotency key', async () => {
    const key = 'idem-key-1';
    await repo.save({ ...input, idempotencyKey: key });
    await expect(repo.save({ ...input, idempotencyKey: key }))
      .rejects.toThrow(/duplicate/i);
  });
});
```
Real database, real migrations. The test catches missing indices, wrong constraints, and ORM edge cases.

### Bad — Mocking the repository in a "unit" test of the service
```typescript
const mockRepo = { save: jest.fn().mockResolvedValue(order) };
const service = new OrderService(mockRepo);
await service.placeOrder(input);
expect(mockRepo.save).toHaveBeenCalled();
// Validates that the code called the mock. Not that data is saved correctly.
```

### Good — E2e test for the critical path, narrow scope
```typescript
// Playwright
test('user can place and cancel an order', async ({ page }) => {
  await page.goto('/products/abc');
  await page.getByRole('button', { name: 'Add to cart' }).click();
  await page.getByRole('button', { name: 'Checkout' }).click();
  await expect(page.getByText('Order placed')).toBeVisible();
  await page.getByRole('button', { name: 'Cancel order' }).click();
  await expect(page.getByText('Order cancelled')).toBeVisible();
});
```
One user flow. One assertion per step. Runs against a deployed environment, not a mock.

### Bad — E2e test covering every scenario
A single Playwright test with 40 steps covering registration, login, browsing, checkout, payment, refund, and support chat. Flaky at step 27; takes 3 minutes; fails half the CI runs.

### Good — Contract validation in CI
```json
// package.json
"test:contract": "openapi-typescript ./docs/api/openapi.yaml -o ./src/api/schema.d.ts && tsc --noEmit"
```
Runs on every commit. Fails if the OpenAPI spec and the TypeScript types diverge. Catches the schema-drift class of bugs before they reach production.

## Boundaries

- Owns developer-level test strategy and implementation for both ends of the feature.
- Does not own QA strategy, test planning at the team or release level → `qa-engineer`.
- Does not own e2e infrastructure, grid setup, or release-level regression suite → `qa-engineer`.
- Does not own CI/CD pipeline setup and parallelization → `devops-sre`.
- Does not own load testing or performance benchmarks → backend specialist.

## Sources

### Priority 1 — Testing tool canon
- Testing Library Documentation — https://testing-library.com/docs/
- Mock Service Worker (MSW) Documentation — https://mswjs.io/docs/
- Vitest Documentation — https://vitest.dev/
- Playwright Documentation — https://playwright.dev/
- TypeScript Handbook — https://www.typescriptlang.org/docs/handbook/

### Priority 2 — Testing methodology
- Kent C. Dodds: Testing Trophy — https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications
- Node.js Best Practices (testing section) — https://github.com/goldbergyoni/nodebestpractices
- Google Engineering Practices — https://google.github.io/eng-practices/

### Priority 3 — Background
- martinfowler.com on testing — https://martinfowler.com/testing/
- web.dev — https://web.dev/

## Handoff

- QA strategy, team-level test planning, release regression → `qa-engineer`.
- E2e infrastructure, grid, parallelization → `devops-sre` + `qa-engineer`.
- Load and performance testing → `backend-go-developer` / `python-developer` + `devops-sre`.
- API contract schema that tests validate → `api-contract-design`.
