---
name: product-strategy
description: Use when product direction, target segment, value proposition, strategic bets, or product outcome framing must be defined or revisited. Covers problem space definition, market positioning, strategic options analysis, and north star alignment.
family: method
profile_level: Senior+
---

# Product Strategy

## Purpose

Define a clear product direction from business goals, user needs, market signals, and constraints — so the team knows which problem the product solves, for whom, and what success looks like at the product level. Strategy is not a feature list; it is a reasoned bet on where to focus and why.

## Use When

- Product direction or target segment is ambiguous or contested.
- A new product, major pivot, or market expansion is being evaluated.
- Roadmap work or discovery lacks a clear product outcome to work toward.
- Stakeholders need a rationale for what the product is (and is not) pursuing.
- Entering an annual or quarterly planning cycle and the strategic baseline must be refreshed.

## Do Not Use When

- The need is to prioritize specific backlog items — use `prioritization-and-tradeoffs`.
- The need is to validate a single product bet — use `product-hypothesis-management`.
- The need is to sequence initiatives across time — use `roadmap-management`.
- Competitive or market research requires primary data collection — hand off to `product-analyst` or UX research.

## Inputs

- Business goals and OKRs from leadership.
- User needs, pain points, JTBD frames, and segmentation data.
- Market signals: competitive landscape, pricing benchmarks, regulatory context.
- Current product state: metrics, retention, activation, monetization, and known gaps.
- Constraints: team capacity, technology, compliance, budget, and timeline.
- Stakeholder expectations and strategic constraints.

## Workflow

1. **Frame the problem space.** State the user segment, the core problem being solved, and the evidence that this problem matters at scale. Distinguish between the problem (observable gap) and the solution (bet).
2. **Articulate the value proposition.** Write a single crisp statement: for whom, what outcome, versus what alternative, and why the product is credible in this space.
3. **Separate evidence from assumptions.** List what is known (data, research, revenue), what is assumed (user behavior, market size, competitor positioning), and what is unknown. Assign a risk level to each assumption.
4. **Generate strategic options.** Produce at least two viable strategic directions with different focus areas, risk profiles, or time horizons. Resist picking the first option that sounds reasonable.
5. **Evaluate options.** Score each on: evidence strength, alignment with business goal, user value, competitive differentiation, cost of delay if deferred, and reversibility of the bet.
6. **Recommend direction with rationale and risks.** State the recommended bet, the trade-offs accepted, the assumptions that must hold, and the early signals that would confirm or disprove the direction.
7. **Define top-level success metrics.** Name the north star metric and two to three input metrics. Pass detailed metric framing to `product-metrics`.
8. **Map handoffs.** Strategy outputs become inputs for discovery planning, roadmap sequencing, and stakeholder alignment.

## Outputs

- Product strategy brief: segment, problem, value proposition, direction, and rationale.
- Strategic options comparison with evidence scores and trade-offs accepted.
- Top-level success metrics and north star direction.
- Named assumptions with risk levels (high / medium / low).
- Handoff tasks for `product-discovery`, `roadmap-management`, `product-stakeholder-alignment`.

## Named Patterns

### Good — Outcome-framed strategy
"For early-career professionals who struggle to build a savings habit, the product delivers a structured auto-save mechanism tied to paycheck events — outperforming generic budgeting apps by removing the need for manual intent. Success: 60-day retention of activated savers > 40%, measured within 90 days of launch."
Clear segment, clear problem, credible differentiation, measurable outcome.

### Bad — Feature factory framing
"Our strategy is to add analytics dashboards, a mobile app, and an API for third parties in Q3."
A delivery list with no problem, no segment, no evidence, no trade-off, and no measurable outcome.

### Good — Phased bets with decision rules
Strategy is sequenced as three reversible bets: (1) validate activation with a concierge MVP in 4 weeks, (2) if activation > threshold, automate and instrument, (3) if retention holds, scale to new segment. Each phase has an explicit decision rule before committing to the next.

### Bad — Big-bang launch without checkpoints
A 12-month plan with no pivoting triggers, no success criteria per phase, and no reversibility. The team learns nothing until the end and has sunk the full investment.

### Good — Assumption ranking by risk
Assumptions listed in risk order: (1) users will share paycheck data — HIGH risk, must validate first; (2) employers will integrate via API — MEDIUM, deferred to phase 2; (3) users prefer weekly saves — LOW, easy to A/B test. Discovery starts with the highest-risk assumption.

### Bad — Strategy without surfaced assumptions
Direction stated confidently with no listed assumptions. When a key belief turns out wrong, there is no mechanism to detect it early.

### Good — Named competitive alternative
"Users currently use a spreadsheet or nothing. We do not compete with robo-advisors (wrong segment) or full-service banks (wrong trust level). Our advantage is zero-friction setup for people who have no saving habit."

### Bad — Vague differentiation
"We will offer a better user experience than competitors." No named competitor, no specific dimension, no evidence.

## Boundaries

- Does not own sprint backlog or delivery plan — those go to `product-owner` and `project-manager`.
- Does not own UX research execution or design solution.
- Does not own statistical analysis, dashboards, or data quality.
- Does not invent market data, user research findings, or revenue projections.
- Does not replace system specification or architecture decisions.

## Sources

### Priority 1 — Foundational PM methodology
- Marty Cagan, "Inspired: How to Create Tech Products Customers Love" (2nd ed.) — SVPG, 2018
- Marty Cagan, "Empowered: Ordinary People, Extraordinary Products" — SVPG, 2020
- Teresa Torres, "Continuous Discovery Habits" — Product Talk, 2021
- SVPG blog on product strategy — https://www.svpg.com/articles/

### Priority 2 — Strategic frameworks and practitioners
- Lenny Rachitsky newsletter on product strategy — https://www.lennysnewsletter.com/
- John Cutler on product thinking — https://cutlefish.substack.com/
- Reforge on product strategy and growth — https://www.reforge.com/blog
- Roger Martin, "Playing to Win" — Harvard Business Review Press, 2013

### Priority 3 — Supporting frameworks
- Clayton Christensen, "The Innovator's Dilemma" — jobs-to-be-done lens
- Geoffrey Moore, "Crossing the Chasm" — segment and positioning
- Mind the Product on strategy — https://www.mindtheproduct.com/

## Handoff

- Discovery planning and assumption validation → `product-discovery`.
- Roadmap sequencing of strategic bets → `roadmap-management`.
- North star and metric tree → `product-metrics`.
- Stakeholder narrative and alignment → `product-stakeholder-alignment`.
- Competitive research or market sizing requiring primary data → `product-analyst`.
- System scope and specification → `system-analyst`.
