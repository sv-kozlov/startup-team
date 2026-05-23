---
name: usability-and-design-review
description: Use when reviewing an interface, prototype, flow, or design artifact for usability risks, heuristic issues, friction, design quality, consistency, state coverage, handoff readiness, ownership boundaries, and iteration-readiness — combining heuristic evaluation with design critique into a single review pass.
family: method
profile_level: Senior+
---

# Usability and Design Review

## Purpose

Detect usability problems and design quality issues before research, development, QA, or release — and translate findings into actionable recommendations. This skill combines heuristic usability review (detecting friction, confusion, error recovery problems) with design critique (checking completeness, consistency, ownership, and handoff readiness). Both are conducted in the same pass because they share the artifact and the review perspective. When evidence from analytics, research, or support points to a specific friction area, this skill also frames the next iteration direction.

## Use When

- A design needs a heuristic review before testing, development, or release.
- A flow, prototype, UI mockup, or handoff needs critique for quality and readiness.
- Users may struggle with navigation, feedback, language, error recovery, or task flow.
- A team needs a prioritized list of UX risks and design improvements.
- A design may violate accessibility, consistency, state coverage, or ownership boundaries.
- Analytics, usability evidence, or support feedback points to a specific friction area and the design must be reviewed against that evidence before the next iteration.

## Do Not Use When

- The design has not yet reached wireframe or prototype stage — use `wireframing-and-prototyping` to produce the artifact first.
- A formal user study with recruited participants is required — hand off to `ux-researcher`.
- Statistical impact measurement or A/B test design is needed — hand off to `product-analyst`.
- Product launch decisions, release approval, or QA strategy are in scope — these are owned by `product-owner`, `product-manager`, and `qa-engineer`.

## Inputs

- Prototype, UI mockup, flow, wireframe, or design artifact.
- User goal, target audience, task scenario, and platform.
- Known constraints, decisions, and acceptance criteria.
- Analytics, support feedback, research findings, or usability evidence (if available).
- Design-system rules, requirements, and expected handoff state.

## Workflow

1. **Define the review target and perspective.** State: what artifact is being reviewed, for what user goal, for what team decision (should this go to development? should this be tested?). Separate the artifact's purpose from its quality — the review is always against the stated purpose.

2. **Check core usability heuristics (Nielsen 10).** Work through all 10 in order:
   - Visibility of system status: does the user know what is happening?
   - Match to real world: does the interface use user language and concepts?
   - User control and freedom: can the user undo, cancel, or go back?
   - Consistency and standards: are UI patterns used consistently across screens?
   - Error prevention: does the design prevent errors before they occur?
   - Recognition over recall: is information visible rather than requiring memory?
   - Flexibility and efficiency: are shortcuts or affordances available for expert users?
   - Aesthetic and minimalist design: is there information that is rarely needed and dilutes focus?
   - Help users recognize, diagnose, recover from errors: are error messages clear and actionable?
   - Help and documentation: if needed, is help findable and task-oriented?

3. **Check design quality: completeness, consistency, state coverage.** Completeness: are all screens, states, and edge cases accounted for? Consistency: are components, spacing, labels, and patterns used consistently with the design system? State coverage: are all non-happy-path states (empty, error, loading, success, permission) present?

4. **Check ownership and handoff readiness.** Does the design overstep into requirements, system spec, or product strategy? Are all handoff needs identified (frontend, QA, SA, BA)? Are annotations present and sufficient? Is the design specific enough to implement without guessing?

5. **If evidence from analytics or research is available — connect findings to the review.** When support tickets report error-recovery failures, check the specific error states in the design. When funnel data shows drop-off at a specific step, check that step for heuristic violations and friction. The review is evidence-grounded, not purely expert opinion.

6. **Classify findings by severity.** Blocker: will prevent task completion or cause significant user harm. Major: causes significant friction, confusion, or error rate increase. Minor: causes inconvenience but users can work around it. Improvement: not a problem, but a better solution exists. Preference: subjective, not validated as a user problem.

7. **Separate findings from iteration direction.** For each blocker or major finding: propose a concrete fix. For findings that require user evidence to validate: create a research handoff. Do not present subjective design preferences as usability findings.

## Outputs

- Usability findings ordered by severity (blocker / major / minor / improvement / preference).
- Recommended fixes for each blocker and major finding.
- Design quality review (completeness, consistency, state coverage check results).
- Handoff readiness assessment.
- Research questions or handoff tasks for findings that need user validation.
- Evidence-to-finding trace when analytics or support data is the input.
- Residual risks and assumptions.

## Named Patterns

**Good — Heuristic finding with severity and fix:**
> "H9 (Error recovery): MAJOR. Checkout step 3, payment declined state shows 'An error occurred' with no recovery action. User cannot retry, change payment method, or contact support from this screen. Fix: add 'Try again' button, 'Change payment method' link, and support contact. Expected impact: reduce payment abandonment at error state."

**Bad — Preference stated as usability finding:**
> "The button color is blue, which feels cold. It should be warmer to encourage action." (Subjective aesthetic preference with no user evidence — not a usability finding. Would not survive a prioritized defect list.)

**Good — Evidence-grounded review:**
> "Support tickets (past 30 days): 47 reports of 'I can't find how to cancel my subscription.' Usability review of settings page: 'Cancel subscription' is in Account > Settings > Plan > Manage > Advanced. Heuristic violation: recognition over recall (H6) — the option requires 4 navigation steps and is labeled 'Advanced' which does not suggest cancellation. Recommendation: surface 'Cancel subscription' at Plan level, direct label."

**Bad — Usability review without evidence context:**
> "The settings page has too many options. It should be simplified." (Unsupported opinion — no heuristic, no user evidence, no specific finding, no proposed fix. Does not help the team make a decision.)

**Good — Scenario-based review with task framing:**
> "Review perspective: user who has never used the product, completing first-time onboarding (step 1: create account). Heuristic 2 (match to real world): step 1 asks for 'handle' — users in target segment use Instagram and understand 'username.' Recommend changing label from 'Handle' to 'Username.'"

**Bad — Review without user context:**
> "The onboarding is confusing." (Who is the user? What task? What specifically is confusing? Not actionable.)

**Good — Design quality check finding:**
> "State coverage gap: product list screen is wireframed for loaded state only. Missing: loading skeleton, empty state (no products matching filter), error state (API failure), and partial state (some products load, image fails). All four are needed before development. Returning for state completion before handoff."

**Bad — Rubber-stamp review:**
> "Design looks good, ready to hand off." (No heuristic check, no state coverage check, no consistency review — design review as a formality rather than a quality gate.)

## Boundaries

- Does not replace `ux-researcher` for study design, recruiting, moderated sessions, or synthesis.
- Does not make product launch decisions — those belong to `product-owner` and `product-manager`.
- Does not produce statistical proof of impact → `product-analyst`.
- Does not approve QA strategy, test cases, or regression → `qa-engineer`.
- Does not rewrite adjacent-role artifacts unless explicitly asked.
- Does not treat subjective taste as a defect without user-evidence rationale.

## Sources

**Priority 1:**
- Nielsen Norman Group, 10 Usability Heuristics: https://www.nngroup.com/articles/ten-usability-heuristics/
- Nielsen Norman Group, Heuristic Evaluation: https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/
- Nielsen Norman Group, Design Critiques: https://www.nngroup.com/articles/design-critiques/
- Nielsen Norman Group, Usability Testing 101: https://www.nngroup.com/articles/usability-testing-101/

**Priority 2:**
- Nielsen Norman Group, Analytics and UX: https://www.nngroup.com/articles/analytics-user-experience/
- Google HEART Framework: https://research.google.com/pubs/pub36299.html
- W3C WCAG 2.2 (for accessibility dimension of review): https://www.w3.org/TR/WCAG22/

**Priority 3:**
- Smashing Magazine, UX Reviews: https://www.smashingmagazine.com/2011/06/improving-ux-through-front-end-performance/
- A List Apart, The Shallows of Critique: https://alistapart.com/article/critique-is-an-act-of-love/

## Handoff

```
To: ux-researcher
Task: Validate usability findings that require user evidence
Context: Heuristic review identified friction areas; severity classified as major but not confirmed by user data
Inputs: Usability findings list, severity classification, unvalidated assumptions
Expected artifact: Research plan or 3–5 session guerrilla test results confirming or disconfirming major findings
Acceptance criteria: Each unvalidated major finding addressed; confirmed/rejected with user evidence
```

```
To: product-analyst
Task: Provide metric context for evidence-grounded review findings
Context: Review references funnel drop-off or support ticket clusters; need metric baseline
Inputs: Specific friction areas identified in review, current metric values if known
Expected artifact: Baseline metric for friction areas, signal definition for measuring improvement
Acceptance criteria: Metric baseline established; signal agreed for iteration validation
```
