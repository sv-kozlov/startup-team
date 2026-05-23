# Interaction Map — Product Analyst

```yaml
weight_scale:
  5: critical
  4: regular
  3: periodic
  2: consultative
  1: rare

connections:
  - role: product-manager
    weight: 5
    interaction: "Success metrics, hypothesis framing, experiment decisions, roadmap evidence, feature impact, opportunity sizing."
    boundary: "Owns product strategy, roadmap, and final launch/cancel decision. Product analyst owns evidence and recommendation."

  - role: data-engineer
    weight: 4
    interaction: "Source tables, DWH freshness, lineage, data contracts, pipeline SLAs, data quality escalations."
    boundary: "Owns DWH, ETL, and production data infrastructure. Product analyst specifies requirements and diagnoses quality issues."

  - role: system-analyst
    weight: 4
    interaction: "Event tracking requirements, event parameter definitions, system constraints, data shape, integration context."
    boundary: "Owns system specification and API design. Product analyst owns analytical event semantics and tracking spec."

  - role: product-owner
    weight: 3
    interaction: "Backlog scope, product-level acceptance criteria, delivery readiness constraints, analytical input for prioritization."
    boundary: "Owns backlog and delivery readiness. Product analyst provides data-backed prioritization input."

  - role: frontend-developer
    weight: 3
    interaction: "Client-side event instrumentation, UI state tracking, experiment exposure logging, A/B flag parameters."
    boundary: "Owns implementation. Product analyst owns event specification and instrumentation acceptance criteria."

  - role: backend-developer
    weight: 3
    interaction: "Server-side events, business logic sources, feature flags, error states, experiment assignment."
    boundary: "Owns implementation. Product analyst owns event spec and analytical interpretation."

  - role: qa-engineer
    weight: 3
    interaction: "Analytics event validation, tracking test scenarios, instrumentation defects, experiment exposure QA."
    boundary: "Owns QA strategy and release regression. Product analyst owns analytics acceptance criteria."

  - role: ui-ux-designer
    weight: 3
    interaction: "User journey maps, UX hypotheses, behavioral analysis results, funnel-informed design input."
    boundary: "Owns UX solution and qualitative research. Product analyst provides quantitative behavioral context."

  - role: data-scientist
    weight: 3
    interaction: "ML product metrics, online experiment design for ML features, scoring/uplift framing, model impact evaluation handoff."
    boundary: "Owns model training, feature engineering, and ML quality. Product analyst owns product-facing metric and online evaluation spec."

  - role: business-analyst
    weight: 2
    interaction: "Business context, process rules, expected business effect, alignment on business metric definitions."
    boundary: "Owns business process modeling and BA artifacts. Product analyst owns product metric system and behavioral analytics."

  - role: data-bi-analyst
    weight: 2
    interaction: "Metric definitions, data mart alignment, dashboard ownership, recurring reporting coordination."
    boundary: "Owns enterprise BI semantic layer and governed reporting. Product analyst owns product analytics and feeds requirements."

  - role: project-manager
    weight: 2
    interaction: "Analytics delivery dates, experiment launch risk, data readiness dependencies, sprint-level analytical capacity."
    boundary: "Owns delivery governance, schedule, and resource allocation. Product analyst surfaces analytical risks and dependencies."

  - role: executive-leadership
    weight: 1
    interaction: "Strategic findings, growth quality, unit economics, forecast framing, risk interpretation."
    boundary: "Owns strategic decisions. Product analyst provides evidence and framing, not decisions."
```
