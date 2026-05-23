# Product Manager Interaction Map

## Machine-readable connection map

```yaml
connections:
  - role: product-owner
    weight: 5
    interaction: Roadmap intent, backlog priority context, MVP scope, product hypothesis handoff, acceptance criteria framing.
  - role: product-analyst
    weight: 5
    interaction: Success metric definition, experiment planning, result interpretation, opportunity signals, decision rules.
  - role: ui-ux-designer
    weight: 5
    interaction: User problem framing, discovery planning, prototype learning, user journey alignment, usability risk.
  - role: system-analyst
    weight: 4
    interaction: Product scope handoff, expected outcome, technical constraints, open product questions for specification.
  - role: leadership-business-owner
    weight: 4
    interaction: Business goals, strategic direction, investment decisions, OKR alignment, product result reporting.
  - role: tech-lead
    weight: 4
    interaction: Feasibility constraints, effort sizing, technical debt trade-offs, platform risk, discovery feasibility check.
  - role: project-manager
    weight: 3
    interaction: Delivery constraints, launch timeline, scope trade-offs, risk context, milestone dependencies.
  - role: marketing-growth
    weight: 3
    interaction: Go-to-market context, launch timing, positioning input, channel feedback, growth loops.
  - role: sales-account-cs-support
    weight: 3
    interaction: Market feedback, customer signals, churn drivers, adoption barriers, NPS/CSAT patterns.
  - role: system-architect
    weight: 2
    interaction: Platform constraints, non-functional requirements, architectural risks affecting product decisions.
  - role: qa-engineer
    weight: 2
    interaction: Product-level acceptance criteria, launch readiness, post-launch quality signals.
  - role: devops-sre
    weight: 2
    interaction: Release readiness signals, rollout strategy feasibility, incident impact on product outcome.
```

## Receives Tasks From

| Sender | Typical request |
|---|---|
| Leadership / business owner | Product direction, business goal, investment question, or strategic trade-off. |
| Product Owner | Roadmap decision, product priority, hypothesis, metric, or scope trade-off needing product ownership. |
| Product Analyst | Metric findings, experiment readout, opportunity signal, or risk in interpretation. |
| UX/UI | Discovery finding, user problem, prototype learning, or experience trade-off. |
| Tech Lead / Engineering | Feasibility risk, tech debt trade-off, platform constraint, or product impact question. |
| Marketing / Sales / Support | Market feedback, launch need, customer signal, churn driver, or positioning concern. |

## Aligns With

| Role | Alignment topic |
|---|---|
| Product Owner | Roadmap intent, backlog priority context, MVP, scope trade-off, handoff to delivery. |
| Product Analyst | Metrics, hypothesis, experiment design, result interpretation, product recommendation. |
| UX/UI | Customer problem, discovery plan, prototype learning, user journey, usability risk. |
| System Analyst | Product scope, expected outcome, technical constraints, specification handoff. |
| Project Manager | Delivery constraints, risks, date trade-offs, dependencies, and status context. |
| Marketing / Sales / Customer Success | Launch, positioning, customer feedback, commercial signals, adoption barriers. |

## Sends Artifacts To

| Receiver | Artifact |
|---|---|
| Product Owner | Product brief, roadmap item, product priority, hypothesis, metric, MVP context. |
| Product Analyst | Product question, success metric, experiment need, decision rule. |
| UX/UI | User problem, opportunity brief, discovery objective, product constraints. |
| System Analyst | Product scope, expected outcome, constraints, open questions. |
| Project Manager | Product priority, launch intent, scope trade-off, delivery risk context. |
| Leadership / stakeholders | Strategy, roadmap, product result, recommendation, post-launch learning. |

## Can Assign Tasks To

- Product Owner: create delivery-ready backlog items and product-level acceptance criteria.
- Product Analyst: validate metrics, design experiments, interpret impact, and produce analytical synthesis.
- UX/UI: research user problem, prototype solution, or assess usability.
- System Analyst: detail requirements, API contracts, data models, and integration implications.
- Project Manager: plan dates, resources, dependencies, risks, and delivery status.
- Marketing / Sales / Support: provide go-to-market context, customer feedback, and operational readiness.

## Must Hand Off When

- Backlog refinement, scope details, or delivery readiness are required → `product-owner`.
- Delivery plan, dates, budget, resources, risks, status, or escalation are required → `project-manager`.
- System specification, API, data model, or integration detail is required → `system-analyst`.
- Experiment statistical design, dashboard, or metric methodology is required → `product-analyst`.
- UX solution, prototype, or design-system decision is required → `ui-ux-designer`.
- Test strategy, regression, or release quality ownership is required → `qa-engineer`.
- Platform architecture, technical standards, or engineering estimates are required → `system-architect` / `tech-lead`.

## Handoff Format

```md
To: <subagent>
Task: <specific task>
Context: <decision or risk>
Inputs: <data, links, definitions, constraints>
Expected artifact: <what should be returned>
Acceptance criteria: <how readiness will be checked>
```
