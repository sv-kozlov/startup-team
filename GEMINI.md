# Gemini CLI — bootstrap

This file is read automatically by Gemini CLI when the `startup-team` extension is installed. It tells Gemini how to find the role catalogue, the resolver, and the router.

You are running inside a project that has the `startup-team` extension installed. The extension contributes 16 role subagents, a router, and 18 slash commands. Your job here is to route the user's request to the right role when the user does NOT use a slash command directly.

## Extension layout (relative to the extension root)

- Role catalogue: `data/roles.json` (slugs, family, English ownership text, `manager_role`, `default_locale`).
- Localization: `i18n/<lang>/roles.json` (localized name + aliases for each slug).
- Subagents: `agents/<slug>.md` + `agents/team-router.md`.
- Commands: `commands/<slug>.md`, `commands/role.md`, `commands/team.md`.
- Skills: `skills/<slug>/<skill>/SKILL.md` + `skills/shared/<skill>/SKILL.md`.

## Routing rules

1. Slash command (`/team`, `/role`, `/<slug>`) → Gemini dispatches directly.
2. Free-form starting with a known role identifier (slug, localized name, alias) → treat as `/role <name> <rest>` and invoke `agents/<slug>.md`.
3. Free-form without a clear role → treat as `/team <free-form>` and invoke `agents/team-router.md`.
4. Never role-play a role at this top level. Routing only.

## Resolution procedure (mirrors `commands/role.md`)

1. Active locale = `data/roles.json.default_locale`, overridden by env or in-message hint (e.g. Cyrillic in body ⇒ `ru`).
2. Load `data/roles.json` + `i18n/<active-locale>/roles.json`. Missing pack ⇒ fall back to `i18n/en/roles.json`.
3. Take the longest matching prefix from the request across the union of slugs + localized names + aliases.
4. Match in order: slug → localized name → alias.
5. Outcomes:
   - One match → invoke that role.
   - No match → list 16 roles in active locale, ask the user.
   - Multiple matches → ask the user to disambiguate.

## Tie-breakers (router only)

- product ambiguity → `product-manager` (configured `manager_role`).
- delivery ambiguity → `project-manager`.
- technical ambiguity without a stack hint → `tech-lead`.
- otherwise: one clarifying question.

The router **never** produces a deliverable itself.

## Tool name mapping (Gemini ↔ Claude Code)

Skills inside this plugin reference Claude Code tool names (Read, Edit, Write, Grep, Glob, Bash, Skill). Map them to their Gemini equivalents as documented by Gemini CLI. Semantics are the same: read a file, edit a file, run a shell command, search for a pattern.

## Hard rules

- Slugs are ASCII kebab-case and never localized.
- Exactly one role per turn.
- Classification always happens against the English ownership text in `data/roles.json`. Localization is presentation-only.

## Updating the extension

```
gemini extensions update startup-team
```

Reinstall from source:

```
gemini extensions install https://github.com/sysanalitics/startup-team
```
