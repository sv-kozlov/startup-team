---
name: event-driven-integration
description: Use when a fullstack feature requires asynchronous integration — consuming from a message queue, handling a webhook, pushing live updates to the browser via SSE or WebSocket, or implementing client-side async stream handling. Fullstack focus: how asynchronous events reach the UI and how the client manages async state. For deep broker cluster design (Kafka partitioning, NATS JetStream), route to backend-go-developer or python-developer.
family: method
profile_level: Senior+
---

# Event-Driven Integration (Fullstack)

## Purpose

Connect a fullstack feature to asynchronous event sources so the UI reflects real-time or near-real-time state without polling, the backend handles events idempotently, and failures on the async path are observable and recoverable.

## Use When

- A feature requires live updates in the UI (order status changes, notifications, collaborative edits).
- A backend endpoint needs to consume from a queue (webhook handler, job queue consumer).
- Choosing between SSE, WebSocket, polling, and a broker for a real-time requirement.
- Implementing client-side error handling for an async stream.
- Adding an outbox to make event emission transactionally safe.

## Do Not Use When

- The task is synchronous API contract design → `api-contract-design`.
- The task is choosing the broker platform or configuring the cluster → `devops-sre` / `backend-go-developer`.
- The task is deep Kafka partitioning, consumer group strategy, or NATS JetStream → `backend-go-developer` / `python-developer`.
- The task is batch data pipelines → `data-engineer`.

## Inputs

- Real-time requirement: what changes, how often, what latency is acceptable.
- Event producer: is it the same service or an external system?
- Failure behavior: what happens when the client loses the stream? What happens when a handler fails?
- Existing infrastructure: is there a broker in the stack? Is SSE already used?

## Workflow

1. **Choose the real-time mechanism** for the frontend:
   - **Polling** (interval > 10s, low event frequency, no real-time SLA) — start here; change when needed.
   - **SSE** (server pushes unidirectional events; browser auto-reconnects; works over HTTP/1.1 and HTTP/2) — default for live feeds.
   - **WebSocket** (bidirectional; needed for collaborative or chat-like features) — only when SSE is insufficient.
   - **Queue consumer** (backend-only; frontend gets state via REST + SSE after the job completes).
2. **Design the backend event handler.** For webhook or queue consumer: validate the event signature, check idempotency key, process the business logic, emit a downstream event or update the DB.
3. **Make handlers idempotent.** Store the event ID or idempotency key before processing. If the event is seen again, return the stored result without re-processing side effects.
4. **Add outbox for transactional event emission.** If the backend must emit an event AND write to the DB atomically, use the outbox pattern: insert the event into an `outbox` table in the same transaction as the DB write. A relay process publishes from the outbox.
5. **Handle client-side stream failure.** SSE: the browser `EventSource` auto-reconnects; handle `reconnect` events and reconcile state. WebSocket: implement exponential backoff reconnect; replay missed events from the REST API.
6. **Update the React Query cache on incoming events.** SSE/WebSocket events should call `queryClient.setQueryData` or `queryClient.invalidateQueries` — not trigger a full page reload.
7. **Instrument the async path.** Add trace spans on the handler, log the event ID, and track consumer lag if using a broker.

## Outputs

- Real-time mechanism decision with rationale (polling/SSE/WebSocket).
- Idempotent event handler with idempotency key storage.
- Outbox pattern implementation if transactional event emission is required.
- Client-side stream management with reconnection and state reconciliation.
- React Query cache update strategy on incoming events.
- Observability: handler trace span, event ID in logs, consumer lag metric.

## Named Patterns

### Good — SSE for server-pushed live feed
```typescript
// Backend (Express/Fastify): stream events over text/event-stream
app.get('/v1/orders/events', authenticateUser, (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  const listener = (event: OrderEvent) => {
    if (event.userId === req.user.id) {
      res.write(`id: ${event.id}\ndata: ${JSON.stringify(event)}\n\n`);
    }
  };

  eventBus.on('OrderUpdated', listener);
  req.on('close', () => eventBus.off('OrderUpdated', listener));
});

// Frontend: React hook with EventSource
const useOrderEvents = () => {
  const queryClient = useQueryClient();
  useEffect(() => {
    const source = new EventSource('/v1/orders/events');
    source.onmessage = ({ data }) => {
      const event: OrderEvent = JSON.parse(data);
      queryClient.setQueryData<Order>(orderKeys.byId(event.orderId), (prev) =>
        prev ? { ...prev, status: event.status } : prev
      );
    };
    source.onerror = () => source.close(); // let browser auto-reconnect after close
    return () => source.close();
  }, [queryClient]);
};
```
Server pushes per-user events. Client updates the React Query cache in-place. No full refetch on every event.

### Bad — Polling every second
```typescript
useQuery({
  queryKey: ['orders'],
  queryFn: fetchAllOrders,
  refetchInterval: 1_000,
});
// 1 request/s per active tab. 5,000 users = 5,000 req/s for order list.
// SSE would serve the same UX with one long-lived connection per user.
```

### Good — Idempotent webhook handler
```typescript
app.post('/webhooks/payment', async (req, res) => {
  const eventId = req.headers['x-event-id'] as string;

  // Check if already processed
  const existing = await db('processed_events').where({ event_id: eventId }).first();
  if (existing) {
    return res.status(200).json({ status: 'already_processed' });
  }

  await db.transaction(async (trx) => {
    await trx('processed_events').insert({ event_id: eventId, processed_at: new Date() });
    await paymentService.applyPaymentConfirmed(trx, req.body);
  });

  res.status(200).json({ status: 'ok' });
});
```
The same webhook can arrive multiple times (network retry, provider bug). Only the first call has side effects.

### Bad — Non-idempotent webhook
```typescript
app.post('/webhooks/payment', async (req, res) => {
  await paymentService.applyPaymentConfirmed(req.body);
  res.status(200).json({ status: 'ok' });
});
// Provider retries on timeout → double charge, duplicate order, double inventory decrement.
```

### Good — Outbox for transactional event emission
```typescript
await db.transaction(async (trx) => {
  const order = await trx('orders').insert(orderData).returning('*');
  await trx('outbox').insert({
    aggregate_id: order[0].id,
    event_type: 'OrderPlaced',
    payload: JSON.stringify({ orderId: order[0].id }),
    created_at: new Date(),
  });
  // Both writes succeed or both fail. The relay publishes the outbox row to the broker.
});
```
No event is lost. No event is emitted for a DB write that was rolled back.

### Bad — Emit event before DB commit
```typescript
await orderRepo.save(orderData);
await eventBus.publish('OrderPlaced', { orderId }); // DB write might fail after this
await db.commit();
```
If commit fails after the event is published, consumers act on an order that does not exist.

## Boundaries

- Owns real-time mechanism selection, client-side stream management, idempotent handlers, and outbox implementation for a feature.
- Does not own broker cluster setup (Kafka, NATS), consumer group configuration, or topic partitioning → `devops-sre` / `backend-go-developer`.
- Does not own synchronous API contract → `api-contract-design`.
- Does not own batch data pipelines or data lake ingestion → `data-engineer`.
- Does not own deep Go/Python async runtime and performance tuning → `backend-go-developer` / `python-developer`.

## Sources

### Priority 1 — Protocol and standard canon
- MDN: Server-Sent Events — https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events
- MDN: WebSocket API — https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API
- RFC 9110 HTTP Semantics — https://www.rfc-editor.org/rfc/rfc9110

### Priority 2 — Integration patterns
- martinfowler.com: Transactional Outbox Pattern — https://microservices.io/patterns/data/transactional-outbox.html
- The Twelve-Factor App — https://12factor.net/
- TanStack Query: SSE integration — https://tanstack.com/query/latest

### Priority 3 — Background
- microservices.io patterns — https://microservices.io/patterns/
- web.dev — https://web.dev/

## Handoff

- Broker cluster configuration (Kafka, NATS, RabbitMQ) → `devops-sre`.
- Deep Kafka partitioning, consumer group strategy → `backend-go-developer` / `python-developer`.
- Batch pipeline and data lake ingestion → `data-engineer`.
- API contract for the synchronous layer alongside events → `api-contract-design`.
- Real-time infrastructure (WebSocket server scaling, connection limits) → `devops-sre`.
