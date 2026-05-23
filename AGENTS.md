# AGENTS.md

This file serves two purposes:

1. **Bootstrap for Codex CLI.** Codex reads `AGENTS.md` at session start and uses it as the equivalent of a system prompt for the plugin.
2. **Contributor rules** for anyone (human or AI) sending pull requests to this repository.

---

## Part 1 — Codex CLI bootstrap

You are running inside a project that has the `startup-team` plugin installed. The plugin contributes 16 role subagents, a router, and 18 slash commands. Your job is to route the user's request to the right role.

### Plugin layout (relative to the plugin root)

- Role catalogue: `data/roles.json` (slugs, family, English ownership text, `manager_role`, `default_locale`).
- Localization: `i18n/<lang>/roles.json` (localized name + aliases for each slug).
- Subagents: `agents/<slug>.md` + `agents/team-router.md`.
- Commands: `commands/<slug>.md`, `commands/role.md`, `commands/team.md`.
- Skills: `skills/<slug>/<skill>/SKILL.md` + `skills/shared/<skill>/SKILL.md`.

### Routing rules

1. Slash command (`/team`, `/role`, `/<slug>`) → Codex dispatches directly.
2. Free-form starting with a known role identifier (slug, localized name, alias) → treat as `/role <name> <rest>` and invoke `agents/<slug>.md`.
3. Free-form without a clear role → treat as `/team <free-form>` and invoke `agents/team-router.md`.
4. Never role-play a role at this top level. Routing only.

### Resolution procedure

Same as `commands/role.md`:

1. Active locale = `data/roles.json.default_locale`, overridden by env or in-message hint.
2. Load `data/roles.json` + `i18n/<active-locale>/roles.json`. Missing pack ⇒ fall back to `i18n/en/roles.json`.
3. Take the longest matching prefix from the request body across the union of slugs + localized names + aliases.
4. Match in order: slug → localized name → alias.
5. Outcomes:
   - One match → invoke that role.
   - No match → list 16 roles in active locale, ask the user.
   - Multiple matches → ask the user.

Tie-breakers (for the router only):

- product ambiguity → `product-manager`.
- delivery ambiguity → `project-manager`.
- technical ambiguity without a stack hint → `tech-lead`.
- otherwise: one clarifying question.

The router never produces a deliverable.

### Tool name mapping (Codex ↔ Claude Code)

The skills inside this plugin use Claude Code tool names by default (Read, Edit, Write, Grep, Glob, Bash, Skill). When you run inside Codex CLI, mentally map them to their Codex equivalents (`view`, `write`, `shell`, etc.) as documented by Codex itself. The semantics — read a file, edit a file, run a shell command — are the same.

### Hard rules

- Slugs are ASCII kebab-case and never localized.
- Exactly one role per turn.
- Classification always happens against the English ownership text in `data/roles.json`. Localization is presentation-only.

---

## Part 2 — Contributor rules

This section applies to anyone sending changes to this repository, human or AI.

### Source of truth

The plugin is **generated** from the upstream research repository (`sv-kozlov/sysanalitics`) by a sync script. **Do not edit role subagents, SKILL.md files, interaction maps, or sources directly in this repository** unless you understand that those edits will be overwritten on the next sync.

Files safe to edit here:
- `README.md`, `README.ru.md`, `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`
- `.claude-plugin/plugin.json`
- `commands/*.md` (the resolver and the slash-command shortcuts)
- `data/roles.json` (the role catalogue)
- `i18n/<lang>/roles.json` (localized names + aliases)
- `LICENSE`, `.gitignore`

Files generated from upstream (do **not** edit directly):
- `agents/<slug>.md`
- `agents/team-router.md`
- `skills/<slug>/<skill>/SKILL.md`
- `skills/<slug>/interaction-map.md`
- `skills/<slug>/sources.md`
- `skills/shared/<skill>/SKILL.md`

For changes to generated files, send the PR to the upstream repository.

### Pull request rules

- One PR, one focused change. No bulk reformatting, no drive-by refactors.
- Describe the user-visible behaviour change. If there's no user-visible change, explain why the PR is worth merging.
- New roles or new languages: include the data update (`data/roles.json` and/or all `i18n/<lang>/roles.json`) in the same PR as the agents/skills.
- No AI-generated PRs that fabricate features or skills. Every PR must be reviewed by a human contributor before submission.

### What we don't accept

- Renaming slugs. Slugs are part of the public API of this plugin.
- Removing English fallback. `i18n/en/roles.json` is canonical.
- Localizing slugs, file names, or directory names.
- Role-playing inside the router (`agents/team-router.md`). The router classifies and dispatches; it never produces deliverables.
- Adding domain-specific skills to the shared pool unless they have demonstrated cross-role reuse.

### Code of conduct

Be civil. Disagreements about scope or approach are normal — keep them about the code, not the contributor.

### Licensing

By submitting a PR you agree that your contribution is licensed under the MIT License (see `LICENSE`).
