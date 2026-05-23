---
name: engineering-quality-and-standards
description: Use when establishing, updating, or enforcing team engineering standards — Definition of Done, test pyramid targets, observability requirements, CI green-light rules, feature flag discipline, and coding conventions. Covers both writing the standards and maintaining the feedback loop that keeps them alive.
family: method
profile_level: Senior+
---

# Engineering Quality and Standards

## Purpose

Give the team an explicit, written set of quality requirements so that "done" means the same thing to every engineer, every sprint, and every reviewer. Replace implicit expectations with documented standards that can be checked in CI and discussed in review without personal judgment.

## Use When

- The team's Definition of Done is verbal or inconsistent between sprints.
- Test coverage targets do not exist or are not enforced.
- Observability requirements (logging, metrics, traces) are applied inconsistently across services.
- CI passes green but production reliability is declining — standards are inadequate, not just untested.
- A new capability, framework, or service type is introduced and no standards exist for it.
- After a major incident that reveals a gap in engineering standards.

## Do Not Use When

- The request is about a specific PR's review quality → `code-review-leadership`.
- The request is about classifying and scheduling debt → `tech-debt-management`.
- The request is about platform-level quality gates (org-wide SLOs, platform NFR) → `system-architect` or `devops-sre`.
- The request is about QA strategy, test plan, or release-level regression → `qa-engineer`.

## Inputs

- Current DoD if it exists: what "done" means today.
- Test coverage metrics across services.
- CI pipeline configuration: what gates exist, what is advisory.
- Incident and defect data: categories, root causes, frequency.
- Observability gaps: signals that were missing during recent incidents.
- Input from qa-engineer on testability gaps; from devops-sre on production-readiness gaps.

## Workflow

1. Audit the current state. Collect: test coverage P50 across services, CI pass rate, defect escape rate by category (unit catchable, integration catchable, manual-only), observability gaps from last three incidents. Use data to identify which standards are missing or unenforced.
2. Define or update the Definition of Done. DoD should specify: tests written (unit, integration, E2E as applicable), CI passes with all gates green, observability added (log events, metrics, traces as applicable), documentation updated (API spec, runbook entry if on-call-relevant), feature flag added for risky changes, security review completed if the change touches auth, payment, or user data.
3. Set test pyramid targets for the team context. Example: unit tests cover all business logic branches; integration tests cover external service calls and database interactions; E2E tests cover the critical user-facing flows only. Write numerical targets (e.g., unit coverage ≥ 80% on new code) only if the team will measure them in CI. Unmeasured targets become aspirations.
4. Define observability requirements per change type. New endpoint → metric (RED: rate, errors, duration), trace span on the critical path, structured log event at state transitions. Changed external integration → trace on outbound call, error log on non-retriable failure. New batch job → job start/end log event, metric on processed and failed records.
5. Write CI gate requirements. Separate mandatory gates (failing these blocks merge: unit tests, linter, security scan baseline) from advisory gates (passing these is encouraged but does not block: integration tests, coverage threshold). Make the distinction explicit and documented. Advisory gates that block delivery erode trust in the gate system.
6. Define feature flag discipline. When is a flag required? (Risky changes, A/B experiments, rollout control.) Who creates the flag? Who owns cleanup? Stale flags are technical debt; set a maximum TTL per category.
7. Publish standards in the team handbook with a version date. Standards not published are not standards.
8. Run a quarterly standards review. What escaped production that the standards should have caught? What gates are consistently bypassed with override reasons? Adjust the standards based on evidence. Standards that never change are either perfect or ignored.

## Outputs

- Definition of Done document (versioned, dated).
- Test pyramid targets per service type.
- Observability checklist per change category.
- CI gate policy: mandatory vs. advisory, with rationale.
- Feature flag discipline policy: when required, TTL, cleanup owner.
- Quarterly standards review notes.

## Named Patterns

### Good — DoD with observable criteria
```
Definition of Done — Team Checkout (v2.1, 2026-01-10):
[ ] Unit tests: all new branches covered, CI gate green.
[ ] Integration tests: new external calls have a contract test.
[ ] Metrics: new endpoint has rate, error, and duration metrics in Prometheus.
[ ] Trace: new endpoint has an OTel span on the critical path.
[ ] Runbook: if the change adds on-call-relevant behaviour, runbook is updated.
[ ] Feature flag: changes affecting >5% of traffic are behind a flag with a cleanup issue filed.
```
Every engineer reads the same list. "Done" is checkable.

### Bad — "It works on my machine"
DoD is verbal: "make sure it's tested and reviewed." Different engineers interpret this differently. Production incidents reveal the gaps.

### Good — CI gate taxonomy
```
Mandatory (blocks merge):
  - unit-test: all tests pass
  - lint: zero errors on configured rules
  - security-scan: no NEW critical/high findings (existing backlog tracked separately)

Advisory (reported, not blocking):
  - integration-test: failures go to #test-failures channel for investigation
  - coverage: drops below 75% trigger a comment on PR, not a block
```
Engineers know what to fix before merging and what to flag for follow-up.

### Bad — Every gate blocks
Integration tests are flaky. They block every PR 20% of the time. Engineers click "override" reflexively. The gate is theatrical.

### Good — Observability standard per change type
"New REST endpoint: add histogram for request_duration_seconds with labels {method, route, status_class}. Add OTel span named 'ServiceName.MethodName'. Log one INFO event at entry with request_id and user_id."
The next engineer adding an endpoint knows exactly what to add without asking.

### Bad — Observability by heroism
"The senior adds proper metrics; juniors add none; tech lead catches it in review." Incidents reveal observability gaps. Standards are the retrospective solution, not the prevention.

### Good — Feature flag TTL policy
"Feature flags of type rollout: TTL 4 weeks from full rollout date. Experiment flags: TTL 2 weeks from decision date. Owner files a cleanup issue at flag creation. Stale flags reported weekly in #tech-debt channel."
Flags don't accumulate. The team knows when to clean up.

### Bad — Flags that live forever
Fourteen flags in production, seven of which are always-on. Code has conditional paths that will never be false. No one knows which flags are safe to remove.

## Boundaries

- Owns team-level engineering standards, DoD, and CI gate policy.
- Does not own org-wide quality standards or platform NFR → `system-architect`.
- Does not own QA strategy, test plan, or release-level regression testing → `qa-engineer`.
- Does not own infrastructure or CI platform configuration → `devops-sre`.
- Does not own review conventions and PR culture → `code-review-leadership`.

## Sources

### Priority 1 — Engineering quality canon
- Google Engineering Practices — https://google.github.io/eng-practices/
- DORA State of DevOps Reports — https://dora.dev/research/ (deployment frequency, lead time, change failure rate, MTTR).
- The Twelve-Factor App — https://12factor.net/

### Priority 2 — Reliability and quality practice
- Google SRE Book — https://sre.google/sre-book/table-of-contents/
- Martin Fowler: Testing Strategies in a Microservice Architecture — https://martinfowler.com/articles/microservice-testing/
- Camille Fournier: The Manager's Path — O'Reilly, 2017.

### Priority 3 — Background
- ThoughtWorks Technology Radar — https://www.thoughtworks.com/radar
- LeadDev: Engineering standards articles — https://leaddev.com/

## Handoff

- Test plan and QA strategy → `qa-engineer`.
- Platform-level NFR and org-wide quality gates → `system-architect`.
- Infrastructure and CI platform → `devops-sre`.
- Review conventions and PR feedback norms → `code-review-leadership`.
- Specific technical debt items from standards gaps → `tech-debt-management`.
