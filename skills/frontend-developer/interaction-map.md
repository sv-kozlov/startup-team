# Interaction Map — Frontend Developer

```yaml
weight_scale:
  5: critical
  4: regular
  3: periodic
  2: consultative
  1: rare

connections:
  - role: ui-ux-designer
    weight: 5
    interaction: "Design handoff, component states, adaptive layouts, design system tokens, edge cases in UI flows."
    boundary: "Owns UX research, user flows, and visual design. Frontend developer implements the design and clarifies technical constraints on states and responsiveness."

  - role: backend-go-developer
    weight: 5
    interaction: "API contracts, error shapes, auth flows, performance budgets on client-visible paths, breaking change coordination."
    boundary: "Owns server logic and contract from the server side. Frontend developer owns client-side consumption and state derived from the contract."

  - role: qa-engineer
    weight: 4
    interaction: "E2e test coverage, defect triage, regression scenarios, testability of component design."
    boundary: "Owns QA strategy and release-level regression. Frontend developer writes developer tests and fixes client-side defects."

  - role: system-analyst
    weight: 4
    interaction: "UI scenarios, API semantics, integration constraints, edge case specification, validation rules."
    boundary: "Owns system requirements and specification. Frontend developer clarifies implementability and edge cases of UI scenarios."

  - role: tech-lead
    weight: 4
    interaction: "Frontend architecture decisions, team-wide standards, ADR review, dependency choices, tech debt direction."
    boundary: "Owns team-wide technical direction and standards. Frontend developer owns implementation and quality of the frontend module."

  - role: python-developer
    weight: 3
    interaction: "API contracts, error shapes, auth flows for Python-backed services, performance on client-visible paths."
    boundary: "Owns Python backend logic and contract. Frontend developer owns client-side usage."

  - role: product-owner
    weight: 3
    interaction: "Feature scope, acceptance criteria, user value, prioritization of frontend tech debt."
    boundary: "Owns backlog content and priorities. Frontend developer clarifies estimates and technical constraints."

  - role: product-manager
    weight: 3
    interaction: "Technical feasibility, risk assessment, cost estimates, UI metrics visible to product."
    boundary: "Owns product outcome and roadmap. Frontend developer surfaces technical reality without owning prioritization."

  - role: devops-sre
    weight: 2
    interaction: "Build configuration, deployment environments, feature flags, release pipeline, CDN/caching configuration."
    boundary: "Owns CI/CD platform and runtime. Frontend developer makes the app production-ready and provides build artifacts."

  - role: system-architect
    weight: 2
    interaction: "Frontend module boundaries, NFRs for the frontend layer, micro-frontend decisions, cross-team contract design."
    boundary: "Owns target platform architecture. Frontend developer proposes module-level designs within agreed boundaries."

  - role: mobile-developer
    weight: 2
    interaction: "Shared component libraries, design system tokens, API contracts shared between web and mobile."
    boundary: "Owns mobile client. Frontend developer owns web client."

  - role: project-manager
    weight: 2
    interaction: "Delivery dates, dependency surfacing, risk flagging on frontend-side technical work."
    boundary: "Owns delivery schedule and coordination. Frontend developer surfaces technical risk and dependencies."
```
