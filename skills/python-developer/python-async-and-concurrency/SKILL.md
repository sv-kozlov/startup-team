---
name: python-async-and-concurrency
description: Use when adding or reviewing async tasks, event loop usage, graceful shutdown of a Python service, TaskGroup lifecycle, or CPU-bound offloading. Covers async/await patterns, asyncio.TaskGroup ownership, CancelledError handling, resource management via async context managers, and safe offloading of blocking work.
family: code
profile_level: Senior+
---

# Python Async and Concurrency

## Purpose

Make async code correct, cancellation-safe, and understandable. Ensure every coroutine has an owner, every resource is released on exit, and CPU-bound work never blocks the event loop.

## Use When

- Adding or reviewing `async def` functions, coroutines, or background tasks.
- Designing graceful shutdown for a FastAPI or aiohttp service.
- Offloading CPU-bound or blocking-I/O work from the event loop.
- Debugging suspected event loop stalls, slow endpoints, or leaked tasks.

## Do Not Use When

- The task is service package structure → `python-service-design`.
- The task is data layer query optimization → `data-layer-python`.
- The task is message broker consumer lifecycle → `event-driven-integration`.

## Inputs

- Entry point of the service (FastAPI `lifespan`, aiohttp `Application`, or `asyncio.run`).
- List of background tasks and their expected lifetimes.
- Known blocking libraries used (ORM, HTTP client, file I/O).

## Workflow

1. Identify all async entry points. Every `asyncio.create_task` must have an owner that can cancel and `await` it.
2. Use `asyncio.TaskGroup` (Python 3.11+) for fan-out tasks. On any child failure the group cancels siblings and propagates the exception.
3. Wrap resource acquisition in `async with`; use `contextlib.asynccontextmanager` for custom teardown.
4. Never `await` a blocking call directly in an `async def`. Replace with `asyncio.to_thread` (I/O) or `loop.run_in_executor(ProcessPoolExecutor, ...)` (CPU).
5. Always re-raise `asyncio.CancelledError` after cleanup. Swallowing it prevents graceful shutdown.
6. For FastAPI: use `lifespan` context manager to start/stop background tasks. Do not put startup logic in a `@app.on_event("startup")` decorator (deprecated).
7. Validate with `asyncio.run(..., debug=True)` in tests to surface task leaks and unawaited coroutine warnings.

## Outputs

- Async code with explicit task ownership and cancellation paths.
- Graceful shutdown sequence documented in `lifespan` or `main.py`.
- List of blocking calls replaced with async equivalents.

## Named Patterns

### Good — TaskGroup for fan-out with automatic cleanup
```python
import asyncio
from typing import AsyncIterator
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    async with asyncio.TaskGroup() as tg:
        tg.create_task(run_background_worker(app.state.queue))
        tg.create_task(refresh_config_loop())
        yield
        # On yield exit: TaskGroup cancels all tasks and awaits them
```
`TaskGroup` guarantees no orphan tasks on shutdown; exceptions from any task surface immediately.

### Bad — Fire-and-forget `create_task` with no owner
```python
@app.on_event("startup")
async def startup():
    asyncio.create_task(run_background_worker())  # no reference kept
```
On exception the task fails silently; on shutdown the task leaks; `asyncio.on_event` is deprecated.

### Good — async context manager for resource lifecycle
```python
from contextlib import asynccontextmanager
from typing import AsyncIterator

@asynccontextmanager
async def get_redis(url: str) -> AsyncIterator[Redis]:
    client = await Redis.from_url(url)
    try:
        yield client
    finally:
        await client.aclose()

# Usage
async with get_redis(settings.REDIS_URL) as redis:
    await redis.set("key", "value")
```
Resource is always released, even on exception or cancellation.

### Bad — Manual try/finally for connections
```python
redis = await Redis.from_url(settings.REDIS_URL)
try:
    result = await redis.get("key")
finally:
    await redis.close()  # easy to forget in complex flows; not composable
```

### Good — Re-raise CancelledError after cleanup
```python
async def process_job(job: Job) -> None:
    try:
        await job.execute()
    except asyncio.CancelledError:
        await job.rollback()
        raise  # MUST re-raise — do not swallow
    except Exception as exc:
        logger.error("job failed", job_id=job.id, exc_info=exc)
        raise
```
Swallowing `CancelledError` prevents the task from being cancelled, stalling shutdown.

### Bad — Swallowed CancelledError
```python
async def process_job(job: Job) -> None:
    try:
        await job.execute()
    except Exception:
        pass  # catches CancelledError too — shutdown hangs
```

### Good — Offload blocking call with asyncio.to_thread
```python
import asyncio

async def resize_image(path: str, width: int) -> bytes:
    # PIL is synchronous — run in thread pool
    return await asyncio.to_thread(_sync_resize, path, width)

def _sync_resize(path: str, width: int) -> bytes:
    from PIL import Image
    img = Image.open(path)
    img.thumbnail((width, width))
    ...
```
Event loop is free during the blocking PIL call; other requests proceed normally.

### Bad — Blocking call in async function
```python
async def resize_image(path: str, width: int) -> bytes:
    img = Image.open(path)   # blocks event loop
    img.thumbnail((width, width))
    ...
```
All other coroutines stall while PIL runs; throughput collapses under load.

## Boundaries

- Owns async lifecycle, task management, and blocking-call offloading within the service.
- Does not own broker consumer lifecycle (Kafka/Celery) → `event-driven-integration`.
- Does not own database connection pool configuration → `data-layer-python`.
- Does not own infrastructure runtime settings (worker count, ulimits) → `devops-sre`.

## Sources

### Priority 1 — asyncio canon
- asyncio documentation — https://docs.python.org/3/library/asyncio.html
- PEP 492 Coroutines with async and await — https://peps.python.org/pep-0492/
- PEP 525 Asynchronous Generators — https://peps.python.org/pep-0525/
- FastAPI lifespan events — https://fastapi.tiangolo.com/advanced/events/

### Priority 2 — Reliability orientation
- Google SRE Book (graceful degradation) — https://sre.google/sre-book/table-of-contents/

### Priority 3 — Practice background
- Real Python: Async IO in Python — https://realpython.com/async-io-python/

## Handoff

- Broker consumer async lifecycle → `event-driven-integration`.
- Database async connection pool → `data-layer-python`.
- Service package and DI wiring → `python-service-design`.
- Worker/process count and OS-level settings → `devops-sre`.
