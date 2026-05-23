# startup-team

> **A 16-role product/engineering team as subagents — for Claude Code, Codex CLI, and Gemini CLI.**

[Russian / Русский ▶ README.ru.md](README.ru.md)

Address each role by its English slug, its localized name, a short alias, or a slash command. Ambiguous requests go through an LLM-based router that classifies and dispatches to exactly one role.

The plugin core is **language-neutral**. All localized strings live under `i18n/`.

---

## Installation

Install commands differ per platform. Pick the one that matches your CLI.

### Claude Code

Marketplace:

```
/plugin marketplace add sv-kozlov/startup-team
/plugin install startup-team@startup-team
```

Or from this git repository directly:

```
/plugin marketplace add https://github.com/sv-kozlov/startup-team
/plugin install startup-team
```

Local development (clone the repo and point Claude Code at the folder):

```
git clone https://github.com/sv-kozlov/startup-team
/plugin marketplace add ./startup-team
/plugin install startup-team
```

Verify:

```
/plugin
```

After install you get 18 slash commands (`/team`, `/role`, one `/<slug>` per role), 17 subagents (16 roles + `team-router`), and 152 skills available to those subagents.

### Codex CLI

Open the plugin manager and search for `startup-team`:

```
/plugins
startup-team
```

Then choose **Install Plugin**.

Codex auto-discovers the same `agents/`, `commands/`, and `skills/` folders that Claude Code uses. Tool-name differences are handled by the bootstrap files (`AGENTS.md` is read on session start, and skill files include a Codex tool mapping where relevant).

### Gemini CLI

Install as a Gemini extension straight from this repository:

```
gemini extensions install https://github.com/sv-kozlov/startup-team
```

Update later with:

```
gemini extensions update startup-team
```

Gemini loads `GEMINI.md` on session start, which activates the role catalogue and resolver behaviour.

---

## What's inside

- **16 role subagents** in `agents/<slug>.md` — each one carries its own curated set of skills (workflow, named patterns, sources, handoff blocks).
- **1 router subagent** in `agents/team-router.md` — classifies free-form requests against the 16-role taxonomy and dispatches.
- **18 slash commands** in `commands/` — `/team`, `/role`, and one direct `/<slug>` per role.
- **152 skills** in `skills/<slug>/<skill-name>/SKILL.md` (16 roles) plus 10 cross-role skills in `skills/shared/`.
- **Language-neutral metadata** in `data/roles.json` and **localized strings** in `i18n/<lang>/roles.json`.

```
startup-team/
├── .claude-plugin/plugin.json
├── README.md                              # this file (English)
├── README.ru.md                           # Russian translation
├── CLAUDE.md                              # Claude Code bootstrap
├── AGENTS.md                              # Codex CLI bootstrap + contributor rules
├── GEMINI.md                              # Gemini CLI bootstrap
├── LICENSE
├── agents/
│   ├── team-router.md
│   └── <16 role subagents>.md
├── commands/
│   ├── team.md
│   ├── role.md
│   └── <16 direct slash commands>.md
├── data/
│   └── roles.json                         # slugs + family + ownership (English)
├── i18n/
│   ├── README.md                          # i18n contract
│   ├── en/roles.json
│   └── ru/roles.json
└── skills/
    ├── shared/<10 shared skills>/SKILL.md
    └── <16 roles>/<each with skills, interaction-map.md, sources.md>
```

## The 16 roles

| slug | family | owns |
|---|---|---|
| system-analyst | analysis | Requirements, specifications, API/integration contracts, data contracts. |
| business-analyst | analysis | Business processes, business rules, impact analysis, acceptance criteria. |
| product-analyst | analysis | Product metrics, experiments, funnels, dashboards, hypothesis testing. |
| product-owner | product | Backlog, prioritization, scope, delivery-team coupling, acceptance. |
| product-manager | product | Strategy, discovery, roadmap, product outcomes, north-star metrics. |
| project-manager | delivery | Timelines, budget, resources, dependencies, risks, delivery comms. |
| system-architect | architecture | System architecture, components, integrations, NFR, architecture decisions. |
| ui-ux-designer | design | User flows, IA, wireframes, prototypes, UI, design system, handoff. |
| tech-lead | engineering | Engineering direction, code standards, technical mentoring, cross-cutting tech decisions. |
| backend-go-developer | engineering | Go services, concurrency, error handling, data layer in Go. |
| python-developer | engineering | Python services, data/ML-adjacent backend, async Python. |
| frontend-developer | engineering | TypeScript/React UI, state, accessibility, web performance. |
| mobile-developer | engineering | iOS / Android / cross-platform apps, mobile UX, store delivery. |
| fullstack-developer | engineering | End-to-end feature delivery across the web stack. |
| ml-engineer | engineering | ML models, training pipelines, feature stores, inference services. |
| qa-engineer | quality | Test strategy, automation, defect triage, quality gates, performance testing. |

The canonical list lives in `data/roles.json`. Localized names and aliases live in `i18n/<lang>/roles.json`.

---

## How to use

### Direct slash command (you know who you need)

```
/system-analyst design the order placement contract
/qa-engineer draft a test strategy for the new checkout flow
/backend-go-developer implement an idempotent Kafka producer
```

### Generic `/role` with any identifier (slug, localized name, alias)

```
/role system-analyst design the order placement contract
/role системный аналитик опиши контракт заказа     # ru name
/role гофер реализуй идемпотентного продьюсера Kafka  # ru alias
/role PM we need a retention metric                # short alias
```

`/role` loads `data/roles.json` plus `i18n/<active-locale>/roles.json`, normalizes the role token, and matches against slug / localized name / aliases. On an unrecognized name it prints the 16-role list in the active locale and asks you to pick — it does NOT silently fall through to the router.

### Free-form via `/team` (you don't know who you need)

```
/team we're seeing a slow checkout, need to understand why
/team should we invest in expanding to mobile?
/team how do we measure whether onboarding is working?
```

The `team-router` subagent classifies the request against the catalogue and dispatches to exactly one role using the rules in `agents/team-router.md`. Tie-breakers:

- product ambiguity → `product-manager` (designated manager role, configured in `data/roles.json.manager_role`).
- delivery ambiguity → `project-manager`.
- technical ambiguity without a clear stack → `tech-lead`.
- otherwise: one clarifying question.

The router never produces a deliverable itself.

---

## Internationalization

The plugin core is language-neutral:

- `data/roles.json` is the source of truth for slugs, families, and ownership statements (English).
- `i18n/<lang>/roles.json` carries localized names and aliases for a single language.
- `agents/`, `commands/`, and `skills/` contain **no localized strings** in this build — they hold only English content and reference i18n through the resolution procedure in `commands/role.md`.

Active locale is read from `data/roles.json.default_locale` (currently `en`) unless the user environment or a request hint overrides it. If a locale pack is missing, the resolver falls back to `i18n/en/roles.json`.

See `i18n/README.md` for the i18n contract and how to add a new language.

## How the resolver decides

```
user input ──► slug match?                yes → invoke agents/<slug>.md
                │ no
                ▼
            localized name match
            in i18n/<lang>/roles.json?    yes → invoke agents/<slug>.md
                │ no
                ▼
            alias match in
            i18n/<lang>/roles.json?       yes → invoke agents/<slug>.md
                │ no
                ▼
       command was /role?                 yes → print 16-role list, ask user
                │ no (command was /team)
                ▼
       team-router classifies              ── one of:
                                              single-role dispatch
                                              | product-manager (product ambiguity)
                                              | project-manager (delivery ambiguity)
                                              | tech-lead (tech ambiguity)
                                              | clarifying question
```

## Hard rules

- Slugs are ASCII kebab-case and never localized.
- The router never role-plays a role and never produces a deliverable.
- A request resolves to exactly one role per turn.
- Adding a new role: add it to `data/roles.json` first, then to every `i18n/<lang>/roles.json`, then create `agents/<slug>.md` and `skills/<slug>/`.
- Adding a new language: create `i18n/<lang>/roles.json` mirroring slugs from `data/roles.json`. No other plugin file needs to change.
- Localization is presentation-only. The router and every skill classify on the English ownership text.

## Skill discipline

Each role's skills follow a strict structure: Purpose, Use When, Do Not Use When, Inputs, Workflow, Outputs, Named Patterns (Good/Bad pairs), Boundaries, Sources (Priority 1/2/3), Handoff. Shared skills add a Role Modes section describing how each consuming role uses the skill.

Skill files are 100–250 lines of focused content. Code skills carry idiomatic examples; method skills carry decision-bearing workflows; lead skills carry review and standards material.

## Layout cheatsheet

```
agents/<slug>.md                     # the role's system prompt + skill routing
skills/<slug>/SKILL-NAME/SKILL.md    # one skill of that role
skills/<slug>/interaction-map.md     # the role's connection map with weights
skills/<slug>/sources.md             # the role's consolidated sources
skills/shared/<name>/SKILL.md        # cross-role skill (with Role Modes)
data/roles.json                      # slug list, ownership, manager role, default locale
i18n/<lang>/roles.json               # localized names + aliases for that language
commands/<slug>.md                   # /<slug> direct shortcut
commands/role.md                     # /role <any identifier> generic shortcut
commands/team.md                     # /team <free-form> router entry
```

---

## License

MIT — see [LICENSE](LICENSE).
