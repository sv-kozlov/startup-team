---
name: frontend-architecture-and-component-design
description: Use when starting a new React application, restructuring module layout, deciding how to decompose components, or evaluating whether to introduce a layered/feature-sliced architecture. Covers module structure, UI/logic/data separation, consumer-side composition, and proportionality of architectural choice to problem size.
family: code
profile_level: Senior+
---

# Frontend Architecture and Component Design

## Purpose

Shape a React/TypeScript application so it is easy to read, easy to change, and pays for every architectural layer it carries. Optimize for clear module boundaries, explicit data flows, and a code structure a new Senior can navigate without a guide.

## Use When

- Bootstrapping a new React application or significant module.
- Adding a feature that does not cleanly fit the current structure.
- Reviewing a design where component responsibilities, data flow, or module dependencies are unclear.
- The team is considering feature-sliced design, micro-frontend split, or significant layering and the cost is not obvious.

## Do Not Use When

- The task is purely about TypeScript types and schema validation → `typescript-and-type-safety`.
- The task is state library choice and cache invalidation → `state-management-and-data-flow`.
- The task is API loading and error handling → `api-integration-frontend`.
- The task is cross-application or platform architecture → handoff to `system-architect`.

## Inputs

- Current module/folder tree and known pain points.
- Business capabilities and expected change axes (what will change most often).
- Visible scale: single-team or multi-team, number of major user flows.
- Design system availability and fidelity.

## Workflow

1. Name the application's main change axes: routes, features, shared UI, domain logic. This determines the primary structural split.
2. Draft a minimum module layout. For a medium React app: `app/` (providers, router), `pages/` or `routes/`, `features/<name>/` (self-contained slices), `shared/` (cross-feature utilities, design system wrappers).
3. Apply the single-responsibility rule per layer: UI components render, hooks manage local state and side effects, query/store modules manage data. Do not mix all three in one component.
4. Place abstractions on the consumer side. A feature that needs data owns its query hook; the shared layer exports a fetcher function, not an interface every feature must implement.
5. Verify dependency direction: `features/` depends on `shared/`, not on each other. If two features need the same sub-component, it moves to `shared/`, not cross-imports.
6. Check for God components. A component over 200 lines that handles layout, API fetching, form validation, and state transitions simultaneously is a structural symptom.
7. Decide architectural complexity by team size and number of long-lived change axes. Feature-sliced design pays for itself at ≥3 long-lived feature domains or ≥2 teams. Before that threshold it adds process without benefit.

## Outputs

- Module tree with explicit dependency arrows.
- ADR or PR description naming the chosen structure and the trade-off accepted.
- List of shared components/hooks with explicit consumer owners.
- Storybook entries for shared UI components.

## Named Patterns

### Good — Vertical feature slice
```
features/
  orders/
    api/         ← fetchers and types
    hooks/       ← useOrderList, useOrderDetail
    components/  ← OrderRow, OrderForm
    index.ts     ← public API of the slice
```
Changes to the Orders feature are contained within one folder. Other features import from `features/orders/index.ts`, not from internals.

### Bad — Horizontal technical layer split
```
components/   ← all components from all features
hooks/        ← all hooks
services/     ← all API calls
```
A change to the Orders flow requires editing five folders. Feature ownership is invisible; import graph becomes a tangle.

### Good — Consumer-side hook composition
```tsx
// features/orders/hooks/useOrderList.ts
export function useOrderList(filter: OrderFilter) {
  return useQuery({
    queryKey: ['orders', filter],
    queryFn: () => ordersApi.list(filter),
    staleTime: 30_000,
  });
}

// features/orders/components/OrderList.tsx
export function OrderList({ filter }: { filter: OrderFilter }) {
  const { data, isLoading, error } = useOrderList(filter);
  if (isLoading) return <OrderListSkeleton />;
  if (error)     return <ErrorState error={error} />;
  if (!data?.length) return <EmptyState label="No orders" />;
  return <ul>{data.map(o => <OrderRow key={o.id} order={o} />)}</ul>;
}
```
UI, data, and state are in separate units. Every state has a visual branch.

### Bad — God component
```tsx
export function OrderList() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    setLoading(true);
    fetch('/api/orders')
      .then(r => r.json())
      .then(d => { setOrders(d); setLoading(false); })
      .catch(e => { setError(e.message); setLoading(false); });
  }, []);
  // + 120 lines of JSX, inline styles, form logic
}
```
Untestable, unshareable, impossible to refactor one concern without touching all others.

### Good — Explicit public API (barrel export)
```ts
// features/orders/index.ts
export { OrderList } from './components/OrderList';
export { useOrderList } from './hooks/useOrderList';
export type { Order } from './api/types';
```
Consumers import from the feature's public API; internals can be refactored freely.

### Bad — Deep import paths
```ts
import { OrderRow } from '../../features/orders/components/internal/OrderRow';
```
Couples consumers to internal structure; refactoring internals breaks consumers.

### Good — Proportional layering
A three-route internal tool ships with `pages/`, `components/`, `api/`. No feature slices, no micro-frontend split, no domain layer until the product justifies the overhead.

### Bad — Premature feature-sliced design
A single-team dashboard with five screens introduces full FSD with layers, slices, and segments. Twelve folders for one change axis; new developers spend a week understanding the structure.

## Boundaries

- Owns the module structure, component composition, and dependency direction within the frontend application.
- Does not own cross-application architecture or micro-frontend infrastructure → `system-architect`.
- Does not own team-wide frontend standards across multiple applications → `tech-lead`.
- Does not own data fetching strategy or cache model → `state-management-and-data-flow`.

## Sources

### Priority 1 — React and web canon
- React docs: Thinking in React — https://react.dev/learn/thinking-in-react
- React docs: Managing State — https://react.dev/learn/managing-state
- MDN Web Docs — https://developer.mozilla.org/

### Priority 2 — Architectural orientation
- Feature-Sliced Design — https://feature-sliced.design/
- The Twelve-Factor App — https://12factor.net/

### Priority 3 — Pattern background
- martinfowler.com on Presentation Domain Data Layering — https://martinfowler.com/bliki/PresentationDomainDataLayering.html

## Handoff

- Cross-application module boundaries and micro-frontend topology → `system-architect`.
- Team-wide frontend standards and direction → `tech-lead`.
- TypeScript type design within the chosen structure → `typescript-and-type-safety`.
- Data fetching and state management within the chosen structure → `state-management-and-data-flow`.
