---
name: wireframing-and-prototyping
description: Use when turning user flows, product goals, or requirements into wireframes, clickable prototypes, interaction logic, state coverage per screen, and validation-ready UX concepts — choosing fidelity that matches the decision to be made.
family: method
profile_level: Senior+
---

# Wireframing and Prototyping

## Purpose

Create the smallest useful representation of an interface concept that lets the team discuss, test, refine, or hand off the solution. A wireframe is a structure-and-behavior contract, not a visual decoration exercise. Every wireframe should cover not only the happy state but all critical states for the screens it represents.

## Use When

- A flow or feature needs low- or mid-fidelity exploration before high-fidelity UI or development.
- Stakeholders need to compare solution options without investing in polished visuals.
- A prototype is needed for usability testing, stakeholder review, or development clarification.
- Interface states (empty, error, loading, disabled, partial, permission-restricted) need to be specified for a set of screens.
- An interaction model, transition logic, or conditional behavior needs to be made explicit before handoff.

## Do Not Use When

- The problem has not been framed — use `design-discovery-and-research` first.
- Structure and navigation have not been defined — use `information-architecture-and-user-flows` first.
- A formal usability study with scenario tasks and synthesis is required — hand off to `ux-researcher`.
- Production code is needed — hand off to `frontend-developer`.
- High-fidelity visual design with brand application is the deliverable — this skill covers structure and interaction, not final visual execution.

## Inputs

- User flow, IA, requirements, constraints, target platform, and known states.
- Existing components, design-system rules, and token constraints.
- Research questions or validation goal if the prototype is for testing.
- State inventory: all data states, permission levels, API responses, and edge conditions for the screens in scope.

## Workflow

1. **Choose fidelity based on the decision to be made.** Low-fi (sketch / rough wireframe): for alignment on structure and flow before investing detail. Mid-fi (annotated wireframe): for state coverage, team review, and development scoping. High-fi prototype: for usability testing or stakeholder approval of interaction design. Never reach for high fidelity until structure and state coverage are confirmed.

2. **Start with the primary task screen, then branch.** Wireframe the screen that carries the main user action first. Then add: empty state (no data yet), loading state (data fetching), error state (system failure), validation state (user input error), partial state (incomplete data or permissions), success state (task completed).

3. **Annotate state triggers and behavior.** For each non-default state, label: what triggers it, what the user sees, what action is available, and what happens on that action. This annotation is what developers and QA read — it is not decorative.

4. **Keep visual detail proportional to the decision stage.** At wireframe stage: layout and hierarchy matter; pixel-level color and typography do not. Add real or representative content (not Lorem Ipsum) where content length or type affects layout decisions.

5. **Mark design system constraints.** Note which components map to existing design-system patterns and where a new pattern may be needed. This prepares the handoff to `design-system-and-tokens` and prevents layout decisions that cannot be implemented with existing components.

6. **Build the prototype connection map.** Define which screens link to which, under what conditions, with what transitions. For usability test prototypes: define the scenario task entry point and mark which paths are in scope for the test.

7. **Identify open questions and handoff needs.** Missing data states → `system-analyst`. Business rule ambiguity → `business-analyst`. Unfamiliar platform component → `frontend-developer` for feasibility check. Research question unresolved → `ux-researcher`.

## Outputs

- Wireframe set (annotated screens with state coverage per screen).
- Clickable prototype brief (screen connection map, scenario entry points, scope).
- Alternative concepts (if comparing approaches).
- State inventory: list of all states covered per screen and any remaining gaps.
- Validation questions and open assumptions.
- Handoff notes: design system constraints, feasibility questions, missing specs.

## Named Patterns

**Good — Fidelity matched to decision stage:**
> "We are comparing two navigation approaches before committing to one. Producing rough low-fi wireframes (15 min each approach) to test structural logic with the PM and SA. Not producing high-fi mockups for a decision that will likely change the entire layout."

**Bad — High-fidelity too early:**
> "I spent 2 days on a polished UI mockup with real colors, icons, and typography. The PM reviewed it and asked to change the navigation model — now all visual work is invalidated." (High fidelity spent on unvalidated structure.)

**Good — State coverage per screen:**
> "Checkout step 2 (payment form) has 6 states: default, card number invalid (inline error on blur), card expired, CVV mismatch, payment declined (server error with retry option), and payment success. All 6 are wireframed with annotation."

**Bad — Only happy path wireframed:**
> "Here is the checkout flow with 5 screens." (No empty state, no errors, no loading — QA will invent behavior, developers will guess, and users will encounter blank screens and unexplained failures.)

**Good — Annotation as a behavior contract:**
> "State: 'no items in cart' (empty). Trigger: user lands on cart page with zero items. Display: illustration + 'Your cart is empty' + 'Browse products' CTA. No 'Checkout' button. On CTA: navigate to product catalog."

**Bad — Wireframe without annotation:**
> "Screens shared in Figma without notes. Developers ask: what happens if cart is empty? Designer answers in Slack 3 days later." (State behavior is implicit; handoff is unreliable.)

**Good — Low-fi with representative content:**
> "Product card wireframe uses a realistic product name (14 chars), price ($12.99), and a badge ('New') to validate layout at real content length — not 'Product Title Here' placeholder."

**Bad — Lorem Ipsum hiding layout problems:**
> "'Lorem ipsum dolor sit amet...' fills all text fields. Deployed: product names truncate at 8 characters. Truncation was invisible in the wireframe." (Placeholder content conceals real-content layout failure.)

## Boundaries

- Does not replace `ux-researcher` for formal study design, recruiting, or moderated synthesis.
- Does not decide product direction or feature scope → `product-manager`.
- Does not produce production code or frontend components → `frontend-developer`.
- Does not own design-system governance or token definitions → `design-system-and-tokens` + Design System Lead.
- Does not specify API error taxonomy or business rule logic — annotates them as requirements for `system-analyst` and `business-analyst`.

## Sources

**Priority 1:**
- Nielsen Norman Group, Wireframing: https://www.nngroup.com/articles/wireframing-steps-guide/
- Nielsen Norman Group, Paper Prototyping: https://www.nngroup.com/articles/paper-prototyping/
- GOV.UK Prototype Kit (low-fi convention): https://prototype-kit.service.gov.uk/
- Figma Help, Guide to prototyping: https://help.figma.com/hc/en-us/articles/360040314193-Getting-Started-with-Prototyping

**Priority 2:**
- Nielsen Norman Group, Fidelity of UX Prototypes: https://www.nngroup.com/articles/ux-prototype-hi-lo-fidelity/
- Inside Design InVision, Wireframe vs Mockup vs Prototype: https://www.invisionapp.com/inside-design/wireframe-mockup-prototype/

**Priority 3:**
- Smashing Magazine, Effective Wireframing: https://www.smashingmagazine.com/2020/04/wireframing-best-practices/

## Handoff

```
To: frontend-developer
Task: Confirm layout feasibility for proposed wireframe composition
Context: Wireframe uses a non-standard layout that may conflict with auto-layout constraints
Inputs: Annotated wireframe, component notes, responsive behavior notes
Expected artifact: Feasibility note (possible as-is / possible with modification / requires new component)
Acceptance criteria: Response covers: desktop + mobile behavior, design-system impact
```

```
To: qa-engineer
Task: Build test cases from wireframe state inventory
Context: Wireframe includes state coverage annotations for all non-default states
Inputs: Annotated wireframe set, state inventory list
Expected artifact: QA test case outline covering all annotated states
Acceptance criteria: Each wireframe state has a corresponding test case with trigger and expected behavior
```
