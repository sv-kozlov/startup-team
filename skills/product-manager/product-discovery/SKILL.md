---
name: product-discovery
description: Use when customer, market, business, or data signals must be turned into validated product opportunities and testable hypotheses. Covers opportunity framing, assumption mapping, interview planning, synthesis, and validation path selection using Continuous Discovery and Opportunity Solution Tree frameworks.
family: method
profile_level: Senior+
---

# Product Discovery

## Purpose

Reduce product uncertainty before delivery by continuously surfacing opportunities, mapping assumptions, and selecting the most valuable and least risky bets — so the team builds products that create real user and business outcomes rather than shipping assumptions at scale.

## Use When

- A user problem, market gap, or business opportunity needs framing and prioritization.
- A solution idea exists but its desirability, feasibility, or viability is unconfirmed.
- Discovery evidence (interviews, analytics, support signals) must be synthesized into product direction.
- The team is starting a new initiative and must identify riskiest assumptions before committing to design or engineering.
- An Opportunity Solution Tree needs building or updating.

## Do Not Use When

- The need is to frame a specific bet as a hypothesis — use `product-hypothesis-management`.
- The need is to prioritize already-confirmed opportunities against each other — use `prioritization-and-tradeoffs`.
- UX research execution (recruiting, interview moderation, usability testing) is required — hand off to `ui-ux-designer`.
- Statistical experiment design or metric calculation is required — hand off to `product-analyst`.

## Inputs

- Interview notes, survey data, NPS/CSAT verbatims, support tickets, sales call recordings.
- Analytics events, funnel drop-offs, retention curves, and segment cohorts.
- Market signals: competitor moves, regulatory change, industry reports.
- Business goal or OKR that frames the discovery focus.
- Current product hypothesis backlog and any existing Opportunity Solution Tree.

## Workflow

1. **Set the discovery goal.** Anchor to a specific business or product outcome (e.g., improve 30-day activation rate for SMB segment). Avoid open-ended "explore everything" scopes.
2. **Build or update the Opportunity Solution Tree.** Map the desired outcome → opportunities (user needs, pain points, desires) → solution candidates → experiment ideas. Keep each node distinct; do not mix opportunities with solutions.
3. **Run or review discovery interviews.** Use JTBD and Continuous Discovery framing: ask about past behavior, triggers, and outcomes — not hypothetical preferences. Prioritize frequency and recency of experience.
4. **Synthesize signals into opportunity themes.** Cluster raw signals by underlying need or pain. Weight by frequency, severity, and alignment with the target outcome. Distinguish evidence from inference.
5. **Rank opportunities.** Apply a simple rubric: (a) how many users are affected, (b) how much does it impede the target outcome, (c) how underserved is the need compared to alternatives. Pick the top opportunity to validate.
6. **Map assumptions for the top opportunity.** For each candidate solution, list: (a) desirability — users want this; (b) feasibility — engineering can build this at acceptable cost; (c) viability — business can support it (pricing, ops, regulation). Rank by risk.
7. **Select a validation approach.** Match method to assumption risk: prototype test for desirability, spike for feasibility, financial model or pilot for viability. Set a decision rule: what result confirms, what result stops or pivots.
8. **Create handoff tasks.** Pass prototype need to `ui-ux-designer`, experiment design to `product-analyst`, system constraint check to `system-analyst`, and confirmed opportunities to `product-hypothesis-management`.

## Outputs

- Opportunity Solution Tree (current state with ranked opportunities).
- Discovery synthesis: clustered opportunities with evidence and inference labels.
- Top opportunity brief: affected users, severity, underservice score, and alignment with outcome.
- Assumption map with risk ranking per solution candidate.
- Validation plan: method, timeline, decision rule, and handoff tasks.

## Named Patterns

### Good — Opportunity-leading interview question
"Tell me about the last time you tried to track your team's project status. What happened? What did you do?" Surfaces actual behavior, triggers, and friction without anchoring on a product feature.

### Bad — Solution-leading interview question
"Would you use a dashboard that showed all your projects in one place?" Anchors the respondent to a solution; response tells you nothing about the real need or how acute it is.

### Good — Opportunity Solution Tree with separated layers
Outcome: "Increase team activation within 7 days." Opportunities at layer 2: "Users do not know how to invite teammates," "Users abandon setup when they hit a blank state," "Users do not understand how value is created." Solutions at layer 3 linked to specific opportunities. Experiments at layer 4 linked to specific solutions.

### Bad — Flat opportunity-solution mix
A single list mixes "Add an onboarding checklist," "Users are confused at setup," "Build a template library," and "Improve notifications." The team cannot tell which are problems and which are solutions, cannot prioritize, and cannot test assumptions cleanly.

### Good — Evidence vs inference distinction
"Six of nine interviewees described abandoning the setup flow when they had to invite others (evidence). We infer this creates a solo-use bias that limits the network effect (inference). The inference must be validated before building a social feature."

### Bad — Treating synthesis as certainty
"Users want a collaborative mode." Stated as fact after 3 interviews with no evidence label, no sample size caveat, and no rival explanation. Drives straight to design without testing the assumption.

### Good — Continuous discovery cadence
Discovery runs weekly in parallel with delivery: PM talks to 1–2 users per week, updates the Opportunity Solution Tree, and surfaces assumption risks before the next planning cycle. No separate "discovery phase."

### Bad — Discovery as a one-time phase
A 6-week discovery sprint happens, produces a document, and is shelved. When the market or user behavior shifts, the team has no mechanism to detect it. Discovery evidence goes stale before delivery is complete.

## Boundaries

- Does not own UX research execution (recruiting, moderation, usability test) — `ui-ux-designer`.
- Does not own statistical experiment design, significance calculation, or dashboard — `product-analyst`.
- Does not own backlog refinement or sprint scope — `product-owner`.
- Does not invent customer evidence, market size, or research findings.
- Strategy direction that frames what to discover comes from `product-strategy`.

## Sources

### Priority 1 — Continuous Discovery and OST
- Teresa Torres, "Continuous Discovery Habits" — Product Talk, 2021
- Teresa Torres, Opportunity Solution Tree guide — https://www.producttalk.org/2016/08/opportunity-solution-tree/
- Marty Cagan, "Inspired" chapters on discovery — SVPG, 2018

### Priority 2 — JTBD and user research methods
- Clayton Christensen, Bob Moesta — Jobs to Be Done framework
- Lenny Rachitsky, "How to run effective user interviews" — https://www.lennysnewsletter.com/
- Reforge, Discovery practices — https://www.reforge.com/blog

### Priority 3 — Supplementary
- Mind the Product on discovery — https://www.mindtheproduct.com/
- John Cutler on opportunity framing — https://cutlefish.substack.com/

## Handoff

- Specific bet framing and validation planning → `product-hypothesis-management`.
- Prototype or usability test → `ui-ux-designer`.
- Experiment design and statistical validity → `product-analyst`.
- System constraint or feasibility check → `system-analyst`.
- Prioritization of confirmed opportunities → `prioritization-and-tradeoffs`.
- Strategy refresh based on discovery findings → `product-strategy`.
