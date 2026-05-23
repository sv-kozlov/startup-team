# Interaction Map — Mobile Developer

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
    interaction: "Mobile UX flows, screen states, platform guidelines (HIG/Material Design), accessibility, design handoff."
    boundary: "Owns UX research, user flows, wireframes, prototypes, and visual design system. Mobile developer implements and clarifies platform constraints."

  - role: backend-developers
    weight: 5
    interaction: "API contracts, authentication, token refresh, push notification payload, deep link schemes, latency budgets, offline/online semantics, backward compatibility."
    boundary: "Owns server-side business logic and API contract ownership. Mobile developer owns client integration and negotiates mobile-friendly contract shape."

  - role: qa-engineer
    weight: 4
    interaction: "Device matrix, regression coverage, crash report triage, testability of code, UI test scaffolding, acceptance criteria for mobile scenarios."
    boundary: "Owns QA strategy and release-level regression. Mobile developer writes developer-level tests and fixes defects."

  - role: tech-lead
    weight: 4
    interaction: "Mobile architecture decisions, team standards, code review on complex PRs, technical debt, ADR review, cross-team dependency escalation."
    boundary: "Owns team-wide technical direction and standards. Mobile developer owns implementation and quality of the mobile codebase."

  - role: product-manager
    weight: 3
    interaction: "Feature scope, release constraints, technical feasibility, risk surfacing on mobile timelines."
    boundary: "Owns product outcome, roadmap, and prioritization. Mobile developer surfaces technical reality without owning priorities."

  - role: product-owner
    weight: 3
    interaction: "Backlog refinement on mobile items, acceptance criteria clarification, release readiness sign-off."
    boundary: "Owns backlog content and priorities. Mobile developer clarifies estimates and constraints."

  - role: product-analyst
    weight: 3
    interaction: "Analytics event schemas, experiment instrumentation, metric definitions, A/B test setup in mobile."
    boundary: "Owns experiment design and metric analysis. Mobile developer implements event instrumentation per agreed schema."

  - role: devops-sre
    weight: 3
    interaction: "Mobile CI/CD pipeline, build signing, artifact distribution, crash alert routing, release tooling (Fastlane, Bitrise, GitHub Actions)."
    boundary: "Owns CI/CD platform infrastructure and on-call rotation. Mobile developer makes the app build-reproducible and contributes release runbooks."

  - role: system-analyst
    weight: 2
    interaction: "API contract details, integration scenarios, data shapes visible to mobile, edge cases and error semantics."
    boundary: "Owns requirements baseline and system specification. Mobile developer clarifies client-side constraints and integration detail."

  - role: system-architect
    weight: 2
    interaction: "Cross-service contracts affecting mobile, NFRs for the mobile client, architectural fitness of proposed designs."
    boundary: "Owns target platform architecture. Mobile developer proposes client-side designs within the agreed architectural boundaries."

  - role: project-manager
    weight: 1
    interaction: "Delivery dates, technical dependencies, risk surfacing on mobile work."
    boundary: "Owns delivery schedule and coordination. Mobile developer surfaces technical risk and dependency on store review timelines."
```
