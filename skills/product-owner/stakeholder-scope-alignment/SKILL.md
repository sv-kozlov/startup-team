---
name: stakeholder-scope-alignment
description: Use when Product Owner scope, backlog priority, trade-offs, or exclusions must be communicated to and accepted by stakeholders — business, engineering, design, QA, or management — without absorbing commercial, strategic, or delivery decisions.
family: method
profile_level: Senior+
---

# Stakeholder Scope Alignment

## Purpose

Create shared understanding of scope, exclusions, trade-offs, and open decisions among stakeholders so that each party can act on correct information and PO does not accumulate adjacent ownership to fill a communication gap.

## Use When

- Business stakeholders, engineering, or management disagree on what is included in the current increment.
- Scope changes must be explained, justified, and recorded before the team acts.
- A key stakeholder needs a structured update on backlog state, priorities, or trade-offs.
- Competing requests from multiple stakeholders must be resolved at the scope level.
- A cross-team dependency creates a scope conflict that must be negotiated and recorded.

## Do Not Use When

- The strategic decision (roadmap bet, product priority, commercial outcome) is unresolved — escalate to Product Manager before aligning stakeholders on scope.
- Delivery governance, budget, or staffing disputes are the main issue — route to Project Manager / Delivery Manager.
- Business process redesign or regulatory alignment is the core topic — route to Business Analyst.
- Technical feasibility or architecture trade-off is the primary question — route to Tech Lead or System Architect.

## Inputs

- Current backlog state, scope brief, scope change log, and MVP definition.
- Stakeholder request, conflict, or question that affects scope or priority.
- Known constraints: timeline, dependency, architecture, regulatory, or commercial.
- Decision log: what has already been decided and by whom.

## Workflow

1. **Identify affected stakeholders and their scope concern.** Name who has a stake in this scope decision: business owner, product team, engineering, QA, design, Project Manager / Delivery Manager, or cross-team PO.
2. **Separate ownership layers.** Clarify what is a product decision (PO scope), what is a business or strategic decision (Product Manager), what is a technical constraint (Tech Lead / SA), and what is a delivery constraint (Project Manager / Delivery Manager). Route non-PO questions to the right owner.
3. **Present scope options and trade-offs.** For each open scope question, offer 2–3 options with explicit trade-offs: what is gained, what is lost, what changes in timeline or dependency. Do not present a single option as the only choice unless it genuinely is.
4. **Facilitate the decision.** Surface the decision to the correct owner. If the decision belongs to the PO, make it and record it. If it belongs to Product Manager, Business Analyst, or leadership, create a handoff rather than deciding unilaterally.
5. **Record decision and impact.** Capture: decision made, who made it, rationale, impact on backlog or acceptance criteria, and who was notified.
6. **Communicate closure.** Confirm with all affected parties that the decision is recorded and the scope is now clear. Update backlog, scope change log, and any active sprint or release artifacts.

## Outputs

- Scope alignment note: options, trade-offs, decision, and owner.
- Decision log entry with date, owner, and backlog impact.
- Updated backlog or scope brief reflecting the decision.
- Handoff tasks for Product Manager, Business Analyst, Project Manager / Delivery Manager, or Tech Lead where their decision is required.

## Named Patterns

**Good — Trade-off presented with options:**
```
Scope question: "Should onboarding wizard include step 4 (advanced settings) for v1?"

Option A: Include step 4.
  + Complete onboarding experience for power users.
  - Adds 2 sprint points; delays v1 by 1 sprint.
  
Option B: Exclude step 4; add "Explore advanced settings" link.
  + v1 on schedule; step 4 in v2 backlog.
  - Power users may be confused; support ticket risk.

Recommendation: Option B (PO scope decision). Risk: support ticket increase.
Decision owner: PO. PM notified. Engineering confirmed 0-point effort for link.
Recorded: scope change log entry #42, 2026-05-15.
```

**Bad — Scope forced without options:**
```
PO: "Step 4 is out. Ship without it."
Engineering: "But PM said it's critical?"
Result: 2h debate in sprint review. Decision reversed. 1-sprint delay anyway.
```

---

**Good — Competing stakeholder requests resolved:**
```
Marketing: "Add promo banner to checkout."
Finance: "Add invoice download to checkout."
PO analysis:
  - Promo banner: 2 points, high visibility, low risk.
  - Invoice download: 5 points, blocks checkout load; SA estimates dependency on billing service.
Decision: Promo banner in Sprint 15. Invoice download deferred to Sprint 16 (SA to confirm billing dependency first).
Both stakeholders notified. Decision log updated.
```

**Bad — Both requests pulled into sprint:**
```
PO adds both without trade-off analysis. Sprint overloaded. Invoice download blocked day 3.
Promo banner shipped without regression. Sprint goal missed.
```

---

**Good — Scope change communicated proactively:**
```
Change: "Dark mode" removed from Sprint 17 scope.
Reason: UX/UI design not finalized; cannot ship without design sign-off.
Impact: Sprint 17 goal unchanged; dark mode moved to Sprint 18 (UX/UI to confirm date).
Notified: PM, Project Manager, UX/UI lead, engineering team (Slack + backlog comment).
Recorded: scope change log #57, 2026-05-19.
```

**Bad — Scope change communicated in planning:**
```
"By the way, dark mode is out." 
Stakeholder: "Why? PM promised it." Sprint planning consumed by re-discussion.
```

---

**Good — Decision escalated correctly:**
```
Scope conflict: Finance wants invoice in v1; PM said defer.
PO: "This is a product strategy call — do we prioritize operational compliance or speed to market?"
Action: PO creates handoff to PM with both stakeholder positions and timeline impact.
PO does not decide unilaterally on a strategic priority question.
```

**Bad — PO decides strategic question:**
```
PO: "Finance is louder, so invoice goes in v1."
PM: "This was a deliberate strategy decision. You overrode the roadmap."
Trust broken; backlog governance questioned.
```

---

**Good — Stakeholder alignment summary:**
```
Scope alignment call 2026-05-18 — Sprint 16 scope:
Participants: PM, Project Manager, Tech Lead, QA lead.
Agreed: 8 stories in scope; 2 deferred (reasons noted).
Open: AB test variant for checkout — PM to decide by 2026-05-22.
Actions: PO updates backlog; PM confirms test variant; Project Manager confirms sprint start date.
```

**Bad — No record of alignment call:**
```
Scope discussed verbally. Next sprint: "But we agreed X?" "No, we agreed Y."
```

## Boundaries

- Does not own business strategy, commercial decisions, or product roadmap — those belong to Product Manager.
- Does not own delivery governance, escalation, or budget decisions — those belong to Project Manager / Delivery Manager.
- Does not replace Business Analyst stakeholder analysis when business process ownership is at stake.
- Does not make technical feasibility decisions — those belong to Tech Lead or System Architect.

## Sources

**Priority 1 — Canonical method references:**
- Marty Cagan, "Inspired" (2nd ed.) — stakeholder management in product teams.
- Roman Pichler, "Strategize": https://www.romanpichler.com/books/strategize/
- Scrum Guide (Schwaber & Sutherland): https://scrumguides.org/scrum-guide.html — Sprint Review and transparency.

**Priority 2 — Practice guides:**
- Atlassian, Stakeholder Management: https://www.atlassian.com/teams/marketing/guide/stakeholder-management
- Atlassian, Stakeholder Communications Plan: https://www.atlassian.com/team-playbook/plays/stakeholder-communications-plan
- Mike Cohn, "Agile Estimating and Planning" — trade-off communication.

**Priority 3 — Supplementary reading:**
- SVPG Blog: https://www.svpg.com/articles/
- ProductPlan, Stakeholder Management: https://www.productplan.com/learn/product-manager-stakeholder-management/

## Handoff

```
To: product-manager
Task: Decide [strategic scope question] — PO cannot make this call unilaterally.
Context: Stakeholder conflict on [feature] has a strategic dimension (roadmap priority / commercial outcome).
Inputs: Options, stakeholder positions, timeline impact.
Expected artifact: Go/no-go decision with rationale.
Acceptance criteria: PO can communicate the decision to all stakeholders with PM backing.
```

```
To: project-manager
Task: Assess delivery impact of scope decision for [sprint or release].
Context: Scope alignment requires knowing what timeline flexibility exists before finalizing the trade-off.
Inputs: Proposed scope options, current sprint/release plan.
Expected artifact: Timeline impact per option; feasibility confirmation.
Acceptance criteria: PO can present options to stakeholders with accurate delivery context.
```
