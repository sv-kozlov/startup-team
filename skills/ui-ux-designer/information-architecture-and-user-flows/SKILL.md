---
name: information-architecture-and-user-flows
description: Use when a product area needs structural design before screen layout — content grouping, navigation models, labeling, page hierarchy, sitemap, user journeys, task sequences, decision points, error paths, and flow variants — to give wireframing a validated structural foundation.
family: method
profile_level: Senior+
---

# Information Architecture and User Flows

## Purpose

Define how information is organized and how users move through it. Information architecture answers "what exists and where?" — structure, navigation, labels, and hierarchy. User flows answer "how do users get from intent to outcome?" — task sequences, decisions, variants, and exception paths. Both are produced before detailed UI design to prevent layout decisions from driving structure.

## Use When

- A product area, new feature, or redesign needs structure before wireframes.
- Navigation, grouping, labeling, or page hierarchy is unclear or contested.
- A feature requires a user flow, journey map, or scenario path before screen design.
- A current flow is fragmented, confusing, or missing edge cases.
- Business process, system behavior, and user interaction views need to be separated.
- Users must compare options, filter content, find items, or complete multi-step tasks.

## Do Not Use When

- The design problem is not yet framed — use `design-discovery-and-research` first.
- A detailed screen layout is needed — use `wireframing-and-prototyping`.
- A business process or BPMN model is the goal — hand off to `business-analyst`.
- A system state diagram, API flow, or data model is required — hand off to `system-analyst`.
- SEO content strategy, editorial policy, or marketing taxonomy is in scope — hand off to the content owner.

## Inputs

**For IA:**
- User goals, content inventory, product entities, terminology, and categories.
- Business rules, system objects, analytics search logs, or research findings.
- Existing navigation, menu, taxonomy, or sitemap (if any).

**For user flows:**
- User goal, segment, scenario, entry point, and desired outcome.
- Product goal, business rules, system constraints, known metrics, or research.
- Existing screens, process notes, requirements, or support feedback.

## Workflow

1. **Define primary user intents.** Before grouping content or drawing flows, list the 3–7 most common user goals in this area. Each goal becomes an anchor for structure and flow design.

2. **Inventory content, actions, entities, and states.** For IA: list everything the user can encounter or act on. For flows: list all steps, decision points, data inputs, permissions, and system responses.

3. **Group by user mental model, not internal org structure.** Use card sorting logic (open or closed) to validate groupings against user expectations. Flag groupings that reflect internal department logic rather than user behavior patterns.

4. **Define navigation, hierarchy, progressive disclosure, and labeling.** For IA: create sitemap, navigation model, and label recommendations. Labels must use user-facing terminology, not system or admin terms. For flows: map the happy path first, then variants (user role, permission level, data state), decision points, and failure paths.

5. **Separate concerns.** Mark what is user interaction (UX owns), what is business rule (Business Analyst owns), what is system/API behavior (System Analyst owns). Never embed system logic as UI logic in a flow.

6. **Check findability, flow completeness, and ambiguity.** IA check: can users find their primary goal in ≤3 navigation steps? Flow check: are all terminal states (success, error, cancel, timeout) covered? Are all decision points labeled with the decision, not just the outcome?

7. **Produce deliverables and identify open questions.** Mark assumptions, unresolved labels, and ownership gaps. Route them to the right role before proceeding to wireframing.

## Outputs

- IA model: sitemap, navigation brief, or content grouping diagram.
- Labeling recommendations with rationale (user terms vs. system terms).
- User flow or journey brief (happy path + variants + failure paths).
- Scenario variants and edge-case list.
- Open questions and handoff tasks for BA, SA, Product, or content owner.
- Flow readiness checklist for wireframing.

## Named Patterns

**Good — IA grouped by user mental model (card sort evidence):**
> "Users sorted 'account settings,' 'billing,' and 'notifications' together in card sort sessions. Navigation groups these under 'My account' rather than the internal org split of 'Finance > Billing' and 'Profile > Settings.'"

**Bad — IA mirroring internal org chart:**
> "'Finance & Payments' is a top-level navigation item because the Finance department manages it. Users in card sorting never created this grouping — they searched under 'account' and 'subscription.'"

**Good — User flow with all decision points labeled:**
> "Step 4: 'User selects payment method.' Decision: credit card → go to card form; saved card → go to confirmation; Apple Pay → go to native sheet. Each branch has an error path (card declined, Apple Pay unavailable) with a labeled recovery action."

**Bad — Happy-path-only flow:**
> "User fills the form → submits → sees success screen." (No decision points, no error states, no permission variants — QA will invent behavior and developers will guess edge cases.)

**Good — Terminology using user-facing labels:**
> "Navigation label: 'My orders' (user terminology, confirmed by search log analysis showing 'orders' is the most queried term). Not 'Transaction history' (finance terminology) or 'Purchase archive' (system terminology)."

**Bad — Terminology inherited from data model:**
> "Page labeled 'Entities' because that is the database table name. Users in usability tests called it 'companies' or 'clients' — 'Entities' caused 6 out of 8 users to hesitate."

**Good — Separation of user interaction from system behavior:**
> "Flow step: 'System validates card in real time (Stripe API).' Noted as system behavior, not a user step. UI shows loading state + error message if validation fails. SA owns the error taxonomy; designer owns the error message copy and state design."

**Bad — System logic embedded as user flow step:**
> "User waits for fraud check → if passed, goes to confirmation." (System behavior modeled as user decision — the user cannot choose to 'pass' fraud check; this is a system event. Flow is misleading for both developer and QA.)

## Boundaries

- Does not own domain glossary or terminology validation → `business-analyst`.
- Does not own data model, API object structure, or system state diagrams → `system-analyst`.
- Does not own SEO, marketing content strategy, or editorial policy.
- Does not own product priority or roadmap decisions embedded in navigation choices → `product-manager`.
- Does not produce wireframes or screen layouts — this skill ends at the flow/IA artifact.

## Sources

**Priority 1:**
- Rosenfeld, Morville, Arango, "Information Architecture for the Web and Beyond" (4th ed.): https://www.oreilly.com/library/view/information-architecture-4th/9781491913529/
- Nielsen Norman Group, IA Basics: https://www.nngroup.com/articles/ia-basics/
- Nielsen Norman Group, Journey Mapping 101: https://www.nngroup.com/articles/journey-mapping-101/
- GOV.UK Service Manual, User journeys: https://www.gov.uk/service-manual/design/user-journeys

**Priority 2:**
- Nielsen Norman Group, Card Sorting: https://www.nngroup.com/articles/card-sorting-definition/
- Apple Human Interface Guidelines, Navigation and search: https://developer.apple.com/design/human-interface-guidelines/navigation-and-search
- GOV.UK Service Manual, Naming your service: https://www.gov.uk/service-manual/design/naming-your-service

**Priority 3:**
- Smashing Magazine, Complete Beginner's Guide to Information Architecture: https://www.smashingmagazine.com/2022/11/complete-beginners-guide-information-architecture/
- A List Apart, The Discipline of Content Strategy: https://alistapart.com/article/thedisciplineofcontentstrategy/

## Handoff

```
To: business-analyst
Task: Validate terminology and business rule assumptions embedded in the IA
Context: Navigation labels and flow decision rules rely on business terminology
Inputs: IA draft with labeled groupings and flow decision points
Expected artifact: Confirmed terminology, corrected business rule boundaries, flagged exceptions
Acceptance criteria: All labels reviewed against business glossary; rule ambiguities resolved
```

```
To: system-analyst
Task: Specify API/data states for each flow decision point and error path
Context: User flow includes system behavior steps that need technical specification
Inputs: User flow with marked system events, error states, and data requirements
Expected artifact: System state specification, error taxonomy, API behavior for each flow branch
Acceptance criteria: Every system event in the flow has a documented behavior and error response
```
