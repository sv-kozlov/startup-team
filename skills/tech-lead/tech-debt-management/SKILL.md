---
name: tech-debt-management
description: Use when identifying, classifying, prioritizing, and planning the payoff of technical debt — building a debt register, communicating debt impact to product, and incorporating payoff work into regular planning. Covers the full debt lifecycle from detection to resolution.
family: method
profile_level: Senior+
---

# Tech Debt Management

## Purpose

Make technical debt visible, classified, and planned — so it is paid off at a controlled rate rather than accumulating until it becomes a crisis. Replace "we have a lot of debt" with a register, a prioritized list, and a shared understanding of what each item costs to carry and to fix.

## Use When

- The team mentions "technical debt" frequently but has no register or prioritized list.
- Delivery is slowing and engineers cite debt as a factor, but product has no visibility into the cause.
- A refactoring or migration is being proposed without an explicit cost/benefit case for product and leadership.
- After a major incident where a known debt item contributed to the failure.
- At the start of a planning cycle when engineering needs to negotiate time for improvement work.
- Debt items are being silently absorbed into feature work without explicit tracking.

## Do Not Use When

- The request is about setting team-wide engineering standards to prevent future debt → `engineering-quality-and-standards`.
- The request is about team-level technical direction and roadmap → `tech-strategy-and-roadmap`.
- The request is about a single refactoring PR's review → `code-review-leadership`.
- The request is about infrastructure modernization owned by DevOps/SRE → handoff to `devops-sre`.

## Inputs

- Engineering signals: deployment frequency, change failure rate, time to onboard a new engineer, mean time to understand a module.
- Incident history: recurring issues attributed to specific components or patterns.
- Code health signals: test coverage, cyclomatic complexity, module coupling, build time trends.
- Team retrospective outputs: recurring friction points.
- Product roadmap: upcoming capabilities that will be hindered by specific debt items.

## Workflow

1. Classify debt by category before prioritizing. Use three categories:
   - Intentional debt: a deliberate shortcut taken to hit a deadline, documented at the time. Cost is known.
   - Accidental debt: discovered after the fact — design that seemed fine but did not age well. Cost is emerging.
   - Outdated debt: code that was correct for a previous constraint (framework version, scale, team size) but is now wrong for the current context. Cost is growing.
   Do not treat all debt as equal. Intentional debt with a documented payoff date is different from accidental debt with no owner.

2. Build a debt register. For each item: name, category, affected components, estimated carrying cost (how much does this slow delivery per sprint), estimated fix cost (sprints), discovered date, owner, and status. Use a spreadsheet, a JIRA epic, or a Notion database — the tool matters less than the discipline of maintaining it.

3. Score and prioritize. Use a simple formula: priority = carrying cost × risk × strategic impact. Carrying cost: how much does this item slow the team per sprint (0.5 = half a day per sprint, 2 = two full days per sprint). Risk: probability that this item causes a production incident in the next 90 days (low/medium/high). Strategic impact: does a planned feature become significantly cheaper if this debt is paid? High-carrying-cost, high-risk, strategically-blocking items go to the top.

4. Communicate to product as a trade-off, not as a complaint. For each top-priority debt item: "This item costs us N days per sprint. Over the next two quarters, the cost is M days. Fixing it takes P sprints. If we fix it before Feature X, Feature X delivery is Q% faster." Product can now make an informed trade-off.

5. Negotiate debt capacity in planning. Establish a sustainable rate: typically 15–20% of team capacity per sprint for improvement work (debt payoff, refactoring, dependency upgrades). This is not a tax — it is the maintenance cost of a complex system. Below 10%, debt compounds. Above 30%, delivery stalls without strong justification.

6. Define acceptance criteria for debt payoff. A debt item is closed when: the specific metric that drove its priority has improved, the code change is merged and tested, and the register entry is updated. "Closed when refactored" is not sufficient — closed when the build time for module X drops from 4 minutes to 45 seconds.

7. Track and report. At each sprint review, report: items closed, carrying cost reduced, items added to register. Make debt velocity visible alongside feature velocity. A team that is adding debt faster than it is closing it will slow down — show the data before the slowdown is felt.

## Outputs

- Technical debt register: categorized, scored, and prioritized list.
- Debt trade-off memo per top-priority item: carrying cost, fix cost, strategic impact.
- Debt capacity agreement with product: what percentage of sprint capacity is allocated.
- Sprint debt velocity: items closed and added, carrying cost delta.

## Named Patterns

### Good — Debt register entry
```
ID: DEBT-042
Name: Shared database schema across Order and Payment services
Category: Accidental (discovered Q3 2024)
Affected: order-service, payment-service
Carrying cost: 1.5 days/sprint (migration coordination, schema locks, incident risk)
Fix cost: 6 sprints (schema decomposition + service boundary refactor)
Risk: High (shared schema caused 2 P1s in last 6 months)
Strategic impact: Blocker for Payment v2 feature (Q3 plan)
Owner: @alex
Status: Prioritized for Q2
```
The item is complete enough for a product conversation.

### Bad — Debt as a feeling
"We have a lot of debt in the payment service." No cost, no owner, no priority, no plan. Product cannot fund something with no defined scope or return.

### Good — Debt capacity negotiation
"We are proposing 20% of sprint capacity (2 sprints per quarter) for debt payoff. Based on the register, this rate closes the top 3 items in Q2–Q3. Without this allocation, Feature X will take 40% longer due to item DEBT-042 alone."
Product has a business case to evaluate, not a request to trust engineering.

### Bad — Debt absorbed silently
Developers fix debt inside feature tasks without tracking it. The sprint feels slower and product does not understand why. No register, no visibility, no negotiation.

### Good — Closed debt with evidence
"DEBT-042 closed. Schema decomposed. Schema lock incidents: 0 in 30 days post-fix. Migration coordination time: 0 days/sprint. Payment v2 feature estimate reduced by 3 sprints."
The payoff is demonstrated, not asserted.

### Bad — Debt "closed" by deletion from the list
The item disappears from the register with no evidence of improvement. Three months later the same friction returns.

### Good — Carrying cost formula applied
"Item DEBT-017: outdated auth library. Carrying cost: 0.5 day/sprint (manual patching, no automation). Fix cost: 1 sprint. Over 2 quarters (12 sprints): 6 days carrying cost vs. 1 sprint fix cost. ROI is clear. Recommend fixing in Q2."
Simple arithmetic makes the trade-off obvious.

### Bad — "It's important, trust us"
No carrying cost estimate. No fix cost. Product rationally deprioritizes.

## Boundaries

- Owns the debt register, prioritization, capacity negotiation, and payoff tracking within the team.
- Does not own product prioritization of debt vs. features → that trade-off belongs to `product-manager`.
- Does not own infrastructure-level debt (platform, CI, Kubernetes cluster) → `devops-sre`.
- Does not own the engineering standards that prevent future debt → `engineering-quality-and-standards`.
- Does not own cross-team architectural debt → `system-architect` or `cross-team-technical-alignment`.

## Sources

### Priority 1 — Debt canon
- Martin Fowler: Technical Debt — https://martinfowler.com/bliki/TechnicalDebt.html
- Ward Cunningham: Ward Explains Debt Metaphor — https://wiki.c2.com/?WardExplainsDebtMetaphor
- Will Larson: An Elegant Puzzle — Stripe Press, 2019. Technical debt strategy and management.

### Priority 2 — Orientation
- DORA State of DevOps Reports — https://dora.dev/research/ (change failure rate, lead time as debt signals).
- Gergely Orosz: The Pragmatic Engineer Newsletter — https://newsletter.pragmaticengineer.com/

### Priority 3 — Background
- LeadDev: Technical debt management — https://leaddev.com/
- martinfowler.com: Strangler Fig, Branch by Abstraction patterns — https://martinfowler.com/

## Handoff

- Product prioritization of debt vs. features → `product-manager`.
- Platform and infrastructure debt → `devops-sre`.
- Engineering standards to prevent future debt → `engineering-quality-and-standards`.
- Team-level technical direction that incorporates debt payoff → `tech-strategy-and-roadmap`.
- Cross-team architectural debt → `system-architect`.
