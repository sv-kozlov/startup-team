---
name: architectural-risk-and-technical-debt
description: Use when identifying SPOFs, excessive coupling, architectural risks, and technical debt — building a prioritized debt registry, assessing architectural reach and business impact of each item, and defining a mitigation roadmap that fits delivery realities. Not for delivery prioritization, code-level refactoring, or incident response.
family: method
profile_level: Senior+
---

# Architectural Risk and Technical Debt

## Purpose

Identify, classify, and prioritize architectural risks and technical debt, and define a mitigation roadmap that is actionable in delivery. Produce a risk register and debt registry that are honest about SPOF, coupling, and fragility — and that connect each item to an architectural impact, an owner, and a revisit trigger.

## Use When

- A system shows recurring incidents, scaling limits, or change friction tied to architecture.
- SPOFs, excessive coupling, hidden dependencies, or fragile integrations must be mapped before planning a significant change.
- A technical-debt registry must be created or refreshed for architecture governance or delivery planning.
- Mitigation must be prioritized against business value, risk, and delivery capacity.
- A pre-migration risk assessment is needed before a target/transition architecture is baselined.
- Fitness functions must be defined to detect when debt or risk crosses an unacceptable threshold.

## Do Not Use When

- The task is executing code-level refactoring or operational fixes → handoff to `tech-lead` / engineering / `devops-sre`.
- The task is running incident response or postmortem facilitation → handoff to `devops-sre`.
- The task is prioritizing the product backlog or product roadmap → handoff to `product-manager` / `product-owner`.
- The task is security audit, vulnerability scanning, or penetration testing → handoff to `security-engineer`.
- The task is delivery planning (dates, resources, sprint allocation) → handoff to `project-manager`.

## Inputs

- Incident history, change-failure rate, postmortem patterns, and defect clustering.
- Current architecture (components, integrations, data flows), existing debt notes, and ADRs.
- Product and delivery roadmap with capacity context and upcoming major changes.
- Operational data: latency spikes, scaling incidents, error rates, deployment failure patterns.
- Stakeholder input on pain points and constraints.

## Workflow

1. **Inventory candidate risks and debt items.** Collect from: postmortem action items, engineering team retrospectives, architecture review findings, DORA metrics trends (deployment frequency, change failure rate, MTTR). Each item gets an evidence reference, not just an opinion.
2. **Classify each item.** Categories: SPOF (single point of failure), Coupling (shared database, circular dependency, tight synchronous chain), Capacity (at-limit scaling path), Security (trust boundary gap, unaudited path), Observability (dark component, missing trace coverage), Integration (brittle contract, undocumented dependency), Data (consistency model violation, unbounded table, data migration debt), Lifecycle (end-of-life component or library).
3. **Assess architectural reach.** For each item: how many components or teams are affected? Is the item localized (one service) or systemic (cross-domain)? Can it be resolved incrementally or does it require a coordinated migration?
4. **Score likelihood and impact.** Simple 3×3 matrix: likelihood (low/medium/high based on frequency of related incidents or proximity to scaling limit), impact (low = one team, medium = one domain, high = cross-domain or user-visible). Priority = likelihood × impact.
5. **Define fitness functions for high-priority items.** A fitness function is an automated check that detects when a risk threshold is crossed. Examples: "no direct cross-schema queries" checked in CI; "p99 latency on /checkout < 300ms" monitored in production; "no service has > 5 synchronous upstream dependencies" validated by architecture test.
6. **Propose mitigation options.** For each high-priority item: at least two options (quick-fix vs structural fix), effort estimate, reversibility (can it be done incrementally?), and risk introduced by the mitigation itself.
7. **Align with delivery and product owners.** Architectural debt reduction competes with feature work. Present the risk register with business impact framing (e.g., "this SPOF caused 3 P1 incidents last quarter totaling 4 hours downtime"). Agree on capacity allocation and revisit cadence.
8. **Record in ADRs where mitigation involves an architectural decision.** The debt registry is a living document; mitigation decisions that change the target architecture go into ADRs.

## Outputs

- Architectural risk register: item, category, likelihood, impact, priority, owner, mitigation options.
- Technical debt registry: item, component/domain scope, architectural reach, effort estimate, mitigation plan.
- Fitness function definitions for high-priority risks.
- Mitigation roadmap with priorities, options, and trade-offs.
- Handoff items for engineering / `tech-lead` (implementation), `devops-sre` (operational fixes), `security-engineer` (security audit items), `project-manager` (delivery sequencing).

## Named Patterns

### Good — Risk item with evidence and fitness function
```
Risk-07: Single point of failure — OrderDB
Category: SPOF
Evidence: 3 P1 incidents in Q1 caused by OrderDB primary failure; MTTR avg 47 min.
Likelihood: High (primary failure 3× per quarter)
Impact: High (all order flows blocked)
Fitness function: Automated failover test monthly; recovery time target ≤ 5 min.
Mitigation option A: Read replica promotion automation (2 sprint effort, reversible).
Mitigation option B: Active-active multi-region setup (8 sprint effort, high complexity).
Recommended: Option A as immediate mitigation; Option B in H2 roadmap pending capacity.
```

### Bad — Debt item as a vague note
```
Tech debt: "the order module is a mess"
```
No classification, no evidence, no scope, no owner. Cannot be prioritized, cannot be resolved, cannot be measured.

### Good — Fowler debt quadrant applied
Martin Fowler's quadrant: Reckless/Deliberate, Reckless/Inadvertent, Prudent/Deliberate, Prudent/Inadvertent.
```
ADR-021 shared DB exception:
Quadrant: Prudent/Deliberate — accepted as time-bounded exception with expiry 2026-09-01.
Action: Promote to migration task in Q3 backlog with owner assigned.
```

### Bad — All debt treated equally
A 30-item debt list with no quadrant, no priority, and no owner. Every sprint the list grows. Nobody resolves anything because there is no agreement on what matters.

### Good — Coupling risk with architectural reach
```
Risk-12: Synchronous call chain — Checkout → Inventory → Pricing → Discount → Tax
Reach: 5 services, 3 teams, p99 additive latency = 620ms at current load.
Scaling limit: At 2× current RPS, chain p99 exceeds 1s SLO.
Mitigation: Convert Pricing and Discount to async pre-computation; Tax to cached lookup.
Fitness function: No synchronous chain > 3 hops in critical path (CI architecture test).
```

### Bad — Invisible coupling
Five services call each other synchronously. Nobody has mapped the chain. Load test reveals the cascade only at 1.5× production load, one week before a major launch.

## Boundaries

- Does not own delivery prioritization or product roadmap → `product-manager` / `product-owner`.
- Does not run code-level refactoring, operational fixes, or incident response → engineering / `devops-sre`.
- Does not own security audit, penetration test, or vulnerability management programs → `security-engineer`.
- Does not own sprint allocation or resource planning → `project-manager`.

## Sources

### Priority 1 — Canonical References
- Software Engineering Institute — Technical Debt overview: https://www.sei.cmu.edu/our-work/projects/display.cfm?customel_datapageid_4050=21536
- SEI — Architecture Tradeoff Analysis Method (ATAM): https://resources.sei.cmu.edu/library/asset-view.cfm?assetid=513908
- Martin Fowler — TechnicalDebtQuadrant: https://martinfowler.com/bliki/TechnicalDebtQuadrant.html
- Neal Ford et al. — Building Evolutionary Architectures (fitness functions): https://evolutionaryarchitecture.com/

### Priority 2 — Practitioner Guidance
- Google SRE Workbook — Managing Risk and Error Budgets: https://sre.google/workbook/managing-risk/
- AWS Well-Architected reliability pillar — failure management: https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/failure-management.html
- DORA metrics — deployment frequency, change failure rate, MTTR: https://dora.dev/

### Priority 3 — Supplementary
- ThoughtWorks Tech Radar — fitness function–driven development: https://www.thoughtworks.com/radar/techniques/fitness-function-driven-development
- InfoQ — technical debt and architecture quality articles: https://www.infoq.com/technical-debt/

## Handoff

- Code-level refactoring and implementation of mitigation items → `tech-lead` / engineering.
- Operational fixes (infrastructure, monitoring, runbooks) → `devops-sre`.
- Security audit items → `security-engineer`.
- Delivery sequencing of mitigation roadmap → `project-manager`.
- Recording mitigation decisions that change target architecture → `architecture-decision-records`.
