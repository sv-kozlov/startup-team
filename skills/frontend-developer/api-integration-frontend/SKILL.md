---
name: api-integration-frontend
description: Use when integrating a React application with a backend API — setting up an HTTP client, handling loading/error/empty/success states, implementing error boundaries and Suspense, managing authentication flows (JWT, OAuth, cookie refresh), validating API response shapes, and applying client-side security practices.
family: code
profile_level: Senior+
---

# API Integration — Frontend

## Purpose

Make API integration robust: every fetch path has a loading branch, every error has a recovery path, and malformed server responses surface immediately rather than propagating as silent undefined-access failures. Make auth flows correct: tokens are refreshed transparently, session expiry is handled gracefully, and sensitive data is not exposed to scripts.

## Use When

- Adding a new API call with loading, error, and empty state handling.
- Setting up or refactoring the HTTP client (Axios, fetch wrapper, or generated client).
- Implementing authentication: JWT storage, refresh token cycle, OAuth PKCE flow.
- Adding an error boundary around a route or feature.
- Reviewing a component that calls an API inline without state handling.

## Do Not Use When

- The task is state library selection and cache strategy → `state-management-and-data-flow`.
- The task is API contract design on the server side → `backend-go-developer` / `python-developer`.
- The task is performance of the data fetch (staleTime, background refresh) → `state-management-and-data-flow`.
- The task is e2e or component testing of the integration → `frontend-testing`.

## Inputs

- API contract: OpenAPI spec, documented endpoint, or backend code.
- Auth method: JWT, OAuth 2.0 (PKCE), cookie-based session, API key.
- Error response shape from the backend.
- Relevant UI screens and their loading/error/empty expectations.

## Workflow

1. Define the HTTP client once: base URL, default headers, interceptors for auth token injection and 401 refresh. Do not create per-component fetch calls.
2. Generate or write typed API functions that return `Promise<T>`. Validate the response shape with Zod at the boundary — never return `as T`.
3. Use React Query or SWR for data-fetching hooks. The component receives `{ data, isLoading, error }` and renders all three branches. An `isLoading` without a `data` branch is incomplete.
4. Wrap every significant route or feature in an `<ErrorBoundary>`. The boundary catches render-phase errors and unexpected runtime exceptions from resolved data shapes. Provide a meaningful fallback with a retry action.
5. Use `<Suspense>` for deferred data loading. Colocate `Suspense` boundaries with the component that triggers the fetch, not at the top of the tree.
6. For auth:
   - Store access tokens in memory (not `localStorage`) when possible. Use `HttpOnly` cookies for refresh tokens.
   - Implement silent refresh: if a request returns 401, refresh the access token and replay the original request exactly once.
   - Handle session expiry globally in the HTTP client interceptor; redirect to login without leaking the destination.
7. Apply client-side security: no sensitive data in query params (URLs are logged), no secrets in JS bundles (env vars for build-time config, not runtime secrets), Content Security Policy headers, sanitize any server-rendered HTML.

## Outputs

- Typed API client module with interceptors and Zod validation.
- Query hooks with loading/error/empty handling for each data domain.
- Error boundaries at route and feature level.
- Auth flow implementation: token storage, refresh cycle, session expiry handling.

## Named Patterns

### Good — Typed HTTP client with interceptor
```ts
// lib/http.ts
const http = axios.create({ baseURL: process.env.NEXT_PUBLIC_API_URL });

http.interceptors.request.use(config => {
  const token = authStore.getState().accessToken;
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

http.interceptors.response.use(
  res => res,
  async error => {
    if (error.response?.status === 401 && !error.config._retry) {
      error.config._retry = true;
      await authStore.getState().refreshTokens();
      return http(error.config);
    }
    return Promise.reject(error);
  },
);
```
Single entry point for auth; refresh is transparent to all callers.

### Bad — Per-component fetch with manual token
```tsx
export function OrderList() {
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    fetch('/api/orders', { headers: { Authorization: `Bearer ${token}` } })
      .then(r => r.json())
      .then(setOrders);
  }, []);
}
```
Token access scattered; no refresh; no error handling; no loading state.

### Good — Complete loading/error/empty/success cycle
```tsx
export function OrderList({ filter }: { filter: OrderFilter }) {
  const { data, isLoading, error } = useOrderList(filter);

  if (isLoading) return <OrderListSkeleton />;
  if (error)     return <ApiErrorState error={error} onRetry={refetch} />;
  if (!data?.length) return <EmptyState label="No orders yet" />;

  return (
    <ul>
      {data.map(order => <OrderRow key={order.id} order={order} />)}
    </ul>
  );
}
```
All four UI states are handled. The user always sees a meaningful interface.

### Bad — Missing loading and error branches
```tsx
export function OrderList({ filter }: { filter: OrderFilter }) {
  const { data } = useOrderList(filter);
  return <ul>{data?.map(o => <OrderRow key={o.id} order={o} />)}</ul>;
}
```
If `data` is undefined during loading, nothing renders. If the request fails, nothing renders. If `data` is an empty array, nothing renders — user cannot distinguish these three states.

### Good — Error boundary with retry
```tsx
export function OrdersFeature() {
  return (
    <ErrorBoundary
      fallback={({ error, reset }) => (
        <FeatureErrorFallback message={error.message} onRetry={reset} />
      )}
    >
      <Suspense fallback={<OrderListSkeleton />}>
        <OrderList filter={defaultFilter} />
      </Suspense>
    </ErrorBoundary>
  );
}
```
Runtime and render errors are caught at the feature boundary; the rest of the page is unaffected.

### Bad — No error boundary
```tsx
export function OrdersPage() {
  return <OrderList filter={defaultFilter} />;
}
```
An unhandled runtime error in `OrderList` unmounts the entire React tree.

### Good — Zod validation at fetch boundary
```ts
export async function fetchOrder(id: string): Promise<Order> {
  const { data } = await http.get(`/orders/${id}`);
  return OrderSchema.parse(data); // ZodError → caught by React Query → error state
}
```

### Bad — Silent type assertion
```ts
export async function fetchOrder(id: string): Promise<Order> {
  const { data } = await http.get(`/orders/${id}`);
  return data as Order; // shape not verified; undefined fields propagate to UI
}
```

## Boundaries

- Owns loading/error/empty handling, auth flows, and API client setup on the client side.
- Does not own API contract design on the server — that is `backend-go-developer` / `python-developer`.
- Does not own state caching and invalidation strategy — that is `state-management-and-data-flow`.
- Does not own infrastructure-level security (CORS, CSP headers config in server) — that is `devops-sre`.

## Sources

### Priority 1 — React and HTTP canon
- React docs: Synchronizing with Effects — https://react.dev/learn/synchronizing-with-effects
- React Query docs — https://tanstack.com/query/latest
- MDN: Fetch API — https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API

### Priority 2 — Security and auth
- OWASP Frontend Security Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/
- OAuth 2.0 / OIDC — https://oauth.net/2/
- RFC 6749 OAuth 2.0 — https://www.rfc-editor.org/rfc/rfc6749

### Priority 3 — Pattern background
- martinfowler.com: Backend for Frontend — https://martinfowler.com/articles/gateway-offloading.html

## Handoff

- API contract design on the server side → `backend-go-developer` / `python-developer`.
- System-level requirements behind the API → `system-analyst`.
- State caching and invalidation → `state-management-and-data-flow`.
- Auth service setup and token issuance → `devops-sre` / `system-architect`.
- E2e testing of auth flows → `frontend-testing`.
