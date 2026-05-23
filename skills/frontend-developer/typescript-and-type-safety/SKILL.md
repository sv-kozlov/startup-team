---
name: typescript-and-type-safety
description: Use when introducing strict TypeScript, designing type-safe UI state models, validating API responses with Zod, eliminating `any` leaks, or reviewing the type coverage of components, hooks, and API clients. Covers strict config, discriminated unions, type inference, schema validation, and generics for reusable utilities.
family: code
profile_level: Senior+
---

# TypeScript and Type Safety

## Purpose

Make invalid UI states unrepresentable and API contract violations visible at compile time or at the data entry point. Eliminate the category of "runtime shape mismatch" errors that occur because the client trusted the server's undocumented response format.

## Use When

- Enabling or tightening TypeScript config (`strict: true`, `noUncheckedIndexedAccess`).
- Modelling loading/error/success/empty UI states for a component or hook.
- Adding runtime validation for API responses, environment variables, or form inputs.
- Reviewing code for `any` usage, type assertions (`as T`), or missing null checks.
- Creating reusable generic hooks or utilities.

## Do Not Use When

- The task is component decomposition and module layout → `frontend-architecture-and-component-design`.
- The task is data fetching lifecycle and cache strategy → `state-management-and-data-flow`.
- The task is full API integration including auth and error boundaries → `api-integration-frontend`.

## Inputs

- Existing `tsconfig.json` and `strict` flag status.
- API response shapes (OpenAPI spec, backend code, or documented contract).
- Components or hooks with `any` occurrences or unhandled nulls.

## Workflow

1. Enable `strict: true` in `tsconfig.json`. If the codebase is large, enable incrementally with `// @ts-strict-ignore` per file rather than delaying the whole project. Address the resulting errors file by file.
2. Model UI states with discriminated unions. Every component that has loading/error/data transitions should have a type that makes partial states impossible.
3. Validate API responses at the boundary with Zod. Generate the TypeScript type from the schema with `z.infer<>`. Do not use `as` casts on raw API data.
4. Replace `any` with `unknown` for values whose shape is genuinely unknown; narrow with type guards or Zod `.parse()`.
5. Prefer type inference over explicit annotations for function return types when the return type is obvious from the body. Write explicit annotations for public APIs and hook return shapes.
6. Use generic hooks/utilities when ≥2 consumers share the same shape logic. A single consumer is not enough reason to add a generic.

## Outputs

- Tightened `tsconfig.json` with `strict: true`.
- Discriminated union types for component state machines.
- Zod schemas for API response validation with `z.infer<>` derived types.
- Zero `any` annotations in new code; documented exceptions for legacy.

## Named Patterns

### Good — Discriminated union for async state
```ts
type AsyncState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };

function OrderDetail({ state }: { state: AsyncState<Order> }) {
  switch (state.status) {
    case 'idle':    return <Placeholder />;
    case 'loading': return <Skeleton />;
    case 'error':   return <ErrorState error={state.error} />;
    case 'success': return <OrderCard order={state.data} />;
  }
}
```
TypeScript ensures every branch is handled; `state.data` is only accessible in the `success` case.

### Bad — Boolean flags soup
```ts
interface OrderState {
  loading: boolean;
  error: string | null;
  data: Order | null;
}
// loading=true, error=null, data={…} — valid type, invalid state
```
The type permits impossible combinations. Defensive null checks pollute every render.

### Good — Zod schema at API boundary
```ts
import { z } from 'zod';

const OrderSchema = z.object({
  id: z.string().uuid(),
  status: z.enum(['pending', 'paid', 'cancelled']),
  total: z.number().positive(),
  createdAt: z.string().datetime(),
});

export type Order = z.infer<typeof OrderSchema>;

export async function fetchOrder(id: string): Promise<Order> {
  const raw = await httpClient.get(`/orders/${id}`);
  return OrderSchema.parse(raw); // throws ZodError on schema mismatch
}
```
Contract mismatch surfaces immediately in the fetch function, not ten rendering layers later.

### Bad — `as` cast on raw response
```ts
const raw = await httpClient.get(`/orders/${id}`);
const order = raw as Order; // silent lie — shape is not verified
```
The cast suppresses the TypeScript error; runtime shape mismatches produce cryptic undefined-access errors.

### Good — `unknown` + type guard
```ts
function isApiError(value: unknown): value is { message: string; code: string } {
  return (
    typeof value === 'object' &&
    value !== null &&
    'message' in value &&
    'code' in value
  );
}
```
Narrows the shape with evidence, not assertion.

### Bad — `any` for "I'll fix later"
```ts
function handleError(err: any) {
  console.error(err.message); // crashes if err is a string
}
```
Deferred typing accumulates and is rarely paid back.

### Good — Generic reusable hook
```ts
function usePaginatedQuery<T>(
  key: string[],
  fetcher: (page: number) => Promise<T[]>,
) {
  const [page, setPage] = useState(1);
  const query = useQuery({ queryKey: [...key, page], queryFn: () => fetcher(page) });
  return { ...query, page, setPage };
}
```
Shared shape logic extracted once; concrete hooks stay thin.

## Boundaries

- Owns type configuration and schema design at component, hook, and API client level.
- Does not own data fetching lifecycle — that is `state-management-and-data-flow` and `api-integration-frontend`.
- Does not own form validation UX — that is part of `api-integration-frontend` (form/submit error handling).
- Does not own runtime API contract on the server side — that is `backend-go-developer` / `python-developer`.

## Sources

### Priority 1 — TypeScript canon
- TypeScript Handbook — https://www.typescriptlang.org/docs/
- TypeScript strict mode — https://www.typescriptlang.org/tsconfig#strict
- Zod documentation — https://zod.dev/

### Priority 2 — Orientation
- Matt Pocock: Total TypeScript — https://www.totaltypescript.com/
- The Twelve-Factor App (config typing) — https://12factor.net/

### Priority 3 — Pattern background
- martinfowler.com: Make Illegal States Unrepresentable — https://martinfowler.com/

## Handoff

- Runtime API contract enforcement on the server side → `backend-go-developer` / `python-developer`.
- Component structure and module layout → `frontend-architecture-and-component-design`.
- Data fetching lifecycle and cache invalidation → `state-management-and-data-flow`.
