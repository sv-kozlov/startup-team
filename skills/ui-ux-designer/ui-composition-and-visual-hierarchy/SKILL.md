---
name: ui-composition-and-visual-hierarchy
description: Use when designing or reviewing screen layouts, visual hierarchy, typography, spacing, density, affordances, adaptive behavior, breakpoints, touch targets, and platform conventions — for any target device context (desktop, tablet, mobile, embedded).
family: method
profile_level: Senior+
---

# UI Composition and Visual Hierarchy

## Purpose

Make screens readable, scannable, actionable, and consistent with the product's goals across all target platforms. Composition decisions (layout structure, hierarchy, spacing, density) and adaptive decisions (breakpoints, stacking, touch targets) are made in the same pass because they are inseparable: a hierarchy decision for desktop that ignores mobile reflow is incomplete.

## Use When

- A screen needs layout direction or visual design review.
- Users must compare, scan, prioritize, or act on complex information.
- UI density, hierarchy, typography, spacing, or affordance clarity is at risk.
- A design must adapt across desktop, tablet, mobile, or embedded contexts.
- Breakpoints, wrapping, resizing, sticky areas, touch targets, or density need definition.
- Platform conventions (iOS vs. Android vs. web) or mobile interaction patterns are unclear.
- A layout is reviewed for consistency with the design system before handoff.

## Do Not Use When

- Screen structure has not been defined — use `wireframing-and-prototyping` first.
- Brand identity, marketing campaign visuals, or editorial design is the goal — hand off to Brand / Communication Design.
- Frontend implementation, performance, or code architecture is needed — hand off to `frontend-developer`.
- The task is purely a design-system token or component decision — use `design-system-and-tokens`.

## Inputs

- User goal, primary task, and decision the screen must support.
- Content inventory, actions, entity types, and data density constraints.
- Target device contexts, platform constraints, and breakpoints.
- Design-system components, semantic tokens, grid, and spacing rules.
- Existing screen, wireframe, prototype, or UI mockup.
- Analytics by device (if available) for prioritization of mobile vs. desktop hierarchy.

## Workflow

1. **Identify the primary task and decision the screen must support.** A screen has one primary action; everything else is secondary or tertiary. If a screen has two equally prominent primary actions, that is a hierarchy failure, not a design choice.

2. **Rank content and actions by user value, risk, and frequency.** Use this ranking to drive visual weight, position, size, and contrast. High-value, high-frequency actions sit at the top of the visual hierarchy. Destructive actions are visually de-emphasized and placed away from primary actions.

3. **Define layout structure for desktop first, then adapt.** Set the grid, grouping, whitespace, and visual hierarchy for the primary viewport. Then define adaptive behavior for each breakpoint: what stacks, what wraps, what collapses, what is hidden, what changes position.

4. **Check adaptive behavior explicitly.** For each element: does it stack or wrap gracefully? Is touch target ≥ 44×44pt (Apple) / 48×48dp (Material) on mobile? Is content density appropriate for the screen size? Is sticky navigation or toolbar behavior defined for scroll contexts?

5. **Check readability and scan path.** Apply F-pattern and Z-pattern reading order logic. Check: contrast ratio meets WCAG 2.2 AA (4.5:1 for normal text, 3:1 for large text). Line length is 50–75 characters for body text. Font size is ≥16px for body on web; ≥14sp on mobile.

6. **Check platform conventions.** Navigation patterns differ by platform: bottom tab bar on iOS/Android, sidebar or top nav on web. Swipe, back-button, and gesture behaviors differ. Flag any design that violates a platform's primary navigation convention.

7. **Mark design-system inconsistencies and handoff notes.** Note spacing values that don't map to the token scale, typography that doesn't match text styles, components used outside their intended context, and any responsive behavior that needs frontend confirmation.

## Outputs

- Layout recommendation (structure, grouping, hierarchy, spacing).
- Responsive adaptation brief (breakpoint behavior, stacking, hiding, touch targets).
- Visual hierarchy review findings.
- Platform convention check notes.
- UI issue list with suggested fixes.
- Design-system and accessibility handoff notes.

## Named Patterns

**Good — Single primary action per screen:**
> "Dashboard: primary action is 'Create new report' (top-right, filled primary button). All other actions — filter, export, sort — are secondary (icon buttons or text links). Hierarchy is clear; eye-tracking would confirm top-right fixation first."

**Bad — Competing primary actions:**
> "'Save' and 'Publish' are both large, filled, blue buttons at the same visual weight. Users do not know which to press first — both are treated as equally important." (Two primary actions at the same hierarchy level cause decision paralysis.)

**Good — Adaptive layout with explicit breakpoint behavior:**
> "Desktop: 3-column card grid. Tablet (768px): 2-column grid. Mobile (<480px): 1-column list, card image collapsed to icon. Navigation collapses to bottom bar. Filter panel moves from sidebar to bottom sheet."

**Bad — Mobile treatment not designed:**
> "'The mobile version will just stack.' (No breakpoint spec, no consideration of navigation, dense data tables not adapted for touch — developers implement a broken layout.)"

**Good — Touch target size confirmed:**
> "Icon buttons in the action toolbar: 44×44pt tap area (icon is 24×24, surrounded by 10pt padding on all sides). Confirmed against Apple HIG minimum. On desktop, same layout is fine at smaller visual size due to pointer precision."

**Bad — Touch targets from desktop assumptions:**
> "Icon buttons at 20×20px on mobile. Users report tapping wrong buttons constantly — the tap target is 50% below the platform minimum. This is a design defect, not a development issue."

**Good — WCAG-aligned contrast check:**
> "Body text: #1A1A1A on #FFFFFF → 18.1:1 contrast ratio (AAA). Primary button label: #FFFFFF on #1D4ED8 → 5.6:1 (AA passed). Muted helper text: #9CA3AF on #FFFFFF → 2.5:1 (FAILS AA — flagged for redesign; using #6B7280 gives 4.6:1)."

**Bad — Contrast not checked:**
> "'Light gray text looks subtle and clean.' Deployed with 2.5:1 contrast. Users with low vision cannot read helper text. WCAG 2.2 AA failure goes undetected until accessibility audit."

## Boundaries

- Does not own brand identity, campaign visuals, or communication design → Brand / Communication Design.
- Does not own final product priority or content policy → `product-manager`.
- Does not implement frontend layout or CSS → `frontend-developer`.
- Does not own mobile app architecture or release policy → `mobile-developer` / Tech Lead.
- Does not override platform design-system conventions without an explicit rationale reviewed by the design system owner.

## Sources

**Priority 1:**
- Apple Human Interface Guidelines: https://developer.apple.com/design/human-interface-guidelines
- Material Design 3, Adaptive design: https://m3.material.io/foundations/adaptive-design/overview
- W3C WCAG 2.2 (contrast criteria): https://www.w3.org/TR/WCAG22/
- Nielsen Norman Group, Visual Hierarchy: https://www.nngroup.com/articles/visual-hierarchy-ux-definition/

**Priority 2:**
- Figma Help, Auto layout: https://help.figma.com/hc/en-us/articles/360040451373-Explore-auto-layout-properties
- Nielsen Norman Group, F-Pattern Reading: https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/
- Refactoring UI (Adam Wathan, Steve Schoger): https://www.refactoringui.com/

**Priority 3:**
- Inside Design InVision, Responsive Design Best Practices: https://www.invisionapp.com/inside-design/responsive-design-best-practices/
- Smashing Magazine, Designing for Touch: https://www.smashingmagazine.com/2016/11/designing-ar-challenges-and-considerations/

## Handoff

```
To: frontend-developer
Task: Confirm adaptive layout implementation for defined breakpoints
Context: Responsive behavior spec is ready; need feasibility and component confirmation
Inputs: Layout brief, breakpoint table, component notes, touch target specs
Expected artifact: Implementation notes (which components handle each adaptive state, any known constraints)
Acceptance criteria: Each breakpoint behavior addressed; constraints flagged before design is finalized
```

```
To: mobile-developer
Task: Confirm platform-specific interaction conventions for proposed navigation pattern
Context: Design proposes a navigation model that may differ from iOS/Android conventions
Inputs: Navigation design, platform target, interaction notes
Expected artifact: Platform conformance review — accepted as-is / adjusted / needs redesign
Acceptance criteria: Covers both iOS and Android if applicable; references platform guidelines
```
