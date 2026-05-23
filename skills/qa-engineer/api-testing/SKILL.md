---
name: api-testing
description: Use when designing, executing, or validating API tests — REST/gRPC/WebSocket contract verification, schema validation, negative and boundary API checks, consumer-driven contract testing, and mock service setup. Owned by QA; API contract authorship belongs to system-analyst.
family: code
profile_level: Senior+
---

# API Testing

## Purpose

Verify that API contracts behave as specified across valid inputs, invalid inputs, boundary conditions, error
scenarios, and integration sequences. Catch contract violations, schema drift, and broken error handling before
they reach the UI layer or downstream consumers. Provide fast, stable, and reproducible API-level feedback
that does not require a full e2e stack.

## Use When

- A new API endpoint or changed contract needs verification before UI integration.
- Validating that error codes, error bodies, and HTTP status codes match the specification.
- Verifying async API behavior: webhooks, polling, long-running operations.
- Setting up consumer-driven contract tests between services.
- Replacing unstable e2e tests with faster API-level coverage.
- Validating API security: authentication, authorization, input validation at the API layer.

## Do Not Use When

- The API contract itself needs to be authored or changed -> `system-analyst`.
- Full user journey through the browser is required -> `test-automation-framework` (e2e).
- Performance under load is the goal -> `performance-and-load-testing`.
- CI/CD pipeline integration for the test suite -> `ci-cd-test-integration`.

## Inputs

- API specification: OpenAPI 3.x document, protobuf schema, or equivalent.
- Acceptance criteria for the endpoint: expected status codes, response bodies, error codes.
- Authentication mechanism: API key, OAuth2 token, JWT, mTLS.
- Test environment base URL and any required test data preconditions.
- Known edge cases from system analyst or defect history.

## Workflow

1. Read the API specification before writing any test. Identify: endpoints, methods, required and optional
   parameters, response schemas, error codes, and documented constraints. Flag untestable or ambiguous
   specifications to system-analyst before proceeding.

2. Classify tests by scenario type:
   - Happy path: valid input, expected 2xx response, correct body schema.
   - Negative: invalid input types, missing required fields, constraint violations -> expected 4xx.
   - Boundary: edge values for numeric/string fields per the spec.
   - Authentication: unauthenticated request, expired token, insufficient permissions.
   - Error handling: downstream service failure simulation, timeout behavior.
   - Idempotency: repeated identical requests produce same result (for PUT, DELETE, POST with idempotency key).

3. Design the test structure. Each test is independent: sets up its own data, makes the request,
   asserts the response, and cleans up. Tests do not rely on execution order.

4. Assert at multiple levels for each response:
   - HTTP status code.
   - Response body schema (validate against OpenAPI schema or JSON Schema).
   - Business-meaningful field values (not just "field exists" but "field has the correct value").
   - Response headers where specified (Content-Type, Location for 201, etc.).
   - Timing: for latency-sensitive paths, assert response time is within budget.

5. Set up mock services for dependencies that are not under test. Use WireMock, Mockoon, or language-native
   HTTP stubs. Mocks must match the real service's contract (schema-backed mocks, not arbitrary stubs).

6. Implement consumer-driven contract tests where services communicate. Consumer writes the expected
   contract; provider verifies it. Tools: Pact framework or schema-backed validation.

7. Validate error response bodies for structure. A valid error response is not just a 4xx status.
   It has a consistent error schema: error code, message, and details (RFC 7807 Problem Details or
   the team's equivalent). Assert all three, not just the status code.

8. Document test cases with traceability to API specification sections. When the spec changes,
   it must be visible which tests need updating.

## Outputs

- API test suite covering happy path, negative, boundary, auth, and error scenarios.
- Schema validation assertions linked to the OpenAPI document.
- Mock service configuration files for dependency isolation.
- Consumer contract files (Pact or equivalent) where applicable.
- Test coverage report: endpoints covered, scenario types per endpoint.
- Open questions for system analyst on ambiguous or untestable spec sections.

## Named Patterns

### Good — Structured API test with full assertion

```python
# pytest + requests style
def test_create_order_returns_201_with_location(api_client, auth_token, seeded_product):
    payload = {
        "product_id": seeded_product.id,
        "quantity": 2,
        "idempotency_key": str(uuid4())
    }
    response = api_client.post(
        "/orders",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 201
    body = response.json()
    assert "id" in body
    assert body["status"] == "pending"
    assert body["quantity"] == 2
    assert "Location" in response.headers
    # schema validation
    validate(body, schema=ORDER_SCHEMA)   # jsonschema or equivalent
```

Status code, body values, header, and schema are all asserted. One test, one scenario.

### Bad — Testing only status code

```python
response = requests.post("/orders", json=payload)
assert response.status_code == 201
```

Schema drift, missing Location header, wrong status field — all pass undetected.

### Good — Negative test with error body assertion

```python
def test_create_order_returns_422_when_quantity_zero(api_client, auth_token, seeded_product):
    payload = {"product_id": seeded_product.id, "quantity": 0}
    response = api_client.post("/orders", json=payload,
                               headers={"Authorization": f"Bearer {auth_token}"})

    assert response.status_code == 422
    error = response.json()
    assert error["code"] == "INVALID_QUANTITY"
    assert "quantity" in error["detail"]   # field-level error reference
```

The error structure is verified, not just the status code. Regression catches changes to error codes.

### Bad — Accepting any 4xx as success

```python
response = requests.post("/orders", json={"quantity": 0})
assert response.status_code >= 400  # "it errored, good"
```

A 500 Internal Server Error also passes this assertion. A changed error code is not detected.

### Good — Schema-backed mock matching the real contract

```yaml
# WireMock stub for payment service
{
  "request": {
    "method": "POST",
    "url": "/payments/charge",
    "bodyPatterns": [{"matchesJsonPath": "$.amount"}]
  },
  "response": {
    "status": 200,
    "jsonBody": {
      "transaction_id": "txn_test_001",
      "status": "approved"
    },
    "headers": {"Content-Type": "application/json"}
  }
}
```

The stub response matches the OpenAPI schema for the payment service. When the real contract changes,
the stub is updated alongside the spec.

### Bad — Arbitrary stub with invented response shape

```python
mock.return_value = {"ok": True, "data": 42}
```

The stub does not match the real contract. Tests pass; integration fails because the real service
returns `{"status": "approved", "transaction_id": "..."}`.

### Good — Consumer-driven contract test (Pact style)

```python
# Consumer (order service) defines what it expects from payment service
pact = Consumer("order-service").has_pact_with(Provider("payment-service"))

pact.given("payment service is available") \
    .upon_receiving("a charge request") \
    .with_request(method="POST", path="/payments/charge",
                  body={"amount": 5000, "currency": "USD"}) \
    .will_respond_with(status=200,
                       body={"transaction_id": Like("txn_123"), "status": "approved"})
```

Payment service CI runs the pact and verifies it can fulfill the consumer's contract.
Breakage detected before deployment, not in production.

### Bad — No contract test between services

Services evolve independently. Order service assumes `transaction_id` in the response.
Payment service renames it to `txn_ref`. Integration breaks in production.

### Good — Idempotency test

```python
def test_create_order_idempotent(api_client, auth_token, seeded_product):
    idem_key = str(uuid4())
    payload = {"product_id": seeded_product.id, "quantity": 1, "idempotency_key": idem_key}

    r1 = api_client.post("/orders", json=payload, headers={"Authorization": f"Bearer {auth_token}"})
    r2 = api_client.post("/orders", json=payload, headers={"Authorization": f"Bearer {auth_token}"})

    assert r1.status_code == 201
    assert r2.status_code == 200      # or 201 depending on spec; key: same order id
    assert r1.json()["id"] == r2.json()["id"]   # same resource, not duplicated
```

Duplicate request does not create a second order.

### Bad — No idempotency test

The API claims idempotency support but it is never tested. A retry storm in production
creates duplicate charges. QA did not cover it because "it looked obvious."

## Boundaries

- Owns API test design, execution, schema validation, and mock configuration.
- Does not own API contract authorship (OpenAPI spec, protobuf definition) -> `system-analyst`.
- Does not own full browser-based e2e tests -> `test-automation-framework`.
- Does not own performance testing of the API -> `performance-and-load-testing`.
- Does not own the security pen-testing program -> `security-engineer` (QA may add OWASP-scope checks).

## Sources

### Priority 1 — Standards and tool documentation

- Postman Learning Center — https://learning.postman.com/
- OpenAPI Specification 3.1 — https://spec.openapis.org/oas/v3.1.0
- Pact consumer-driven contract testing — https://docs.pact.io/
- WireMock documentation — https://wiremock.org/docs/
- OWASP Testing Guide v4.2: API Testing section — https://owasp.org/www-project-web-security-testing-guide/
- RFC 7807: Problem Details for HTTP APIs — https://www.rfc-editor.org/rfc/rfc7807
- gRPC Core Concepts — https://grpc.io/docs/what-is-grpc/core-concepts/

### Priority 2 — Orientation

- ISTQB CTFL v4.0: API Testing chapter — https://www.istqb.org/certifications/certified-tester-foundation-level
- REST Assured documentation — https://rest-assured.io/
- pytest-httpx and responses libraries (Python) — https://pypi.org/project/pytest-httpx/
- JSON Schema specification — https://json-schema.org/

### Priority 3 — Background

- Martin Fowler: Contract Tests — https://martinfowler.com/bliki/ContractTest.html
- Google Testing Blog — https://testing.googleblog.com/

## Handoff

- API specification is ambiguous or missing -> `system-analyst` with specific questions.
- Performance testing of the API under load -> `performance-and-load-testing`.
- E2E test covering the API through the browser -> `test-automation-framework`.
- CI/CD pipeline integration for API tests -> `ci-cd-test-integration`.
- Security-specific API penetration testing -> `security-engineer`.
