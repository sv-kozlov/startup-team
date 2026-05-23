---
name: prioritization-and-tradeoffs
description: Use when product initiatives, opportunities, or roadmap items must be ranked with explicit value, risk, evidence, cost-of-delay, and effort trade-offs. Covers RICE, ICE, WSJF, cost-of-delay scoring, and the construction of a prioritization rationale that can be explained and challenged by stakeholders.
family: method
profile_level: Senior+
---

# Prioritization and Trade-offs

## Purpose

Help product teams choose what to pursue and what to defer by applying transparent product logic — not authority, recency bias, or stakeholder volume. Every prioritization decision must be explainable and revisable when evidence changes.

## Use When

- Multiple product options compete for the same team capacity.
- A stakeholder challenges current priorities or lobbies for a specific initiative.
- Product value conflicts with delivery risk, effort, technical dependency, or timing.
- The team must decide what to defer and needs a documented rationale for the deferred items.
- A quarterly or roadmap planning cycle requires a ranked backlog of initiatives.

## Do Not Use When

- Sprint-level backlog ordering within confirmed scope — that belongs to `product-owner`.
- Roadmap horizon sequencing (Now / Next / Later) across time — use `roadmap-management`.
- Individual initiative metric framing — use `product-metrics`.
- Delivery effort estimation and resource capacity modeling — use inputs from `tech-lead` and `project-manager`.

## Inputs

- Initiative list: confirmed opportunities, proposed features, tech debt items, regulatory requirements.
- Metric targets: outcome the initiative contributes to, expected lift, and evidence strength.
- Delivery effort signals from Tech Lead or Engineering (rough T-shirt sizing, not sprint plans).
- Known dependencies and blockers.
- Regulatory or contractual deadlines that create hard priority floors.
- Stakeholder context: who is invested in what and why.

## Workflow

1. **Define the prioritization objective.** Name the strategic goal the ranking serves: maximize impact on north star metric, reduce risk before scaling, clear a regulatory blocker, or create options for a future bet.
2. **Select or adapt a scoring framework.** Choose based on confidence level and decision speed needed:
   - **RICE**: Reach × Impact × Confidence ÷ Effort. Good for comparing items with different user populations.
   - **ICE**: Impact × Confidence × Ease. Faster; useful for early discovery bets.
   - **WSJF** (Weighted Shortest Job First): Cost of Delay ÷ Duration. Good when timing matters and delay has a measurable cost.
   - **Cost of Delay** alone: useful when the item is already agreed; only the timing is in question.
3. **Score each initiative.** Apply the selected framework consistently. Use the same scale per dimension. Record confidence levels — do not false-precision a low-evidence estimate.
4. **Name the trade-offs explicitly.** For each top-ranked item: what is being deferred to accommodate it? What risk does the deferral create? Make the swap visible rather than implicit.
5. **Apply constraints and hard floors.** Regulatory items with deadlines, contractual obligations, or items that block other high-priority work float regardless of score. Name these explicitly so the scoring rationale remains honest.
6. **Run a stakeholder smell check.** Before finalizing: does the ranking pass the "explain it to the sponsor" test? If a result looks wrong, diagnose whether the scoring inputs were wrong or the framework needs adjustment.
7. **Document deferred items.** For each item below the cut: record why it was deferred, what evidence or condition would change its rank, and when it should be revisited.

## Outputs

- Prioritization matrix: items ranked by chosen framework with raw scores.
- Trade-off decision note: what is displaced and why.
- Deferred-scope register: items below the cut with revision conditions.
- Handoff to `product-owner` for top-ranked items entering the backlog.

## Named Patterns

### Good — RICE scoring with explicit confidence
"Initiative A: Reach=5000 users/month, Impact=3 (medium), Confidence=70% (one interview study, no A/B data), Effort=3 weeks. RICE = 5000 × 3 × 0.7 / 3 = 3,500. Initiative B: Reach=800 users/month, Impact=5 (high), Confidence=90% (A/B validated in adjacent segment), Effort=1 week. RICE = 800 × 5 × 0.9 / 1 = 3,600. B ranks higher despite smaller reach because high confidence and low effort."
Scores are visible; confidence is honest; ranking is explainable.

### Bad — HiPPO prioritization
"The VP asked about feature X last week, so it goes to the top of the roadmap." No value evidence, no cost-of-delay analysis, no trade-off visibility. Every other item displaced for unstated reasons.

### Good — Cost-of-delay reasoning for timing
"The onboarding improvement has a cost of delay of ~30 activations per week at the current growth rate. Deferring 4 weeks costs ~120 activations, which at our 90-day retention rate represents ~18 accounts at risk. The tech debt refactor has a cost of delay of 0.5 developer-days per week in velocity loss. Timing is not urgent."

### Bad — All items treated as equally urgent
"Everything is a priority." No differentiation, no cost of delay, no trade-off reasoning. The team works on whatever stakeholder spoke last.

### Good — Deferred-item register with revision condition
"Auth SSO integration deferred from Q2. Revision condition: if enterprise sales close 3 deals blocked by SSO absence, it moves to the top regardless of quarterly plan. Current state: 0 deals blocked."

### Bad — Silent deferral
Items are removed from the roadmap without explanation. Stakeholders continue asking about them because they have no visibility into the deferral reasoning. Trust erodes.

### Good — Framework matched to decision context
For early discovery bets with high uncertainty: ICE scoring (fast, low-effort). For confirmed initiatives competing for limited Q3 capacity: RICE (more rigorous). For regulatory items: cost-of-delay + deadline hard floor — no scoring needed.

### Bad — Uniform framework regardless of context
WSJF applied to a rough discovery idea with no data. Scores look precise but the inputs are invented. The precision signal misleads rather than informs.

## Boundaries

- Does not own delivery estimates; uses rough sizing from Tech Lead as input.
- Does not own sprint backlog ordering — `product-owner`.
- Does not own project schedule, resource allocation, or capacity planning — `project-manager`.
- Does not hide uncertainty or low-confidence evidence behind precise-looking scores.

## Sources

### Priority 1 — Prioritization frameworks
- Marty Cagan, "Inspired" — chapters on prioritization and opportunity assessment
- Jeff Gothelf and Josh Seiden, "Lean UX" — evidence-based prioritization
- SAFe WSJF — https://scaledagileframework.com/wsjf/ (cost of delay methodology)

### Priority 2 — RICE and ICE
- Lenny Rachitsky, "How to prioritize features" — https://www.lennysnewsletter.com/
- Reforge on product prioritization — https://www.reforge.com/blog
- John Cutler on prioritization reasoning — https://cutlefish.substack.com/

### Priority 3 — Supplementary
- Mind the Product on prioritization — https://www.mindtheproduct.com/
- Roman Pichler, prioritization and roadmap — https://www.romanpichler.com/

## Handoff

- Top-ranked initiatives entering the backlog → `product-owner`.
- Delivery effort and capacity constraints → `tech-lead` / `project-manager` (inputs from).
- Roadmap sequence and horizon positioning → `roadmap-management`.
- Metric expected impact framing → `product-metrics`.
- Stakeholder narrative for trade-off explanation → `product-stakeholder-alignment`.
