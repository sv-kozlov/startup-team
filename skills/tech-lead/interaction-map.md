# Interaction Map — Tech Lead

```yaml
weight_scale:
  5: critical
  4: regular
  3: periodic
  2: consultative
  1: rare

connections:
  - role: developers
    weight: 5
    interaction: "Technical decisions, code review, help on complex tasks, developer growth, mentoring, onboarding."
    boundary: "Tech Lead owns team-wide standards and direction. Developers own implementation quality of their own tasks."

  - role: system-architect
    weight: 5
    interaction: "Architectural decisions and constraints, ADR alignment, NFR for the team's domain, architectural fitness of proposed designs."
    boundary: "System architect owns target architecture at platform or system level. Tech Lead owns component and service-level decisions within the team boundary."

  - role: system-analyst
    weight: 4
    interaction: "Technical feasibility of requirements, API and integration constraints, data model limitations, implementation boundary clarification."
    boundary: "System analyst owns requirements, specifications, and API contracts. Tech Lead verifies implementability and surfaces technical constraints."

  - role: product-manager
    weight: 4
    interaction: "Technical feasibility, risk and trade-off visibility, technical debt impact on roadmap, engineering capacity signals."
    boundary: "Product manager owns product strategy and roadmap. Tech Lead surfaces technical reality without owning prioritization."

  - role: product-owner
    weight: 4
    interaction: "Technical decomposition of backlog items, technical readiness criteria, dependency and risk clarification."
    boundary: "Product owner owns backlog content and scope. Tech Lead provides technical input and constraints."

  - role: qa-engineer
    weight: 4
    interaction: "Testability of architecture, defect root cause, test pyramid targets, integration of quality requirements into DoD."
    boundary: "QA engineer owns test strategy and release-level testing. Tech Lead owns code testability and engineering quality inside the team."

  - role: devops-sre
    weight: 4
    interaction: "CI/CD pipeline, observability stack, incident response, deployment readiness, SLO/SLI negotiation."
    boundary: "DevOps/SRE owns infrastructure, on-call rotation, and SRE practices. Tech Lead owns the code's production-readiness and contributes to runbook content."

  - role: project-manager
    weight: 3
    interaction: "Technical estimates, dependency map, risk flags on technical work, release readiness signal."
    boundary: "Project manager owns delivery schedule, budget, and status reporting. Tech Lead surfaces technical risk and dependency without owning governance."

  - role: backend-developer
    weight: 5
    interaction: "Service design, code review, technical decisions, complex implementation help, standards enforcement."
    boundary: "Tech Lead owns team-wide engineering direction. Backend developer owns implementation quality of individual services."

  - role: frontend-developer
    weight: 4
    interaction: "Technical approach alignment, API contracts, performance, cross-cutting standards applicable to frontend."
    boundary: "Tech Lead aligns technical approaches and cross-cutting dependencies. Frontend developer owns client implementation quality."

  - role: mobile-developer
    weight: 3
    interaction: "API contracts, offline/online scenarios, release constraints, dependency alignment."
    boundary: "Tech Lead aligns technical decisions. Mobile developer owns mobile platform implementation."

  - role: engineering-manager
    weight: 3
    interaction: "Developer growth signals, team capacity, technical hiring bar calibration, engineering culture."
    boundary: "Engineering manager owns administrative people management, compensation, and organizational decisions. Tech Lead owns technical development and mentoring."

  - role: hr-recruiter
    weight: 2
    interaction: "Interview loop coordination, role definition for technical positions, technical assessment criteria."
    boundary: "HR recruiter owns administrative hiring process. Tech Lead owns technical assessment and hiring bar."
```
