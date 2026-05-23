---
name: roadmap-management
description: Use when roadmap options, outcome sequencing, Now-Next-Later framing, or roadmap trade-offs must be built or explained to the team or stakeholders. Covers outcome roadmap construction, bet sequencing, dependency surfacing, and handoff to delivery roles.
family: method
profile_level: Senior+
---

# Roadmap Management

## Purpose

Connect product strategy to an explainable, time-sequenced set of outcome bets — so the team and stakeholders understand what is being pursued, in what order, and why — without locking into a feature delivery schedule that cannot absorb learning.

## Use When

- Strategy bets must be sequenced across a time horizon (Now / Next / Later or quarterly).
- Stakeholders need to understand why item A is ahead of item B.
- Roadmap items conflict with capacity, risk, dependencies, or product goals.
- A roadmap must be updated after a pivot, new discovery finding, or changed business priority.
- Product Owner or delivery roles need product context for backlog planning.

## Do Not Use When

- Individual initiative ranking is needed without roadmap structure — use `prioritization-and-tradeoffs`.
- Sprint-level scope or backlog refinement is needed — that belongs to `product-owner`.
- Delivery timeline, date commitments, and resource allocation — that belongs to `project-manager`.
- Portfolio-level investment governance across business units — escalate to leadership.

## Inputs

- Product strategy and agreed outcomes.
- Confirmed and ranked opportunities from `product-discovery`.
- Prioritization scores from `prioritization-and-tradeoffs`.
- Capacity signals from Tech Lead / Engineering (rough sizing, not sprint plan).
- Known dependencies, technical debt risks, and regulatory deadlines.
- Stakeholder expectations and planning horizon (quarter, half-year, annual).

## Workflow

1. **Set the roadmap horizon and goal.** Name the planning period, the overarching outcome the roadmap serves, and the key result it targets. Avoid "build X" framing; use "achieve Y" framing.
2. **Cluster initiatives by outcome theme.** Group items under the outcomes they contribute to (e.g., activation, retention, monetization, platform health). A roadmap organized by outcomes is easier to explain and adjust than one organized by features.
3. **Apply Now / Next / Later framing.** Place confirmed and resourced bets in Now. Validated opportunities with known direction in Next. Explored or aspirational bets in Later. Be honest about uncertainty: Later is not a commitment.
4. **Surface dependencies and blockers.** For each Now and Next item, name what it depends on: technical prerequisite, regulatory approval, partner availability, or data readiness. Flag items that are blocked without these.
5. **Evaluate sequencing trade-offs.** For each candidate ordering, state: value delivered early, risk reduced, learning gained, cost of delay if deferred, and whether the sequence creates irreversible commitments.
6. **Explain deferred items explicitly.** For every important initiative placed in Later or removed entirely, record the rationale: resource conflict, strategic deprioritization, evidence gap, or dependency not yet resolved. Stakeholders will ask.
7. **Produce the handoff package.** Pass Now items to `product-owner` for backlog creation. Pass delivery constraints and timeline questions to `project-manager`. Pass metric framing for each item to `product-metrics`.

## Outputs

- Outcome roadmap: Now / Next / Later with item descriptions, outcome links, and sequencing rationale.
- Dependency and blocker register.
- Trade-off decision log: what was deferred and why.
- Handoff context for `product-owner` (backlog intent) and `project-manager` (delivery constraints).

## Named Patterns

### Good — Outcome-organized roadmap
Now: "Reduce onboarding drop at step 3 (target: activation +8pp, Q2)." Next: "Enable team collaboration to unlock network effect (target: invite rate +20%, Q3)." Later: "Self-serve billing to reduce CS load (no date yet; depends on billing platform migration)."
Every item has an outcome, a metric target, and a horizon based on evidence.

### Bad — Feature list roadmap
"Q2: Dashboard v2, dark mode, CSV export, API v3, mobile notifications, admin panel."
No outcomes, no rationale for sequence, no metrics. Cannot be explained to a stakeholder or adjusted when priorities shift.

### Good — Honest Later horizon
"Later: AI-generated summaries. This idea has signal from user interviews but no validation yet. It moves to Next only when we have a prototype result and the ML platform team has spare capacity. No date commitment."
Sets expectations; prevents roadmap theater.

### Bad — Roadmap theater
"Q4: AI features (TBD)." Listed to signal ambition but with no strategy basis, no resource plan, and no decision rule for what moves it forward. Stakeholders treat it as a commitment; the team treats it as noise.

### Good — Explicit cost-of-delay reasoning
"We defer self-serve billing to Q3 because the Q2 activation problem has a 3x higher cost of delay: each week of delayed activation costs N users who churn before experiencing value. Billing delay costs only CS overhead, which is recoverable."

### Bad — Priority by stakeholder recency
"Legal asked about the compliance feature last week, so it jumped to top of the roadmap." No evidence, no cost-of-delay comparison, no explicit trade-off against what it displaced.

## Boundaries

- Does not own sprint backlog administration — `product-owner`.
- Does not commit delivery dates or resource allocation — `project-manager`.
- Does not replace portfolio governance for organization-level investment decisions.
- Does not invent engineering estimates; takes rough sizing from Tech Lead as input.

## Sources

### Priority 1 — Outcome roadmap and Continuous Discovery
- Marty Cagan, "Inspired" and "Empowered" — SVPG Press
- Teresa Torres, "Continuous Discovery Habits" — Product Talk, 2021
- Janna Bastow, Now-Next-Later roadmap format — https://www.prodpad.com/blog/

### Priority 2 — Prioritization and roadmap frameworks
- Lenny Rachitsky, roadmap practices — https://www.lennysnewsletter.com/
- Reforge, roadmap and sequencing — https://www.reforge.com/blog
- John Cutler on roadmap trade-offs — https://cutlefish.substack.com/

### Priority 3 — Supplementary
- Mind the Product on roadmaps — https://www.mindtheproduct.com/
- Roman Pichler, roadmap formats — https://www.romanpichler.com/

## Handoff

- Backlog creation and refinement for Now items → `product-owner`.
- Delivery timeline, date constraints, and resource questions → `project-manager`.
- Metric framing for each roadmap item → `product-metrics`.
- Discovery needed to confirm Next items → `product-discovery`.
- Stakeholder narrative for roadmap rationale → `product-stakeholder-alignment`.
