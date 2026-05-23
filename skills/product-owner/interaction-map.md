---
role: product-owner
updated: 2026-05-23
---

# Product Owner Interaction Map

## Communication Map

```yaml
connections:
  - role: product-manager
    weight: 5
    interaction: Receives product direction, roadmap items, and strategic decisions; escalates open product decisions; routes strategy questions back.
  - role: engineering-team
    weight: 5
    interaction: Delivers ordered backlog, sprint goal, and acceptance criteria; answers product intent questions; accepts or rejects sprint deliverables.
  - role: tech-lead
    weight: 5
    interaction: Collaborates on decomposition, feasibility, technical risks, and tech debt; receives engineering blockers; routes cycle time signals.
  - role: qa-engineer
    weight: 5
    interaction: Provides product-level acceptance criteria; receives QA feedback on AC quality; aligns on release readiness and defect classification.
  - role: system-analyst
    weight: 4
    interaction: Hands off product scope for system specification; receives API and data constraints; aligns on DoR for system-dependent stories.
  - role: business-analyst
    weight: 4
    interaction: Aligns on business rules, process context, and regulatory requirements; routes process-level scope questions.
  - role: ui-ux-designer
    weight: 4
    interaction: Aligns on user flows, design scope, and prototype readiness; confirms UX dependencies for DoR.
  - role: product-analyst
    weight: 4
    interaction: Receives metrics context and experiment signals; routes analytics and hypothesis ownership; hands off post-release data questions.
  - role: project-manager
    weight: 3
    interaction: Aligns on delivery timeline, dependency governance, and release calendar; routes delivery blockers and escalation.
  - role: business-stakeholder
    weight: 3
    interaction: Communicates scope, priorities, trade-offs, and release content; receives scope requests; routes strategic decisions to product-manager.
  - role: domain-expert
    weight: 3
    interaction: Consults on domain rules, regulatory constraints, and solution validation for scope decisions.
  - role: adjacent-product-teams
    weight: 3
    interaction: Synchronizes on cross-team dependencies, shared scope boundaries, and release coordination.
  - role: devops-sre
    weight: 2
    interaction: Receives infrastructure and reliability constraints relevant to release scope; routes operational decisions.
  - role: data-scientist-ml
    weight: 2
    interaction: Routes ML feature scoping and model constraint questions; accepts ML capability context for backlog.
  - role: technical-writer
    weight: 2
    interaction: Provides product context for user documentation; routes documentation ownership.
  - role: security-compliance
    weight: 2
    interaction: Aligns on security and regulatory constraints affecting scope and acceptance criteria.
```

## Receives Tasks From

| Sender | Typical request |
|---|---|
| Product Manager | Convert roadmap item, product initiative, or hypothesis into backlog and delivery-ready scope. |
| Business stakeholder | Clarify scope, expected behavior, acceptance conditions, and product-side trade-offs. |
| Tech Lead / Engineering | Clarify product intent, priority, acceptance conditions, constraints, and readiness. |
| System Analyst / Business Analyst | Align business or system requirements with product scope and backlog priority. |
| QA | Clarify product-level acceptance and release readiness before regression. |

## Aligns With

| Role | Alignment topic |
|---|---|
| Product Manager | Roadmap intent, product goal, priority decisions, and final product call. |
| Project Manager / Delivery Manager | Release scope, delivery risks, dependencies, status, escalation, and timeline constraints. |
| System Analyst | Functional behavior, API constraints, data requirements, and developer-ready specification. |
| Business Analyst | Business rules, process variants, stakeholder constraints, and regulatory requirements. |
| UX/UI Designer | User flow, prototype scope, usability constraints, and design readiness for DoR. |
| Product Analyst | Metrics context, experiment evidence, tracking needs, and post-release analytics signals. |

## Sends Artifacts To

| Receiver | Artifact |
|---|---|
| Engineering / Tech Lead | Ordered backlog, sprint goal, scope brief, acceptance criteria, open questions. |
| QA | Product-level acceptance criteria, release scope note, defect severity classification. |
| System Analyst | Product scope and expected behavior for system specification input. |
| Project Manager / Delivery Manager | Scope baseline, change log, readiness signal, delivery blockers. |
| Product Manager | Backlog state, trade-off options, open product decisions requiring PM authority. |

## Can Assign Tasks To

- System Analyst: detail system behavior, API, data, integration, or non-functional constraints.
- Business Analyst: clarify business rules, process variants, or stakeholder constraints.
- Product Analyst: validate metric impact, experiment evidence, or tracking requirements.
- UX/UI Designer: refine user flow, prototype detail, or interaction specification.
- QA: design test approach, regression scope, and release quality plan.
- Project Manager / Delivery Manager: plan dates, dependencies, status tracking, and escalation.

## Must Hand Off When

- Product strategy, roadmap priority, product bet, or final launch decision is required → hand off to `product-manager`.
- Delivery plan, dates, budget, resource allocation, dependency governance, or escalation → hand off to `project-manager`.
- API contracts, data models, integration specs, or technical specifications → hand off to `system-analyst`.
- Business process, policy, or business rule ownership → hand off to `business-analyst` or process analyst.
- Test strategy, test cases, or regression ownership → hand off to `qa-engineer`.
- Metrics methodology, experiment design, dashboard ownership, or analytics conclusions → hand off to `product-analyst`.
- UX flow, wireframe, prototype, or design system ownership → hand off to `ui-ux-designer`.
- Architecture decisions, NFR definition, or engineering technical choices → hand off to `system-architect` or `tech-lead`.
- Infrastructure, CI/CD, deployment, monitoring, or incident response → hand off to `devops-sre`.

## Handoff Format

```md
To: <subagent>
Task: <specific task>
Context: <decision or risk>
Inputs: <data, links, definitions, constraints>
Expected artifact: <what should be returned>
Acceptance criteria: <how readiness will be checked>
```
