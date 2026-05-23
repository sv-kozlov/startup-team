---
name: team
description: Route an ambiguous request to the right role from the 14-role team. Use when you don't know which specialist to address.
---

You received a free-form request: $ARGUMENTS

Dispatch this request via the `team-router` subagent. The router will classify the request
against the 14-role taxonomy and hand it off to exactly one role agent. Do not answer the
request yourself. Do not preempt the router's classification.
