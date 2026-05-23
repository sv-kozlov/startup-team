---
name: typescript-and-quality
description: Use when setting up or improving TypeScript type discipline across a fullstack project — enabling strict mode, generating shared types from OpenAPI schema, enforcing type-safe API clients, removing `any` from public interfaces, typing DTO and domain boundaries, and configuring tsconfig for both frontend and backend. Covers TypeScript as the primary quality gate on both ends of the stack.
family: code
profile_level: Senior+
---

# TypeScript and Quality

## Purpose

Make TypeScript the first quality gate on both ends of the stack: types catch schema drift, wrong API shapes, and boundary leakage before tests or production. A team that generates types from a contract schema catches an entire class of bugs automatically. A team that uses `any` freely does not.

## Use When

- Starting a new fullstack project and setting up `tsconfig.json` for frontend and backend.
- Eliminating `any` from a codebase that accumulated it over time.
- Setting up type generation from an OpenAPI schema (`openapi-typescript`, `tRPC`, or similar).
- Typing the DTO / domain / transport boundary in the backend service.
- Reviewing a PR where type safety is weak: too many type assertions, `as`, or `any`.

## Do Not Use When

- The task is API contract schema design → `api-contract-design`.
- The task is data fetching logic and React Query hooks → `fullstack-data-flow`.
- The task is runtime type validation (Zod, Yup) as a separate concern from static types → covered here only as it relates to boundary typing.
- The task is JavaScript (no TypeScript) → not in scope.

## Inputs

- Existing `tsconfig.json` files (frontend and backend).
- OpenAPI schema or other contract definition.
- Locations of `any`, type assertions (`as`), and `@ts-ignore` in the codebase.
- Monorepo layout (if shared types package exists).

## Workflow

1. Enable `strict: true` in `tsconfig.json` on both ends. This activates `strictNullChecks`, `noImplicitAny`, `strictFunctionTypes`, and others. Fix the resulting errors — do not suppress them with `as` or `any`.
2. Set `noUncheckedIndexedAccess: true` to make array and object index access return `T | undefined` instead of `T`. Prevents a class of runtime crashes.
3. Set up type generation from the OpenAPI schema: `openapi-typescript ./docs/api/openapi.yaml -o ./src/api/schema.d.ts`. Run this in CI. Both frontend and backend import from the same source.
4. Define layer boundaries as TypeScript types: `ApiDto` (wire shape), `DomainModel` (business entity), `ViewModel` (UI-specific shape). Write mapping functions between them. Do not pass `ApiDto` into domain logic.
5. Eliminate `any` in public module interfaces. Allow `any` internally only with an explicit `// eslint-disable-next-line @typescript-eslint/no-explicit-any` comment with a reason.
6. Use Zod (or equivalent) at system entry points — HTTP request parsing, environment variables, config files — to validate at runtime and derive static types from validators.
7. In a monorepo, put shared types (API contract types, domain value objects) in a `@packages/types` package imported by both `apps/frontend` and `apps/backend`. No copy-paste.

## Outputs

- `tsconfig.json` with `strict: true` and `noUncheckedIndexedAccess: true` on both ends.
- Generated TypeScript types from the OpenAPI schema tracked in the repository.
- Layer boundary types (`ApiDto`, `DomainModel`, `ViewModel`) with explicit mapping.
- CI step running `tsc --noEmit` and type generation validation.
- Zero `any` in public module interfaces (residual `any` annotated with rationale).

## Named Patterns

### Good — Strict tsconfig for both ends
```json
// tsconfig.json (applies to both frontend and backend)
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "forceConsistentCasingInFileNames": true,
    "isolatedModules": true
  }
}
```

### Bad — No strict mode
```json
{ "compilerOptions": { "target": "ES2020" } }
// TypeScript is used but provides no meaningful checks.
// `any` propagates silently; null/undefined errors appear at runtime.
```

### Good — Layer boundary types with mapping
```typescript
// types/api-dto.ts — wire shape (generated from OpenAPI)
export interface OrderDto {
  id: string;
  total_cents: number;
  status: 'placed' | 'confirmed' | 'cancelled';
}

// domain/order.ts — business entity (no wire coupling)
export interface Order {
  id: string;
  totalCents: number;
  status: OrderStatus;
}

// mappers/order.mapper.ts — explicit conversion
export const toDomain = (dto: OrderDto): Order => ({
  id: dto.id,
  totalCents: dto.total_cents,
  status: dto.status as OrderStatus,
});
```
Domain logic never receives a raw `OrderDto`. Mapping is a single place to update when the API evolves.

### Bad — Raw DTO throughout the codebase
```typescript
// The same object flows from API response through components to business logic
const order = await fetchOrder(id); // any
order.total_cents;      // in components
order.total_cents * 2;  // in business calculations
// Backend renames to totalCents → runtime crash in three places
```

### Good — Zod at the entry point
```typescript
import { z } from 'zod';

const CreateOrderSchema = z.object({
  productId: z.string().uuid(),
  quantity: z.number().int().positive(),
  idempotencyKey: z.string().uuid(),
});

type CreateOrderRequest = z.infer<typeof CreateOrderSchema>;

// In the HTTP handler:
const body = CreateOrderSchema.parse(req.body); // throws on invalid input
// body is now typed CreateOrderRequest — safe to use in service layer
```
Validate once at the boundary. Everywhere else in the service, `productId` is `string`, not `unknown`.

### Bad — Type assertion at the boundary
```typescript
const body = req.body as CreateOrderRequest;
// Trusts the client completely. A missing field throws deep in the service layer.
```

### Good — Shared types in monorepo
```typescript
// packages/types/src/order.ts
export interface Order { id: string; totalCents: number; status: OrderStatus; }
export type OrderStatus = 'placed' | 'confirmed' | 'cancelled';

// apps/frontend — imports from the shared package
import type { Order } from '@packages/types';

// apps/backend — same import
import type { Order } from '@packages/types';
```
One type definition. Both ends in sync. Removing a field causes compile errors on both sides.

### Bad — Manual type sync
```typescript
// apps/frontend/types.ts
interface Order { id: string; totalCents: number; }

// apps/backend/types.ts — copied from frontend
interface Order { id: string; totalCents: number; }
// Three months later they diverge. Nobody notices until production.
```

### Good — Type narrowing over type assertion
```typescript
const processEvent = (event: OrderEvent) => {
  if (event.type === 'OrderPlaced') {
    // event.type is narrowed to literal 'OrderPlaced'
    // event.payload is inferred from the discriminated union
    sendConfirmation(event.payload.userId);
  }
};
```

### Bad — Type assertion to "help" TypeScript
```typescript
const event = getEvent() as OrderPlacedEvent;
event.payload.userId; // TypeScript is silent; runtime error if wrong type
```

## Boundaries

- Owns TypeScript configuration, type boundaries, shared types, and static type quality across the stack.
- Does not own the runtime validation library choice beyond its role as a boundary enforcer.
- Does not own the API contract design (what fields exist) → `api-contract-design`.
- Does not own the data fetching logic that uses the generated types → `fullstack-data-flow`.

## Sources

### Priority 1 — TypeScript canon
- TypeScript Handbook — https://www.typescriptlang.org/docs/handbook/
- TypeScript Strict Mode (`tsconfig`) — https://www.typescriptlang.org/tsconfig#strict
- openapi-typescript — https://openapi-ts.dev/
- Zod Documentation — https://zod.dev/

### Priority 2 — Quality practices
- Matt Pocock's TypeScript tips — https://www.totaltypescript.com/
- Node.js Best Practices (TypeScript section) — https://github.com/goldbergyoni/nodebestpractices

### Priority 3 — Background
- TypeScript Deep Dive (Basarat Ali Syed) — https://basarat.gitbook.io/typescript/
- ThoughtWorks Technology Radar — https://www.thoughtworks.com/radar

## Handoff

- API contract schema (the source for type generation) → `api-contract-design`.
- Data fetching hooks that consume generated types → `fullstack-data-flow`.
- Test infrastructure that checks type generation in CI → `fullstack-testing`.
- Backend runtime type validation under high load edge cases → backend specialist.
