---
name: shared-prd
description: Use when the user asks to create, refine, review, structure, or document a Product Requirements Document, PRD, product requirements, feature specification, user stories, acceptance criteria, product metrics, MVP scope, rollout plan, or requirements for AI-powered product features.
---

# PRD

## Overview

Create practical Product Requirements Documents that are clear enough for product, design, engineering, QA, analytics, and stakeholders to continue work from them. Favor concrete requirements, measurable outcomes, explicit scope, and open questions over polished but vague prose.

## Role Modes

Use this shared skill without blurring ownership:

- **Product Manager**: owns product-level PRD framing — problem, users, product goals, success metrics, discovery assumptions, roadmap context, MVP rationale, risks, and open product decisions.
- **Product Owner**: refines PRD within agreed product direction — MVP/release scope, product-level acceptance, backlog handoff, delivery readiness, open scope decisions, and traceability.
- **Business Analyst**: owns business-facing PRD content — business problem, stakeholders, business goals, user needs, business requirements, scope boundaries, acceptance signals, assumptions, risks, and open questions.
- **System Analyst**: reviews and extracts PRD context into system requirements, SRS/FRD, functional scenarios, acceptance criteria, NFR hints, dependencies, traceability, and open system questions.

Do not use this shared skill to transfer ownership of product strategy, backlog priority, system/API specification, UX solution design, QA strategy, analytics methodology, delivery governance, architecture, or implementation details to the wrong role.

## When to Use

Use this skill when the user asks to:

- write or improve a PRD;
- turn an idea into product requirements;
- define a feature, MVP, or rollout scope;
- produce user stories, acceptance criteria, success metrics, or risks;
- document requirements for AI-powered features.

Do not use this skill for low-level engineering specs unless the user explicitly wants a PRD-style product document.

## Model Requirements

This skill works best with models capable of multi-step product analysis, structured Markdown generation, file editing, and Python tool use.

Minimum recommended capabilities:

- follows mandatory gates before final output;
- handles 8k+ tokens of PRD or project context;
- produces structured Markdown without dropping required sections;
- runs and interprets Python helper scripts;
- preserves the user-specified language: Russian, English, or both.

For weaker or smaller models:

- warn the user before starting full PRD work that the model may miss structure, skip gates, or lose context;
- prefer `One-pager` or `Lean PRD`;
- use `scripts/prd-context-pack.py` before follow-up work;
- use `scripts/extract-prd-section.py` instead of loading full PRDs;
- always run `scripts/validate-prd.py` and `scripts/score-prd.py`;
- avoid full PRD generation from vague input without additional clarification.

If the current model cannot reliably follow multi-step instructions, cannot run tools, has limited context, or the user explicitly says they are using a weak/small/cheap model, give this warning before continuing:

```text
Warning: this PRD skill may be unreliable on weaker models. I recommend Lean PRD mode with script-assisted validation, section extraction, and explicit checkpoints before saving files.
```

## Subagent Usage

This skill can be used by subagents for bounded PRD tasks.

Good subagent tasks:

- review an existing PRD for gaps, risks, weak metrics, missing acceptance criteria, and unclear scope;
- generate a traceability matrix or backlog export from a saved PRD;
- extract open questions, assumptions, dependencies, risks, metrics, or section summaries;
- run script-assisted validation and report findings;
- perform an independent second pass after the main agent drafts the PRD.

Do not delegate:

- final user-facing PRD decisions;
- language and file-saving choices;
- unresolved product assumptions;
- stakeholder trade-offs;
- saving files unless the main agent has already confirmed path and language with the user.

When delegating, pass only the needed section or `scripts/prd-context-pack.py` output instead of the full PRD whenever possible. The subagent must return findings, proposed changes, and uncertainty; the main agent owns final synthesis and user confirmation.

## Mandatory Start Gate

Before producing the final PRD, ask the user:

1. Should the result be saved to file(s) or returned only in the chat?
2. What language should the PRD be prepared in: Russian, English, or both?

If the user wants files, also ask for the target path or propose a reasonable path such as `docs/<feature-slug>-prd.md`. Do not save files until the user confirms.

If the user already specified one of these choices, ask only for the missing choice. If both are already specified, briefly confirm them before proceeding.

Ask discovery questions in the user's conversation language by default.

If the requested PRD output language differs from the conversation language:

- ask clarification questions in the conversation language;
- prepare the PRD in the requested output language;
- if output is `both`, ask questions in the conversation language and prepare two separate PRD files: one Russian file and one English file. Do not mix both languages in one PRD unless the user explicitly asks for a single bilingual file.

## Workflow

### 1. Gather Context

Read nearby project context when relevant and cheap: `README.md`, product docs, package metadata, or existing specs. Do not over-read unrelated directories.

Clarify missing critical information. Ask 2-4 focused questions at a time, prioritizing the weakest area:

- Problem: what user or business pain exists now?
- Users: who is affected, and what are their goals?
- Value: why build this now, and what changes if it succeeds?
- Scope: what is MVP, what is out of scope, and what can wait?
- Metrics: how success will be measured, with baseline and target if known?
- Constraints: deadlines, platforms, tech stack, compliance, performance, integrations.

If the user gives a detailed brief, do not ask boilerplate questions. Ask only about real gaps.

If the input is vague, ask these first: what problem are we solving and for whom; what outcome would make this successful; what is explicitly out of scope. Use `references/discovery-question-bank.md` when the first request is vague, readiness score is below 80, or a specific score area is weak.

### 2. Score Requirement Readiness

Estimate readiness on a 100-point scale:

| Area | Points | Look for |
| --- | ---: | --- |
| Business value and goals | 25 | Problem, user/business impact, why now, expected outcome |
| Functional scope | 25 | Main workflows, user stories, acceptance criteria, edge cases |
| Users and UX | 15 | Personas, journeys, interaction constraints, accessibility needs |
| Metrics and validation | 15 | KPIs, targets, analytics events, experiment or validation plan |
| Technical and delivery constraints | 15 | Integrations, security, performance, data, platform, dependencies |
| Risks and boundaries | 5 | Assumptions, risks, non-goals, open questions |

If score is below 80, continue discovery before drafting the full PRD. If the user explicitly asks for a draft despite gaps, mark unknowns as `TBD` and include an `Open Questions` section.

### 3. Choose PRD Depth

Pick the smallest useful format:

- **One-pager**: small change, bug-adjacent improvement, early alignment.
- **Lean PRD**: normal feature with moderate uncertainty.
- **Full PRD**: large initiative, cross-team work, strategic feature, compliance, AI feature, or high delivery risk.
- **Technical PRD**: product requirements for infrastructure, platform, data, security, or AI systems; still explain user/business impact.

Use `references/prd-template.md` for the full structure and trim sections that do not add value.

### 4. Draft the PRD

The PRD must cover:

- executive summary;
- problem statement and why now;
- goals, non-goals, and scope;
- target users/personas;
- user stories or jobs-to-be-done;
- acceptance criteria;
- functional requirements;
- non-functional requirements when relevant;
- success metrics and validation method;
- dependencies, assumptions, risks, and mitigations;
- rollout or phasing;
- open questions.

For AI features, also include:

- model/tool/API requirements;
- input/output expectations;
- quality evaluation strategy;
- fallback and human-review behavior;
- privacy, data retention, and misuse risks;
- measurable accuracy, citation, latency, cost, or safety criteria.

### 5. Quality Rules

Write requirements that are specific, measurable, testable, and bounded.

Avoid:

- vague language such as "fast", "simple", "intuitive", "modern" without measurable criteria;
- implementation ownership hidden inside product requirements;
- unvalidated assumptions presented as facts;
- scope creep without explicit priority;
- user stories without acceptance criteria.

Prefer:

- `Given / When / Then` acceptance criteria;
- P0/P1/P2 prioritization;
- measurable thresholds;
- explicit out-of-scope items;
- clear baseline and target for each key metric;
- open questions instead of invented details.

Use `references/user-stories-and-metrics.md` for story and metrics guidance.

### 6. Use Supporting Scripts

When a PRD is saved as Markdown, use the Python scripts in `scripts/` when they fit the task:

- `scripts/validate-prd.py <file> --lang auto|ru|en|both` checks required sections, language, stories, acceptance criteria, metrics, placeholders, vague wording, and document length.
- `scripts/score-prd.py <file> --lang auto|ru|en|both` estimates readiness on the same 100-point model used in this skill.
- `scripts/extract-open-questions.py <file>` extracts open questions, `TBD`, `TODO`, and unresolved assumptions for follow-up.
- `scripts/prd-context-pack.py <file>` creates a compact context pack for future agent turns without reading the full PRD.
- `scripts/extract-prd-section.py <file> --section scope|stories|metrics|risks|open-questions` extracts only the needed section.
- `scripts/assign-prd-ids.py <file> --output <file>` adds stable IDs such as `STORY-001`, `AC-001-01`, `METRIC-001`, and `RISK-001`.
- `scripts/build-traceability-matrix.py <file> --format markdown|csv` links goals, stories, acceptance criteria, metrics, and risks.
- `scripts/compare-prd-versions.py <old> <new>` shows changed PRD sections across versions.
- `scripts/prd-to-backlog.py <file> --output backlog.csv` exports stories and acceptance criteria for delivery tools.

If a script is not applicable to the PRD format, language, or project conventions, do not ignore the need for automation. Adapt the script so it can be used in the current PRD workflow, then run the adapted script and report what changed.

To verify the script suite after changes, run this from the skill directory:

```bash
python3 tests/test_prd_scripts.py
```

### 7. Review Before Finalizing

Before final output, self-check:

- Can a stakeholder understand why this matters?
- Can engineering estimate and challenge the scope?
- Can design identify flows, states, and UX constraints?
- Can QA derive test cases?
- Can analytics measure success?
- Are assumptions, dependencies, and open questions visible?
- Is the selected language exactly what the user requested?
- If saving to files, did the user explicitly confirm the path and language?

If the PRD is saved, state the path. If it is not saved, state that the result was returned only in chat.
