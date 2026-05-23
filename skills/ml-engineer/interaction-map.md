# Interaction Map — ML Engineer

```yaml
weight_scale:
  5: critical
  4: regular
  3: periodic
  2: consultative
  1: rare

connections:
  - role: data-engineer
    weight: 5
    interaction: "Data sources, feature schemas, pipeline reliability, point-in-time correctness, data quality SLA."
    boundary: "Owns data platform (DWH, ETL/ELT, warehouse, pipeline SLA). ML engineer writes feature specs and validates correctness; data engineer owns industrial delivery."

  - role: backend-python-developer
    weight: 5
    interaction: "Inference API contract, integration of ML service into the product backend, latency and throughput budgets, error semantics."
    boundary: "Owns general product business logic and backend services. ML engineer owns model logic and the ML serving contract."

  - role: backend-go-developer
    weight: 4
    interaction: "Inference service integration when implemented in Go, API contracts, latency and throughput budgets."
    boundary: "Owns Go-side service implementation. ML engineer owns the model and the ML API contract."

  - role: devops-sre
    weight: 4
    interaction: "Model deployment, GPU/CPU resource allocation, container and K8s configuration, CI/CD for ML, observability stack, on-call runbook."
    boundary: "Owns infrastructure, Kubernetes cluster, CI/CD platform, and on-call rotation. ML engineer defines model requirements and monitoring thresholds."

  - role: product-manager
    weight: 4
    interaction: "ML feature goal, business success criteria, feasibility and risk assessment, AI feature acceptance."
    boundary: "Owns product roadmap and prioritization. ML engineer surfaces technical reality, model constraints, and risk without owning business outcome."

  - role: product-owner
    weight: 4
    interaction: "Backlog refinement on ML items, acceptance criteria for model quality, feature delivery scope."
    boundary: "Owns backlog content and delivery scope. ML engineer clarifies model constraints and estimates."

  - role: product-analyst
    weight: 4
    interaction: "Online A/B experiment design, business-metric interpretation, cohort and segment analysis for model impact evaluation."
    boundary: "Owns product metric interpretation and BI reporting. ML engineer provides model metrics and constraints; joint work on A/B experiment results."

  - role: system-analyst
    weight: 3
    interaction: "Integration contracts, data requirements, API specifications for ML services, edge cases and error semantics."
    boundary: "Owns requirements baseline and system specification. ML engineer clarifies technical ML constraints for the contract."

  - role: qa-engineer
    weight: 3
    interaction: "Test coverage for ML code, golden datasets, regression suites for model behavior, defect triage on model responses."
    boundary: "Owns QA strategy and release-level regression. ML engineer keeps ML code testable and maintains model regression tests."

  - role: system-architect
    weight: 2
    interaction: "ML platform architecture, cross-service contracts involving ML services, NFR for inference services, architectural fitness."
    boundary: "Owns target platform architecture outside the ML service. ML engineer proposes ML-layer design within agreed boundaries."

  - role: ui-ux-designer
    weight: 2
    interaction: "UX for AI features, explainability of model outputs, error and uncertainty states visible to users."
    boundary: "Owns interaction and visual design. ML engineer ensures model outputs and confidence levels support the agreed UX states."

  - role: tech-lead
    weight: 2
    interaction: "Engineering standards, cross-team technical direction, ADR review for ML decisions with broad impact."
    boundary: "Owns team-wide standards and direction. ML engineer owns ML engineering practices within the ML domain."
```
