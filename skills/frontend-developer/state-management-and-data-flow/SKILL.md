---
name: state-management-and-data-flow
description: Use when choosing a state management approach, designing data flow between components, adding optimistic updates, fixing stale cache, or resolving prop drilling. Covers React Query/SWR for server state, Zustand/Redux Toolkit for client state, the server-client state split, and when each tool is appropriate.
family: code
profile_level: Senior+
---

# State Management and Data Flow

## Purpose

Keep server state and client state in separate domains, choose the simplest tool that meets the requirement, and prevent the class of bugs that arises when UI state and server data diverge silently. Make data flow traceable: every piece of state has exactly one owner.

## Use When

- Choosing between React Query, SWR, Zustand, Redux Toolkit, or React Context for a specific use case.
- Adding optimistic updates with a rollback path.
- Fixing stale or inconsistent data after a mutation.
- Resolving prop drilling more than two levels deep.
- Reviewing state design when global store is growing without clear owners.

## Do Not Use When

- The task is TypeScript type design for state shapes → `typescript-and-type-safety`.
- The task is loading/error/empty rendering including error boundaries → `api-integration-frontend`.
- The task is performance optimization (re-renders, memoization) → `web-performance-and-bundling`.

## Inputs

- Data origin: server-fetched vs computed client-only.
- Update frequency and staleness tolerance.
- Sharing scope: component-local, feature-level, or app-wide.
- Whether mutations need optimistic updates.

## Workflow

1. Classify the state by origin before choosing a tool:
   - **Server state** (data fetched from an API, lives on the server, needs cache + invalidation) → React Query or SWR.
   - **Client state** (UI-only: modals open/closed, selected tab, form draft, undo stack) → Zustand, Redux Toolkit, or `useState`/`useReducer`.
   - Never put server data into a global client store unless it requires client-side enrichment that cannot be done in the query layer.

2. For **server state** with React Query:
   - Define a stable `queryKey` array that encodes all parameters. If a parameter changes, the key changes, and the cache is automatically separated.
   - Set `staleTime` by data freshness requirements; default 0 fetches on every mount — usually too aggressive for lists.
   - Colocate query hooks with the feature slice that owns the data.

3. For **client state** with Zustand:
   - Keep stores small and feature-scoped. A single global mega-store is Redux without the tooling.
   - Use Zustand's `subscribeWithSelector` or selector functions to avoid re-renders on unrelated state changes.

4. For **optimistic updates**:
   - Cancel in-flight queries before applying the update to avoid race conditions.
   - Store the previous cache snapshot as rollback data.
   - Always `invalidate` after `onSettled` to reconcile the server's authoritative state.

5. For **prop drilling**:
   - First check if the shared data belongs to the feature's query cache (common case).
   - If the data is client-only and needed at 3+ levels: use Zustand store or React Context with a stable value.
   - Do not add a global store entry for data that only two components share; lift state or use composition.

6. Document state ownership in an ADR when the data flow is non-obvious or becomes a repeated source of bugs.

## Outputs

- Query hooks colocated with their feature slice.
- Store slices with explicit owner features.
- Optimistic update mutations with rollback and invalidation.
- ADR or PR description for non-obvious state architecture decisions.

## Named Patterns

### Good — React Query with stable key
```ts
// Encodes all filter params in the key — each unique filter has its own cache entry
export function useOrderList(filter: OrderFilter) {
  return useQuery({
    queryKey: ['orders', filter],
    queryFn: () => ordersApi.list(filter),
    staleTime: 30_000,
  });
}
```

### Bad — Shared mutation state in global store
```ts
// Global store stores a list fetched from the server
const useOrderStore = create(() => ({ orders: [] as Order[] }));
// Manually managed; never automatically refreshed; diverges after mutations
```

### Good — Optimistic update with rollback
```ts
const cancelOrder = useMutation({
  mutationFn: (id: string) => ordersApi.cancel(id),
  onMutate: async (id) => {
    await queryClient.cancelQueries({ queryKey: ['orders'] });
    const previous = queryClient.getQueryData<Order[]>(['orders']);
    queryClient.setQueryData<Order[]>(['orders'], old =>
      old?.map(o => o.id === id ? { ...o, status: 'cancelled' } : o) ?? []
    );
    return { previous };
  },
  onError: (_err, _id, ctx) => {
    queryClient.setQueryData(['orders'], ctx?.previous);
  },
  onSettled: () => {
    queryClient.invalidateQueries({ queryKey: ['orders'] });
  },
});
```
The UI updates immediately; if the server rejects, the cache is restored; in all cases the cache is refreshed.

### Bad — Optimistic update without rollback
```ts
const cancelOrder = useMutation({
  mutationFn: ordersApi.cancel,
  onSuccess: () => queryClient.invalidateQueries({ queryKey: ['orders'] }),
});
```
The UI does not respond until the request completes. If the server rejects, the user sees a generic error with no state recovery.

### Good — Feature-scoped Zustand store
```ts
// features/cart/store.ts
interface CartState {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (id: string) => void;
}

export const useCartStore = create<CartState>()(set => ({
  items: [],
  addItem: item => set(s => ({ items: [...s.items, item] })),
  removeItem: id => set(s => ({ items: s.items.filter(i => i.id !== id) })),
}));
```
Store is owned by the `cart` feature; other features import from its public API.

### Bad — Global UI state in one mega-store
```ts
const useAppStore = create(() => ({
  cartItems: [],
  isModalOpen: false,
  selectedOrderId: null,
  currentUser: null,
  theme: 'light',
  // … 30 more fields
}));
```
Every component that reads any field re-renders on every unrelated update; ownership is implicit; testing is painful.

## Boundaries

- Owns state model design and tool selection for client and server state.
- Does not own network loading and error boundary rendering — that is `api-integration-frontend`.
- Does not own type shapes for state — that is `typescript-and-type-safety`.
- Does not own render performance and memoization decisions — that is `web-performance-and-bundling`.

## Sources

### Priority 1 — React and library canon
- React Query (TanStack Query) docs — https://tanstack.com/query/latest
- Zustand docs — https://docs.pmnd.rs/zustand/getting-started/introduction
- Redux Toolkit docs — https://redux-toolkit.js.org/
- React docs: Managing State — https://react.dev/learn/managing-state

### Priority 2 — Orientation
- React Query: Why you don't need global state — https://tkdodo.eu/blog/
- The Twelve-Factor App — https://12factor.net/

### Priority 3 — Pattern background
- martinfowler.com: Event Sourcing and CQRS — https://martinfowler.com/

## Handoff

- Network loading and error rendering → `api-integration-frontend`.
- TypeScript state type design → `typescript-and-type-safety`.
- Re-render and memoization optimization → `web-performance-and-bundling`.
- Backend cache invalidation semantics → `backend-go-developer` / `python-developer`.
