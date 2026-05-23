---
name: incident-and-on-call-review
description: Use when running a blameless post-incident review — facilitating the postmortem session, writing the postmortem document, deriving actionable items, tracking their resolution, and feeding findings back into engineering quality improvements. Covers the full incident learning loop.
family: method
profile_level: Senior+
---

# Incident and On-Call Review

## Purpose

Convert incidents from one-time failures into permanent improvements. Run a blameless review that produces concrete, owned, time-bound action items — and then track those items to completion. Prevent the same incident from occurring a second time due to inaction.

## Use When

- A production incident (P1 or P2) has been resolved and requires a formal postmortem.
- A near-miss or degradation event revealed a gap that warrants investigation even without full impact.
- Action items from a previous postmortem are overdue and require accountability.
- A recurring pattern of minor incidents suggests a systemic root cause that has not been addressed.
- The on-call rotation is burning out the team and incident patterns need a structural analysis.

## Do Not Use When

- The incident is ongoing — this skill covers the review after resolution, not incident response.
- The request is about on-call rotation design, paging configuration, or alerting setup → handoff to `devops-sre`.
- The request is about defining SLO/SLI targets → that is a joint conversation with `devops-sre` and is part of `engineering-quality-and-standards`.
- The request is about a performance issue that has not surfaced as an incident → use `tech-debt-management` or `engineering-quality-and-standards`.

## Inputs

- Incident timeline: raw on-call notes, alert timestamps, Slack/chat logs, deploy records.
- Impact data: user-visible error rates, SLO burn, customer-facing impact duration.
- Mitigation and resolution steps taken.
- Previous postmortems for the same service or component.
- Runbook state: did the runbook exist? Was it followed? Did it help?

## Workflow

1. Schedule the postmortem within 48–72 hours of resolution. Immediate review captures details that fade. Delay signals that the incident is not taken seriously. Invite: the on-call engineers, the tech lead, a representative from the affected product area, and optionally QA and DevOps/SRE.
2. Establish the blameless norm at the start of every session. Individuals made the best decisions they could with the information they had. The goal is to understand the system, not to assign fault. If blame enters the room, the session will produce cover-ups, not improvements.
3. Build the timeline collaboratively. Walk through: what was the first signal, when was it detected, when was the decision to escalate made, what mitigation was tried and in what order, when was the impact contained, when was full resolution achieved. Use a shared doc with a table: timestamp, actor, action, outcome.
4. Identify contributing factors, not a single root cause. Complex systems rarely have one cause. Ask "why" five times on each contributing factor. Stop when you reach a systemic property (design choice, missing automation, absent standard) rather than a human error.
5. Classify findings by type: detection gap (we did not know fast enough), response gap (we knew but could not act effectively), prevention gap (we could have built this differently), runbook gap (the instructions were wrong or absent), standard gap (a coding or observability standard would have caught this).
6. Write action items with three mandatory fields: owner (a named person, not a team), due date, and success criterion. "Fix the alert" is not an action item. "Add a PagerDuty alert on error_rate > 1% for 5m on the /checkout path, threshold calibrated against the incident data, owned by @alex, due 2026-06-15, verified in staging" is an action item.
7. Publish the postmortem document within five business days. Audience: the team, adjacent teams affected, and leadership for P1s. Format: impact summary, timeline, contributing factors, action items table, lessons learned. Make it findable.
8. Track action items to completion. Review the action items table at each sprint review. Overdue items get an explicit status update from the owner. Closed items get a verification note: "alert added, confirmed firing on a synthetic test." An action item that is never closed means the postmortem was theatrical.

## Outputs

- Postmortem document: impact, timeline, contributing factors, lessons learned.
- Action items table: owner, due date, success criterion, status.
- Runbook update if the review reveals a gap.
- Engineering quality backlog entry if the finding warrants a standard change.

## Named Patterns

### Good — Blameless framing
"On Tuesday at 14:32, the payment service returned 5xx errors for 12 minutes. The on-call engineer restarted the service at 14:44, which resolved the issue. We want to understand why the restart was necessary and why it took 12 minutes to detect."
Describes actions and outcomes without labeling the on-call engineer's decision as a mistake.

### Bad — Blame framing
"The on-call engineer should have caught this faster. The deployment that caused this was not properly reviewed."
The on-call engineer stops being candid. The real contributing factors stay hidden.

### Good — Timeline table
```
14:20  Deploy of v1.4.2 completed (automated, green CI)
14:28  Connection pool exhaustion begins (not alerted)
14:32  First 5xx errors visible in Grafana (no alert, discovered by user report)
14:38  User report received in #support
14:40  On-call paged manually by product manager
14:44  On-call restarts service
14:44  Error rate drops to 0
```
Every decision is traceable. No actor is singled out. The gaps are visible: 8 minutes from first error to detection, no automated alert.

### Bad — Narrative summary
"The deploy caused connection pool issues and after some investigation the on-call fixed it."
No timestamps. No decision points. Cannot identify where automation would have helped.

### Good — Five-why chain
Why did the connection pool exhaust? — The deploy doubled the number of DB queries per request.
Why was the doubling not caught in testing? — Integration tests run against a pool of 5; production uses 20.
Why is the test pool 5? — Default config from 2021, never revisited.
Why was there no alert on pool utilization? — Observability was added for request rate only.
Why? — Observability standard did not require pool metrics until this incident.
Root cause: observability standard gap. Action: add pool utilization metric to observability checklist.

### Bad — Single root cause assigned to a person
"The developer who wrote the query caused the incident." The systemic gap (test config, alerting standard) remains. The next deploy causes the same failure.

### Good — Action item with three fields
```
Action: Add connection pool utilization metric (gauge, pool_size and pool_used labels) to all services using pgx.
Owner: @maria
Due: 2026-06-10
Success criterion: Metric visible in Grafana for all 5 services, alert configured at 80% utilization.
```
Reviewable, accountable, verifiable.

### Bad — Vague action item
"Improve our observability." No owner. No date. No criterion. Appears in every postmortem. Never closes.

### Good — Action item tracking
Sprint review agenda item: "Postmortem DEBT-P1-2026-05-14 action items: 3 of 4 closed. Item 4 (alert on pool utilization) delayed by @maria due to dependency on devops/sre setup — scheduled for next sprint."
Overdue items surface in a predictable cadence, not six months later.

### Bad — Postmortem published and forgotten
Document exists in Confluence. No one checks the action items. Same incident occurs six months later. New postmortem written. Same action items appear.

## Boundaries

- Owns the blameless review process, postmortem document, and action-item tracking loop for the team.
- Does not own on-call rotation design, paging configuration, or alert routing → `devops-sre`.
- Does not own SLO/SLI definition → joint with `devops-sre` and `engineering-quality-and-standards`.
- Does not own customer-facing incident communication → `project-manager` or designated communication owner.
- Does not own root-cause work on infrastructure failures → `devops-sre`.

## Sources

### Priority 1 — Postmortem canon
- Google SRE Book: Postmortem Culture — https://sre.google/sre-book/postmortem-culture/
- Google SRE Workbook: Postmortem example — https://sre.google/workbook/postmortem-example/
- PagerDuty: Postmortem guide — https://response.pagerduty.com/after/post_mortem_process/

### Priority 2 — Reliability practice
- Charity Majors: On-call and reliability — https://charity.wtf/
- Lara Hogan: Resilient Management — A Book Apart, 2019. Blameless culture and feedback.
- Google SRE Workbook — https://sre.google/workbook/table-of-contents/

### Priority 3 — Background
- Increment Magazine: Reliability edition — https://increment.com/
- LeadDev: Incident culture articles — https://leaddev.com/

## Handoff

- On-call rotation, paging, and alerting configuration → `devops-sre`.
- SLO/SLI definition and error budget policy → `devops-sre` + `engineering-quality-and-standards`.
- Customer-facing incident communication → `project-manager` or designated owner.
- Systemic engineering standard gaps revealed by the incident → `engineering-quality-and-standards`.
- Technical debt items identified in the postmortem → `tech-debt-management`.
