# Interaction Map — System Analyst

Machine-readable connection map. Weight scale: 5 = critical / 4 = regular / 3 = periodic / 2 = consultative / 1 = rare.

```yaml
connections:
  - role: business-analyst
    weight: 5
    interaction: Business context, process ownership, AS IS/TO BE, business rules, stakeholder decisions.
  - role: system-architect
    weight: 5
    interaction: Architecture constraints, component boundaries, integration patterns, NFR trade-offs.
  - role: tech-lead
    weight: 5
    interaction: Feasibility, implementation constraints, codebase impact, technical risk, decomposition.
  - role: backend-developer
    weight: 5
    interaction: API contracts, service logic, data structures, mappings, errors, integrations, tasking.
  - role: qa-engineer
    weight: 5
    interaction: Acceptance criteria, testability, test scenarios, requirement defects, verification.
  - role: other-system-analysts
    weight: 5
    interaction: Cross-team requirements, shared contracts, analysis standards, specification review.
  - role: product-manager
    weight: 4
    interaction: Product goals, roadmap context, MVP, priority constraints, launch criteria.
  - role: product-owner
    weight: 4
    interaction: Backlog scope, product-level acceptance, delivery readiness, scope decisions.
  - role: frontend-developer
    weight: 4
    interaction: User scenarios, UI states, frontend/backend contracts, validation, errors.
  - role: domain-expert
    weight: 4
    interaction: Domain rules, exceptions, terminology, regulatory constraints, ubiquitous language.
  - role: ux-ui-designer
    weight: 3
    interaction: User flows, prototypes, interface states, edge cases, usability constraints.
  - role: devops-sre
    weight: 3
    interaction: Logging, monitoring, observability, reliability, operational scenarios.
  - role: data-analyst-bi
    weight: 3
    interaction: Data definitions, analytical events, reference data, source interpretation.
  - role: data-engineer
    weight: 3
    interaction: Data flows, schemas, source availability, data contracts, quality requirements.
  - role: technical-writer
    weight: 3
    interaction: System behavior, user-visible rules, error cases, documentation source material.
  - role: product-analyst
    weight: 2
    interaction: Tracking requirements, product events, metric data constraints, experiment data needs.
  - role: data-scientist-ml
    weight: 2
    interaction: ML model result integration, input/output requirements, model constraints.
  - role: support-operations
    weight: 2
    interaction: Incident patterns, user problems, diagnostics, operational feedback.
```

## Receives Tasks From

| Role | Typical tasks |
|---|---|
| Product Manager | Feature scope, MVP questions, product changes that need system requirements. |
| Business Analyst | Business process, rules, AS IS/TO BE, stakeholder context for system translation. |
| System Architect | Architecture constraints, component boundaries, NFR requirements, integration approach. |
| Tech Lead | Feasibility check, implementation constraints, codebase impact questions. |
| Backend / Frontend | Clarification of contracts, data, edge cases, states, errors, task scope. |
| QA Engineer | Testability gaps, requirement defects, scenario clarification, acceptance review. |
| Product Owner | Scope readiness, dependency analysis, requirement risks, task readiness gates. |

## Aligns With

| Role | Topics |
|---|---|
| Product Manager | Product goal, roadmap context, MVP scope, launch criteria, priority constraints. |
| Product Owner | Backlog scope, product-level acceptance, delivery readiness. |
| Business Analyst | Business rules, process boundaries, business terminology, stakeholder decisions. |
| System Architect | Target architecture, integration principles, NFR constraints, component boundaries. |
| Tech Lead | Feasibility, implementation constraints, codebase impact, technical risks. |
| Backend Developer | API, service logic, data structures, mappings, errors, events, idempotency. |
| Frontend Developer | User/system scenarios, UI states, validation, backend contracts. |
| QA Engineer | Acceptance criteria, test scenarios, test data, requirement traceability. |
| UX/UI Designer | User flows, interface states, edge cases, usability constraints. |
| DevOps / SRE | Logging, monitoring, observability, reliability, operational scenarios. |
| Data / BI Analyst | Data definitions, analytical events, reference data interpretation. |
| Data Engineer | Data flows, schemas, source availability, data contracts, quality requirements. |
| Product Analyst | Tracking requirements, product events, metric data constraints. |
| Technical Writer | External documentation inputs, user-facing behavior, release notes. |

## Sends Artifacts To

| Receiver | Artifacts |
|---|---|
| System Architect | Requirements, constraints, API/data/integration options, architecture impact notes. |
| Tech Lead | Developer-ready tasking, feasibility notes, implementation constraints, open questions. |
| Backend / Frontend | Developer-ready tasking, API contracts, scenarios, edge cases, mappings. |
| QA Engineer | Acceptance criteria, scenario list, testability notes, requirement traceability. |
| Data Engineer | Data requirements, entity mappings, schemas, event and freshness requirements. |
| Product Analyst | Tracking event requirements, parameter definitions, data constraints. |
| Technical Writer | System behavior, user-visible rules, error cases, documentation source material. |
| Product Manager | Scope clarification, requirement risks, decision options, unresolved questions. |
| Business Analyst | System interpretation of business rules and process constraints. |
| Product Owner | Task readiness state, dependencies, open questions, requirement risks. |

## Can Assign Tasks To

| Receiver | Example tasks |
|---|---|
| Product Manager | Decide scope, priority, MVP inclusion, or launch criterion. |
| Business Analyst | Clarify business rule, process owner, exception, or business term. |
| System Architect | Decide architecture option, integration pattern, NFR trade-off, or component boundary. |
| Tech Lead | Validate feasibility, implementation risk, backward compatibility, or estimate assumptions. |
| Backend / Frontend | Implement or clarify contract, event emission, validation, state handling, or error behavior. |
| QA Engineer | Validate testability, test cases, regression scope, or acceptance evidence. |
| Data Engineer | Confirm source, schema, data contract, freshness, lineage, or pipeline feasibility. |
| UX/UI Designer | Clarify flow, state, prototype, wording, or edge-case behavior. |
| DevOps / SRE | Confirm observability, logging, monitoring, alerting, or operational readiness. |

## Handoff Rules

- Hand off to `system-architect` when target architecture, component ownership, system decomposition, or major NFR trade-offs require a decision.
- Hand off to `tech-lead` when feasibility, codebase impact, implementation design, or engineering estimates are needed.
- Hand off to `qa-engineer` when test strategy, regression scope, test design, or release quality ownership is required.
- Hand off to `product-manager` when product strategy, roadmap priority, product metric definition, or business outcome decision is required.
- Hand off to `product-owner` when backlog ownership, scope authority, product-level acceptance, or delivery readiness sign-off is required.
- Hand off to `business-analyst` when business owner identity, business rule ownership, value case, or process authority is unclear.
- Hand off to `data-engineer` when DWH design, pipeline construction, lineage tracking, freshness SLA implementation, or industrial data contracts are required.
- Hand off to `product-analyst` when product metrics interpretation, experiment design, funnel analysis, or behavioral insight is required.
- Hand off to `devops-sre` when infrastructure design, deployment, monitoring implementation, or incident response is required.

## Handoff Payload

```md
To: <role>
Task: <specific task>
Context: <decision or risk that triggered the handoff>
Inputs: <data, links, definitions, constraints>
Expected artifact: <what to return>
Acceptance criteria: <how readiness will be checked>
```
