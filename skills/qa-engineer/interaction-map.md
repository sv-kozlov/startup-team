# Interaction Map — QA Engineer

Machine-readable map of roles the QA engineer interacts with, with weights (1=rare ... 5=critical) and topics.

```yaml
weight_scale:
  5: critical
  4: regular
  3: periodic
  2: consultative
  1: rare

connections:
  - role: developer
    weight: 5
    interaction: "Defect reports, root cause triage, test data setup, automation stability, log analysis, retest coordination."
    boundary: "Developer owns implementation and bug fixes. QA owns defect registration, localization to layer, and retest."

  - role: system-analyst
    weight: 5
    interaction: "Requirements testability review, API contracts, edge cases, negative scenarios, data behavior, acceptance criteria clarification."
    boundary: "System analyst owns requirements baseline, API contracts, and data models. QA verifies testability and returns questions; does not author specs."

  - role: product-owner
    weight: 4
    interaction: "Release risk assessment, critical defect escalation, acceptance sign-off status, residual risk communication."
    boundary: "Product owner defines acceptance criteria and owns release decision. QA provides quality facts, not the go/no-go decision."

  - role: product-manager
    weight: 4
    interaction: "Defect criticality from product value perspective, release risk, feature coverage status."
    boundary: "Product manager owns product strategy, roadmap, and scope. QA surfaces quality facts and escalates blockers."

  - role: tech-lead
    weight: 4
    interaction: "Test architecture alignment, engineering standards for automation code, technical risk surfacing, Definition of Done quality."
    boundary: "Tech Lead owns team engineering standards and technical direction. QA proposes automation architecture within those standards."

  - role: devops-sre
    weight: 3
    interaction: "Test environment provisioning, CI/CD pipeline setup for test stages, log access, environment stability diagnosis."
    boundary: "DevOps/SRE owns CI/CD platform, Kubernetes, and infrastructure. QA owns test execution logic and reports environment issues."

  - role: project-manager
    weight: 3
    interaction: "Release readiness report, blocking defect status, regression schedule, testing timeline."
    boundary: "Project manager owns delivery schedule and resource allocation. QA provides quality status and timeline estimates for test work."

  - role: delivery-manager
    weight: 3
    interaction: "Release readiness, blocker escalation, quality risk communication for delivery decision."
    boundary: "Delivery manager owns delivery governance and go/no-go coordination. QA supplies the quality evidence."

  - role: ui-ux-designer
    weight: 2
    interaction: "UI state verification, error state checks, adaptive layout defects, UX-adjacent defect clarification."
    boundary: "UX/UI designer owns interaction flows, prototypes, and design system. QA verifies implementation against spec and reports discrepancies."

  - role: mobile-developer
    weight: 2
    interaction: "Mobile-specific defects, platform version coverage, offline/online scenario testing, device-level reproduction."
    boundary: "Mobile developer owns platform client implementation. QA owns mobile regression and cross-platform scenario verification."

  - role: frontend-developer
    weight: 2
    interaction: "Frontend defects, browser compatibility issues, e2e test stability, DOM-level test locator stability."
    boundary: "Frontend developer owns client code and component implementation. QA owns functional and e2e coverage of the client."

  - role: security-engineer
    weight: 1
    interaction: "OWASP-scoped defect referrals, security-adjacent test findings that require pen-test follow-up."
    boundary: "Security engineer owns the pen-testing program and remediation. QA may surface OWASP-type issues found during functional testing but does not own the security program."

  - role: data-engineer
    weight: 1
    interaction: "Data pipeline output verification, data quality checks relevant to product features, event schema validation."
    boundary: "Data engineer owns pipeline and warehouse. QA verifies data behavior in the product context, not the pipeline itself."
```

## Interaction Summary Table

| Role | Weight | Primary QA direction | Boundary note |
|---|---|---|---|
| developer | 5 | QA -> Developer: defect reports, test data needs | Developer fixes; QA retests |
| system-analyst | 5 | Bidirectional: requirements clarity <-> testability | SA owns spec; QA verifies |
| product-owner | 4 | QA -> PO: quality facts, release risk | PO owns go/no-go |
| product-manager | 4 | QA -> PM: defect criticality, risk summary | PM owns scope and strategy |
| tech-lead | 4 | Bidirectional: automation standards | TL owns engineering direction |
| devops-sre | 3 | QA -> DevOps: environment needs and pipeline test stages | DevOps owns platform |
| project-manager | 3 | QA -> PM: readiness status, regression timeline | PM owns schedule |
| delivery-manager | 3 | QA -> DM: quality evidence for release | DM owns delivery governance |
| ui-ux-designer | 2 | QA -> Designer: UI defect clarification | Designer owns UX/UI spec |
| mobile-developer | 2 | QA -> Mobile: mobile defects and reproduction | Mobile dev owns client |
| frontend-developer | 2 | QA -> Frontend: client defects, locator issues | Frontend dev owns client code |
| security-engineer | 1 | QA -> Security: OWASP-scoped finding referrals | Security owns pen-test program |
| data-engineer | 1 | QA -> Data: data quality in product context | Data eng owns pipelines |

## Participation Without Ownership

QA participates in the following activities but is not the owner:

- Requirements refinement sessions: QA contributes testability questions; system analyst owns the output.
- Architecture reviews: QA raises testability and observability needs; system architect and tech lead own the decision.
- Sprint planning: QA provides testing scope estimates; project manager or delivery manager owns the plan.
- Production incident post-mortems: QA contributes test coverage gaps view; DevOps/SRE and tech lead own the incident review.
- Acceptance criteria definition: QA verifies testability; product-owner or system analyst authors and owns the criteria.
