---
name: api-contract-design
description: Role-specific addendum for api-contract-design in the Python Developer context. Use shared-api-contract-design for the full method. This file contains Python/FastAPI-specific code examples and implementation constraints.
family: method
profile_level: Senior+
superseded_by: shared-api-contract-design
---

# API Contract Design — Python Addendum

> **Primary skill:** `shared-api-contract-design` at `skills/shared/shared-api-contract-design/SKILL.md`.
> This file is a role-specific addendum. Follow the shared skill's Workflow and apply the Python-specific constraints below.

## Python Implementation Constraints

Apply these in addition to the shared skill's Workflow:

1. **FastAPI: Pydantic v2 models are the schema source.** FastAPI generates OpenAPI from them. Do not maintain a separate `openapi.yaml` by hand when using FastAPI — generate it from the app on CI and commit as an artifact.
2. **Run `oasdiff breaking` in CI** on every PR that changes the generated OpenAPI artifact. For gRPC, run `buf breaking`.
3. **One exception handler for RFC 7807.** Register a single `@app.exception_handler(DomainError)` that maps the exception hierarchy to RFC 7807 JSON. Never return different error shapes from different routes.
4. **`Idempotency-Key` middleware.** Extract the key in a Starlette middleware; check/store in Redis; return `409 Conflict` while processing; return cached response when complete.
5. **gRPC Python error codes** — map domain errors to `grpc.StatusCode` in a dedicated mapper; never raise `StatusCode.UNKNOWN` for a business error.

## Python-Specific Named Patterns

### Good — Pydantic v2 models as schema source (FastAPI)
```python
from fastapi import APIRouter, Header, Depends, status
from pydantic import BaseModel, UUID4
from decimal import Decimal

router = APIRouter(prefix="/v1/orders")

class PlaceOrderRequest(BaseModel):
    items: list[str]
    currency: str
    total: Decimal

class OrderResponse(BaseModel):
    id: UUID4
    status: str
    total: Decimal

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def place_order(
    body: PlaceOrderRequest,
    idempotency_key: str = Header(...),
    service: OrderService = Depends(get_order_service),
) -> OrderResponse:
    order = await service.place(body, idempotency_key)
    return OrderResponse.model_validate(order)
```
OpenAPI is generated from Pydantic models; no schema drift; types validated at request time.

### Bad — Handwritten schema alongside FastAPI models
```python
# DO NOT maintain docs/openapi.yaml manually when using FastAPI
# FastAPI auto-generates it; manual sync always drifts
```

### Good — RFC 7807 unified exception handler
```python
from fastapi import Request
from fastapi.responses import JSONResponse

_STATUS_MAP: dict[type[DomainError], int] = {
    InsufficientFundsError: 422,
    OrderNotFoundError: 404,
    OrderAlreadyCancelledError: 409,
}

@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
    status_code = _STATUS_MAP.get(type(exc), 400)
    return JSONResponse(
        status_code=status_code,
        content={
            "type": f"https://api.example.com/errors/{exc.__class__.__name__}",
            "title": exc.__class__.__name__,
            "status": status_code,
            "detail": str(exc),
            "instance": str(request.url),
        },
    )
```
One shape, one parser for all clients.

### Bad — Per-route error shapes
```python
@router.post("/orders")
async def place_order():
    raise HTTPException(detail="something went wrong")  # plain string

@router.get("/orders/{id}")
async def get_order():
    return {"message": "not found", "code": 404}  # different shape
```
Clients write multiple error parsers; QA cannot write shared error-handling tests.

### Good — gRPC Python domain error mapping
```python
import grpc

_GRPC_STATUS_MAP = {
    InsufficientFundsError: grpc.StatusCode.FAILED_PRECONDITION,
    OrderNotFoundError: grpc.StatusCode.NOT_FOUND,
}

def map_domain_err(err: Exception) -> grpc.RpcError:
    code = _GRPC_STATUS_MAP.get(type(err), grpc.StatusCode.INTERNAL)
    context.abort(code, str(err))
```

## Handoff

- Requirements behind the contract → `system-analyst` (`shared-api-contract-design`, System Analyst mode).
- Platform-wide API style guide → `tech-lead` / `system-architect`.
- Client-side contract consumption → `frontend-developer` / `mobile-developer`.
- Event/message schemas → `event-driven-integration`.
