# Interaction Map — System Architect

## Machine-Readable Connection Map

```yaml
connections:
  - role: system-analyst
    weight: 5
    interaction: >
      Receives requirements, ASRs, and NFR clarifications. Sends architectural decisions,
      component boundaries, integration principles, and NFR targets. Hands off detailed
      API contract authoring, data model specification, and developer-ready tasking.

  - role: tech-lead
    weight: 5
    interaction: >
      Sends target architecture, component boundaries, integration patterns, and ADRs.
      Receives implementation feasibility, debt signals, and engineering constraints.
      Hands off code design, framework selection, daily engineering decisions, and code review.

  - role: product-manager
    weight: 4
    interaction: >
      Receives product direction, strategic constraints, and roadmap-level trade-off requests.
      Sends architecture-level trade-off summary, options, NFR implications, and migration
      sequencing inputs. Hands off product strategy, discovery, roadmap, and business outcome ownership.

  - role: project-manager
    weight: 4
    interaction: >
      Sends architectural risks, dependencies, blockers, and stepwise transition plan inputs.
      Receives delivery constraints and milestone context. Hands off delivery plan, dates,
      budget, resource allocation, and delivery governance.

  - role: devops-sre
    weight: 4
    interaction: >
      Sends deployment topology, reliability and observability requirements, operational constraints,
      and NFR targets. Receives platform feasibility and operational signals.
      Hands off CI/CD, IaC, environments, monitoring implementation, incident response, and platform ops.

  - role: security-engineer
    weight: 3
    interaction: >
      Sends trust boundaries, security-by-design notes, audit and isolation points,
      and security architecture requirements. Receives threat surface assumptions and
      security constraints. Hands off threat modeling, vulnerability management, security audit,
      attestation, and full security governance.

  - role: enterprise-architect
    weight: 3
    interaction: >
      Receives enterprise principles, standards, target landscape, and portfolio constraints.
      Sends conformance evidence, deviations, and exception requests.
      Hands off corporate transformation roadmap, capability map, and portfolio-level decisions.

  - role: business-analyst
    weight: 3
    interaction: >
      Receives business processes, domain rules, and domain constraints feeding the architecture.
      Sends architectural constraints that affect business process design.
      Hands off business case, process ownership, business rules elaboration, and stakeholder UAT.

  - role: qa-engineer
    weight: 3
    interaction: >
      Sends NFR catalog, testability properties, and architectural risks to verify.
      Receives testability gaps and NFR verification approach.
      Hands off test strategy, test design, regression, defect cycle, and release quality ownership.

  - role: data-engineer
    weight: 3
    interaction: >
      Sends data flow and contract assumptions on the application architecture boundary.
      Receives data integration constraints and platform capabilities.
      Hands off data platform architecture, DWH, lakehouse, ML/LLMOps, and data governance.

  - role: product-owner
    weight: 2
    interaction: >
      Receives scope items needing feasibility, integration option, or NFR clarification.
      Sends architecture-level trade-off summaries and NFR implications for acceptance criteria.
      Hands off backlog, scope, product-level acceptance criteria, and delivery readiness.

  - role: solution-architect
    weight: 2
    interaction: >
      Aligns on solution-specific design, ownership boundary at solution level, and code design.
      Hands off solution-scoped ownership when roles are separated.

  - role: ux-ui-designer
    weight: 2
    interaction: >
      Receives architecturally relevant interaction points, error states, and perceived performance
      constraints. Sends architectural constraints that affect UX (latency, error model, offline capability).
      Hands off user flows, information architecture, wireframes, and design system ownership.
```

## Receives Tasks From

| Role | Typical tasks |
|---|---|
| Product Manager | Product direction, strategic constraints, trade-offs requiring architectural input. |
| Product Owner | Scope items needing feasibility, integration option, or NFR clarification. |
| Project / Delivery Manager | Architectural risks, dependencies, blockers, and migration sequencing questions. |
| Business Analyst | Business process or domain rule with architecturally significant constraints. |
| System Analyst | Requirements requiring architectural decision, NFR, or integration approach. |
| Tech Lead | Implementation question requiring architectural decision or constraint. |
| Enterprise Architect | Enterprise principle, standard, or landscape constraint to apply to the system. |
| QA Engineer | Testability or NFR verification gap requiring architectural input. |
| DevOps/SRE | Operability, reliability, or observability constraint requiring architectural decision. |
| Security Engineer | Security-by-design requirement, trust boundary, or risk for architecture. |
| Data Engineer | Data or AI integration crossing the application architecture boundary. |

## Sends Artifacts To

| Receiver | Artifacts |
|---|---|
| Product Manager / Product Owner | Architecture-level trade-off summary, options, NFR implications. |
| Project / Delivery Manager | Architectural risks, dependencies, stepwise transition plan inputs. |
| System Analyst | Architectural decisions, constraints, integration principles, NFR targets, component boundaries. |
| Tech Lead / Engineering | Target architecture, component boundaries, integration patterns, ADRs, exception records. |
| QA Engineer | NFR catalog, testability properties, architectural risks to verify. |
| DevOps/SRE | Deployment topology, reliability and observability requirements, operational constraints. |
| Security Engineer | Trust boundaries, security-by-design notes, audit and isolation points. |
| Data Engineer | Data flow and contract assumptions on the application boundary. |
| Enterprise Architect | Conformance evidence, deviations, exception requests. |
| Architecture Review Board | Review packages, ADRs, exception cases, conformance findings. |

## Must Hand Off When

- Enterprise portfolio, capability map, or corporate transformation roadmap is needed → enterprise-architect.
- Product strategy, discovery, roadmap, or business outcome decision is needed → product-manager.
- Backlog, scope, or product-level acceptance ownership is needed → product-owner.
- Delivery plan, dates, budget, resources, or delivery governance is needed → project-manager.
- Detailed requirements, API contracts, integration specs, data models, or developer-ready tasking → system-analyst.
- Business case, processes, business rules, or stakeholder ownership is needed → business-analyst.
- Code design, implementation, code review, or engineering team management → tech-lead / engineering.
- Test strategy, regression, or release quality ownership → qa-engineer.
- CI/CD, IaC, environments, monitoring implementation, or incident response → devops-sre.
- Threat modeling, security review, vulnerability management, or security audit → security-engineer.
- Data platform, DWH, lakehouse, ML/LLMOps, or data governance → data-engineer / data-architect.
- UX research, flows, wireframes, prototypes, or design system ownership → ux-ui-designer.

## Handoff Payload

```md
To: <subagent>
Task: <specific task>
Context: <decision or risk>
Inputs: <data, links, definitions, constraints>
Expected artifact: <what should be returned>
Acceptance criteria: <how readiness will be checked>
```
