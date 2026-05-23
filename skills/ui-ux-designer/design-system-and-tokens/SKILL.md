---
name: design-system-and-tokens
description: Use when applying design-system components, semantic tokens, variants, and patterns to a product design task — including shadcn/ui component mapping, semantic CSS variable intent, light/dark theme design, and identifying when a new pattern or contribution is needed.
family: method
profile_level: Senior+
---

# Design System and Tokens

## Purpose

Use the design system correctly in product work. Apply existing components, semantic tokens, and patterns before proposing custom UI. Identify gaps that require a contribution. This skill covers both the general design system methodology and the shadcn/ui-specific application (the project's adopted component system), treating shadcn/ui component mapping and token design as implementation details within the broader skill, not as separate capabilities.

## Use When

- A design must use existing components, variants, semantic tokens, or patterns.
- A screen appears inconsistent with the design system.
- A product need may require a component or pattern contribution.
- A design references raw hex or RGB values instead of semantic tokens.
- A project using shadcn/ui needs component mapping, variant selection, or theme token design.
- Dark mode, high-contrast mode, or alternate themes need token-level design intent.
- Chart, sidebar, focus ring, destructive state, muted surface, or overlay surfaces need semantic naming.

## Do Not Use When

- The design-system roadmap, governance, versioning, or contribution model is the topic — hand off to Design System Lead.
- Frontend component implementation, Tailwind configuration, or CSS variable files need to be changed — hand off to `frontend-developer`.
- Brand identity creation or visual language definition is needed — hand off to Brand / Communication Design.
- The task is about screen layout or visual hierarchy — use `ui-composition-and-visual-hierarchy`.

## Inputs

**General:**
- Current UI, design-system rules, component library, semantic tokens, platform, and frontend constraints.
- Product-specific flow, states, and content.

**shadcn/ui-specific (when applicable):**
- Project context: `components.json`, installed components, style (default/new-york), base color, Tailwind version, CSS variable file, dark-mode strategy.
- Existing semantic token set: `background`, `foreground`, `card`, `popover`, `primary`, `secondary`, `muted`, `accent`, `destructive`, `border`, `input`, `ring`, chart tokens (`--chart-1` to `--chart-5`), sidebar tokens, and radius scale.
- Brand palette, typography rules, radius preferences, and accessibility contrast targets.

## Workflow

1. **Check existing components and patterns first.** Before proposing a custom UI element, look for an existing component, variant, block, or pattern. For shadcn/ui: check shadcn blocks (https://ui.shadcn.com/blocks) — many screen-level patterns are already composed. Reuse before proposing custom UI.

2. **Map product states to component semantics.** Button variants, field validation states, selected states, disabled states, skeleton/loading, alerts, dialogs, sheets, drawers, tabs, menus, and tooltips all have defined semantics. Map product requirements to these semantics — do not create a new "warning button" when `variant="destructive"` or a secondary variant serves the purpose.

3. **Design token intent for all surfaces and states.** Token names must encode purpose, not color. Examples:
   - Surface hierarchy: `--background` → `--card` → `--popover` (not `white-bg`, `card-white`, `modal-bg`)
   - State: `--destructive` for error/danger intent (not `red`, `#EF4444`)
   - Interactive: `--ring` for focus rings (not `blue-outline`)
   - For shadcn/ui: define all semantic variables for both `:root` (light) and `.dark` modes. Chart tokens (`--chart-1` to `--chart-5`) are assigned by data-series role, not by aesthetic hue preference.

4. **Check token contrast in both modes.** For each token pair (foreground on background), confirm contrast meets WCAG 2.2 AA (4.5:1 for normal text, 3:1 for large text) in both light and dark themes. When a brand color does not meet contrast requirements, propose a derivative token (adjusted lightness/chroma) rather than bypassing the constraint.

5. **Check composition rules that affect design intent.** Specific patterns for shadcn/ui:
   - `Dialog` requires a `DialogTitle` — do not suppress it (accessibility violation).
   - `Sheet` and `Drawer` follow the same title rule.
   - `Tabs` require `TabsList` containing all `TabsTrigger` elements — order matters for keyboard navigation.
   - `Form` fields require visible `Label` components (not placeholder-only inputs).
   - `Command` requires `CommandInput` + `CommandList` — do not render a command palette without the input.

6. **Identify component gaps and contribution candidates.** If no existing component satisfies the product need, document: the design problem, proposed component behavior, states, token needs, rationale, and usage. Create a contribution request for Design System Lead / Frontend, do not ship a one-off custom pattern silently.

7. **Produce a handoff brief.** Designer-facing: component mapping, token choices, rationale. Frontend-facing: component names, variants, any token overrides, CSS variable names, dark-mode behavior. Do not include CLI commands, import paths, or registry details — those belong to Frontend Engineering.

## Outputs

- Component usage recommendation (shadcn/ui or design-system).
- Semantic token mapping table (light and dark modes, with contrast ratios).
- Chart and sidebar token mapping with intent labels.
- Design-system consistency review.
- Component gap or contribution brief.
- Theme design brief for Frontend Engineering and Design System Lead.
- Handoff to Design System Lead or Frontend.

## Named Patterns

**Good — Semantic token naming:**
```json
{
  "--background": "0 0% 100%",
  "--foreground": "222.2 84% 4.9%",
  "--destructive": "0 84.2% 60.2%",
  "--destructive-foreground": "210 40% 98%",
  "--ring": "221.2 83.2% 53.3%"
}
```
> Each variable encodes purpose. `--destructive` is used on error buttons, error borders, and inline error icons — wherever destructive/danger intent exists.

**Bad — Raw hex colors in component:**
```json
{
  "errorColor": "#EF4444",
  "buttonDanger": "#DC2626",
  "alertBorder": "#F87171"
}
```
> Three different "red" values for the same semantic intent. Dark mode will not work. Token system is bypassed. Consistency breaks when the brand color changes.

**Good — shadcn/ui component mapping brief:**
> "Payment form: use `Form` + `FormField` + `FormItem` + `FormLabel` + `FormControl` + `FormMessage` (shadcn form pattern). Card number field: `Input` with `type='text'` and `inputmode='numeric'`. Error state: `FormMessage` renders inline error below field. Destructive alert on server error: `Alert variant='destructive'`."

**Bad — Custom component duplicating shadcn pattern:**
> "Designer proposes a custom 'FormGroup' component with its own label and error rendering. Project already uses shadcn's `FormField` pattern. Custom component fragments the codebase with no added value." (New component without checking existing — contributes to design system fragmentation.)

**Good — Dark mode token pair with contrast check:**
> "Light: `--primary` = 221.2 83.2% 53.3% (blue), `--primary-foreground` = 210 40% 98% (near-white). Contrast: 4.8:1 — AA passed. Dark: `--primary` = 217.2 91.2% 59.8%, `--primary-foreground` = same near-white. Contrast: 4.6:1 — AA passed."

**Bad — Dark mode as an afterthought:**
> "'Dark mode: just invert the colors.' Light theme button is dark blue with white text. Inverted dark mode: white background with dark blue text — contrast fails at 2.9:1. Dark mode is not a visual filter, it is a token system decision."

**Good — Contribution request instead of silent custom component:**
> "Product needs a multi-value tag input not available in shadcn. Contribution request to Design System Lead: proposed behavior, 4 states (default, focused, value-added, error), token usage, shadcn primitives it builds on (Command + Badge). Frontend estimated effort: 2 days. Awaiting approval."

**Bad — Silent one-off custom component:**
> "Designer creates a 'TagInput' component in the Figma file with custom colors and sizes. Developer implements it without checking the design system. 6 months later, 4 variants of tag inputs exist across the product with inconsistent behavior." (No contribution process — design system fragment accumulates debt.)

## Boundaries

- Does not own design-system roadmap, governance, versioning, or adoption metrics → Design System Lead.
- Does not run shadcn CLI commands, install registry items, edit `components.json`, or write CSS variable files in code → `frontend-developer`.
- Does not own Tailwind configuration, build pipeline, or runtime theme switching logic → `frontend-developer`.
- Does not own brand identity or visual language rules → Brand / Communication Design.
- Does not rename production tokens or change CSS variables without Design System Lead / Frontend ownership.

## Sources

**Priority 1:**
- W3C Design Tokens Community Group specification: https://www.w3.org/community/design-tokens/
- shadcn/ui Theming: https://ui.shadcn.com/docs/theming
- shadcn/ui Components: https://ui.shadcn.com/docs/components
- shadcn/ui Blocks: https://ui.shadcn.com/blocks
- shadcn/ui Dark Mode: https://ui.shadcn.com/docs/dark-mode
- W3C WCAG 2.2: https://www.w3.org/TR/WCAG22/

**Priority 2:**
- Brad Frost, Atomic Design: https://atomicdesign.bradfrost.com/
- Figma Help, Variables (design tokens): https://help.figma.com/hc/en-us/articles/15339657135383-Guide-to-variables-in-Figma
- Figma Help, Variants: https://help.figma.com/hc/en-us/articles/360056440594
- Storybook Docs: https://storybook.js.org/docs
- shadcn/ui Theme Generator (Tweakcn): https://tweakcn.com

**Priority 3:**
- Smashing Magazine, Design Tokens: https://www.smashingmagazine.com/2019/11/smashing-podcast-episode-3/
- Inside Design InVision, Building a Design System: https://www.invisionapp.com/inside-design/guide-to-design-systems/

## Handoff

```
To: frontend-developer
Task: Implement semantic token set and component mapping from design brief
Context: Token table and component mapping brief are ready; CSS variable implementation and shadcn integration required
Inputs: Token table (light + dark), component mapping, contribution requests, contrast ratios
Expected artifact: Implemented CSS variable file, component usage confirmed, any deviations flagged
Acceptance criteria: All tokens named by purpose; WCAG AA contrast confirmed in both modes; shadcn components used per mapping
```

```
To: Design System Lead
Task: Review component gap and contribution request
Context: Product needs a component not covered by current design system
Inputs: Contribution brief (problem, behavior, states, token usage, primitives, effort estimate)
Expected artifact: Approved / rejected / deferred with rationale; alternative if rejected
Acceptance criteria: Decision made within sprint; if deferred, temporary workaround agreed
```
