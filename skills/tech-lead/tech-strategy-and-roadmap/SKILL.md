---
name: tech-strategy-and-roadmap
description: Use when the team needs a documented technical direction — current architectural state, target state, gap analysis, and an ordered list of technical investments. Covers engineering roadmap creation, communicating technical trade-offs to product and management, and maintaining the roadmap as a living document.
family: method
profile_level: Senior+
---

# Tech Strategy and Roadmap

## Purpose

Give the team and its stakeholders a shared, written picture of where the technical foundation is now, where it needs to go, and in what order. Replace ad-hoc engineering decisions with a reasoned directional arc that survives personnel changes and product pivots.

## Use When

- The team lacks a shared understanding of its technical direction for the next one to four quarters.
- Technical debt, architectural drift, or reliability problems are accumulating faster than they are being paid off.
- Product is asking for a roadmap input from engineering and the team has no documented technical priorities.
- A significant new capability or platform change is being proposed and the team needs to reason about sequencing.
- Returning from a major incident and deciding what structural changes to make.

## Do Not Use When

- The request is about system-wide or cross-product architecture → handoff to `system-architect`.
- The request is about product prioritization or feature sequencing → handoff to `product-manager`.
- The request is about a single architectural decision record → use `architecture-decision-records`.
- The request is about categorizing and scheduling specific debt items → use `tech-debt-management`.

## Inputs

- Current architectural state: codebase topology, known debt, reliability data, team throughput metrics.
- Business and product context: upcoming capabilities, growth targets, compliance requirements.
- Team constraints: headcount, skill mix, capacity, delivery commitments.
- Signals from incidents, postmortems, and code review patterns.
- Input from system-architect on platform-level constraints and NFR targets.

## Workflow

1. Describe the current state in one page. Name the architectural elements, their known weaknesses, and the cost of those weaknesses in delivery speed, reliability, or maintainability. Use concrete data: incident count, deployment frequency, time to onboard a new engineer.
2. Define the target state for the planning horizon (one to four quarters). Write it as observable properties, not abstract aspirations. Example: "Any engineer can deploy a service independently in under 10 minutes" rather than "improve DevEx."
3. Identify the gap between current and target state. List the capabilities, refactors, or infrastructure changes needed to close each dimension of the gap.
4. Prioritize the gap items on two axes: impact (how much does this unblock delivery or reduce risk) and effort (quarters of team capacity). Use a 2×2 matrix. Be explicit about what you are not doing and why.
5. Sequence the roadmap. Identify hard dependencies: item B cannot start until item A ships. Surface these as constraints, not preferences.
6. Write the trade-off memo: what gets slower, more expensive, or riskier if the roadmap is not funded. One paragraph per major risk. This is the artifact that surfaces engineering constraints to product and leadership.
7. Review the roadmap with system-architect for alignment on platform-level constraints. Review with product-manager for feasibility against product delivery commitments. Adjust after each review.
8. Publish the roadmap in a shared location (Confluence, Notion, repo wiki) with a dated version and a review cadence (quarterly). Do not let it become a one-off document.

## Outputs

- Technical direction document: current state, target state, gap analysis.
- Engineering roadmap: ordered list of investments with owners, effort estimates, and expected outcomes.
- Trade-off memo: risks if investments are deferred, for stakeholder communication.
- Review calendar: who reviews the roadmap and when.

## Named Patterns

### Good — Observable target state
"In Q3, any engineer on the team can deploy a service change independently, without a senior review gate, in under 15 minutes from merge. Measured by: deploy pipeline duration P95, number of deploy approvals required per week."
Concrete, measurable, time-bound.

### Bad — Abstract aspiration
"Improve our architecture to be more scalable and maintainable."
No measurement, no owner, no timeline. Cannot be reviewed at end of quarter.

### Good — Gap with evidence
"Current: 3 of 5 services share a monolithic PostgreSQL schema. Adding a feature to Service A requires a migration that touches Service B's tables. Average cost per feature: 2 days of schema coordination. Target: each service owns its schema. Gap: schema decomposition for shared tables over 2 quarters."
The gap is grounded in observed cost, not opinion.

### Bad — Gap without cost
"We should separate the database schemas."
No evidence of impact. Product will not fund it.

### Good — Trade-off memo
"If we defer the observability investment to Q4: we will continue to resolve incidents by log reading, adding 4–8 hours per P1. We estimate 2–3 P1s per quarter. Cost of deferral: 8–24 engineering-hours and one on-call burnout risk per quarter."
Product can now make an informed decision.

### Bad — Engineering tells product "trust us"
"This needs to be done. It's important." No quantification, no explicit trade-off. Product rationally deprioritizes.

### Good — Roadmap with hard dependencies
"Step 1: Extract payment service (Q1). Step 2: Introduce event bus (Q2, requires step 1). Step 3: Migrate order service to async (Q3, requires step 2)."
Sequence is non-negotiable because the dependencies are real. Product sees why it cannot be reordered.

### Bad — Roadmap as a wish list
All items at "high priority". No dependencies. No sequencing rationale. Product picks by intuition.

### Good — Quarterly review artifact
"Roadmap v1.3, reviewed 2026-04-01. Item 'schema decomposition' moved from Q2 to Q3 after Q1 incident work consumed capacity. Item 'observability baseline' promoted to Q2 after P1 resolution time exceeded SLO."
Roadmap is a living document. Drift is tracked, not hidden.

### Bad — Roadmap updated never after creation
Created in January, never updated. By April it is fiction. Engineers stop referencing it.

## Boundaries

- Owns team-level technical direction and engineering roadmap within the team or domain.
- Does not own system-wide or platform-level architecture → `system-architect`.
- Does not own product roadmap or feature sequencing → `product-manager`.
- Does not own the detailed debt payoff schedule → `tech-debt-management`.
- Does not own a single architectural decision record → `architecture-decision-records`.

## Sources

### Priority 1 — Leadership canon
- Will Larson: An Elegant Puzzle — Stripe Press, 2019. Chapters on technical strategy, team sizing, and debt management.
- Will Larson: Staff Engineer — Larson, 2021. Technical strategy documents and staff-plus influence.
- Camille Fournier: The Manager's Path — O'Reilly, 2017. Engineering direction-setting at tech lead and director level.

### Priority 2 — Orientation
- Tanya Reilly: The Staff Engineer's Path — O'Reilly, 2022. Technical vision documents, cross-team influence.
- Martin Fowler: Technical Debt — https://martinfowler.com/bliki/TechnicalDebt.html
- DORA State of DevOps Reports — https://dora.dev/research/ (delivery metrics as current-state signals).

### Priority 3 — Background
- LeadDev: Engineering strategy content — https://leaddev.com/
- Gergely Orosz: The Pragmatic Engineer Newsletter — https://newsletter.pragmaticengineer.com/

## Handoff

- System-wide or cross-product architecture → `system-architect`.
- Product roadmap, feature sequencing, product prioritization → `product-manager`.
- Specific debt items and their payoff schedule → `tech-debt-management`.
- Individual architectural decisions → `architecture-decision-records`.
- Delivery schedule and governance → `project-manager`.
