---
name: qa-leadership-and-process
description: Use when improving QA process maturity, defining quality metrics, mentoring QA team members, driving shift-left practices, or establishing a quality culture in a product team. Lead-level scope: owns QA process and quality standards within a team or product domain.
family: lead
profile_level: Lead+
---

# QA Leadership and Process

## Purpose

Build a QA practice that the team trusts and that prevents defects earlier rather than catching them later.
Define quality metrics that drive decisions (not vanity numbers), mentor QA team members through structured
feedback, embed shift-left practices so quality is a design input rather than a release gate, and own the
QA process continuously without waiting for a crisis to improve it.

## Use When

- Establishing a QA process for a new team or product.
- A team's defect escape rate is high and the root cause is process-level, not test execution.
- QA team members need structured growth and feedback.
- Shift-left adoption is needed: requirements review, testability input, early risk flagging.
- Quality metrics are not defined or are not driving decisions.
- The team's Definition of Done is weak on quality conditions.
- Regression strategy is undefined, growing without governance, or consistently missing critical paths.

## Do Not Use When

- Writing specific test cases for a feature -> `test-design-and-coverage`.
- Managing developer performance or team delivery schedule -> manager / `project-manager`.
- Setting architecture-level engineering standards -> `tech-lead`.
- A single test strategy for a feature is needed -> `test-strategy-and-planning`.

## Inputs

- Current QA process description or gap analysis.
- Quality metrics: escaped defects, defect detection rate by phase, flakiness rate, MTTD, MTTR.
- Team composition: QA headcount, skill levels, automation maturity.
- Delivery process: Scrum, Kanban, or hybrid; sprint cadence; release frequency.
- Definition of Done: current version and its quality conditions.
- Recent incident or escaped defect post-mortems.

## Workflow

1. Audit the current QA process. For each phase (requirements, design, development, testing, release),
   answer: where are defects being found vs where should they be found? Calculate the phase containment
   effectiveness (PCE) for the last 3 sprints or releases.

2. Define quality metrics. Choose metrics that drive behavior, not metrics that report activity.
   Core metrics for a QA lead:
   - Escaped defects: defects found by users or in production that QA did not catch.
   - MTTD (Mean Time to Detect): time from defect introduction to defect discovery.
   - MTTR (Mean Time to Resolve): time from defect discovery to verified fix.
   - Defect detection phase: what % of defects are found in requirements review, unit testing,
     integration testing, QA testing, and production?
   - Flakiness rate: flaky test failures / total test runs over rolling 30 days.
   - Test coverage trend: is the coverage matrix growing, shrinking, or stable?

3. Drive shift-left adoption. Shift-left means finding defects earlier by involving QA in:
   - Requirements review: QA attends requirements refinement, raises testability questions,
     flags ambiguous or untestable criteria before development begins.
   - Design review: QA contributes testability requirements (feature flags, controlled state,
     observability hooks) to the design specification.
   - Definition of Done: QA authors or strengthens the quality conditions (AC verifiable,
     test cases written, regression updated, no critical open defects).
   - Code review participation (consultative): QA raises testability concerns in PR descriptions
     without owning the code review process (that belongs to `tech-lead` and developers).

4. Mentor QA team members. Structured mentoring, not general feedback:
   - Review test cases, bug reports, and session reports. Give feedback on specific artifacts,
     not general statements about quality.
   - Ask questions: "What technique did you use to design these cases?" "What layer is this
     defect in?" "What regression risk does this fix carry?"
   - Track growth: set a concrete skill gap to close each quarter and measure it.
   - Pair on complex sessions: walk through a SFDPOT session together; debrief immediately.

5. Manage the regression strategy. Own the regression set as a deliberate selection:
   - Classify existing regression tests by criticality and defect history.
   - Remove tests that have never caught a defect and cover low-risk paths.
   - Prioritize tests for components with the highest defect density.
   - Set a regression runtime budget per delivery stage (e.g., PR check < 10 min, nightly < 60 min).

6. Build a quality culture. Quality culture is not QA-owned; it is team-owned:
   - Make quality metrics visible at sprint reviews and retrospectives.
   - Present escaped defect analysis with root cause and recommended improvement.
   - Celebrate early defect finds (requirements review, dev testing) as much as QA finds.
   - Normalize "not enough information to test" as a valid sprint refinement outcome.

7. Report on QA process health. Produce a monthly or per-release QA health summary:
   - Escaped defects (count and root cause).
   - Defect detection phase distribution (shift over time).
   - Flakiness rate and trend.
   - Coverage additions and gaps.
   - Top 3 process improvements implemented or in progress.

8. Escalate process-blocking issues. If inadequate testability, missing environments, or blocked
   QA capacity is causing systemic quality risk, escalate to tech-lead and project-manager with
   specific evidence and a proposed resolution, not just a complaint.

## Outputs

- QA process audit findings with phase containment effectiveness data.
- Quality metrics dashboard or report (escaped defects, MTTD, MTTR, flakiness rate).
- Updated Definition of Done with quality conditions.
- Regression strategy document: classification, runtime budget, governance rules.
- Mentoring notes and growth plans for QA team members.
- Monthly QA health summary.
- Shift-left adoption plan with milestones.

## Named Patterns

### Good — Phase containment effectiveness analysis

```
Defects by detection phase (last 3 sprints):

Phase            | Defects found | % of total
Requirements     |     2         | 8%
Development      |     5         | 20%
QA testing       |    12         | 48%
UAT / staging    |     4         | 16%
Production       |     2         | 8%

Target state:
  Requirements:  15% (shift-left goal)
  Development:   35%
  QA testing:    40%
  UAT:           8%
  Production:    2%

Action: Requirements review process is missing QA participation. Proposed: QA joins 
refinement sessions; pilot in Sprint 24.
```

Data-driven improvement proposal. Not "we need to do better."

### Bad — Quality report as activity summary

"This sprint we ran 150 test cases and found 18 defects."
No phase data. No comparison to target. No action items. No trend.
The report exists but does not drive any decision.

### Good — Escaped defect analysis with root cause

```
Escaped defect post-mortem (production incident 2026-05-12):

Defect: Null pointer exception when user changes account type while an order is in-flight.
Phase missed: QA testing.

Root cause:
  1. Test design gap: state transition from account change during active order was not in scope.
  2. Requirements gap: the AC did not cover concurrent state changes; SA was not aware of the scenario.
  3. No race condition test in automation.

Actions:
  1. Add state transition matrix for account and order statuses to the test design template.
  2. SA to add concurrent state change handling to the specification pattern.
  3. QA to add race condition smoke test for order + account change paths.
```

Each escaped defect produces a concrete process improvement. Not just a count update.

### Bad — Escaped defect treated as isolated event

"We missed this one. It won't happen again." No root cause analysis. No process change.
The same class of defect escapes two sprints later.

### Good — Shift-left: QA in requirements refinement

```
QA input at Sprint 24 refinement:

Story: "As a user, I can apply a discount code during checkout."

QA questions raised:
  Q1: Can a code be applied after payment is initiated but before confirmation? [AC gap]
  Q2: What is the behavior if the code expires between "Apply" and "Confirm"? [AC gap]
  Q3: Are there constraints on code combinations (stacking)? [missing rule]
  
Outcome: SA updated the AC to cover all three scenarios before development started.
Time saved: ~2 defects not introduced into development.
```

### Bad — QA reviews requirements after the sprint starts

The developer implements the feature based on the original AC. QA finds gaps during testing.
The AC is updated but the code must be reworked. Two days of delay per sprint.

### Good — Quality metrics visible to the team

```
Sprint 24 Review — QA Health Slide:

Escaped defects: 0 (target: 0)   GREEN
MTTD: 1.8 days (target: <2 days) GREEN
MTTR: 3.2 days (target: <4 days) GREEN
Flakiness rate: 0.8% (budget: <1%) GREEN
Regression runtime: 8 min (budget: <10 min) GREEN

Top improvement this sprint:
  - Added 4 state transition tests to the order service regression set.
    Caught the concurrent state change defect in QA, not production.
```

The team sees quality as a shared metric, not a QA-private report.

### Bad — QA metrics reported only to QA lead

Metrics exist but are only visible in QA's internal tracker. The team does not see them.
Escaped defects are treated as QA failures, not team failures.

### Good — Mentoring through artifact review

```
Feedback to junior QA on bug report:

"The steps to reproduce are clear (good), but the 'Expected result' says 'it should work.'
'It should work' is not observable. What specific response code and body does the spec say?
Let's look at the AC together. Also: you've assigned Critical/Critical here — is the feature
unavailable for all users, or only in this edge case? For most users, checkout works fine.
This looks like Major/High. Here is how I distinguish Critical from Major: [explanation]."
```

Specific, educational, standard-anchored feedback on a real artifact.

### Bad — General feedback with no artifact anchor

"You need to write better bug reports." The QA team member does not know what specifically to improve.
The next bug report has the same problems.

### Good — Regression governance policy

```
Regression governance rules (QA team, Sprint 25):

Inclusion criteria:
  - Test covers a path with a defect in the last 6 months.
  - Test covers a critical user journey per the risk matrix.
  - Test covers an integration point with a recent change.

Removal criteria:
  - Test has not detected a defect in 12 months.
  - Test covers a path rated as "low risk" in the strategy document.
  - Test is consistently slower than 60 seconds and duplicates an API test.

Runtime budget: full regression < 60 minutes (nightly). PR check < 10 minutes (smoke only).
Review cadence: regression set reviewed at the end of each sprint.
```

### Bad — Regression set grows indefinitely

Every sprint adds 10 new regression tests. Nothing is ever removed. The suite grows to 800 tests
and takes 4 hours to run. The team stops trusting it and stops running it.

## Boundaries

- Owns QA process, quality metrics, regression strategy, and QA team mentoring.
- Does not own team delivery schedule or resource allocation -> `project-manager`.
- Does not own team-wide engineering standards beyond QA practice -> `tech-lead`.
- Does not own product strategy or feature prioritization -> `product-manager` / `product-owner`.
- Does not own developer performance management -> manager.

## Sources

### Priority 1 — QA leadership and quality engineering canon

- ISTQB Advanced Level Test Manager Syllabus — https://www.istqb.org/certifications/advanced-level-test-manager
- ISO/IEC/IEEE 29119-2: Software Testing Processes (process improvement) — https://www.iso.org/standard/81228.html
- Lisa Crispin and Janet Gregory: More Agile Testing (team quality practices) — book reference
- Google Testing Blog — https://testing.googleblog.com/

### Priority 2 — Orientation

- James Bach: Heuristic Test Strategy Model (process quality section) — https://www.satisfice.com/download/heuristic-test-strategy-model
- Cem Kaner: Lessons Learned in Software Testing (team and process chapters) — book reference
- DORA State of DevOps Report (quality and deployment frequency metrics) — https://dora.dev/
- ISO/IEC 25010: Quality model for metrics definition — https://iso25000.com/index.php/en/iso-25000-standards/iso-25010

### Priority 3 — Background

- Camille Fournier: The Manager's Path (tech lead and mentoring chapters) — book reference
- Software Engineering at Google: Testing culture chapters — https://abseil.io/resources/swe-book
- ThoughtWorks Technology Radar — https://www.thoughtworks.com/radar

## Handoff

- Test strategy for a specific feature -> `test-strategy-and-planning`.
- Individual test case design -> `test-design-and-coverage`.
- Developer engineering standards and code quality -> `tech-lead`.
- Delivery scheduling and capacity planning -> `project-manager`.
- Product priority decisions on deferred defects -> `product-owner` / `product-manager`.
- CI/CD platform improvements -> `devops-sre` with specific requirements.
