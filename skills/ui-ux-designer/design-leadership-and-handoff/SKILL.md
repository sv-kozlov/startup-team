---
name: design-leadership-and-handoff
description: Use when lead-level design direction, review standards, process quality, mentoring, cross-team design alignment, or handoff quality governance is needed — and when preparing or auditing developer-ready design artifacts for correctness, completeness, and implementation clarity.
family: lead
profile_level: Lead+
---

# Design Leadership and Handoff

## Purpose

Provide lead-level design direction and quality practices, and ensure that design handoffs to development are complete, unambiguous, and implementation-ready. At Senior level, handoff is mechanical artifact preparation; at Lead level, handoff becomes a quality standard enforced across the team — a gate that prevents implementation drift, rework, and QA failures caused by incomplete specifications.

## Use When

- A product area needs design direction, review standards, or quality gates.
- Several designers or teams must align around interaction patterns, UX principles, or design-system usage.
- Design process, critique, handoff, or review practice needs improvement.
- A design is ready (or claimed to be ready) for development and needs a handoff completeness audit.
- Developers need states, assets, component mapping, responsive rules, or interaction notes and these are missing or ambiguous.
- QA needs expected UI behavior and visual acceptance notes and these are incomplete.
- Implementation drift is discovered — production diverges from the design intent.

## Do Not Use When

- The design has not yet been completed — run `wireframing-and-prototyping`, `ui-composition-and-visual-hierarchy`, or `forms-and-complex-workflows` first.
- A usability or design quality review is needed — use `usability-and-design-review`.
- Product roadmap, backlog, delivery dates, or resource management is the topic — hand off to `product-manager`, `product-owner`, or `project-manager`.
- Design-system roadmap, governance, or versioning is the topic — hand off to Design System Lead.
- Line management, HR, or formal performance evaluation is required.

## Inputs

**For leadership:**
- Product area, current artifacts, team structure, design issues, design-system rules, process pain points, and adjacent-role ownership.
- Review findings, implementation drift, stakeholder conflicts, or quality risks.

**For handoff:**
- Final or near-final mockups, prototype, flow, components, tokens, states, and constraints.
- System/API notes, acceptance criteria, frontend constraints, and QA concerns.
- Scope, target platforms, breakpoints, and readiness status.

## Workflow

1. **Define the design quality problem or handoff scope.** For leadership: what design quality issue exists? Who is affected? What decision is needed? For handoff: what screens are in scope, what platforms and breakpoints, what is the expected next step (development sprint start / QA readiness / stakeholder approval)?

2. **Establish or audit design quality criteria.** Lead-level: define criteria for the team — what does "ready for development" mean? What must be present in a handoff? What does "ready for QA" mean? Criteria examples: all states annotated, all components named with design-system slug, all responsive breakpoints documented, all copy finalized, all open questions resolved or explicitly flagged.

3. **Audit handoff artifacts against the criteria.** Check: Screens and states — are all states (empty, error, loading, success, permission, partial) present and annotated? Components — are all UI elements mapped to design-system components with variant names? Copy — is all text final (not Lorem Ipsum or TBD)? Responsive behavior — are all breakpoints documented with explicit stacking/hiding rules? Open questions — are all unresolved items listed with an owner?

4. **Conduct critique or align design direction.** For Lead-level: facilitate critique sessions without making all the decisions. Critique gives structured feedback on design decisions; it does not replace designer ownership. Separate blocking issues, improvements, and preferences. Establish design principles that guide future decisions without requiring a Lead review for every choice.

5. **Identify systemic issues that require adjacent-role ownership.** Design-system gap → Design System Lead. Product decision blocked → `product-manager`. System behavior unclear → `system-analyst`. Frontend feasibility question → `frontend-developer`. QA state coverage gap → `qa-engineer`.

6. **Produce handoff deliverables and quality documentation.** Handoff brief: screens, states, components, assets, copy, interactions, responsive behavior. Quality gate summary: what is complete, what is deferred (with explicit agreement), what remains open. If implementation drift is discovered post-handoff: document the delta, decide with product and tech whether to fix in code or update the design, create a correction handoff.

7. **Track and close open items.** Handoff is not complete when the Figma file is shared — it is complete when all open questions have answers and all required items are in the developer's hands. Lead-level: establish a handoff checklist that the team uses consistently, not just for this task.

## Outputs

**Leadership outputs:**
- Design direction brief.
- Design quality criteria for the team or product area.
- Critique plan or review process improvements.
- Mentoring and practice improvement recommendations.
- Cross-role handoff task list.

**Handoff outputs:**
- Development handoff brief (screens, states, components, assets, copy, interaction notes).
- Responsive behavior and breakpoint notes.
- Component and asset checklist (all items with design-system slug and variant).
- Open questions and role handoffs.
- Handoff completeness audit result (ready / not ready / ready with noted exceptions).
- Correction handoff brief (if implementation drift found post-launch).

## Named Patterns

**Good — Handoff completeness checklist:**
> "Before marking this design ready for sprint: (1) All screens present including: empty, loading, error, success, permission states. (2) All components named as design-system slugs (e.g. Button/primary, Input/default, Alert/destructive). (3) All copy is final — no Lorem Ipsum or 'TBD copy here.' (4) Responsive behavior documented: mobile stacking, breakpoints, touch targets. (5) Open questions have owners: 'API error taxonomy — SA to confirm by Friday.' Status: 4/5 complete. Blocking item: error taxonomy not confirmed."

**Bad — Handoff as Figma file share:**
> "Link to Figma file shared in Slack: 'Here's the design, let me know if you have questions.' Developer has 12 questions 2 days later. QA builds test cases that don't match design. Implementation diverges from intent." (Handoff is not a file share — it is a readiness state.)

**Good — Design critique with structured feedback:**
> "Feedback on checkout step 2: Blocking — the error state is not designed; developer will guess the behavior. Major — 'Continue' button is below the fold on mobile; task completion requires scroll. Improvement — secondary action 'Save for later' would reduce abandonment. Preference — I prefer the rounded corners but this is not a user problem."

**Bad — Critique as subjective redesign:**
> "I would have done this completely differently. The hierarchy is wrong, the colors are off, and the layout feels cluttered." (No heuristic, no severity, no specific fix, no rationale — critique as personal taste displaces design ownership.)

**Good — Design principle as a decision rule:**
> "Principle for this product area: 'Show the user's current state before asking them to act.' Applied: dashboard shows account health status before surfacing upgrade CTAs. Applied: form shows saved progress before asking for new inputs."

**Bad — Generic UX platitude as a principle:**
> "Be user-centered." (Not a decision rule — does not help the team choose between design options.)

**Good — Implementation drift correction:**
> "QA review found: mobile navigation uses bottom tabs instead of the designed hamburger menu (implementation drift). Decision with PM and Tech Lead: revert to designed behavior in next sprint — bottom tabs violate platform pattern for this app type and were not the agreed solution. Correction handoff brief created."

**Bad — Ignoring implementation drift:**
> "'It works, ship it.' Design intent was a progressive disclosure flow; implementation is a flat form. Difference affects task completion rate and is measurable — but it is not caught because no handoff verification was done post-implementation."

## Boundaries

- Does not own product roadmap, backlog, delivery plan, or resource/budget governance → `product-manager`, `product-owner`, `project-manager`.
- Does not own design-system roadmap, governance, versioning, or adoption metrics unless explicitly assigned as Design System Lead.
- Does not replace line management, HR, or formal performance evaluation.
- Does not approve product launch decisions → `product-owner` + `product-manager`.
- Does not own QA strategy, test cases, or release regression → `qa-engineer`.

## Sources

**Priority 1:**
- Nielsen Norman Group, Design Critiques: https://www.nngroup.com/articles/design-critiques/
- Figma Dev Mode (handoff tooling): https://www.figma.com/dev-mode/
- Figma developer docs, Working in Dev Mode: https://developers.figma.com/docs/plugins/working-in-dev-mode/
- Storybook Docs (component handoff): https://storybook.js.org/docs

**Priority 2:**
- Design Council, Double Diamond (design leadership framing): https://www.designcouncil.org.uk/our-resources/the-double-diamond/
- Atlassian, Agile design: https://www.atlassian.com/agile/design
- Inside Design InVision, Design Handoff Guide: https://www.invisionapp.com/inside-design/design-handoff-guide/

**Priority 3:**
- Smashing Magazine, Effective Design Handoff: https://www.smashingmagazine.com/2020/12/designers-developers-working-together-effectively/
- A List Apart, Design Systems and Constraints: https://alistapart.com/article/selling-design-systems/

## Handoff

```
To: frontend-developer
Task: Implement UI from development handoff brief
Context: Handoff brief is complete — all states, components, tokens, responsive behavior, and copy are documented
Inputs: Handoff brief, annotated Figma file, component mapping, breakpoint spec, token brief
Expected artifact: Implemented UI confirmed against handoff spec; implementation delta noted
Acceptance criteria: All states implemented; QA can run visual acceptance test against handoff spec
```

```
To: qa-engineer
Task: Build visual acceptance test plan from handoff brief
Context: Development handoff brief defines all expected UI states and behavior
Inputs: Handoff brief, state matrix, responsive notes, component checklist
Expected artifact: QA test plan covering visual acceptance, state behavior, and responsive behavior
Acceptance criteria: Each handoff item has a corresponding QA check; defect reporting links to handoff spec
```
