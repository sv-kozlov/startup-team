---
name: shared-quality-gates-review
description: Use when a role artifact — requirement, specification, process model, rule catalog, acceptance criteria set, metric definition, product brief, delivery plan, or analytical memo — must be reviewed for completeness, clarity, testability, traceability, ownership correctness, and handoff readiness before it advances to the next stage.
---

# Shared Quality Gates Review

## Purpose

Prevent low-quality artifacts from advancing through the delivery pipeline by applying a structured review at each stage boundary — before specification, before development, before testing, and before sign-off. Quality gate review is not the same as QA testing; it is the method of checking whether an artifact is fit for its intended audience and next use, and returning it with actionable fixes when it is not.

## Use When

- A requirements, specifications, process model, rule catalog, acceptance criteria set, or analysis artifact is about to be handed off to the next role and its readiness has not been formally checked.
- A story or backlog item is being considered for sprint entry and "definition of ready" must be verified.
- An artifact shows signs of quality problems: vague language, missing ownership attribution, untestable conditions, no traceability to source decisions.
- A downstream role (QA, Engineering, UX/UI) has returned an artifact as incomplete or ambiguous — the review identifies the specific gaps before it is reworked and resubmitted.
- A release gate requires that certain artifact categories pass quality criteria before the release proceeds.
- A cross-role review session has been scheduled and needs a structured agenda rather than an informal discussion.

## Do Not Use When

- The task is test execution, regression testing, or performance testing → QA Engineer owns those.
- The task is approving product priority, deciding architecture, or committing to delivery dates → Product Manager, System Architect, and Project Manager own those decisions.
- The task is rewriting another role's artifact from scratch when the owning role is available → return the artifact to the owner with a gap list; do not absorb the authoring.
- The artifact has not yet been authored → do not run a quality gate on an empty or outline-only artifact; complete a first draft first.

## Inputs

- The artifact to be reviewed: name, version, and the decision or handoff it supports.
- The intended audience and next stage: who will use this artifact, for what purpose?
- Role boundaries: which role owns the artifact and what is in scope vs. out of scope for that role?
- Acceptance expectations: what does "complete" look like for this artifact type and stage?
- Open questions already recorded in the artifact, if any.

## Workflow

1. **State the review objective and scope.** Define: what artifact is being reviewed, what stage it is at (pre-specification, pre-development, pre-testing, pre-release, pre-sign-off), and what criteria define "ready to advance." A review without a stated gate criterion cannot produce a binary ready / not-ready verdict.

2. **Apply the role-neutral quality checklist.** For every artifact type, check:
   - *Purpose and audience*: Is the artifact's purpose stated? Is it written for its intended audience?
   - *Completeness*: Are all mandatory sections present? Are there unstated exclusions, missing scenarios, or undefined actors?
   - *Clarity*: Are key terms defined? Is ambiguous language resolved? Does the artifact read consistently from start to end?
   - *Testability*: Can each condition or requirement be verified independently? Are success criteria falsifiable?
   - *Traceability*: Does the artifact link to its source (business decision, policy, upstream requirement, stakeholder approval)?
   - *Ownership*: Is each element owned by the role that authored the artifact? Are adjacent-role items correctly marked as handoffs rather than absorbed?
   - *Handoff readiness*: Does the artifact give the receiving role everything it needs, or does it require verbal explanation to be usable?

3. **Apply role-specific criteria.** For requirements and business analysis artifacts: check business completeness (stakeholder alignment, process coverage, exception handling, UAT readiness). For system specifications and API artifacts: check technical precision (unambiguous state transitions, error shape completeness, API versioning notes, integration boundary clarity). For analytical and metric artifacts: check evidence quality (measurement methodology, confidence level, caveat completeness, observability plan).

4. **Identify ownership overreach and missing handoffs.** Check whether the artifact contains content that belongs to another role but was absorbed (e.g., a business requirements document that contains system architecture decisions). Mark each overreach as a finding and suggest the correct handoff. This is one of the most valuable reviews — absorbed ownership creates maintenance debt and boundary confusion downstream.

5. **Return findings ordered by severity.** Classify each finding as:
   - *Blocker*: the artifact cannot advance until this is resolved; the next stage cannot proceed.
   - *Major*: the artifact will cause problems downstream if this is not resolved; strongly recommend fixing before advance.
   - *Minor*: improvement recommended but does not block advance; can be fixed in the next iteration.
   Provide a concrete, actionable fix suggestion for each finding — not just the diagnosis.

6. **Issue a ready / not-ready verdict.** If no blocker findings exist: artifact is ready to advance (note any major or minor items as improvement backlog). If blocker findings exist: artifact is returned to the authoring role with the finding list. The verdict is binary and based only on the stated gate criteria — not on subjective completeness.

## Outputs

- Quality review findings: each finding with ID, type (blocker / major / minor), description, location in the artifact, and suggested fix.
- Readiness verdict: ready to advance / returned for rework.
- Readiness checklist: the gate criteria applied and the pass/fail result for each.
- Required fixes (blockers and majors) formatted as actionable tasks for the authoring role.
- Residual risks: minor findings and open questions that do not block advance but should be tracked.

## Role Modes

### Business Analyst

Reviews business analysis artifacts (business requirements, process models, rule catalogs, UAT scope, business acceptance criteria) for business completeness: are all affected stakeholders covered, are all process variants and exceptions modeled, are business rules traceable to policy sources, is UAT scope defined with named business sign-off owners, and are system-level items correctly identified as handoffs to System Analyst? Returns artifacts to the authoring role with a severity-classified gap list. Does not rewrite the artifact as the reviewer.

### Product Owner

Reviews backlog items and stories for "definition of ready": does each story have a stated objective, clear scope, testable acceptance criteria, no unresolved blockers, and a team estimate? Applies the DoR checklist and returns items that do not pass with a specific gap list. Reviews the overall backlog for sprint-level readiness: is the sprint goal achievable with the items present? Does not review system specification artifacts or analytical memos — those are reviewed by the respective owning roles.

### Product Manager

Reviews product-level artifacts (PRD, product briefs, opportunity assessments, launch plans, metric trees) for product completeness: are the decision drivers stated, is the scope bounded, are success metrics defined and measurable, are adjacent-role handoffs explicit, and is the artifact usable by Product Owner, Engineering, and System Analyst without verbal explanation? Does not review delivery governance documents (Project Manager) or system specifications (System Analyst).

### Project Manager

Reviews delivery governance artifacts (project plans, dependency maps, risk logs, status reports, release plans) for delivery completeness: are all milestones covered, are dependencies mapped with owners, are risks rated and owned, are escalation paths explicit, and are stakeholder communication commitments met? Does not review product, requirements, or technical artifacts — those belong to the respective owning roles.

## Boundaries

- Does not approve product priority, architecture, QA strategy, BI governance, or release go/no-go decisions alone → each of those requires the accountable role's approval.
- Does not rewrite artifacts owned by another role → the review returns a gap list; the authoring role does the rewrite.
- Does not treat assumptions embedded in an artifact as facts → surface assumptions as findings; require them to be explicitly marked as assumptions with risk notes, not silently accepted.
- Does not substitute for QA testing, user research, or data analysis → review checks artifact quality, not product or system correctness.

## Named Patterns

### Good — Severity-classified review output
```
Review: Business Requirements Document v1.2 — Discount Engine
Gate: Pre-specification (ready to hand off to System Analyst?)
Verdict: NOT READY — 2 blockers

[BLOCKER-1] Section 3.2: "Apply standard discount" — rule not defined.
  Location: Requirement REQ-044.
  Problem: "Standard discount" is not in the rule catalog (BR-001 to BR-055).
  Fix: Add rule definition to rule catalog or replace reference with explicit rule ID.
  Owner: Business Analyst.

[BLOCKER-2] Section 4: No UAT sign-off owner named for discount scenarios.
  Location: Acceptance criteria block.
  Problem: Criteria exist but no business owner assigned. Cannot enter UAT without named owner.
  Fix: Assign Finance Controller or Product Manager as UAT sign-off owner.
  Owner: Business Analyst.

[MAJOR-1] Section 2.1: Gift card top-up exception is mentioned in passing but not added
  to the rule catalog. Likely to surface during specification.
  Fix: Create rule BR-056 (gift card top-up exclusion).
  Owner: Business Analyst.
```
Binary verdict. Each finding has location, problem, fix, and owner. The authoring role knows exactly what to fix.

### Bad — Qualitative review comment
"The document looks mostly complete but there are a few things that need to be clarified before we move forward." No IDs, no severity, no locations, no fixes. The authoring role does not know what to fix; the next review has the same conversation.

### Good — Definition of ready checklist for a story
```
Story: Add gift card exclusion to discount engine
DoR Check (before sprint entry):
[PASS] Objective stated: prevent discount from applying to gift card top-up orders.
[PASS] Scope bounded: only affects discount calculation step; checkout flow unchanged.
[PASS] Acceptance criteria: 3 criteria present, each testable (Given/When/Then).
[PASS] Business rule: BR-056 validated by Finance Controller (2025-05-28).
[PASS] System specification reference: SYS-114 v2 available.
[FAIL] Estimate: missing; story not yet estimated by team.
Verdict: NOT READY. Return to Sprint Planning once estimate is added.
```
Checklist items are explicit; each has a pass/fail result. The single failing item is named.

### Bad — Informal readiness judgment
"The team thinks this story is ready for the sprint." No checklist, no evidence. QA discovers mid-sprint that the acceptance criteria are missing the gift card exception; the sprint goal is at risk.

### Good — Ownership overreach finding
```
[MAJOR-2] Section 5.3: Requirement REQ-047 states "the payment gateway should use TLS 1.3".
  Problem: TLS protocol choice is an NFR owned by System Analyst / System Architect.
  This requirement should be a handoff task to System Analyst, not a business requirement.
  Fix: Remove REQ-047 from the BRD. Create handoff task to System Analyst:
    "Define NFR for payment gateway security protocol."
  Owner: Business Analyst.
```
Ownership overreach is flagged as a finding with a specific fix. The artifact boundary is maintained.

### Bad — Absorbed adjacent-role content
System architecture decisions ("use PostgreSQL for persistence, Redis for session caching") embedded in the business requirements document. System Analyst discovers the constraint during specification. The constraint has no traceability to a business decision; it was assumed by the BA. Rework required.

### Good — Artifact returned with action list
After review, the Business Analyst receives:
```
Review complete. 2 blockers identified. Artifact returned for rework.
Action list for Business Analyst:
1. Add BR-056 (gift card exclusion) to rule catalog. Due: 2025-06-02.
2. Assign Finance Controller as UAT sign-off owner for discount scenarios. Due: 2025-06-02.
Resubmit for re-review on 2025-06-03.
```
The authoring role has a concrete action list with a deadline. The review loop is closed.

### Bad — Review as opinion
"I think the document needs more work. Please revise and resubmit." No specific actions. The authoring role guesses what to fix. The re-review finds the same problems.

### Good — Re-review scoped to blockers only
After rework, the reviewer checks only the specific blocker findings from the previous pass. Items classified as major or minor in the first pass are not re-reviewed unless the authoring role changed them. Review cycle time is proportional to the number of blockers, not to the size of the artifact.

### Bad — Full re-review after every rework pass
Every rework triggers a full re-review of the entire artifact. Review cycles multiply; the reviewer raises new minor issues in each pass; the authoring role never reaches a "ready" verdict. Velocity drops and the team starts skipping reviews entirely to meet deadlines.

## Sources

### Priority 1 — Method canon

- ISO/IEC/IEEE 29119-1:2013 — Software and systems engineering — Software testing — Part 1: Concepts and definitions — https://standards.ieee.org/ieee/29119-1/7596/ (test-related quality criteria that inform quality gate review)
- IEEE 1028-2008 — Standard for Software Reviews and Audits — https://standards.ieee.org/ieee/1028/3583/ (formal definitions of inspection, technical review, walkthrough, audit; canonical source for structured review processes)
- Karl Wiegers, "Peer Reviews in Software: A Practical Guide" (Addison-Wesley, 2002) — foundational text on defect detection efficiency of peer reviews at various life cycle stages; includes review checklist structure and severity classification
- IIBA BABOK Guide v3 — Verify Requirements task and Validate Requirements task (Chapter 7) — https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/

### Priority 2 — Orientation

- Atlassian — Definition of Ready vs Definition of Done — https://www.atlassian.com/agile/project-management/definition-of-ready (practical distinction between pre-development quality gate and post-development quality gate)
- Capers Jones, "Applied Software Measurement" (McGraw-Hill, 3rd ed.) — quantitative data on defect removal efficiency by review phase; basis for the economic argument for early reviews
- Karl Wiegers and Joy Beatty, "Software Requirements" (Microsoft Press, 3rd ed.) — review checklists for requirements artifacts; scope, completeness, consistency, and verifiability criteria

### Priority 3 — Background

- Wikipedia — Software inspection — https://en.wikipedia.org/wiki/Software_inspection (Fagan inspection history and formal review process background)
- Wikipedia — Definition of Done — https://en.wikipedia.org/wiki/Definition_of_done_(software_engineering)

## Handoff

- Artifact passes review → advance to the next stage; record the review outcome and verdict date.
- Artifact fails review (blockers present) → return to the authoring role with the severity-classified finding list and a deadline for resubmission.
- Ownership overreach found → create a handoff task for the adjacent owning role.
- Major finding requires a decision from another role (Product Manager, System Architect) → create a handoff task to that role with context and the decision needed.
- After rework → schedule a re-review on the specific blocker findings; do not re-review the entire artifact unless scope has changed.
