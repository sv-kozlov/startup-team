---
name: fullstack-data-flow
description: Use when designing or implementing how data flows between the database, backend service, and React frontend — server state management with React Query or SWR, loading and error states, optimistic updates, caching strategy, backend data access (ORM, SQL, transactions), and real-time patterns (SSE, WebSocket, polling). Covers both ends of the stack as one coherent flow.
family: code
profile_level: Senior+
---

# Fullstack Data Flow

## Purpose

Design the path data takes from the database to the UI and back so loading states are explicit, errors are recoverable, cache is intentional, and mutations are safe. Treat server state and client state as separate concerns, each with its own cache invalidation and error strategy.

## Use When

- Implementing data fetching for a new feature page or component.
- Designing cache invalidation after a mutation.
- Adding optimistic updates or real-time refresh to a feature.
- Designing the backend data access layer: repository shape, transactions, query strategy.
- Choosing between polling, SSE, and WebSocket for a live data requirement.

## Do Not Use When

- The task is the API contract shape (request/response schema) → `api-contract-design`.
- The task is a database migration → `fullstack-release-and-migration`.
- The task is event-driven integration with a broker (Kafka, RabbitMQ) → `event-driven-integration`.
- The task is deep backend performance tuning under high concurrency → handoff to `backend-go-developer` or `python-developer`.

## Inputs

- User scenario: what data is needed, how often it changes, what actions mutate it.
- Existing API contract and backend data model.
- Cache requirements: how stale is acceptable? What triggers a refresh?
- Real-time requirement: does the UI need live updates? What is the acceptable latency?

## Workflow

1. Classify each data need: is this server state (owned by the API, cached locally) or pure client state (owned by the UI, no server sync)? Do not manage server state in `useState`/`useReducer` directly.
2. Choose the fetching library (React Query, SWR, or equivalent). Set `staleTime` per query — not all data ages at the same rate.
3. Define mutation strategy: optimistic update, server-confirm, or pessimistic. For optimistic: always rollback on error. For mutations with side effects on other queries, invalidate relevant query keys on success.
4. Design the backend repository shape: intention-revealing method names (`getOrdersByUser`, not generic `find`), transactions open at the service boundary, parameterized queries only.
5. For real-time: start with polling if refresh interval > 10s. Use SSE if the server pushes unidirectional events. Use WebSocket only when bidirectional real-time is required.
6. Map every API state to a UI state: loading skeleton, success, error with recovery action, empty state. Missing states are future runtime errors.
7. Handle error classification on the client: network error (retry), validation error (show inline), server error (show message + request ID), auth error (redirect).

## Outputs

- React Query / SWR query and mutation hooks with explicit types.
- Cache invalidation strategy per mutation (documented in the query key structure).
- Backend repository with named methods and service-layer transaction boundaries.
- Real-time implementation choice with rationale (polling/SSE/WebSocket).
- UI state map: loading → success → error → empty.

## Named Patterns

### Good — React Query with explicit staleTime and typed response
```typescript
// query key factory — consistent invalidation targets
export const orderKeys = {
  all: ['orders'] as const,
  byId: (id: string) => [...orderKeys.all, id] as const,
};

// typed query hook
export const useOrder = (id: string) =>
  useQuery({
    queryKey: orderKeys.byId(id),
    queryFn: (): Promise<Order> => apiClient.getOrder(id),
    staleTime: 30_000,   // 30s before considered stale
    retry: (failureCount, error) =>
      error.status !== 404 && failureCount < 2,
  });
```
Explicit staleness. Typed response. No retry on not-found.

### Bad — Server state in useState
```typescript
const [order, setOrder] = useState<Order | null>(null);
useEffect(() => {
  fetchOrder(id).then(setOrder);
}, [id]);
// No loading state. No error state. No caching. Refetches on every mount.
```

### Good — Optimistic update with rollback
```tsx
const cancelOrder = useMutation({
  mutationFn: (id: string) => apiClient.cancelOrder(id),
  onMutate: async (id) => {
    await queryClient.cancelQueries({ queryKey: orderKeys.byId(id) });
    const snapshot = queryClient.getQueryData<Order>(orderKeys.byId(id));
    queryClient.setQueryData<Order>(orderKeys.byId(id), (prev) =>
      prev ? { ...prev, status: 'cancelled' } : prev
    );
    return { snapshot };
  },
  onError: (_err, id, context) => {
    // Restore snapshot on failure
    queryClient.setQueryData(orderKeys.byId(id), context?.snapshot);
  },
  onSettled: (_, __, id) => {
    queryClient.invalidateQueries({ queryKey: orderKeys.byId(id) });
  },
});
```
The UI reflects the mutation immediately. On error, state is restored without a stale flash.

### Bad — Optimistic update without rollback
```typescript
// Set status to cancelled in local state, never roll back on error.
// User sees "cancelled" even when the API returned 409 Conflict.
```

### Good — Backend: transaction at service boundary
```typescript
// Service layer opens the transaction, not the repository
async placeOrder(input: PlaceOrderInput): Promise<Order> {
  return this.db.transaction(async (trx) => {
    const order = await this.ordersRepo.save(trx, input);
    await this.outboxRepo.insert(trx, { event: 'OrderPlaced', orderId: order.id });
    return order;
  });
}
```
Both writes succeed or both fail atomically. Outbox is inside the transaction.

### Bad — Transaction inside the repository
```typescript
// repo.save() opens its own transaction internally
// repo.outbox.insert() opens another
// Two separate transactions: order saved, outbox fails silently
```

### Good — SSE for server-push live feed
```typescript
// Backend (Express): text/event-stream with keep-alive
app.get('/v1/orders/live', (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  const unsub = bus.on('OrderUpdated', (event) => {
    res.write(`data: ${JSON.stringify(event)}\n\n`);
  });
  req.on('close', unsub);
});

// Frontend: EventSource with React
const useLiveOrders = () => {
  const queryClient = useQueryClient();
  useEffect(() => {
    const source = new EventSource('/v1/orders/live');
    source.onmessage = (e) => {
      const event = JSON.parse(e.data);
      queryClient.setQueryData(orderKeys.byId(event.orderId), event.order);
    };
    return () => source.close();
  }, [queryClient]);
};
```
Server pushes; client receives without polling. React Query cache updated in-place.

### Bad — Polling every second "to be safe"
```typescript
useQuery({ queryKey: ['orders'], queryFn: fetchOrders, refetchInterval: 1000 });
// 1 request/sec per tab × 10,000 users = server under constant load.
// SSE or 30s polling would serve the same UX.
```

## Boundaries

- Owns client-server data flow: React Query hooks, cache strategy, backend repository, real-time choice.
- Does not own the API contract schema → `api-contract-design`.
- Does not own database migrations → `fullstack-release-and-migration`.
- Does not own deep backend performance (connection pool tuning, query plan analysis under heavy load) → `backend-go-developer` / `python-developer`.
- Does not own broker-based event streams (Kafka, NATS) → `event-driven-integration`.

## Sources

### Priority 1 — Data fetching and backend canon
- TanStack Query (React Query) Documentation — https://tanstack.com/query/latest
- React Documentation (state and effects) — https://react.dev/
- MDN Web Docs — https://developer.mozilla.org/
- PostgreSQL Documentation — https://www.postgresql.org/docs/

### Priority 2 — Patterns and best practices
- TkDodo's Blog (React Query patterns) — https://tkdodo.eu/blog/
- Node.js Best Practices — https://github.com/goldbergyoni/nodebestpractices
- The Twelve-Factor App — https://12factor.net/

### Priority 3 — Background
- martinfowler.com on data patterns — https://martinfowler.com/
- web.dev — https://web.dev/

## Handoff

- API contract schema and wire format → `api-contract-design`.
- Schema migrations and zero-downtime rollout → `fullstack-release-and-migration`.
- Broker-based event-driven integration (Kafka, NATS) → `event-driven-integration`.
- Deep backend performance and concurrency → `backend-go-developer` / `python-developer`.
- Database cluster operations and HA → `devops-sre`.
