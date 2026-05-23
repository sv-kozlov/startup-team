---
name: design-discovery-and-research
description: Use when product goals, research findings, analytics signals, stakeholder inputs, or user feedback need to be synthesized into a design problem statement, UX hypotheses, and solution directions before ideation or prototyping begins.
family: method
profile_level: Senior+
---

# Design Discovery and Research

## Purpose

Frame the design problem with precision and translate mixed evidence — product goals, analytics, research insights, support feedback, and constraints — into UX hypotheses and design principles so the team can move from "we have a problem" to "here is the framing that will guide solutions." This skill prevents the team from jumping to screens before the problem is understood.

## Use When

- A team is ready to prototype or wireframe but has not aligned on the design problem.
- Multiple sources of evidence (analytics, research, product strategy, support) need to be reconciled into a shared design direction.
- A product area needs UX hypotheses and design principles before ideation starts.
- Analytics or usability findings have revealed user friction and the design team must translate them into hypotheses and iteration targets.
- A discovery sprint, kick-off, or design brief is needed before a feature cycle begins.

## Do Not Use When

- The design problem is already framed and the team needs wireframes or prototypes — use `wireframing-and-prototyping`.
- The goal is to define product metrics, run A/B tests, or interpret statistical results — hand off to `product-analyst`.
- The task is to run formal user research (recruiting, moderated sessions, synthesis at scale) — hand off to `ux-researcher`.
- The task is purely about information architecture or navigation structure — use `information-architecture-and-user-flows`.

## Inputs

- Product goal, user problem statement, user segment, or job-to-be-done framing.
- Research findings: interview notes, usability test results, survey results, field observations.
- Analytics signals: funnel data, drop-off points, session recordings, search logs.
- Support feedback, complaint clusters, or NPS verbatims.
- Business constraints, technical constraints, time constraints, accessibility requirements.
- Existing solutions and known assumptions.

## Workflow

1. **Collect and separate evidence types.** Sort inputs into: confirmed facts, observations, assumptions, hypotheses, constraints, and open decisions. Label each clearly; do not treat assumptions as facts.

2. **Identify the user problem and product goal gap.** State what users are trying to do, where they fail or struggle, and what the product goal requires them to achieve. Map the gap explicitly.

3. **Apply a framing method.** Use Double Diamond problem framing (diverge on "what is the real problem?" before converging on "what should we design?"). For jobs-to-be-done contexts, define the functional, emotional, and social job dimensions. For analytics-driven iteration, apply HEART framework to identify which goal dimension is affected (Happiness, Engagement, Adoption, Retention, Task Success).

4. **Generate UX hypotheses.** Each hypothesis follows the pattern: "We believe that [design change] will result in [user behavior change] because [evidence or rationale]. We will know we were right when [measurable signal]."

5. **Define design principles for this context.** Principles are decision rules that help the team choose between design options. They are specific to the problem, not generic UX platitudes. Example: "Confirm before deleting, not before viewing" rather than "Be clear."

6. **Map evidence gaps to owning roles.** If product strategy is unclear — hand off to `product-manager`. If user research is insufficient — hand off to `ux-researcher`. If metric definition is missing — hand off to `product-analyst`. If business rules are ambiguous — hand off to `business-analyst`.

7. **Produce a design brief.** Summarize: problem statement, user segment, hypotheses, design principles, known constraints, evidence gaps, and handoff tasks. This brief is the input for `information-architecture-and-user-flows` and `wireframing-and-prototyping`.

## Outputs

- Design problem statement (1–3 sentences, user-centered, not solution-framed).
- UX hypotheses (structured: change → expected behavior → signal).
- Design principles for this product area or feature (3–7 decision rules).
- Evidence map: what is known, what is assumed, what is missing, and who owns each gap.
- Evidence gaps and handoff tasks for adjacent roles.
- Design brief as a single reference for the ideation phase.

## Named Patterns

**Good — Double Diamond problem framing before screens:**
> "Users drop off at step 3 of onboarding (analytics). Interviews reveal they don't understand why we need their phone number at this point (research). Design problem: reduce perceived risk at the personal data collection step. Hypothesis: showing 'why we need this' inline will reduce drop-off by building trust before asking."

**Bad — Jumping to screens without problem framing:**
> "Analytics show 40% drop-off. Let's redesign the onboarding flow." (No problem statement, no hypothesis, no framing — the team will iterate on layouts instead of solving the real problem.)

**Good — HEART framework applied to evidence:**
> "Task Success metric for search is 34%. Session recordings show users scan results, don't find what they need, and abandon. Hypothesis: improving result relevance labels (showing match reason) will increase Task Success by reducing misclick rate."

**Bad — Treating analytics as requirements:**
> "Bounce rate is high on the dashboard page. We need to add more content to keep users engaged." (Analytics signal is misread as a solution instruction; no framing of why users leave.)

**Good — Structured UX hypothesis:**
> "We believe that moving the primary CTA above the fold on mobile will increase conversion because scroll depth analysis shows 68% of mobile users never reach the current CTA position. We will know we succeeded when mobile conversion rate improves by ≥10% in a 2-week A/B test."

**Bad — Unstructured opinion dressed as hypothesis:**
> "The button should be more prominent. Users probably don't see it." (No evidence linkage, no success signal, not testable.)

**Good — Evidence gap routed to owner:**
> "We don't have user research on why enterprise admins abandon the settings flow. Hypothesis is based on support tickets only. Routing to UX Researcher: plan 3–5 user interviews with admin segment to validate the friction assumption before committing to a redesign."

**Bad — Absorbing research ownership:**
> "I'll just assume the issue is confusing labels based on what I've seen in support." (Designer absorbs research ownership, builds on unvalidated assumption, skips handoff.)

## Boundaries

- Does not own product strategy, roadmap, or product prioritization → `product-manager`.
- Does not own metric definitions, A/B methodology, or statistical interpretation → `product-analyst`.
- Does not own formal research design, recruitment, or synthesis → `ux-researcher`.
- Does not own business rules or process mapping → `business-analyst`.
- Does not turn unvalidated assumptions into confirmed facts; marks assumptions explicitly.
- Does not produce wireframes or layout decisions — this skill ends at the design brief.

## Sources

**Priority 1:**
- Design Council, Double Diamond: https://www.designcouncil.org.uk/our-resources/the-double-diamond/
- Google HEART Framework (Rodden et al.): https://research.google.com/pubs/pub36299.html
- Lean UX Canvas by Jeff Gothelf: https://jeffgothelf.com/blog/leanuxcanvas-v2/
- IDEO Design Thinking: https://designthinking.ideo.com/

**Priority 2:**
- Nielsen Norman Group, UX Research Cheat Sheet: https://www.nngroup.com/articles/ux-research-cheat-sheet/
- Nielsen Norman Group, Analytics and UX: https://www.nngroup.com/articles/analytics-user-experience/
- Smashing Magazine, Design Hypothesis: https://www.smashingmagazine.com/2023/01/creating-testable-ux-hypotheses/

**Priority 3:**
- GOV.UK Service Manual, User research: https://www.gov.uk/service-manual/user-research
- A List Apart, Framing Design Decisions: https://alistapart.com/article/framingdesign/

## Handoff

```
To: product-analyst
Task: Define metrics and success signals for UX hypothesis validation
Context: UX hypotheses produced; need metric ownership and A/B setup
Inputs: UX hypotheses with proposed behavioral signals
Expected artifact: Metric definition, tracking plan, A/B readiness assessment
Acceptance criteria: Each hypothesis has a named metric, baseline value, and detection threshold
```

```
To: ux-researcher
Task: Validate design problem framing with user interviews
Context: Evidence gap identified — assumption-based problem framing needs user confirmation
Inputs: Design problem statement, evidence map, assumed friction points
Expected artifact: Interview notes or synthesis with confirmed/rejected assumptions
Acceptance criteria: At least 3 user sessions; findings address the specific evidence gap
```
