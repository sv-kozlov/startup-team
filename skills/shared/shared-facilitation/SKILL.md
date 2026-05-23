---
name: shared-facilitation
description: Use when a structured session — workshop, interview, refinement, review, decision meeting, or analytical readout — must be planned, run, and converted into owned artifacts and action items; includes situations where one-on-one clarification has failed or multiple stakeholders must reach a shared understanding within a bounded time box.
---

# Shared Facilitation

## Purpose

Run structured sessions that produce decisions, validated artifacts, clarified requirements, or explicit open questions within a bounded time box — with every output assigned to a named owner. Facilitation is not about managing a meeting calendar; it is about designing the conditions under which a group can reach a shared understanding or make a decision that they could not reach asynchronously. The facilitator does not own the session's substantive outputs; the accountable role does.

## Use When

- Multiple stakeholders or roles must align on scope, requirements, rules, process, system behavior, or decisions, and async communication has produced conflicting interpretations.
- A session needs an explicit objective, defined participants, structured agenda, and named outputs before it can be productive.
- A working session has been generating debate without converging — a structured technique (silent brainstorming, dot voting, 1-2-4-All, DACI) is needed to move past the impasse.
- An artifact (requirement, rule, process map, metric definition, specification) must be reviewed and signed off by multiple stakeholders in a single session.
- A retrospective, pre-mortem, or lessons-learned session must surface real issues rather than polite summaries.
- A discovery or research readout needs to translate data into shared understanding and next decisions.
- A cross-role dependency cannot be resolved through written handoff alone and requires a synchronous alignment session.

## Do Not Use When

- The decision is single-role: one role owns the decision and no other role's input is required → use the role-local skill directly.
- The session is a status update where no decision or artifact output is expected → manage as a communication, not a facilitated session.
- The task is delivery governance ceremonies owned by another role (sprint planning owned by Product Owner, stand-up owned by Engineering, QA sign-off owned by QA Lead) → facilitate only if explicitly delegated; do not absorb ownership of another role's ceremony.
- The question can be resolved by reading an existing artifact → escalate the artifact, do not schedule a session.
- The session topic requires organizational authority that the facilitating role does not have → escalate to leadership rather than facilitate a pseudo-decision.

## Inputs

- Session objective: the one question or decision the session must answer, or the one artifact it must validate.
- Participant list: roles, names, and their relationship to the session objective (owner, approver, contributor, informed).
- Current artifact or context: what participants need to read before the session.
- Known conflicts, assumptions, and open questions to be resolved in the session.
- Constraints: time box, decision-making authority present, tool or format requirements.
- Expected output: specific artifact, decision record, or action list.

## Workflow

1. **Define the session objective as a decision question.** Write it as: "By the end of this session, we will have decided / validated / clarified ___." If the objective cannot be stated this way, the session is not ready to run. Split unclear objectives into multiple sessions or resolve prerequisites async first.

2. **Choose the session format.** Match format to objective:
   - *Discovery / divergent*: structured brainstorming (1-2-4-All, brainwriting, silent cards), affinity grouping. Output: shared map of options or issues.
   - *Alignment / convergent*: dot voting, DACI assignment, force-ranked list. Output: prioritized list or decision.
   - *Validation / review*: structured walkthrough, red-green-refactor review, fishbowl. Output: signed-off artifact or defect list.
   - *Retrospective / learning*: timeline reconstruction, five whys, sailboat, FLAP. Output: action list with owners.
   - *Decision / approval*: DACI or RACI agreement, fist-to-five, consent vote. Output: recorded decision with approver and rationale.

3. **Design the agenda with time boxes.** Each agenda block must have: topic, format or technique, time box, owner of the block, and expected mini-output. Agenda blocks without a time box run over; blocks without a mini-output produce conversation without artifacts.

4. **Prepare working artifacts.** The facilitator prepares: pre-read material, working document or template, any visual aids or prompts. Participants who arrive without context cannot contribute productively. If a working document does not exist yet, create a draft outline specifically for the session — not to fill in the substance, but to give participants a structure to react to.

5. **Run the session: open, converge, and close.** Open by stating the objective, time box, and roles. Use the chosen technique to surface input (diverge), then narrow to decisions or action items (converge). Close by reading back all decisions, action items, and open questions — with owners and dates — before the session ends. Do not let participants leave without a shared record of what was decided.

6. **Capture and classify session output.** For each item from the session, assign one of: decision (made, owner recorded), action (named owner, deadline), assumption (recorded, risk noted), open question (owner must answer by date), or deferred (explicitly out of scope, with handoff target). Do not leave items unclassified.

7. **Convert results into owned artifacts and handoffs.** Within 24 hours of the session, produce the session summary and route each output item to its owner. Decisions that require an artifact (updated specification, rule catalog, acceptance criteria) become handoff tasks with explicit expected artifact and acceptance criteria.

## Outputs

- Facilitation plan and agenda: objective, participants, format, time boxes, and expected output per block.
- Decision record: each decision with approver, rationale, date, and downstream impact note.
- Action list: each action with owner, deadline, and description.
- Open-question log: each unresolved item with owner, resolution path, and deadline.
- Session summary: compact narrative of what happened, what was decided, what was deferred.
- Handoff tasks: for each item that requires an artifact from another role.

## Role Modes

### Business Analyst

Facilitates business discovery sessions (stakeholder interviews, workshops, process mapping), rule validation sessions, scope clarification meetings, and UAT preparation sessions. Uses structured techniques (AS IS / TO BE process walkthroughs, rule table reviews, affinity grouping of requirements) to elicit content that belongs in business analysis artifacts. Does not make product priority decisions in the session; surfaces those as open questions for Product Manager. Does not facilitate sprint ceremonies owned by other roles unless explicitly delegated.

### Product Owner

Facilitates backlog refinement sessions, sprint planning sessions (when the role owns facilitation), story mapping, and acceptance criteria review sessions with the delivery team. Uses structured techniques (story point estimation, MoSCoW prioritization, acceptance criteria walkthrough) to ensure every story entering the sprint is ready and every team member has the context to deliver it. Does not facilitate product strategy sessions (Product Manager) or technical design sessions (Tech Lead or System Analyst).

### Product Manager

Facilitates product discovery sessions, opportunity-to-bet framing sessions, roadmap review meetings, and stakeholder alignment sessions around product rationale. Uses structured techniques (opportunity solution trees, RICE scoring sessions, North Star metric definition workshops) to produce product-level decisions and a shared product rationale. Does not facilitate sprint planning or backlog refinement (Product Owner) or delivery governance sessions (Project Manager).

### Project Manager

Facilitates project kick-off sessions, dependency mapping workshops, risk identification sessions, steering committee meetings, and cross-team escalation sessions. Uses structured techniques (dependency mapping, risk heat mapping, decision escalation trees) to produce delivery governance artifacts. Does not facilitate product discovery, requirements elicitation, or technical design sessions — those belong to Product Manager, Business Analyst, or System Analyst.

## Boundaries

- Does not make substantive decisions for accountable stakeholders. The facilitator holds the process; the accountable role holds the decision.
- Does not own delivery communications or organization-wide change management → Project Manager or Change Manager owns those.
- Does not replace role-specific ceremonies when another role owns them. Facilitate only when explicitly delegated or when no other role has taken ownership.
- Does not produce the session's substantive output artifacts as the owner. Session artifacts (requirement documents, rule catalogs, decision records) are owned by the role responsible for them, not by the facilitator.

## Named Patterns

### Good — Session objective as decision question
```
Objective: "By the end of this 90-minute session, the team will have agreed on which discount
rules apply to B2B customers in Q2 scope, and the Product Manager will have approved or
explicitly deferred each rule."
```
The objective is falsifiable. At the end of the session, you can state whether it was achieved.

### Bad — Vague session objective
"Discuss the discount rules for B2B." Not falsifiable. No one knows when the session succeeded. The same discussion repeats in the next meeting.

### Good — Agenda with time boxes and mini-outputs
```
[00:00] Context and ground rules (5 min) — Facilitator — Output: shared understanding of goal
[00:05] Silent rule review: mark unclear/conflicting rules (15 min) — All — Output: annotated rule list
[00:20] Cluster and discuss conflicts (20 min) — All — Output: conflict log
[00:40] DACI: assign approvers for each conflict (15 min) — All — Output: DACI matrix
[00:55] Decisions and action items read-back (10 min) — Facilitator — Output: session summary
[01:05] Buffer / overflow (5 min)
```
Each block has a time box, owner, and mini-output. The session can run without the facilitator improvising.

### Bad — Agenda as topic list
```
1. Discount rules
2. B2B scope
3. Q2 timeline
4. Other
```
No time boxes, no techniques, no expected outputs. The session runs as long as the loudest voice speaks.

### Good — 1-2-4-All for divergent input
Step 1 (1 min): each participant writes their top concern on a card silently.
Step 2 (2 min): pairs share and synthesize to two concerns.
Step 3 (4 min): groups of four share and synthesize to one.
Step 4 (5 min): all groups report; facilitator clusters on a board.
Output: shared map of concerns that no single voice dominated.

### Bad — Open discussion as the only technique
Facilitator asks "Does anyone have concerns?" The two senior people speak; the rest nod. The session captures two concerns from two voices and misses six concerns that the junior participants did not voice.

### Good — Session close with read-back
"Before we close, I will read back what we decided and who owns each action.
DEC-1: Gold discount threshold confirmed at 10 000 RUB. Approver: Finance Controller.
ACT-1: Business Analyst updates rule catalog BR-041 by 2025-06-05.
OPEN-1: B2B exception for promotional codes — owner: Product Manager, answer by 2025-06-03."
Everyone hears the same record. Disputes surface before the session ends, not in follow-up email chains.

### Bad — Session without close
Meeting ends when time runs out. No read-back. Participants leave with different memories of what was agreed. Follow-up messages correct each other for a week.

### Good — Pre-read sent 24 hours before session
Current artifact or context document sent to all participants 24 hours before the session with a cover note: "Please read sections 2–4 and note any questions or conflicts you want to raise."
Session time is used for discussion and decision, not for reading the document aloud.

### Bad — Session begins with "let me share my screen and walk you through this"
First 20 minutes spent reading the document to participants who have not seen it. Participants are reactive rather than prepared. Convergent techniques fail because participants do not have shared context. Session overruns without reaching decisions.

## Sources

### Priority 1 — Method canon

- Sam Kaner et al., "Facilitator's Guide to Participatory Decision-Making" (Jossey-Bass, 3rd ed., 2014) — canonical reference on diverge-converge facilitation, the groan zone model, and structured techniques for group decision-making
- Liberating Structures — 1-2-4-All, TRIZ, What/So What/Now What, and other facilitation microstructures — https://www.liberatingstructures.com/ (freely available; used by ThoughtWorks, IDEO, and government digital services)
- International Association of Facilitators (IAF) — Core Competencies for professional facilitators — https://www.iaf-world.org/site/professional/core-competencies (defines the six core competency domains: co-create results, facilitate learning, model positive professional attitude, build and maintain relationships, design and customize applications, guide group to appropriate and useful outcomes)
- Esther Derby and Diana Larsen, "Agile Retrospectives: Making Good Teams Great" (Pragmatic Bookshelf, 2006) — canonical reference on retrospective facilitation structures (timeline, sailboat, FLAP, five whys)

### Priority 2 — Orientation

- IREB CPRE — Requirements elicitation techniques — https://cpre.ireb.org/en/concept/requirements-elicitation (structured elicitation as a facilitation sub-skill; interviews, workshops, observation)
- IIBA BABOK Guide v3 — Elicitation and Collaboration knowledge area — https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/
- Google re:Work — Meetings at Google: How to run effective meetings — https://rework.withgoogle.com/guides/meetings-how-to-run-effective-meetings/steps/introduction/

### Priority 3 — Background

- Wikipedia — Facilitation (business) — https://en.wikipedia.org/wiki/Facilitation_(business)
- Scrum Guide 2020 — Sprint Planning and Sprint Retrospective event descriptions — https://scrumguides.org/scrum-guide.html (orientation on ceremony ownership in Scrum; useful for knowing when facilitation belongs to the Scrum Master vs another role)

## Handoff

- When a session produces a decision that requires an artifact update → hand off to the artifact owner with a specific task, expected output, and deadline.
- When a session surfaces a requirement that belongs to System Analyst or Business Analyst → create a handoff task; do not absorb the authoring.
- When a session reveals a product priority decision that was not resolved → hand off to Product Manager with the options, rationale, and decision deadline.
- When a session reveals a delivery risk or schedule impact → hand off to Project Manager with the risk description, affected milestone, and decision path.
- When a session objective cannot be achieved because a prerequisite decision is missing → cancel or reschedule; do not run a session that cannot reach its objective.
