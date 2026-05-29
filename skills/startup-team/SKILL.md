---
name: startup-team
description: Use when a user asks for /team, startup-team routing, role selection, or delegation to product, analysis, architecture, engineering, design, delivery, or QA roles.
---

# Startup Team

Route the request to exactly one role from `data/roles.json`.

Use `agents/team-router.md` for free-form `/team` requests. Use `commands/role.md` for `/role <identifier>` requests. After resolving a role, load that role's `agents/<slug>.md`, then use the role's nested skills under `skills/<slug>/` only when they match the task.

Do not produce the role deliverable from this wrapper when the router has not resolved a role. Ask one concise clarifying question when the router rules require it.
