# Release Notes

## v0.1.0 — 2026-05-23

Initial public release of `startup-team`.

### What's in this release

- **16 role subagents** in `agents/<slug>.md` covering analysis, product, delivery, architecture, design, engineering, and quality:
  `system-analyst`, `business-analyst`, `product-analyst`, `product-owner`, `product-manager`, `project-manager`, `system-architect`, `ui-ux-designer`, `tech-lead`, `backend-go-developer`, `python-developer`, `frontend-developer`, `mobile-developer`, `fullstack-developer`, `ml-engineer`, `qa-engineer`.
- **1 router subagent** `agents/team-router.md` that classifies free-form requests against the 16-role taxonomy.
- **18 slash commands** in `commands/`: `/team`, `/role`, and one direct `/<slug>` per role.
- **152 skills** in `skills/<slug>/<skill>/SKILL.md` plus 10 cross-role skills in `skills/shared/`.
- **Language-neutral core** in `data/roles.json` and localized strings in `i18n/en/roles.json` and `i18n/ru/roles.json`.
- **Multi-CLI bootstrap**: `CLAUDE.md` (Claude Code), `AGENTS.md` (Codex CLI), `GEMINI.md` (Gemini CLI).
- **Bilingual README**: `README.md` (English) and `README.ru.md` (Russian).

### Routing

- Slug, localized name, alias, or slash command → direct dispatch.
- Free-form without a clear role → `team-router` classifies and dispatches to exactly one role.
- Tie-breakers: product ambiguity → `product-manager`; delivery ambiguity → `project-manager`; technical ambiguity without stack hint → `tech-lead`.

### Known limitations

- Locale packs ship for `en` and `ru` only. New languages: add `i18n/<lang>/roles.json` mirroring slugs from `data/roles.json`.
- `commands/role.md` matches role identifiers as a longest prefix at the start of the message. A role name in the middle of a sentence falls through to the router.

### Compatibility

- Claude Code: install via `/plugin marketplace add sysanalitics/startup-team` + `/plugin install startup-team@startup-team`.
- Codex CLI: `/plugins` → search `startup-team` → Install Plugin.
- Gemini CLI: `gemini extensions install https://github.com/sysanalitics/startup-team`.
