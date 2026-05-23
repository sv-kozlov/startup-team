# Claude Code — bootstrap

This file is read automatically by Claude Code at session start when the `startup-team` plugin is installed. It tells Claude how to find the role catalogue, the resolver, and the router.

You (Claude) are running inside a project that has the `startup-team` plugin installed. The plugin contributes 16 role subagents, a router, and 18 slash commands. Your job in this file is to know **how to route a user's request to the right role** when the user does NOT use a slash command directly.

## Plugin layout (relative to the plugin root)

- Role catalogue: `data/roles.json` (slugs, family, English ownership text, `manager_role`, `default_locale`).
- Localization: `i18n/<lang>/roles.json` (localized name + aliases for each slug).
- Subagents: `agents/<slug>.md` (one per role) + `agents/team-router.md` (the router).
- Commands: `commands/<slug>.md`, `commands/role.md`, `commands/team.md`.
- Skills: `skills/<slug>/<skill>/SKILL.md` + `skills/shared/<skill>/SKILL.md`.

## Routing rules

When the user invokes a slash command, Claude Code dispatches it directly — nothing more to do here. When the user phrases a request in free form without a slash:

1. If the request names a role (slug / localized name / alias) at the start of the message, treat it as `/role <name> <rest>` and route to that subagent.
2. If the request is free-form and you cannot identify a single role, treat it as `/team <free-form>` and invoke the `team-router` subagent.
3. Never role-play a role yourself in this file. Routing only.

## Resolution procedure (mirrors `commands/role.md`)

1. Determine active locale: `data/roles.json.default_locale`, overridden by user environment or explicit hint in the request (e.g. Cyrillic in body ⇒ `ru`).
2. Load `data/roles.json` and `i18n/<active-locale>/roles.json`. If the locale pack is missing, fall back to `i18n/en/roles.json`.
3. Tokenize the request: take the longest prefix that matches any known identifier (slug, localized name, alias).
4. Match in order: slug → localized name → alias.
5. Outcomes:
   - **Exactly one match** → invoke `agents/<slug>.md` with the remainder.
   - **No match** → list all 16 roles in the active locale and ask the user to pick. Do NOT silently fall through to the router when the user named a role.
   - **Multiple matches** (defensive) → ask the user to disambiguate.

For ambiguous free-form requests, the `team-router` subagent applies these tie-breakers:

- product ambiguity → `product-manager` (the designated `manager_role`).
- delivery ambiguity → `project-manager`.
- technical ambiguity without a stack hint → `tech-lead`.
- otherwise: one clarifying question.

The router **never** produces a deliverable itself.

## Hard rules

- Slugs are ASCII kebab-case and never localized.
- A request resolves to exactly one role per turn.
- Localization is presentation-only. The router and every skill classify on the English ownership text in `data/roles.json`.

## Adding to a project

When a project consumes this plugin, the project's own `CLAUDE.md` (if any) takes precedence. Project-level instructions override plugin-level routing.
