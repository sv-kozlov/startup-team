# Interaction Map — Fullstack Developer

```yaml
weight_scale:
  5: critical
  4: regular
  3: periodic
  2: consultative
  1: rare

connections:
  - role: tech-lead
    weight: 5
    interaction: "Feature architecture, team standards, ADR review, technical debt, escalation of cross-feature decisions."
    boundary: "Owns team-wide technical direction and standards. Fullstack developer owns implementation and quality of own feature."

  - role: system-analyst
    weight: 4
    interaction: "API contracts, integration scenarios, data shapes, edge cases, error semantics, idempotency, acceptance criteria."
    boundary: "Owns requirements baseline and system specification. Fullstack developer implements the contract and clarifies technical detail."

  - role: ui-ux-designer
    weight: 4
    interaction: "UI states (loading, error, empty, success), layout constraints, responsive breakpoints, design handoff, accessibility."
    boundary: "Owns user experience and visual design. Fullstack developer implements and surfaces technical constraints."

  - role: qa-engineer
    weight: 4
    interaction: "Testability of the feature, defect triage, contract tests, regression coverage, e2e scenario alignment."
    boundary: "Owns QA strategy and release-level regression. Fullstack developer keeps code testable and writes developer-level tests."

  - role: product-owner
    weight: 4
    interaction: "Feature scope refinement, acceptance criteria, priority of technical items, release readiness."
    boundary: "Owns backlog content and priorities. Fullstack developer clarifies technical constraints and estimates."

  - role: frontend-developer
    weight: 4
    interaction: "API contracts, component design, state management patterns, shared UI standards, complex rendering concerns."
    boundary: "Owns frontend platform and design system depth. Fullstack developer routes deep frontend platform tasks to frontend-developer."

  - role: backend-go-developer
    weight: 4
    interaction: "API contracts, service boundaries, concurrency concerns, performance-critical paths."
    boundary: "Owns Go backend platform and service internals. Fullstack developer routes deep Go runtime / concurrency tasks to backend-go-developer."

  - role: devops-sre
    weight: 3
    interaction: "Deploy configuration, environment variables, health checks, observability stack, CI/CD pipelines."
    boundary: "Owns platform, runtime, on-call. Fullstack developer makes the feature production-ready and contributes runbook content."

  - role: system-architect
    weight: 3
    interaction: "Feature fit within platform architecture, NFRs for the feature, cross-service contract boundaries."
    boundary: "Owns target platform architecture. Fullstack developer proposes feature-level designs within agreed architectural boundaries."

  - role: python-developer
    weight: 3
    interaction: "API contracts, shared data schemas, integration with Python backend services."
    boundary: "Owns Python backend platform. Fullstack developer routes deep Python ML/data pipeline tasks to python-developer."

  - role: product-manager
    weight: 2
    interaction: "Technical feasibility, risk, cost estimates, trade-offs visible to product."
    boundary: "Owns product outcome and roadmap. Fullstack developer surfaces technical reality without owning prioritization."

  - role: project-manager
    weight: 2
    interaction: "Delivery dates, dependencies, risk surfacing on technical work."
    boundary: "Owns delivery schedule and coordination. Fullstack developer surfaces technical risk and dependencies."

  - role: mobile-developer
    weight: 1
    interaction: "Shared API contracts, backward compatibility for mobile clients."
    boundary: "Owns mobile client. Fullstack developer owns the server contract; does not implement mobile."
```
