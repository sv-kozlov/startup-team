---
name: mentoring-and-growth
description: Use when developing engineers from Middle to Senior to Lead — structuring growth conversations, identifying skill gaps, designing stretch assignments, giving feedback that changes behavior, and maintaining a skill matrix that makes the team's growth trajectory visible. Lead-level skill; does not include performance management or career administration.
family: lead
profile_level: Lead
---

# Mentoring and Growth

## Purpose

Build the team's engineering capability so that the team can solve increasingly complex problems without relying on one expert. Develop each engineer deliberately: identify their current gap, design a stretch that closes it, give feedback that changes behavior, and track progress on a visible skill matrix. The goal is a team that grows, not a team that depends.

## Use When

- An engineer is ready to move from Middle to Senior and needs a structured growth path.
- A Senior engineer wants to develop towards Staff or Lead impact and needs cross-cutting skill development.
- A new team member is onboarding and needs to understand what growth looks like in the team's context.
- The tech lead is preparing for 1-1 conversations and needs a structured framework.
- The team's skill matrix has not been updated in more than one quarter.
- The team has knowledge concentration risk: one person is the expert in a critical area and no one else can act as backup.

## Do Not Use When

- The issue is performance management: an engineer is consistently below expectations despite feedback — `line-manager` / `engineering-manager`.
- The issue is compensation or promotion administration — `engineering-manager` / HR function.
- The issue is an immediate interpersonal conflict — `line-manager`.
- The request is about hiring a new engineer, not developing an existing one — `hiring-and-interview-loop`.

## Inputs

- Engineer's current level and recent work: what tasks they own, what quality they produce, where they struggle.
- Team's growth needs: which skills are underrepresented, which areas need knowledge depth beyond one person.
- Career expectations: what the engineer wants to develop, at what pace.
- Company's leveling framework if it exists; team's adaptation of it if the framework is vague.
- Previous 1-1 notes, growth plan, and last quarter's goals.

## Workflow

1. **Establish the current baseline.** For each dimension of the role (technical depth, system thinking, communication, influence, delivery), assess the engineer's current level. Use observable evidence: "can complete X tasks independently", "can review Y artifacts", "has explained Z decision to stakeholders." Avoid impressions.
2. **Identify the next gap.** A growth gap is the most valuable next step for the engineer and the team. It is not the biggest gap — it is the one that, when closed, most increases the engineer's independent contribution. For a Middle engineer: the ability to own a medium-complexity task end-to-end without daily check-ins. For a Senior: the ability to lead a cross-component design without the tech lead drafting the design first.
3. **Design a stretch assignment.** A stretch is a task that is slightly beyond the current capability of the engineer: doable with effort, not guaranteed without support. Key properties: has a real output (not a training exercise), has a mentor touchpoint (the tech lead reviews, not guides), has a specific completion criterion, and has a time bound (1–6 weeks depending on scope).
4. **Structure the 1-1.** Monthly minimum for growth-focused engineers; biweekly if active stretch is in progress. 1-1 structure: (a) engineer's agenda first — what do they want to talk about? (b) stretch assignment status — what is going well, what is stuck? (c) feedback — one concrete observation from the previous two weeks; (d) forward — what is the one thing to focus on next? 1-1 is not a status update — it is a growth conversation.
5. **Give feedback that changes behavior.** Feedback must be: specific (tied to an observable action), timely (within 48 hours of the observation), behavioral (about what the engineer did, not who they are), and action-oriented (what to do differently). The test: can the engineer do something different next week based on this feedback?
6. **Maintain the skill matrix.** The team's skill matrix maps engineers to skill dimensions and their current level on each (for example, 1–4 scale per dimension). Update quarterly. Use the matrix to identify: knowledge concentration risk (only one person at level 3+ on a critical dimension), growth bottlenecks (multiple people at the same level with no path to the next), and hiring gaps (skills the team needs but no internal path to acquire).
7. **Track progress explicitly.** At the end of each quarter, review the engineer's growth plan: did the stretch close the gap? What changed? What is the next gap? Growth without tracking is drift. An engineer who has been "working on senior skills" for 18 months without a clear milestone has a management gap, not a personal gap.
8. **Delegate to build capability.** When a new challenge arrives, the default question is: which engineer is 80% ready for this and can grow into the remaining 20% with support? Not: who can do this fastest? Delegating to the fastest person creates dependency; delegating to the 80%-ready person creates capability.

## Outputs

- Individual growth plan: current baseline, next gap, stretch assignment, 1-1 cadence.
- Skill matrix: team-level view of dimensions and levels, updated quarterly.
- 1-1 notes with action items (private, kept by the tech lead).
- Quarterly growth review: progress on stretch assignments, updated matrix, next growth cycle plan.
- Knowledge resilience report: concentration risks identified and mitigation plan.

## Named Patterns

### Good — Baseline with observable evidence
"Current level: Maria can independently complete backend tasks scoped to a single service with clear requirements. She can review code for correctness and basic patterns. She needs guidance on API design decisions and does not yet initiate cross-service discussions. Next gap: API design ownership."

Observable, not impressionistic.

### Bad — Impressionistic baseline
"Maria is a solid developer. Not sure she's quite Senior yet." No evidence, no gap, no direction. Nothing changes next quarter.

### Good — Stretch assignment format
"Stretch: own the API design for the notification service integration with Stripe webhooks. Duration: 3 weeks. Deliverable: draft API spec reviewed by system-analyst and approved by tech lead. Mentor touchpoint: 30-min review at week 1 (direction check), feedback on the draft at week 2. Success: spec is ready for implementation without further re-design."

Real output, real deadline, mentor touchpoint defined, completion criterion clear.

### Bad — Training as stretch
"Complete the system design course on Udemy." No real output, no team impact, no observable skill gained. The engineer finishes the course and the skill gap is unchanged.

### Good — Feedback that changes behavior
"On Tuesday in the architecture review, you presented the solution without first stating the constraints it was solving. Two people in the room didn't have the context. Next time, open with: here is the problem, here are the constraints, here is the solution. That pattern works in both 1-on-1 and group settings."

Specific event, specific action, immediately applicable.

### Bad — Feedback without action
"You need to improve your communication skills." The engineer nods. Next week is identical. Nothing changes.

### Good — Skill matrix identifying concentration risk
```
Dimension          | Alex | Maria | Ivan | Risk
Payment integration|  3   |   1   |  1   | High (single expert)
API design         |  2   |   2   |  3   | Low
Incident response  |  3   |   1   |  2   | Medium
```
"Payment integration: Alex is the single expert. Ivan is the next target for growth in this area. Stretch planned for Q3."

### Bad — Skill matrix as a spreadsheet no one opens
Updated once in 2024. Tells the team nothing about who can cover what. The payment service has an incident; the only engineer who knows the integration is on vacation.

### Good — Delegation to build capability
New integration scope: "Lena is 80% ready for this — she's done similar scoped work but hasn't led a cross-team dependency. Assign to her with a check-in at the dependency negotiation point."
Three months later: Lena owns cross-team integrations independently.

### Bad — Delegation to the fastest person
Tech lead always assigns the hardest work to Alex. Alex grows. The rest of the team does simpler tasks. Alex becomes the bottleneck. The team cannot ship without Alex.

### Good — Quarterly review
"Q1 review for Ivan: stretch complete — he ran the postmortem and produced 4 action items, all tracked. Gap closed: facilitation under pressure. Next gap: mentoring a junior engineer. Q2 stretch: run onboarding for the next hire with 2 weekly check-ins."

Deliberate progression. The record shows movement.

### Bad — Annual review with no intermediate tracking
"Ivan has been working on senior skills for 18 months. We'll review in the annual performance cycle." No growth plan, no stretch, no check-in. The annual review confirms he is still not Senior. No one knows why.

## Boundaries

- Owns technical growth planning, stretch assignments, 1-1 structure, skill matrix, and deliberate feedback.
- Does not own performance management (sustained underperformance, PIPs, termination) — `line-manager` / `engineering-manager`.
- Does not own compensation decisions, promotion administration, or leveling approval — `engineering-manager` / HR.
- Does not own interpersonal conflict resolution — `line-manager`.
- Does not own hiring decisions — `hiring-and-interview-loop` + `engineering-manager`.

## Sources

### Priority 1
- Camille Fournier: The Manager's Path — O'Reilly, 2017. 1-1 structure, feedback, and engineer growth at tech lead level.
- Lara Hogan: Resilient Management — A Book Apart, 2019. Feedback delivery, growth conversations, skip-level dynamics.
- Will Larson: An Elegant Puzzle — Stripe Press, 2019. Skill matrix, knowledge concentration risk, team composition.

### Priority 2
- Patrick Kua: Talking with Tech Leads — Leanpub, 2014. Tech lead perspective on mentoring.
- Tanya Reilly: The Staff Engineer's Path — O'Reilly, 2022. Developing senior and staff engineers.
- Gergely Orosz: Developer career paths — https://newsletter.pragmaticengineer.com/

### Priority 3
- Engineering Ladders reference framework — https://www.engineeringladders.com/
- LeadDev: Engineer growth articles — https://leaddev.com/
- CTO Craft: Mentoring practices — https://ctocraft.com/

## Handoff

- Performance management, sustained underperformance, PIPs → `line-manager` / `engineering-manager`.
- Compensation, promotion approval, leveling decisions → `engineering-manager` / HR.
- Hiring new engineers to fill identified skill gaps → `hiring-and-interview-loop`.
- Interpersonal conflict between engineers → `line-manager`.
