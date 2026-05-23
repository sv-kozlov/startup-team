---
name: api-contract-design
description: Role-specific addendum for api-contract-design in the Fullstack Developer context. Use shared-api-contract-design for the full method. This file contains TypeScript/openapi-typescript-specific code examples and type boundary constraints.
family: method
profile_level: Senior+
superseded_by: shared-api-contract-design
---

# API Contract Design — Fullstack Addendum

> **Primary skill:** `shared-api-contract-design` at `skills/shared/shared-api-contract-design/SKILL.md`.
> This file is a role-specific addendum. Follow the shared skill's Workflow and apply the fullstack-specific constraints below.

## Fullstack Implementation Constraints

Apply these in addition to the shared skill's Workflow:

1. **OpenAPI 3.1 is the single source of truth for types on both ends.** Generate TypeScript types via `openapi-typescript`; use `openapi-fetch` for typed HTTP calls. Never maintain parallel type declarations in frontend and backend code.
2. **Run `openapi-typescript` + `tsc --noEmit` in CI** on every PR that changes `openapi.yaml`. A compile error is a breaking change detection.
3. **No `any` in the type boundary.** All API request/response types must be derived from generated schemas.
4. **One RFC 7807 error type on the client.** Define `ProblemDetails` from the generated schema; use a single error handler across all routes.
5. **Idempotency-Key** — always generate client-side with `crypto.randomUUID()` before the first send; never reuse across retries of a different operation.

## Fullstack-Specific Named Patterns

### Good — Single source of truth via code generation
```typescript
// package.json
// "generate:api": "openapi-typescript ./docs/api/openapi.yaml -o ./src/api/schema.d.ts"

// Both ends use generated types
import type { components, paths } from '@/api/schema';

type Order = components['schemas']['Order'];
type PlaceOrderRequest = components['schemas']['PlaceOrderRequest'];

// Typed React Query hook
const useOrder = (id: string) =>
  useQuery<Order>({
    queryKey: ['order', id],
    queryFn: () =>
      apiClient.GET('/v1/orders/{id}', { params: { path: { id } } }),
  });
```
One schema file. One generation command. Type errors in CI before a broken deploy.

### Bad — Manual type duplication
```typescript
// backend/types.ts
interface Order { id: string; amount: number; }

// frontend/types.ts — copied manually
interface Order { id: string; amount: number; }
// backend silently renames amount → totalCents
// frontend breaks at runtime, not at compile time
```

### Good — Typed error handler (RFC 7807)
```typescript
// Generated from OpenAPI schema
import type { components } from '@/api/schema';
type ProblemDetails = components['schemas']['ProblemDetails'];

const handleApiError = (err: ProblemDetails): void => {
  switch (err.code) {
    case 'ORDER_ALREADY_CANCELLED':
      showToast('Order was already cancelled.');
      break;
    case 'INSUFFICIENT_FUNDS':
      showToast(`Insufficient balance: ${err.detail}`);
      break;
    default:
      showToast('An unexpected error occurred.');
  }
};
```
One parser for all endpoints; new error codes produce compile-time warnings via discriminated union.

### Bad — Per-endpoint error handling
```typescript
// POST /orders: response.data.error (string)
// GET /orders/:id: response.data.message + response.data.code (number)
// DELETE /orders/:id: plain text "not found"
// Three different parsers; coverage gaps in edge cases.
```

### Good — Idempotent POST with client-generated key
```typescript
const placeOrder = async (payload: PlaceOrderRequest): Promise<Order> => {
  const idempotencyKey = crypto.randomUUID(); // generate before first attempt
  const { data, error } = await apiClient.POST('/v1/orders', {
    body: payload,
    headers: { 'Idempotency-Key': idempotencyKey },
  });
  if (error) throw error;
  return data;
};
```
Safe to retry on network timeout. Server deduplicates using the key.

### Good — CI validation step
```yaml
# .github/workflows/ci.yml
- name: Generate API types
  run: npm run generate:api
- name: Type-check
  run: tsc --noEmit
- name: Schema diff
  run: oasdiff breaking docs/api/openapi.yaml docs/api/openapi.prev.yaml
```
Breaking changes are caught before merge, not after deploy.

## Handoff

- Requirements behind the contract → `system-analyst` (`shared-api-contract-design`, System Analyst mode).
- Deep Go/gRPC/protobuf implementation → `backend-go-developer`.
- Platform-wide API style guide → `tech-lead` / `system-architect`.
- Client-side data fetching patterns → `fullstack-data-flow`.
- Event/message schemas → `event-driven-integration`.
