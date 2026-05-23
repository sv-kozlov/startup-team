# Interaction Map — Python Developer

```yaml
weight_scale:
  5: critical
  4: regular
  3: periodic
  2: consultative
  1: rare

connections:
  - role: system-analyst
    weight: 5
    interaction: "API contracts, integration scenarios, data shapes, edge cases, error semantics, idempotency."
    boundary: "Owns requirements baseline and system specification. Python developer implements the contract and clarifies technical detail."

  - role: tech-lead
    weight: 5
    interaction: "Service architecture, team standards, technical debt, ADR review, escalation of cross-service decisions."
    boundary: "Owns team-wide direction and standards. Python developer owns implementation and quality of own service."

  - role: frontend-developer
    weight: 4
    interaction: "API contracts, error shapes, performance budgets on client-visible paths, breaking changes coordination."
    boundary: "Owns client UX and state. Python developer owns server contract and stability."

  - role: qa-engineer
    weight: 4
    interaction: "Testability of code, defect triage, contract tests, regression coverage."
    boundary: "Owns QA strategy and release-level regression. Python developer keeps code testable and writes service-level tests."

  - role: devops-sre
    weight: 4
    interaction: "Deploy, runtime configuration, observability stack, alert routing, capacity, SRE runbooks."
    boundary: "Owns platform, runtime, on-call. Python developer makes the service production-ready and contributes runbook content."

  - role: ml-engineer
    weight: 3
    interaction: "ML API integration, inference service wrapping, model constraints, feature pipeline contracts."
    boundary: "Owns model quality and ML experiments. Python developer owns the serving/integration service when implemented in Python."

  - role: product-owner
    weight: 3
    interaction: "Backlog refinement on technical items, acceptance criteria clarification, scope decomposition."
    boundary: "Owns backlog content and priorities. Python developer clarifies estimates and constraints."

  - role: data-engineer
    weight: 3
    interaction: "Event schemas, stream latency and ordering, platform services for data pipelines."
    boundary: "Owns data lake/warehouse and pipelines. Python developer owns service-side event production and consumption."

  - role: system-architect
    weight: 3
    interaction: "Bounded contexts, cross-service contracts, NFR for the service, architectural fitness of proposed designs."
    boundary: "Owns target architecture of the platform. Python developer proposes service-level designs within the agreed boundaries."

  - role: mobile-developer
    weight: 2
    interaction: "API contracts, offline/online semantics, version coexistence, backward compatibility on mobile clients."
    boundary: "Owns mobile client. Python developer owns the contract and rollout coordination on the server side."

  - role: product-manager
    weight: 2
    interaction: "Technical feasibility, risk, cost estimates, trade-offs visible to product."
    boundary: "Owns product outcome and roadmap. Python developer surfaces technical reality without owning prioritization."

  - role: project-manager
    weight: 2
    interaction: "Delivery dates, dependencies, risk surfacing on technical work."
    boundary: "Owns delivery schedule and coordination. Python developer surfaces technical risk and dependencies."

  - role: ui-ux-designer
    weight: 1
    interaction: "API shapes that affect interaction patterns, state machines visible to UI."
    boundary: "Owns interaction and visual design. Python developer ensures API supports the agreed states."
```
