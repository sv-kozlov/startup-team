# Interaction Map

## Communication Map

```yaml
connections:
  - role: product-manager
    weight: 5
    interaction: Receives product goals, user problems, hypotheses, constraints, and direction decisions. Sends design direction, UX risks, hypothesis framing, and trade-off rationale.
  - role: product-owner
    weight: 4
    interaction: Receives backlog scope, acceptance context, and delivery readiness questions. Sends UX scope definition, state coverage notes, handoff readiness, and acceptance notes.
  - role: frontend-developer
    weight: 5
    interaction: Receives feasibility questions, component constraints, and shadcn/ui context. Sends design specs, layouts, components, token mapping, state notes, and responsive behavior.
  - role: system-analyst
    weight: 4
    interaction: Receives system states, API behavior, error taxonomy, and integration constraints. Sends UI state requirements, data/status/error behavior questions, and system-event annotations.
  - role: product-analyst
    weight: 4
    interaction: Receives funnel data, behavioral signals, and experiment inputs. Sends UX hypotheses, measurement needs, expected behavior changes, and iteration direction.
  - role: qa-engineer
    weight: 4
    interaction: Receives expected UI behavior questions and visual defect reports. Sends state coverage specs, visual acceptance notes, accessibility checklists, and edge-case behavior.
  - role: business-analyst
    weight: 3
    interaction: Receives business rules, stakeholder constraints, and user role context. Sends terminology questions, rule ambiguity, and scenario clarifications.
  - role: ux-researcher
    weight: 3
    interaction: Receives research insights, usability findings, and participant evidence. Sends research questions, prototype for test, and evidence gap handoffs.
  - role: design-system-lead
    weight: 3
    interaction: Receives component usage guidance, pattern alignment, and contribution decisions. Sends component gap requests, token governance questions, and pattern contribution briefs.
  - role: mobile-developer
    weight: 3
    interaction: Receives platform-specific feasibility questions. Sends adaptive layout specs, platform-specific interaction notes, and touch target requirements.
  - role: project-manager
    weight: 2
    interaction: Receives design readiness, dependency, and risk questions. Sends handoff date estimates, dependency flags, and blocker notifications.
  - role: brand-communication-designer
    weight: 2
    interaction: Receives visual consistency guidance and brand constraints. Sends alignment questions for visual elements at the product/brand boundary.
```

## Receives Tasks From

| Subagent / Role | Typical tasks |
|---|---|
| Product Manager | Product problem, hypothesis, user outcome, design exploration, trade-off decision. |
| Product Owner | Backlog item UX scope, acceptance context, readiness questions, UI clarification. |
| Product Analyst | Funnel issue, behavioral signal, experiment input, UX metric concern. |
| Business Analyst | Business process, business rule, stakeholder constraint, user role context. |
| System Analyst | System states, API/data limits, error behavior, integration constraint. |
| UX Researcher | Research insight, usability issue, participant evidence, user need. |
| Design System Lead | Component usage, pattern alignment, contribution request, consistency issue. |
| Frontend Developer | Feasibility question, state clarification, responsive behavior, shadcn/ui component mapping. |
| QA Engineer | Expected UI behavior, state coverage gap, visual defect, accessibility risk. |
| Project Manager | Design readiness, dependency, risk, handoff date. |

## Aligns With

| Subagent / Role | Topics |
|---|---|
| Product Manager | User outcome, product goal, metric intent, trade-off, priority signal. |
| Product Owner | Scope, backlog readiness, acceptance criteria, delivery boundaries. |
| Product Analyst | Metrics, funnel evidence, experiment framing, behavior signals. |
| Business Analyst | Business process, rules, roles, policy constraints, terminology validation. |
| System Analyst | Data states, API limits, integration behavior, edge cases, error taxonomy. |
| UX Researcher | Research plan input, usability findings, user needs, evidence limits. |
| Design System Lead | Components, semantic tokens, patterns, contribution rules, governance boundaries. |
| Frontend Developer | Responsive behavior, component feasibility, shadcn/ui composition, token implementation. |
| QA Engineer | UI states, expected behavior, accessibility checks, acceptance risks. |
| Brand / Communication Designer | Visual consistency, tone, imagery, product/brand boundary. |

## Sends Artifacts To

| Receiver | Artifacts |
|---|---|
| Product Manager | Design direction, variants, UX risks, hypothesis framing, user-impact rationale. |
| Product Owner | UX scope, state coverage, acceptance notes, handoff readiness. |
| Product Analyst | UX hypothesis, measurement needs, expected behavior changes, iteration direction. |
| Business Analyst | Scenario questions, terminology ambiguity, rule clarification requests. |
| System Analyst | UI state requirements, data/status/error behavior needs, integration constraint questions. |
| UX Researcher | Research questions, prototype for test, observed usability risks, evidence gap handoffs. |
| Design System Lead | Component gap requests, pattern proposals, token governance questions, contribution briefs. |
| Frontend Developer | Design specs, layouts, component mapping, token brief, responsive notes, state annotations. |
| QA Engineer | State coverage specs, visual acceptance notes, edge cases, accessibility checklists. |
| Mobile Developer | Adaptive layout specs, platform-specific interaction notes, touch target requirements. |

## Can Assign Tasks To

| Receiver | Example tasks |
|---|---|
| Product Manager | Decide product priority, target outcome, or trade-off. |
| Product Owner | Clarify backlog scope, acceptance criteria, or delivery readiness. |
| Product Analyst | Validate metric baseline, define success signal, plan A/B, interpret effect. |
| Business Analyst | Clarify business rule, role, process, policy, or exception. |
| System Analyst | Specify API/data/status/error behavior or integration constraint. |
| UX Researcher | Plan or run user research, recruit participants, synthesize findings. |
| Design System Lead | Approve new component, token, pattern, or system contribution. |
| Frontend Developer | Confirm feasibility, implement UI, map design to code component. |
| QA Engineer | Build test cases from state matrix, validate states, report visual defects. |
| Brand / Communication Designer | Provide identity, tone, or external communication guidance at the product/brand boundary. |

## Handoff Rules

- Hand off to Product Manager when product strategy, roadmap, priority, or final product direction is required.
- Hand off to Product Owner when backlog scope, product-level acceptance criteria, or delivery readiness must be decided.
- Hand off to Project Manager when delivery dates, resources, dependencies, status, escalation, or delivery governance are required.
- Hand off to Product Analyst when metric definition, A/B methodology, event tracking, experiment interpretation, or quantitative conclusion is required.
- Hand off to Business Analyst when business process, policy, stakeholder intent, rule, or terminology is unclear.
- Hand off to System Analyst when system requirements, API, integration, data model, error taxonomy, or developer-ready specification is required.
- Hand off to UX Researcher when formal research design, recruiting, moderated sessions, or large-scale synthesis is required.
- Hand off to Design System Lead when a component, token, pattern, contribution model, versioning, or governance decision affects the design system.
- Hand off to Frontend Developer when production implementation, architecture, performance, or code-level component decisions are required.
- Hand off to QA when test strategy, test cases, regression, defect lifecycle, or release quality decision is required.
- Hand off to Brand / Communication Design or Marketing when identity, campaign, SMM, promo, or external communication ownership is required.

## Handoff Payload

```md
To: <subagent>
Task: <specific task>
Context: <decision or risk>
Inputs: <data, links, definitions, constraints>
Expected artifact: <what should be returned>
Acceptance criteria: <how readiness will be checked>
```
