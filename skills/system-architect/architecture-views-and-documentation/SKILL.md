---
name: architecture-views-and-documentation
description: Use when communicating system architecture through stakeholder-mapped views — choosing between C4, UML sequence/component/deployment, ArchiMate, or 4+1; creating the minimal effective notation set for a given audience; and maintaining traceable, current architecture documentation. Not for creating product, requirements, UX, test, or operational documentation.
family: method
profile_level: Senior+
---

# Architecture Views and Documentation

## Purpose

Communicate the architecture through views fit for each stakeholder concern, using consistent notations and minimal redundancy. Produce a minimal viable documentation set that enables implementation, review, onboarding, and evolution — without over-documenting or creating stale diagrams that nobody trusts.

## Use When

- Stakeholders need a shared picture of system structure, behavior, or deployment and current diagrams do not exist or are outdated.
- Multiple views — logical, process, deployment, scenarios — must be aligned after architectural decisions.
- A notation must be chosen and consistently applied for a team, domain, or architecture review.
- Architecture documentation must be updated after significant decisions (ADRs) or structural changes.
- An onboarding package must allow a new team member or reviewer to navigate the architecture without a guide.
- A governance or review body requires a structured architecture package.

## Do Not Use When

- The task is authoring product or requirements documentation → handoff to `system-analyst` / `product-manager`.
- The task is UX flows, wireframes, or interface documentation → handoff to UX/UI designer.
- The task is operational runbooks, deployment playbooks, or SRE documentation → handoff to `devops-sre`.
- The task is making an architectural decision (the decision goes into an ADR, not a view) → `architecture-decision-records`.
- The task is setting up a documentation platform or publishing pipeline → handoff to the owning team.

## Inputs

- Architecture decisions, ADRs, NFR catalog, and integration map.
- Identified stakeholders and their concerns: executives (context), engineers (component/sequence), operations (deployment), security (trust boundaries).
- Existing diagrams, glossaries, and documentation conventions.
- Agreed notation preferences (if any) for the team or organization.

## Workflow

1. **Identify stakeholders and their architectural concerns.** Map each stakeholder group to their primary question: "What does the system do and what does it connect to?" (C4 Context), "How is it deployed?" (C4 Deployment), "How does this flow work?" (UML Sequence), "What components exist and how are they structured?" (C4 Component / UML Component).
2. **Choose the minimal notation set.** Start with C4: Context → Container → Component. Add UML Sequence for behavior-critical flows (auth, checkout, data sync). Add C4 Deployment or UML Deployment when the topology is non-obvious. Add ArchiMate or 4+1 only if the organization requires it for governance or enterprise alignment.
3. **Draft views at the right abstraction level.** C4 Context: one diagram, system + external actors. C4 Container: one diagram per system, containers with tech labels. C4 Component: one diagram per container, only when needed for engineering onboarding. UML Sequence: one diagram per critical flow.
4. **Cross-link views with ADRs, NFRs, and component ownership.** Every diagram element (container, component, integration line) that is covered by an ADR must reference it. Every component with an SLO target must note the NFR ID.
5. **Define maintenance rules.** Specify which views are "always current" (C4 Context, Container), which are "updated on significant change" (Component, Sequence), and which are "point-in-time reference" (approved at review, not live). Assign ownership.
6. **Hand off non-architecture documentation.** API details, data models, scenario descriptions, acceptance criteria → `system-analyst`. User flows, error states → UX/UI. Deployment runbooks → `devops-sre`.

## Outputs

- C4 Context diagram (always).
- C4 Container diagram per system boundary (always for multi-component systems).
- C4 Component diagrams for containers requiring engineering onboarding (selected).
- C4 Deployment or UML Deployment for non-trivial deployment topology (selected).
- UML Sequence diagrams for critical or complex flows (selected).
- ArchiMate or 4+1 views if enterprise or governance requirement applies (conditional).
- View-to-stakeholder mapping table.
- Maintenance rules note (which views are live, point-in-time, or deprecated).

## Named Patterns

### Good — C4 with different depth for different audiences
Executive gets C4 Context (one page, system boundary + external integrations). Engineering team gets C4 Container + Component for their service. Operations gets C4 Deployment overlaid with reliability annotations. Each audience sees what they need; no one gets a 40-element mega-diagram.

### Bad — One "architecture diagram" for all audiences
A single 40-element Visio file with BPMN lanes, deployment nodes, entity boxes, and sequence arrows is used for every discussion. Executives cannot read it. Engineers cannot find their component. Operations cannot see topology. The diagram is never updated because nobody owns it.

### Good — Diagram as code with version control
```
// Structurizr DSL snippet
workspace {
  model {
    user = person "Customer"
    softwareSystem "Order Platform" {
      webApp = container "Web App" "React SPA" "TypeScript"
      api = container "Order API" "REST/gRPC" "Go"
      db = container "Order DB" "PostgreSQL"
    }
    user -> webApp "Places orders"
    webApp -> api "HTTPS"
    api -> db "SQL"
  }
}
```
Version-controlled, reviewable, and auto-rendered. Diff-able in pull requests.

### Bad — Screenshot-only diagrams
Architecture exists only in PowerPoint screenshots. No source. No version history. Updating requires redrawing by hand. After three sprints the diagram diverges from reality and is effectively abandoned.

### Good — ADR-linked view element
C4 Container diagram: the "Event Bus (Kafka)" container has a note linking to ADR-008 "Async integration via Kafka" and ADR-015 "Schema registry adoption." Engineers reviewing the diagram can read the rationale without asking the architect.

### Bad — Orphaned diagram element
A container labeled "Legacy ESB" appears in the diagram with no owner, no ADR, and no indication of whether it is a target-state component or a deprecated dependency. Every meeting begins with clarifying questions.

## Boundaries

- Does not replace product, requirements, UX, test, or operational documentation.
- Does not own the documentation platform or publishing workflow.
- Does not create a notation per request — chooses the minimal viable set for the audience.
- Does not make architectural decisions (decisions go into ADRs) — views communicate already-made decisions.

## Sources

### Priority 1 — Canonical References
- Simon Brown — C4 model for visualising software architecture: https://c4model.com/
- Structurizr DSL documentation: https://docs.structurizr.com/dsl
- ISO/IEC/IEEE 42010 — Architecture Description Standard: https://www.iso.org/standard/74393.html
- Philippe Kruchten — 4+1 View Model of Software Architecture: https://www.cs.ubc.ca/~gregor/teaching/papers/4+1view-architecture.pdf

### Priority 2 — Practitioner Guidance
- The Open Group — ArchiMate 3 Specification: https://pubs.opengroup.org/architecture/archimate3-doc/
- Microsoft Architecture Center — documentation guidance: https://learn.microsoft.com/azure/architecture/
- ThoughtWorks Tech Radar — diagrams as code: https://www.thoughtworks.com/radar/techniques/diagrams-as-code

### Priority 3 — Supplementary
- arc42 architecture documentation template: https://arc42.org/
- InfoQ — architecture documentation articles: https://www.infoq.com/architecture-design/

## Handoff

- Detailed API contracts, data model documentation, scenario documentation → `system-analyst`.
- User flows, interaction states, wireframes → UX/UI designer.
- Operational runbooks, deployment documentation → `devops-sre`.
- Architectural decisions that views communicate → `architecture-decision-records`.
- Architecture review requiring documentation package → `architecture-review-and-governance`.
