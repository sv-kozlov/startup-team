---
name: release-scope-support
description: Use when a Product Owner must confirm product-side release content, assess scope or defect impact on the release, communicate trade-offs to stakeholders, and close the delivery loop with backlog updates after launch.
family: method
profile_level: Senior+
---

# Release Scope Support

## Purpose

Support the release cycle from the product side: confirm what is in scope, flag product-impacting defects and late changes, align with Product Manager and delivery owner on adjustments, and convert post-release learning into backlog updates — without absorbing deployment, QA sign-off, or release governance.

## Use When

- A release date is approaching and product-side scope must be confirmed.
- A defect or late change threatens the release content and the scope impact needs assessment.
- Stakeholders need a clear view of what is and is not in the release from the product perspective.
- A feature is ready technically but needs product-side acceptance before release.
- Post-release user feedback, incident data, or analytics results need to become backlog input.

## Do Not Use When

- Release deployment, CI/CD, and infrastructure readiness are the primary topic — route to DevOps / SRE.
- QA regression sign-off and release quality ownership are required — route to QA.
- Delivery timeline, release calendar, and release governance decisions must be made — route to Project Manager / Delivery Manager.
- Post-release metric conclusions and experiment analysis belong to Product Analyst.
- Go/no-go launch decision involving strategic or commercial considerations — route to Product Manager.

## Inputs

- Release candidate scope: list of features, stories, and defects targeted for this release.
- Backlog and acceptance criteria for each item in scope.
- Defect log and open issue status from QA.
- Product Manager direction and Project Manager / Delivery Manager release plan.
- Post-launch: user feedback, support ticket themes, analytics signals.

## Workflow

1. **Confirm release scope.** Produce the product-side list of what is included in the release: features accepted by PO, scope changes logged, items explicitly deferred.
2. **Identify product-impacting defects and risks.** Review QA defect log for product-level severity: which defects affect core acceptance criteria or user-facing behavior? Do not assess technical severity — that belongs to QA and Tech Lead.
3. **Assess scope impact of late changes.** For each defect or change request arriving late: classify as must-fix (blocks acceptance), should-fix (degrades value), or defer (acceptable for this release). Record decision and owner.
4. **Align with Product Manager and delivery owner.** Surface go/no-go signals to Product Manager for launch decision and scope change rationale to Project Manager / Delivery Manager for delivery plan adjustment.
5. **Update backlog.** Record: what shipped, what was deferred (with reason and target release), what new items arise from the release.
6. **Close the delivery loop.** After launch: collect post-release signals (feedback, support, analytics), convert into actionable backlog items, and prioritize within the next backlog ordering cycle.

## Outputs

- Product-side release scope note: inclusions, exclusions, scope changes with rationale.
- Defect severity assessment from product perspective (must-fix / defer classification).
- Scope impact log for late changes.
- Go/no-go recommendation to Product Manager for launch decision.
- Backlog updates from post-release learning.

## Named Patterns

**Good — Product-side release scope note:**
```
Release 4.1 — Product scope confirmation (2026-05-22):

In scope (PO accepted):
  ✓ "Loyalty points display" — AC verified 2026-05-20
  ✓ "Courier geolocation v1" — AC verified 2026-05-21
  ✓ "Admin CSV export" — AC verified 2026-05-19

Deferred to 4.2:
  - "Push notification on courier arrival" — UX/UI design not finalized.
    Reason: UX/UI delivered mock on 2026-05-21; too late for regression cycle.
    Backlog item #912, target: Release 4.2.

Defects: 1 must-fix (see below), 2 deferred.
```

**Bad — No product-side scope confirmation:**
```
"QA says it's green — ship."
Deferred feature treated as included by stakeholder. Support escalation at launch.
```

---

**Good — Must-fix defect classification:**
```
Defect #1104: "Profile photo — file size error message missing."
Product severity: Must-fix. AC condition 3 explicitly states error message required.
Engineering estimate: 2h. QA regression: 30 min.
Decision: Fix before release. Project Manager notified: +1 day to release window.
Owner: Engineering (fix) + QA (regression) + PO (re-accept).
```

**Bad — Must-fix defect deferred without decision:**
```
Defect #1104 deferred because "it's cosmetic." Released.
Users report file upload broken — 0 error feedback. Support tickets: +40.
```

---

**Good — Late change assessed for scope impact:**
```
Late request: "Add 'share to Instagram' button to product page" — from Marketing, day before release.
PO assessment:
  - Not in release scope; no AC; no design.
  - Impact on release: none if excluded; adds 3 points + regression if included.
Decision: Defer to next sprint. Backlog item created. Marketing notified.
Recorded: scope change log #61, 2026-05-22.
```

**Bad — Late request absorbed without assessment:**
```
PO: "Marketing asked, so let's add it."
Engineering adds button without spec. Button links to wrong URL. Post-release hotfix.
```

---

**Good — Post-release backlog update:**
```
Post-launch review 2026-05-29 (1 week after Release 4.1):

Analytics (Product Analyst):
  - Loyalty points feature: +8% session return rate (above PM target).
  - Courier geolocation: 22% of users opened — below expectation. PA investigating.

Support signal (from Support team):
  - 15 tickets: "Where is my loyalty balance history?" → new backlog item #934.
  - 3 tickets: geolocation map not loading on iOS 15 → QA investigation backlog item #935.

PO action: Items #934 and #935 added to backlog. Priority discussed with PM in next planning.
```

**Bad — No post-release loop:**
```
Release shipped. Team moves to next sprint. Same loyalty balance question appears in next sprint's support escalation.
No backlog item. Same support tickets repeat. Discovery opportunity missed.
```

---

**Good — Go/no-go input to Product Manager:**
```
Release 4.1 — PO go/no-go input to PM (2026-05-22):
  Product-side: Ready (all Must-have AC verified; 1 must-fix defect fixed and re-accepted).
  Open risk: Courier geolocation iOS 15 — QA investigating; fallback = hide map on iOS 15.
  Recommendation: Go with fallback if QA confirms no data loss risk.
  Decision: PM's call.
```

**Bad — PO makes launch call unilaterally:**
```
PO: "It's ready — ship."
PM: "We agreed to check analytics targets before launch."
Launch creates data quality issue. PM not involved. Accountability conflict.
```

## Boundaries

- Does not own release deployment, CI/CD pipeline, or infrastructure — those belong to DevOps / SRE.
- Does not own QA regression sign-off or release quality gate — those belong to QA.
- Does not own release calendar, delivery governance, or release management — those belong to Project Manager / Delivery Manager.
- Does not own post-launch metric analysis — that belongs to Product Analyst.
- Does not make final launch or go/no-go decisions that involve strategic or commercial considerations — those belong to Product Manager.

## Sources

**Priority 1 — Canonical method references:**
- Scrum Guide (Schwaber & Sutherland): https://scrumguides.org/scrum-guide.html — Sprint Review and Increment.
- Marty Cagan, "Inspired" (2nd ed.) — release and delivery cycle from product side.
- Roman Pichler, "Agile Product Management with Scrum": https://www.romanpichler.com/books/

**Priority 2 — Practice guides:**
- Scrum.org, Sprint Review: https://www.scrum.org/resources/what-is-a-sprint-review
- Atlassian, Release Planning: https://www.atlassian.com/agile/project-management/release-planning
- SAFe, Release on Demand: https://scaledagileframework.com/release-on-demand/

**Priority 3 — Supplementary reading:**
- SVPG Blog: https://www.svpg.com/articles/
- ProductPlan, Release Management: https://www.productplan.com/glossary/release-management/

## Handoff

```
To: product-manager
Task: Make launch go/no-go decision for [release] based on PO scope assessment.
Context: Product-side is ready with [n] must-fix defects resolved; [n] risks identified.
Inputs: Scope confirmation note, defect classification, open risk register.
Expected artifact: Go/no-go decision with rationale.
Acceptance criteria: PO can communicate decision to Project Manager and team.
```

```
To: qa-engineer
Task: Confirm regression sign-off for [must-fix defect] before re-acceptance.
Context: PO re-acceptance depends on QA confirming fix does not introduce regression.
Inputs: Defect #[ID], fix description, impacted areas.
Expected artifact: QA regression verdict (pass / fail with notes).
Acceptance criteria: PO can update release scope note with final verdict.
```
