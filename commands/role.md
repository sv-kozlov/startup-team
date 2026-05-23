---
name: role
description: Address a specific role by slug, localized name, or alias. Example — /role system-analyst, /role PM, /role <localized name from i18n>.
---

The user named a role and passed a follow-up request: $ARGUMENTS

## Resolution procedure

1. Determine the active locale: read `data/roles.json.default_locale`, override with
   the user's environment locale if provided, override again if the request body
   contains an explicit locale hint (e.g. a sentence in that language).
2. Load `data/roles.json` (slug list, language-neutral) and
   `i18n/<active-locale>/roles.json` (localized name + aliases). If the locale pack is
   missing, fall back to `i18n/en/roles.json`.
3. Tokenize `$ARGUMENTS`: extract the role token as the longest prefix that matches a
   known role identifier (slug, localized name, or alias), and treat the rest as the
   request body to forward.
4. Normalize the role token: lowercase, trim, collapse internal whitespace.
5. Match the normalized token, in order:
   - against any `slug` in `data/roles.json` (always available, ASCII kebab-case),
   - against `i18n/<active-locale>/roles.<slug>.name` (case-insensitive),
   - against any entry in `i18n/<active-locale>/roles.<slug>.aliases` (case-insensitive).
6. Resolution outcomes:
   - **Exactly one match.** Invoke the subagent at `agents/<slug>.md` with the
     remainder of the request. Pass the body through unchanged.
   - **No match.** Respond with the canonical list — print each `<slug>` together with
     `i18n/<active-locale>/roles.<slug>.name` — and ask the user to pick one. Do NOT
     silently fall back to the router. The user named a role explicitly, so an
     unrecognized name is a user error, not an ambiguity for the router to resolve.
   - **Multiple matches** (defensive — should not happen with the current data).
     Print the matching candidates and ask the user to disambiguate.

## Examples (locale-agnostic)

- `/role system-analyst design an order contract` → invoke `system-analyst`.
- `/role <localized full name> ...` → invoke the matching slug.
- `/role PM need a retention metric` → invoke `product-manager`.
- `/role unknown ...` → list 16 roles in the active locale, ask the user to choose.
