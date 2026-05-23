---
name: component-and-service-decomposition
description: Use when defining component, service, or module boundaries for a system or domain — choosing between modular monolith and microservices, mapping DDD bounded contexts and subdomains, establishing ownership and coupling rules, or resolving excessive coupling and shared-database anti-patterns at the architectural level.
family: method
profile_level: Senior+
---

# Component and Service Decomposition

## Purpose

Define how a system is split into components, services, modules, and DDD bounded contexts, with clear ownership, coupling constraints, and team-to-domain alignment. Produce a decomposition that is realizable, evolvable, and auditable through context maps and architecture decision records.

## Use When

- A new system, domain, or product needs component or service boundaries before implementation begins.
- A team must choose between modular monolith, microservices, or a hybrid topology and needs the trade-offs made explicit.
- DDD strategic design is the decomposition language: subdomains (core, supporting, generic) and bounded contexts must be identified and mapped.
- Excessive coupling, shared databases, ownership conflicts, or unclear service boundaries are causing incidents or change friction.
- A strangler-fig migration or domain split needs architectural framing with transition-state integrity.
- Team topology must be aligned with bounded-context ownership (Conway's Law inversion).

## Do Not Use When

- The task is integration pattern selection between already-bounded services → `integration-architecture`.
- The task is setting measurable NFR targets for the decomposed system → `non-functional-architecture`.
- The task is recording the decomposition decision in an ADR → `architecture-decision-records`.
- The task is internal package layout or code structure within a single service → handoff to `tech-lead`.
- The task is enterprise capability mapping or portfolio-level domain decomposition → handoff to enterprise-architect.

## Inputs

- Domain model, business processes, key entities, and aggregate candidates.
- Functional requirements and known change axes (what changes together, what changes independently).
- Non-functional requirements: scale, availability, team autonomy, deployment independence.
- Current decomposition, known coupling, integration points, and debt evidence.
- Team topology, ownership capacity, and organizational constraints.

## Workflow

1. **Identify subdomains.** Classify business areas as core (competitive differentiator), supporting (necessary but not differentiating), or generic (commodity). Core subdomains get the most decomposition investment.
2. **Define bounded contexts.** For each subdomain, establish a bounded context: a cohesive model with a single ubiquitous language, clear responsibility, and explicit data ownership. Avoid merging contexts with different models or ownership teams.
3. **Draw the context map.** Map upstream/downstream relationships between contexts. Name the integration pattern for each relationship: shared kernel, customer/supplier, conformist, anti-corruption layer (ACL), open-host service, published language, or separate ways. ACL is default when contexts have divergent models.
4. **Choose decomposition style.** Evaluate modular monolith vs microservices vs hybrid against team size, operational maturity, deployment frequency, and scale. Default to modular monolith until a bounded context needs independent deployment, its own data store, or independent scaling.
5. **Define component responsibilities and API surfaces.** For each component or service: what it owns, what it exposes, what it consumes, and what it must not know about.
6. **Define coupling rules.** Specify allowed integration paths, forbidden direct database sharing, and shared-kernel scope. Mark every exception as a deliberate trade-off with a revisit trigger.
7. **Align with team ownership.** Map each bounded context or component to a team or squad. One team per context is the target; document where it is not yet achievable and why.
8. **Record open boundaries.** Mark contested areas as `assumption`, `open question`, or `needs decision` and create ADR stubs for them.

## Outputs

- Subdomain classification (core / supporting / generic) with rationale.
- Bounded context map with named context relationships and integration patterns.
- Component or service decomposition diagram and ownership table.
- Coupling rules: allowed paths, forbidden shared resources, ACL placements.
- Decomposition ADR or ADR stub.
- Handoff items for `system-analyst` (API contracts, data models), `tech-lead` (internal design), and `integration-architecture` (cross-context flow selection).

## Named Patterns

### Good — Bounded context with explicit context map
Each context owns its data store and model. A context map entry names the upstream/downstream relationship and the integration pattern.
```
OrderContext (upstream, open-host service) → PaymentContext (downstream, ACL)
PaymentContext owns payment state; OrderContext never reads payment tables directly.
```

### Bad — Shared database anti-pattern
Two services share a single database schema. One team's migration breaks the other team's queries. Coupling is hidden — no context map captures it, no ACL protects either model.

### Good — Modular monolith by default
A team deploys a single binary split into internal modules with strict import rules. Each module compiles independently; extraction to a service is straightforward when the need arises.

### Bad — Microservices-first without domain justification
Eight services for a two-developer product, each calling the next synchronously. Deployment complexity, distributed tracing overhead, and cross-service transactions cancel any decomposition benefit.

### Good — ACL at divergent model boundary
Context A (CRM, uses "Customer") integrates with Context B (Logistics, uses "Shipment Recipient"). A translation layer in Context B prevents the CRM model from leaking into logistics business logic.

### Bad — Conformist without justification
Context A blindly accepts the upstream model from Context B, including fields it does not need and terminology that does not match its own language. The model pollution accumulates over releases.

### Good — Team-aligned ownership
One bounded context, one squad. The squad owns the schema, the API surface, and the ADR for changes. Coordination cost is local.

### Bad — Cross-team shared kernel without governance
Three teams share a "common domain model" library. Each team adds fields. Nobody owns the library. Breaking changes are discovered at integration time.

## Boundaries

- Does not own the internal code design, framework selection, or class-level patterns within a component → `tech-lead`.
- Does not own enterprise portfolio or capability mapping → enterprise-architect.
- Does not own backlog, scope sequencing, or delivery governance → `product-owner` / `project-manager`.
- Does not write detailed API contracts or OpenAPI specs → `system-analyst`.
- Does not choose the integration protocol or message broker → `integration-architecture`.

## Sources

### Priority 1 — Canonical References
- Eric Evans — Domain-Driven Design reference (DDD Blue Book): https://www.domainlanguage.com/ddd/reference/
- Vaughn Vernon — Implementing Domain-Driven Design: https://vaughnvernon.com/?page_id=168
- Sam Newman — Building Microservices (bounded context decomposition): https://samnewman.io/books/building_microservices/
- microservices.io — Decomposition patterns: https://microservices.io/patterns/decomposition/index.html

### Priority 2 — Practitioner Guidance
- Martin Fowler — MicroservicePremium: https://martinfowler.com/bliki/MicroservicePremium.html
- Sam Newman — Monolith to Microservices: https://samnewman.io/books/monolith-to-microservices/
- Martin Fowler — StranglerFigApplication: https://martinfowler.com/bliki/StranglerFigApplication.html
- Team Topologies — Conway's Law and team alignment: https://teamtopologies.com/

### Priority 3 — Supplementary
- InfoQ — DDD and microservices decomposition articles: https://www.infoq.com/microservices/
- context-mapping reference card (Brandolini): https://www.infoq.com/articles/ddd-contextmapping/

## Handoff

- Detailed API contracts, integration specs, data models → `system-analyst`.
- Cross-context integration pattern and protocol selection → `integration-architecture`.
- Internal code design and framework choice within a component → `tech-lead`.
- Sequencing of decomposition into delivery stages → `target-and-transition-architecture`.
- Risk assessment of chosen decomposition (SPOF, coupling debt) → `architectural-risk-and-technical-debt`.
