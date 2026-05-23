---
name: go-service-design
description: Use when starting a new Go service, restructuring package layout, deciding where interfaces live, or evaluating whether to introduce layered/hexagonal/clean architecture. Covers consumer-side interfaces, dependency direction, package boundaries, and proportionality of architectural choice to problem size.
family: code
profile_level: Senior+
---

# Go Service Design

## Purpose

Shape a Go service so it is easy to read, easy to change, and pays for any architectural layer it carries. Optimize for clear package boundaries, explicit dependencies, and a code shape a new Senior can navigate without a guide.

## Use When

- Bootstrapping a new Go service or module.
- Adding a feature that does not cleanly fit the current package layout.
- Reviewing a design where layers, interfaces, or dependency direction are unclear.
- The team is considering hexagonal/clean/CQRS and the cost of the layer is not obvious.

## Do Not Use When

- The task is purely about concurrency lifecycle → `go-concurrency-and-context`.
- The task is API contract shape (REST/gRPC/OpenAPI/protobuf) → `api-contract-design`.
- The task is the data access layer specifically → `data-layer-go`.
- The task is platform topology across services → handoff to `system-architect`.

## Inputs

- Current package tree, import graph, and known pain points.
- Business capability and expected change axes.
- Visible load profile and team size.

## Workflow

1. State the capability and the change axis. Name what is most likely to change (transport, storage, business rule, integration).
2. Draft the minimum package layout: `cmd/`, `internal/<domain>`, optional `pkg/` only if there is a real external consumer.
3. Place interfaces on the consumer side. The package that uses behavior owns its interface; the package that provides behavior exports a concrete type.
4. Verify dependency direction: domain depends on nothing infrastructural; infrastructure depends on domain.
5. Check for cycles and god-packages. A package named `common`, `utils`, or `helpers` is a smell.
6. Decide layer count by load: start with handler → service → repository. Add hexagonal ports/adapters only when ≥2 transports or ≥2 storages are in scope.

## Outputs

- Package tree with explicit dependency arrows.
- ADR or PR description naming the chosen architectural shape and the trade-off paid.
- List of interfaces with their consumer-side owners.

## Named Patterns

### Good — Consumer-side interface placement
```go
// internal/order: consumer defines what it needs.
package order

type PaymentCharger interface {
    Charge(ctx context.Context, amount Money) (TxID, error)
}

type Service struct {
    pay PaymentCharger
}
```
```go
// internal/payment: provider exports a concrete type, not an interface.
package payment

type StripeClient struct { /* ... */ }

func (c *StripeClient) Charge(ctx context.Context, amount order.Money) (order.TxID, error) { /* ... */ }
```
The consumer owns the abstraction; the provider stays concrete. Test doubles live next to the consumer.

### Bad — Provider-side interface
```go
// internal/payment: provider pre-declares an interface "for flexibility".
package payment

type Service interface {
    Charge(ctx context.Context, amount Money) (TxID, error)
}
```
Pre-declared provider interfaces create import cycles, force every consumer through one shape, and produce empty `mocks/` packages.

### Good — Proportional layering
A small service ships with handler → service → repository. No ports, no adapters, no application/domain split until a second transport or storage appears.

### Bad — Premature hexagonal
A single REST endpoint over a single Postgres table sits behind `ports/in`, `ports/out`, `application/`, `domain/`, `infrastructure/`. Five files to change one field.

### Good — `internal/` is the default
Packages live in `internal/<domain>` until another module needs them. Promotion to `pkg/` is a deliberate decision, with an ADR.

### Bad — `pkg/` as a dumping ground
Everything goes into `pkg/` "in case someone needs it". Public surface grows without owners; refactoring breaks unknown consumers.

### Good — No `common`, `utils`, `helpers`
Shared types live in the domain package that owns them. Cross-cutting helpers move into named packages: `timex`, `httpx`, `errx`.

### Bad — God package
`internal/common` holds time helpers, HTTP middleware, error types, JSON encoders, and three unrelated structs. Every package imports it; nothing imports it cleanly.

## Boundaries

- Owns service-internal package shape and dependency direction.
- Does not own cross-service architecture, bounded contexts, or platform topology — that is `system-architect`.
- Does not own team-wide layout standards across multiple services — that is `tech-lead`.

## Sources

### Priority 1 — Go canon
- Effective Go — https://go.dev/doc/effective_go
- Go Code Review Comments — https://go.dev/wiki/CodeReviewComments
- Google Go Style Guide — https://google.github.io/styleguide/go/
- Organizing a Go module — https://go.dev/doc/modules/layout

### Priority 2 — Architectural orientation
- The Twelve-Factor App — https://12factor.net/
- Hexagonal Architecture (Alistair Cockburn) — https://alistair.cockburn.us/hexagonal-architecture/

### Priority 3 — Pattern background
- martinfowler.com on layered architecture — https://martinfowler.com/bliki/PresentationDomainDataLayering.html

## Handoff

- Cross-service contracts and bounded contexts → `system-architect`.
- Team-wide standards across multiple Go services → `tech-lead`.
- Concurrency lifecycle within the chosen shape → `go-concurrency-and-context`.
- Data layer specifics inside the chosen shape → `data-layer-go`.
