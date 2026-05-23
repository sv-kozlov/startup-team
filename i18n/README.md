# i18n — language packs for startup-team

The plugin core is language-neutral. All human-facing role names, aliases, and
router strings are loaded from this directory based on the active locale.

## Layout

```
i18n/
├── en/
│   └── roles.json    # English names + aliases for the 16 roles
├── ru/
│   └── roles.json    # Russian names + aliases for the 16 roles
└── README.md         # this file
```

## Files

### `<lang>/roles.json`

Locale-specific names and aliases for each role. Keys match the slug list in
`data/roles.json` exactly (one-to-one).

```json
{
  "locale": "ru",
  "roles": {
    "<slug>": { "name": "<localized role name>", "aliases": ["<alias>", ...] }
  }
}
```

## How resolution works

1. `data/roles.json` carries the slug list and language-neutral metadata
   (`family`, `owns`). This is the source of truth — adding a role means adding
   it here first.
2. `i18n/<lang>/roles.json` adds the localized display name and aliases.
3. The `/role` command (see `commands/role.md`) loads both files, normalizes
   the user token, and tries — in order — to match against:
   - `data/roles[].slug` (always available),
   - `i18n/<active-locale>/roles.<slug>.name` (case-insensitive),
   - `i18n/<active-locale>/roles.<slug>.aliases` (case-insensitive).
4. Active locale defaults to `data/roles.json.default_locale` (currently `en`)
   and can be overridden by user environment or an explicit hint in the request
   (e.g. "по-русски ...").
5. The team-router (`agents/team-router.md`) uses slugs only for dispatch. Any
   localized name in router output should be rendered through the i18n file.

## Adding a new language

1. Create `i18n/<lang>/roles.json` mirroring the slug list in `data/roles.json`.
2. Localize the `name` per slug; aliases are optional but recommended.
3. Update this README's "Layout" section.
4. No other plugin file needs to change — the core stays language-neutral.

## Hard rules

- Do NOT put localized strings outside `i18n/`.
- Do NOT remove the `en` pack — it is the canonical fallback.
- Slugs are ASCII kebab-case and never localized.
- Aliases may be locale-specific (e.g. `гофер` only exists in `ru`).
