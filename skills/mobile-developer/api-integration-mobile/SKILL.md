---
name: api-integration-mobile
description: Use when integrating a mobile application with a backend REST, gRPC, or WebSocket API — implementing the network client, retry/backoff, token refresh, error handling for mobile network conditions, request serialization, and negotiating mobile-friendly contract shape with the backend team.
family: code
profile_level: Senior+
---

# API Integration — Mobile

## Purpose

Connect the mobile application to backend APIs reliably under mobile network conditions: intermittent connectivity, high latency, battery constraints, and long-lived sessions with expiring tokens. The client handles all unhappy paths explicitly; the UI never shows a raw HTTP error code to the user.

## Use When

- Implementing a Retrofit / URLSession / Ktor client for a REST or gRPC backend.
- Adding retry logic, exponential backoff, or circuit breaker for unstable endpoints.
- Implementing token refresh (OAuth2, JWT) transparently without logging the user out on 401.
- Designing the mobile-side error handling: distinguishing network error, server error, and domain error.
- Negotiating API contract shape with backend (pagination, field selection, error envelope) for mobile-friendly consumption.
- Adding WebSocket connection with reconnect on mobile network change.

## Do Not Use When

- The task is about local data storage after receiving the response → `mobile-data-and-offline`.
- The task is about server-side API contract ownership → handoff to `backend-developers` / `system-analyst`.
- The task is about overall app architecture and repository layer → `mobile-app-architecture`.
- The task is about observability and analytics instrumentation → `mobile-observability`.

## Inputs

- OpenAPI spec or backend team's API documentation.
- Authentication flow: OAuth2, API key, certificate-based.
- Network error taxonomy: what is retryable, what is permanent, what maps to a user-facing message.
- Platform target: Android (Retrofit + OkHttp + Kotlin Coroutines) or iOS (URLSession + async/await) or cross-platform (Ktor).

## Workflow

1. Define the error taxonomy before writing any client code. Classify: `NetworkError` (no connectivity), `HttpError` (4xx/5xx), `DomainError` (parsed business error from body), `UnknownError`.
2. Implement the HTTP client with a single instance (singleton pattern). Android: OkHttp client with interceptors; configure timeouts (connect 10 s, read 30 s, write 30 s). iOS: URLSession with URLSessionConfiguration.
3. Add the authentication interceptor / adapter. On 401, suspend the request, refresh the token using a mutex (one refresh at a time), retry the original request once. Do not refresh in parallel.
4. Add retry with exponential backoff for idempotent requests (GET, HEAD, PUT with idempotency key). Limit to 3 retries; jitter the delay to avoid thundering herd.
5. Map HTTP responses to domain models at the repository boundary. Never leak `Response<T>` or `HttpException` into the domain layer.
6. For WebSocket: implement reconnect on `onFailure` using exponential backoff; track network state changes with `ConnectivityManager` (Android) / `NWPathMonitor` (iOS).
7. Validate the contract shape with the backend team before implementation: pagination style (cursor vs offset), error envelope (`{ "error": { "code": ..., "message": ... } }`), required vs optional fields for mobile.

## Outputs

- HTTP/gRPC/WebSocket client with singleton lifecycle management.
- Token refresh interceptor.
- Error taxonomy sealed class / enum.
- Repository data source implementation.
- Contract negotiation notes or ADR (if contract shape changed for mobile).

## Named Patterns

### Good — Token refresh with mutex (Android/Kotlin)
```kotlin
class AuthInterceptor(private val tokenStorage: TokenStorage, private val authApi: AuthApi) : Interceptor {
    private val refreshMutex = Mutex()

    override fun intercept(chain: Interceptor.Chain): Response {
        val response = chain.proceed(chain.request().withBearerToken(tokenStorage.accessToken))
        if (response.code != 401) return response

        val newToken = runBlocking {
            refreshMutex.withLock {
                // Another coroutine may have already refreshed; check again
                if (tokenStorage.isAccessTokenValid()) return@withLock tokenStorage.accessToken
                authApi.refresh(tokenStorage.refreshToken).also { tokenStorage.save(it) }
            }
        }
        return chain.proceed(chain.request().withBearerToken(newToken))
    }
}
```

### Bad — Parallel token refresh
```kotlin
// Anti-pattern: every 401 triggers its own refresh without coordination
if (response.code == 401) {
    val newToken = authApi.refresh(tokenStorage.refreshToken) // called N times in parallel
    tokenStorage.save(newToken)
}
```
Refresh token is single-use; parallel refresh invalidates all but the last response and logs the user out.

### Good — Sealed error taxonomy
```kotlin
sealed class ApiResult<out T> {
    data class Success<T>(val data: T) : ApiResult<T>()
    sealed class Failure : ApiResult<Nothing>() {
        data class Network(val cause: IOException) : Failure()
        data class Http(val code: Int, val errorBody: String?) : Failure()
        data class Domain(val code: String, val message: String) : Failure()
        data object Unknown : Failure()
    }
}
```

### Bad — Catching Throwable and returning null
```kotlin
suspend fun fetchOrders(): List<Order>? = try {
    api.getOrders().body()
} catch (e: Throwable) { null } // caller cannot distinguish network error from empty body
```

### Good — iOS token refresh with actor
```swift
actor TokenRefresher {
    private var refreshTask: Task<String, Error>?

    func validToken(using authService: AuthService, storage: TokenStorage) async throws -> String {
        if storage.isAccessTokenValid() { return storage.accessToken }
        if let task = refreshTask { return try await task.value }
        let task = Task { try await authService.refresh(storage.refreshToken) }
        refreshTask = task
        defer { refreshTask = nil }
        let token = try await task.value
        storage.save(token)
        return token
    }
}
```

### Bad — Retry without jitter
```swift
for attempt in 1...3 {
    do { return try await fetchOrders() }
    catch { try await Task.sleep(nanoseconds: UInt64(attempt) * 1_000_000_000) } // no jitter
}
```
All clients retry simultaneously after the same delay; server receives a spike.

## Boundaries

- Owns client-side HTTP/gRPC/WebSocket implementation and mobile-specific network handling.
- Does not own server-side API contract ownership → `backend-developers`.
- Does not own API contract specification from requirements → `system-analyst`.
- Does not own local data storage after receiving response → `mobile-data-and-offline`.

## Sources

### Priority 1 — Platform canon
- OkHttp documentation — https://square.github.io/okhttp/
- Retrofit documentation — https://square.github.io/retrofit/
- URLSession (Apple) — https://developer.apple.com/documentation/foundation/urlsession
- Swift Concurrency (async/await) — https://docs.swift.org/swift-book/documentation/the-swift-programming-language/concurrency/
- Ktor HTTP Client — https://ktor.io/docs/client-create-new-application.html

### Priority 2 — Standards
- OpenAPI Specification 3.1 — https://spec.openapis.org/oas/v3.1.0
- RFC 7807 (Problem Details for HTTP APIs) — https://www.rfc-editor.org/rfc/rfc7807
- OWASP MASVS — https://mas.owasp.org/MASVS/

### Priority 3 — Patterns
- Exponential backoff and jitter (AWS) — https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/

## Handoff

- Server-side API ownership and contract design → `backend-developers` / `system-analyst`.
- Local storage after receiving response → `mobile-data-and-offline`.
- Observability and network error tracking → `mobile-observability`.
- Architecture and repository layer shape → `mobile-app-architecture`.
