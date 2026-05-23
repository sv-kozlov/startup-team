---
name: hiring-and-interview-loop
description: Use when designing or running the technical interview loop for engineering roles — defining what to assess at each stage, calibrating the hiring bar, structuring interview questions, and giving actionable post-interview feedback. Does not include administrative hiring authority, compensation decisions, or offer management.
family: method
profile_level: Senior+
---

# Hiring and Interview Loop

## Purpose

Hire engineers who can do the work the team actually does — at the level the role requires. Design an interview process that assesses this reliably and consistently, without being a hazing ritual or a proxy for "similar to us." Make every rejection explainable and every hire verifiable.

## Use When

- A new engineering role is being opened and the interview loop does not exist or has not been calibrated to the team's current work.
- Interview feedback is inconsistent between interviewers: one says "strong hire," another says "no hire" on the same candidate, with no shared rubric.
- The team is hiring at the wrong level: onboarded engineers are consistently below or above the expected independent capability.
- A specific interview stage is not predictive: engineers who pass it struggle on the job in the assessed area.
- The hiring bar needs calibration after a growth phase or team composition change.

## Do Not Use When

- The question is about performance review of an existing team member → handoff to `line-manager`.
- The question is about developing existing engineers from Middle to Senior → `mentoring-and-growth`.
- The question is about HR process, offer management, or compensation → handoff to `hr-recruiter` / `engineering-manager`.
- The question is about org structure changes or headcount planning → `engineering-manager`.

## Inputs

- Role description: what the engineer will actually do (not a generic job posting).
- Current team composition: skill gaps, level distribution, existing strengths.
- Assessment criteria: what distinguishes a Strong Hire from a Hire from a No Hire at this level.
- Previous interview outcomes: hires who struggled, rejections who succeeded elsewhere (false positives and false negatives).
- Existing interview kit if any: questions, rubrics, take-home assignments.

## Workflow

1. Define the role in terms of observable work, not traits. Instead of "strong communicator," write "can explain a technical trade-off to a product manager without jargon." Instead of "good with ambiguity," write "can scope a feature from a rough description and identify the top three unknowns." Observable criteria produce consistent assessments.
2. Design the loop as a pipeline with defined stages and clear owners. Each stage assesses one or two capabilities, not everything. Example: (a) recruiter screen — communication, motivation, constraints; (b) technical screen — problem-solving and domain basics; (c) systems design — architectural thinking at the role level; (d) coding — code quality and debugging; (e) team fit — how the candidate works with others, growth signals. Each stage has a named interviewer and a rubric.
3. Write the rubric for each stage before running interviews. A rubric has four elements: what is being assessed (observable behavior, not traits), what Strong Hire looks like, what Hire looks like, what No Hire looks like. Without a rubric, feedback reflects the interviewer's preferences, not the role's requirements.
4. Calibrate the hiring bar with a reference set. Use past interview notes for engineers who were hired and succeeded, hired and struggled, and rejected. Do at least one calibration session per quarter with all interviewers in the loop. Agreement on two or three reference cases produces more consistent assessments than a rubric alone.
5. Run structured interviews. Same questions, same order, independent scoring before the debrief. Interviewers who share notes before scoring contaminate each other's assessments. Debrief after all individual scores are written.
6. Give structured post-interview feedback. For every candidate: what specific behavior was observed, how it maps to the rubric, and the resulting recommendation. "Good vibe but not sure about depth" is not feedback. "Candidate correctly identified the race condition on step 3 but could not explain a mitigation beyond 'add a lock.' Meets the bar for Junior but not for Senior" is feedback.
7. Track outcomes and calibrate. Every quarter: what fraction of hires are performing at the expected level at 6 months? Are false positives (hired, struggling) clustered in a specific stage? Are false negatives (rejected, succeeded elsewhere) a pattern? Use the data to adjust the loop.
8. Protect the bar. Pressure to fill a role faster is the most common source of bar erosion. A weak hire costs more than an empty role: onboarding overhead, performance issues, team frustration, eventual exit. When a candidate does not meet the bar, the answer is "no hire and keep searching," not "hire and hope."

## Outputs

- Interview loop design: stages, owners, capabilities assessed per stage.
- Rubric per stage: observable criteria for Strong Hire / Hire / No Hire.
- Calibration session notes: agreed reference cases and bar definition.
- Post-interview feedback: structured, per-candidate, with recommendation and evidence.
- Quarterly outcome review: false positive/negative rate, loop adjustment recommendations.

## Named Patterns

### Good — Observable role criteria
"Senior Backend Engineer: can design a service with clear API boundaries given a product requirement, identify the top two risk areas, and explain the trade-offs. Can review a Go PR, distinguish correctness issues from style differences, and give actionable feedback within the review."
Observable, testable, not a trait list.

### Bad — Trait-based role criteria
"Strong communicator, creative problem-solver, passionate about engineering." Every interviewer has a different definition. Every candidate who is charming passes.

### Good — Stage rubric
```
Systems Design Stage — Senior Backend:
Strong Hire: scopes the problem, identifies constraints, proposes a design with explicit trade-offs, revises under challenge, asks about scale and reliability proactively.
Hire: proposes a reasonable design, can articulate one or two trade-offs when asked, revises when pointed to a gap.
No Hire: proposes a design without considering scale or failure modes, cannot revise when challenged, or requires the interviewer to drive the design.
```
Every interviewer applies the same standard.

### Bad — No rubric
"We'll know a good candidate when we see one." Three interviewers give Strong Hire, Hire, and No Hire on the same candidate. The debrief is an argument, not a decision.

### Good — Structured debrief
"Before we share notes: everyone write your score (1–4) and one key observation. Ready? Go. Alex: 3, could design the service but did not handle failure modes until prompted. Maria: 3, same observation plus the naming was inconsistent. I have 3 as well. Consistent. The gap is failure-mode reasoning — not a hire at senior."
Independent scoring first, then synthesis.

### Bad — Groupthink debrief
"What did you think?" "I liked them." "Me too." "Hire?" "Sure."
The most senior or most vocal interviewer anchors the room. Independent evidence is lost.

### Good — Evidence-based rejection
"Rejection rationale for candidate @jordan-chen: Stage 3 (systems design) — candidate proposed a monolithic design for a service that requires independent scaling. When challenged, revised to microservices without identifying the new failure modes introduced. Does not meet the bar for Senior (rubric: must revise under challenge and identify introduced trade-offs). Recommend re-evaluation at Mid level if available."
Explainable, respectful, and useful for the candidate if feedback is shared.

### Bad — Vague rejection
"Not the right fit." Cannot be shared with the candidate. Does not help calibrate the loop.

## Boundaries

- Owns technical interview loop design, rubric, calibration, and technical post-interview feedback.
- Does not own administrative hiring decisions, offer management, or compensation → `hr-recruiter` / `engineering-manager`.
- Does not own headcount planning or org structure → `engineering-manager`.
- Does not own developing existing team members → `mentoring-and-growth`.
- Does not own performance review of current employees → `line-manager`.

## Sources

### Priority 1 — Hiring practice canon
- Camille Fournier: The Manager's Path — O'Reilly, 2017. Hiring, bar calibration, and structured interviews.
- Lara Hogan: Resilient Management — A Book Apart, 2019. Structured feedback and calibration.
- Ron Lichty, Mickey Mantle: Managing the Unmanageable — Addison-Wesley, 2012. Engineering team hiring.

### Priority 2 — Structured interviewing practice
- Google re:Work Guide: Structured Interviewing — https://rework.withgoogle.com/guides/hiring-use-structured-interviewing/steps/introduction/
- Will Larson: An Elegant Puzzle — Stripe Press, 2019. Hiring bar and calibration.

### Priority 3 — Background
- Gergely Orosz: The Pragmatic Engineer Newsletter — https://newsletter.pragmaticengineer.com/
- LeadDev: Engineering hiring articles — https://leaddev.com/

## Handoff

- Administrative hiring, offer management, compensation → `hr-recruiter` / `engineering-manager`.
- Headcount planning and org structure → `engineering-manager`.
- Developing existing engineers on the team → `mentoring-and-growth`.
- Performance review and career decisions → `line-manager`.
