---
name: product-hypothesis-management
description: Use when a product idea, opportunity, or discovery finding must be framed as a testable hypothesis with explicit assumptions, validation approach, success criteria, and a decision rule. Covers the full hypothesis lifecycle from formulation through validation outcome recording.
family: method
profile_level: Senior+
---

# Product Hypothesis Management

## Purpose

Make product bets testable before committing to full delivery — by writing hypotheses in outcome terms, surfacing riskiest assumptions, selecting the right validation method, and recording decision outcomes. A hypothesis is not a task; it is a falsifiable statement that produces a learning before irreversible investment is made.

## Use When

- A feature idea or opportunity needs to be framed as a testable hypothesis before design or engineering starts.
- A discovery synthesis (from `product-discovery`) must be converted into a trackable validation plan.
- A launch decision must have a clear success criterion and a stop rule.
- The hypothesis backlog needs triage or reprioritization.
- A validation result (positive or negative) must be recorded and acted upon.

## Do Not Use When

- Statistical experiment design, sample size calculation, or significance testing is needed — hand off to `product-analyst`.
- The opportunity framing itself is unclear — start with `product-discovery`.
- The need is to sequence validated hypotheses across the roadmap — use `roadmap-management`.
- UX prototype design and usability test execution — hand off to `ui-ux-designer`.

## Inputs

- Discovery finding, user need, or opportunity from `product-discovery`.
- Metric frame from `product-metrics` (what success looks like).
- Existing hypothesis backlog and prior validation outcomes.
- Constraints: timeline, engineering capacity, analytics readiness.

## Workflow

1. **Write the hypothesis in outcome terms.** Use the template: "We believe [doing X for user segment Y] will result in [outcome Z], because [rationale]. We will know this is true when [measurable signal] improves by [threshold] within [time window]."
2. **List the assumptions.** Name every belief that must be true for the hypothesis to hold. Classify each as: desirability (users want this), feasibility (engineering can build it at acceptable cost), or viability (business can support it — pricing, operations, regulation).
3. **Rank assumptions by risk.** Highest risk = most uncertain AND most consequential if wrong. The validation plan must address the top-ranked assumption first.
4. **Select the validation method.** Match method to assumption type: concierge / wizard of oz for desirability with minimal build; prototype test for UX desirability; technical spike for feasibility; pricing experiment for viability. Prefer the smallest intervention that produces a signal.
5. **Set the decision rule.** Define: what result confirms the hypothesis (go forward), what result invalidates it (stop or pivot), and what result is inconclusive (extend or change method). A hypothesis without a stop rule cannot be falsified.
6. **Create handoff tasks.** Prototype to `ui-ux-designer`, experiment design to `product-analyst`, backlog items to `product-owner`, system constraints to `system-analyst`.
7. **Record the validation outcome.** After the validation window, record: result vs prediction, assumptions confirmed/invalidated, and the decision taken (proceed / pivot / stop). Update the hypothesis backlog.

## Outputs

- Hypothesis statement in outcome-terms template.
- Assumption map with risk ranking (desirability / feasibility / viability).
- Validation method selection with rationale.
- Decision rule: go / stop / pivot thresholds.
- Handoff tasks for each assumption validation thread.
- Validation outcome record and decision log entry.

## Named Patterns

### Good — Outcome-terms hypothesis
"We believe that adding a one-click invite flow for the team lead during onboarding (for SMB users on their first session) will increase 7-day team activation from 28% to 40%, because the current 3-step invite process creates friction that causes leads to defer and forget. We will know this is true when 7-day team activation rate in the experiment group exceeds 38% within 4 weeks."
Falsifiable, measurable, time-bound, with explicit rationale.

### Bad — Feature spec as hypothesis
"We will build a one-click invite button and launch it in Q2." No prediction, no assumption, no decision rule. The feature gets built regardless of whether it solves a problem.

### Good — Riskiest assumption first
Assumptions for the invite flow: (1) team leads do the invite during onboarding session — HIGH risk (unknown behavior); (2) a single-click flow is sufficient — MEDIUM (needs usability test); (3) this drives retention — LOW (historical correlation exists). Validation starts with assumption 1: a concierge test where a CS agent manually invites teammates on behalf of the lead during 10 onboarding sessions.

### Bad — Starting with the easiest assumption
The team builds the UI first because it is faster. The hardest assumption (whether team leads actually do invites in the session) is tested only after 4 weeks of engineering. Discovery that the behavior does not exist invalidates the entire hypothesis retroactively.

### Good — Clear decision rule
"Go if team activation in experiment group > 38% at 4 weeks. Pivot to async invite if result is 32–38% (partial signal). Stop if result < 32% (assumption about trigger timing is wrong; explore other trigger points)."

### Bad — No stop rule
"We will run the experiment and see what happens." Without a stop criterion, every result gets rationalized as a reason to continue. The team never officially kills the hypothesis.

### Good — Concierge before build
Before engineering the invite flow, a PM manually sends invite emails on behalf of 10 team leads within 30 minutes of their onboarding session. Measures: do leads follow through, do invited users join within 24 hours. Result in 2 weeks at zero engineering cost.

### Bad — Full build before validation
6 weeks of engineering → automated invite flow → post-launch review shows low usage. The concierge test would have found this in 2 weeks.

## Boundaries

- Does not own statistical significance, sample size calculation, or A/B test infrastructure — `product-analyst`.
- Does not own UX prototype design or usability test execution — `ui-ux-designer`.
- Does not own backlog refinement or sprint scope — `product-owner`.
- Discovery that generates the opportunity inputs to this skill comes from `product-discovery`.
- Metric framing inputs come from `product-metrics`.

## Sources

### Priority 1 — Hypothesis-driven development
- Teresa Torres, "Continuous Discovery Habits" — Product Talk, 2021 (assumption mapping, OST)
- Marty Cagan, "Inspired" — hypothesis and discovery chapters
- Jeff Gothelf and Josh Seiden, "Lean UX" — hypothesis canvas and assumption mapping

### Priority 2 — Lean validation methods
- Eric Ries, "The Lean Startup" — concierge, wizard of oz, MVP as validation tools
- Lenny Rachitsky on hypothesis and experimentation — https://www.lennysnewsletter.com/
- Reforge on product experimentation — https://www.reforge.com/blog

### Priority 3 — Supplementary
- Mind the Product on hypothesis-driven product development — https://www.mindtheproduct.com/
- John Cutler on assumption mapping — https://cutlefish.substack.com/

## Handoff

- Prototype design and usability test → `ui-ux-designer`.
- Experiment statistical design and A/B test setup → `product-analyst`.
- Backlog items for validated bets → `product-owner`.
- System constraint check for feasibility assumption → `system-analyst`.
- Roadmap sequencing of confirmed hypotheses → `roadmap-management`.
