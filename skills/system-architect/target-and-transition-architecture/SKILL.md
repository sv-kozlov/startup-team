---
name: target-and-transition-architecture
description: Use when defining where a system or domain architecture must go (target state), where it stands today (baseline), and the safe intermediate states that connect them (transition states with exit criteria and migration roadmap). Not for enterprise portfolio architecture or delivery planning.
family: method
profile_level: Senior+
---

# Target and Transition Architecture

## Purpose

Describe where the system architecture must go (target), where it is today (baseline), and the intermediate transition states that get it there safely, with explicit exit criteria, rollback options, and migration sequencing. Produce a plan that is realizable in delivery, inspectable at checkpoints, and does not require a big-bang switch.

## Use When

- A system, domain, or product must move from a current architecture to a target architecture.
- Migration must be staged into transition states with measurable exit criteria.
- Architectural change must be sequenced against delivery capacity, risk, and cross-team dependencies.
- Trade-offs between target-state purity and stepwise delivery feasibility must be made explicit.
- A strangler-fig migration, domain extraction, or platform modernization needs an architectural frame.
- A significant legacy evolution requires a documented baseline before design work begins.

## Do Not Use When

- The task is enterprise portfolio planning or capability-level roadmap → handoff to enterprise-architect.
- The task is delivery planning, resource allocation, dates, or budget → handoff to `project-manager`.
- The task is internal component decomposition without a transition plan → `component-and-service-decomposition`.
- The task is setting NFR targets for the target state → `non-functional-architecture`.
- The task is recording a specific decision made during transition planning → `architecture-decision-records`.

## Inputs

- Product or domain goal and time horizon for the architectural change.
- Baseline architecture: current components, integrations, data flows, known debt, and operational constraints.
- NFR targets for the target state.
- Constraints: regulatory, organizational, enterprise standards, vendor lock-in, capacity, team skills.
- Dependencies on adjacent systems, teams, and vendors.
- Risk appetite and rollback requirements.

## Workflow

1. **Baseline the current architecture.** Document the current state at the container/component level: what exists, what is working, what is painful, what is blocking growth. Identify the gap between current state and the goal.
2. **Define the target architecture.** Specify target-state principles, component boundaries, integration patterns, NFRs, and ownership. Use the outputs of `component-and-service-decomposition`, `integration-architecture`, and `non-functional-architecture` as inputs. Apply evolutionary architecture thinking: design for replaceability, not perfection.
3. **Identify transition states.** Between baseline and target, define intermediate architectures where the system is functional, deployable, and tested. Each transition state is a stable plateau — not a half-migrated mess.
4. **Define exit criteria per transition state.** What must be true for the system to move from one transition state to the next? Criteria must be measurable: tests passing, NFR verified, specific components migrated, traffic shifted, old component decommissioned.
5. **Design migration steps.** For each transition state: what changes, what stays, what runs in parallel (strangler-fig dual-run), how traffic is shifted (feature flags, proxy routing, read-write split). Prefer additive, non-breaking steps over destructive migrations.
6. **Assess risks per transition step.** Each step gets: rollback plan, risk level, dependency on other teams or systems, and data migration reversibility. Mark irreversible steps explicitly.
7. **Define the decommission path.** When does the old component or system go away? What are the triggers for decommission (traffic is zero, dependent systems migrated, data verified)?

## Outputs

- Target architecture brief (principles, components, integrations, NFR targets).
- Baseline architecture summary (current state, pain, gaps relevant to the goal).
- Transition state sequence with exit criteria per state.
- Migration roadmap: steps, parallelism strategy, rollback options, irreversibility markers.
- Decision log entries for major transition choices.
- Handoff items for `project-manager` (delivery sequencing), `tech-lead` (implementation feasibility), `architectural-risk-and-technical-debt` (risk per step).

## Named Patterns

### Good — Strangler-fig with measurable traffic shift
```
Transition T1: Proxy routes 5% of /orders traffic to new OrderService.
               Old monolith handles 95%.
               Exit criteria: p99 ≤ 200ms for new service, zero data inconsistency over 72h canary.
Transition T2: 50% traffic shift. Dual-write to old and new DB.
               Exit criteria: Load test at 1,000 RPS, read replica verified, data sync validated.
Transition T3: 100% traffic to new OrderService. Old /orders endpoint disabled.
               Exit criteria: Old monolith receives zero order traffic for 7 days. Decommission scheduled.
```

### Bad — Big-bang migration with go/no-go
```
Plan: Rewrite the entire order module by Q3. Go live with everything on day one.
Rollback: Not possible — DB schema changes are irreversible.
```
No transition states. No incremental validation. Any unforeseen issue requires full rollback or operating a broken system. Risk is undivided.

### Good — Additive non-breaking migration step
```
Step 1: Add new_column to orders table (nullable, no default).
Step 2: Deploy new code that writes to both old_column and new_column.
Step 3: Backfill new_column for existing rows.
Step 4: Deploy code that reads new_column.
Step 5: Drop old_column after all readers are migrated.
```
Each step is independently deployable and reversible until Step 5. Classic expand/migrate/contract.

### Bad — Breaking schema change in one step
```
ALTER TABLE orders RENAME COLUMN status TO order_status;
```
All deployed instances using status fail immediately. No transition state, no backward compatibility window.

### Good — Explicit fitness function for target state
```
Fitness function: No new service may share a database with another service.
Measurement: Automated check in CI — cross-schema foreign keys fail the build.
Current violation: LegacyReporting reads orders table. Tracked in ADR-021 exception.
Target: Exception closed by 2026-09-01.
```

### Bad — Target architecture as a destination with no measurement
```
Target: Microservices, event-driven, cloud-native.
```
No components named, no NFRs set, no current-to-target gap identified. Implementation teams have no concrete milestone to aim for.

## Boundaries

- Does not own enterprise portfolio, capability map, or corporate transformation roadmap → enterprise-architect.
- Does not own delivery dates, budget, resource allocation, or sprint planning → `project-manager`.
- Does not replace detailed requirements, API contracts, or code design → `system-analyst` / `tech-lead`.
- Does not own infrastructure migration, environment provisioning, or CI/CD changes → `devops-sre`.

## Sources

### Priority 1 — Canonical References
- Neal Ford, Rebecca Parsons, Patrick Kua — Building Evolutionary Architectures: https://evolutionaryarchitecture.com/
- TOGAF Standard — Architecture Development Method (ADM phases): https://pubs.opengroup.org/togaf-standard/adm/
- ISO/IEC/IEEE 42010 — Architecture Description: https://www.iso.org/standard/74393.html
- Martin Fowler — StranglerFigApplication: https://martinfowler.com/bliki/StranglerFigApplication.html

### Priority 2 — Practitioner Guidance
- Sam Newman — Monolith to Microservices (migration patterns): https://samnewman.io/books/monolith-to-microservices/
- Microsoft Architecture Center — migration patterns: https://learn.microsoft.com/azure/architecture/patterns/
- ThoughtWorks Tech Radar — fitness function–driven development: https://www.thoughtworks.com/radar/techniques/fitness-function-driven-development

### Priority 3 — Supplementary
- InfoQ — evolutionary architecture and modernization articles: https://www.infoq.com/evolutionary-architecture/
- Software Engineering Radio — legacy modernization episodes: https://www.se-radio.net/

## Handoff

- Delivery sequencing, dates, resource allocation → `project-manager`.
- Risk per transition step and debt registry → `architectural-risk-and-technical-debt`.
- Implementation feasibility and code design within each transition state → `tech-lead`.
- Infrastructure migration, environment provisioning → `devops-sre`.
- ADRs for major transition decisions → `architecture-decision-records`.
