---
name: python-typing-and-quality
description: Use when improving type annotation coverage, enforcing mypy strict mode, setting up ruff as the unified linter, structuring Pydantic v2 validation at service boundaries, or establishing dependency management with Poetry or pip-tools. Covers the full static analysis and code-quality baseline for a Python service.
family: code
profile_level: Senior+
---

# Python Typing and Quality

## Purpose

Establish a typing and code-quality baseline so that bugs are caught statically, code is self-documenting, and the CI gate is reproducible. Covers type annotations, mypy, ruff, Pydantic v2 at input/output boundaries, and repeatable dependency pinning.

## Use When

- Starting a new Python service and setting up the quality toolchain.
- Raising typing coverage on an existing service toward `mypy --strict` compliance.
- Standardizing linting and formatting (replacing flake8 + isort + black with ruff).
- Choosing between `dataclass`, Pydantic model, and `TypedDict` for a data shape.
- Reviewing a PR for missing type annotations or unsafe casts.

## Do Not Use When

- The task is service layer design and DI → `python-service-design`.
- The task is test pyramid structure → `python-testing`.
- The task is async safety → `python-async-and-concurrency`.

## Inputs

- Current `pyproject.toml` or `setup.cfg` with tool configs.
- `mypy` output on the existing codebase.
- List of third-party libraries needing stubs.

## Workflow

1. Configure `ruff` in `pyproject.toml` as the single tool for lint + format: `select = ["E", "F", "I", "UP", "B", "SIM"]`. Remove flake8, isort, black.
2. Add `[tool.mypy]` section with `strict = true`. Start with `ignore_missing_imports = true` for stubs you don't yet have; remove gradually.
3. Fix `Any`-typed boundaries first: function parameters and return types of public API methods and repository interfaces.
4. Replace untyped dicts at service boundaries with `dataclass` (internal value objects) or Pydantic v2 `BaseModel` (HTTP request/response, config, external data).
5. Use `TypeVar` + `Generic` for container types; use `Protocol` for structural interfaces (see `python-service-design`).
6. Install `types-*` stubs for untyped third-party libraries via pip; add to `dev` dependency group.
7. Add pre-commit hooks: `ruff check --fix`, `ruff format`, `mypy`.
8. Pin dependencies: `poetry lock` or `pip-compile` → commit lockfile. Differentiate `[tool.poetry.dependencies]` (runtime) from `[tool.poetry.dev-dependencies]` (CI/local only).

## Outputs

- `pyproject.toml` with `[tool.ruff]` and `[tool.mypy]` sections.
- Pre-commit config (`.pre-commit-config.yaml`).
- Annotated public API surfaces of all service modules.
- `requirements.txt` lockfile or `poetry.lock` committed to the repo.

## Named Patterns

### Good — Pydantic v2 model at the HTTP boundary only
```python
# api/schemas.py — Pydantic for HTTP
from pydantic import BaseModel, Field, field_validator
from decimal import Decimal

class PlaceOrderRequest(BaseModel):
    items: list[str] = Field(min_length=1)
    currency: str = Field(pattern=r"^[A-Z]{3}$")
    total: Decimal

    @field_validator("total")
    @classmethod
    def positive_total(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("total must be positive")
        return v
```
```python
# domain/models.py — plain dataclass; no Pydantic dependency in domain
from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID, uuid4

@dataclass(frozen=True)
class Order:
    id: UUID = field(default_factory=uuid4)
    items: tuple[str, ...] = ()
    total: Decimal = Decimal("0")
```
Pydantic stays at the transport boundary; domain layer has no framework dependency.

### Bad — Pydantic model as domain entity
```python
# domain/order.py
from pydantic import BaseModel

class Order(BaseModel):
    id: str
    items: list[str]
    # Pydantic validation mixin in domain; domain depends on pydantic
```
Domain serialization logic leaks into business rules; switching serializers requires domain rewrite.

### Good — mypy strict config with per-module overrides
```toml
# pyproject.toml
[tool.mypy]
strict = true
ignore_missing_imports = false

[[tool.mypy.overrides]]
module = ["legacy_module.*", "third_party_untyped.*"]
ignore_missing_imports = true
ignore_errors = true
```
Strict by default; legacy modules opted out explicitly with a comment explaining why.

### Bad — Global `ignore_missing_imports = true`
```toml
[tool.mypy]
ignore_missing_imports = true  # hides real type errors in your own code
```
The whole service runs untyped effectively; errors surface only at runtime.

### Good — TypeVar for generic container
```python
from typing import TypeVar, Generic

T = TypeVar("T")

class Page(Generic[T]):
    def __init__(self, items: list[T], cursor: str | None) -> None:
        self.items = items
        self.cursor = cursor

# Usage: Page[Order], Page[Payment] — fully typed
```
Callers know the item type; `mypy` checks usage.

### Bad — Untyped container
```python
class Page:
    def __init__(self, items: list, cursor):  # items: list[Any]
        self.items = items
        self.cursor = cursor
```
Consumer gets `Any` items; type errors surface at runtime.

### Good — ruff replaces the whole quality stack
```toml
[tool.ruff]
line-length = 120
select = ["E", "F", "I", "UP", "B", "SIM", "ANN"]
ignore = ["ANN101"]  # self annotation not required

[tool.ruff.format]
quote-style = "double"
```
One tool, one pass in CI; no flake8/isort/black conflicts.

### Bad — Three-tool stack
```yaml
# .pre-commit-config.yaml
repos:
  - repo: psf/black
  - repo: pycqa/isort
  - repo: pycqa/flake8
```
Black and isort conflict on import ordering; each has its own config format; three CI steps for one concern.

## Boundaries

- Owns type annotation baseline, static analysis toolchain, and dependency pinning for the service.
- Does not own CI pipeline definition (Dockerfile, GitHub Actions runner) → `devops-sre`.
- Does not own API validation contract semantics → `api-contract-design`.
- Does not own test pyramid structure → `python-testing`.

## Sources

### Priority 1 — Python typing canon
- PEP 484 Type Hints — https://peps.python.org/pep-0484/
- PEP 544 Protocols — https://peps.python.org/pep-0544/
- PEP 557 Data Classes — https://peps.python.org/pep-0557/
- mypy documentation — https://mypy.readthedocs.io/
- ruff documentation — https://docs.astral.sh/ruff/
- Pydantic v2 documentation — https://docs.pydantic.dev/

### Priority 2 — Quality standards
- ISO/IEC 25010 software quality model — https://iso25000.com/index.php/en/iso-25000-standards/iso-25010
- Google Engineering Practices — https://google.github.io/eng-practices/

### Priority 3 — Practice background
- Real Python: Python Type Checking — https://realpython.com/python-type-checking/

## Handoff

- Service layer design and DI wiring → `python-service-design`.
- Test structure and coverage strategy → `python-testing`.
- API input/output validation contract → `api-contract-design`.
- CI/CD pipeline and toolchain runner config → `devops-sre`.
