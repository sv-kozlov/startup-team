---
name: ml-code-review-and-mentoring
description: Use when reviewing an ML pull request or notebook for correctness (leakage, reproducibility, data schema, test coverage), writing an ML architecture decision record, or mentoring a colleague on ML engineering standards.
family: lead
profile_level: Senior+
---

# ML Code Review and Mentoring

## Purpose

Make ML code reviews move both the model and the author forward. Catch correctness issues (leakage, untested transformations, missing reproducibility guards) before they become production incidents. Lift team ML engineering practice through documented decisions and concrete mentoring, not personal taste.

## Use When

- Reviewing a non-trivial ML pull request (training script, inference service, feature pipeline).
- Reviewing a research notebook before it is promoted to a production pipeline.
- A leakage, reproducibility, or schema issue recurs across PRs — time to write an ADR.
- Onboarding a new ML engineer to the team's codebase and conventions.
- Mentoring a Middle toward Senior, or a Senior on team-level ML engineering impact.

## Do Not Use When

- The review is about API contract evolution → `model-serving-and-inference` for substance.
- The review is about feature signal selection → `feature-engineering-and-validation` for substance.
- The discussion is performance management of the author → out of scope; that is the manager's job.
- The task is defining the evaluation protocol → `ml-problem-framing-and-data-design`.

## Inputs

- Pull request or notebook with description, linked ticket, and test coverage (or explicit note on why tests are absent).
- Team conventions: agreed train/val/test split strategy, Pipeline usage rules, experiment tracking schema, naming conventions.
- Author's level and context: how much prior knowledge of the codebase did they have?

## Workflow

1. **Read the description and tests first.** If they do not tell you what the ML change does and why the approach was chosen, ask before reviewing the code. A PR with no description is a blocker regardless of code quality.
2. **Review in three passes:**
   - **Pass 1 — correctness:** leakage, data split integrity, fit-only-on-train, missing quality gate, untested transformations, serialization correctness.
   - **Pass 2 — shape:** Pipeline structure, config parametrization, experiment logging completeness, model card or eval report presence.
   - **Pass 3 — readability:** naming, dead code, notebook cell order, reproducibility documentation.
3. **Mark feedback intent clearly.** Use: `must` (blocker — correctness risk), `should` (strong suggestion), `nit` (style), `question` (clarifying), `praise` (reinforce a good pattern).
4. **Separate wrong from different.** If the code works without correctness risk, your preference for a different approach is a `nit` or `question`, not a `must`.
5. **Reference team standards, not feelings.** Link to the agreed Pipeline usage rule, ADR, or the ML problem statement. If no standard exists for a recurring pattern, write one.
6. **When a pattern repeats, write an ML ADR.** Lightweight format: context, decision, consequences. Review the ADR like code.
7. **Mentor by asking, not dictating.** "What happens if `fit()` is called on the full dataset here?" "How would you detect a label leakage from this feature?" "What test would catch this if it regressed?"
8. **Praise concretely.** "Good: the Pipeline wraps all transformations — no risk of refitting on val data" is more useful than "looks clean".

## Outputs

- PR review with intent-tagged comments and links to standards.
- ML ADRs in the repo's `docs/adr/` folder for recurring decisions.
- Convention updates (Pipeline rules, experiment naming, eval report template) rather than per-PR repetitions.
- Visible improvement in authors across their next PRs.

## Named Patterns

### Good — Intent-tagged ML code review
```
must: fit() is called on the full dataset (line 47), not on X_train.
      This leaks val/test statistics into the scaler. See team Pipeline convention.
should: log the data_version param to MLflow before fit(), not after.
        Ensures params are captured even if training fails.
nit: variable name `df2` — consider `df_val` for clarity.
question: why is the temporal split boundary 2024-07-01?
          Is this documented in the problem statement?
praise: the calibration plot artifact is exactly what we need for the model card.
```
The author knows what requires action and what is taste.

### Bad — Unmarked mixed feedback
```
"This needs to be fixed."
"I would have done this differently."
"The naming here is confusing."
"The AUC seems low."
```
The author cannot distinguish blockers from preferences. High-severity issues get deprioritized.

### Good — Leakage checklist for notebook reviews
```
□ No fit() call on full dataset (including val/test)
□ Temporal split: no future data in train window
□ Features derived from post-event data are flagged or excluded
□ Label is not present as a feature or directly derivable from a feature
□ Transformations are applied through a fitted Pipeline, not refit per split
□ Evaluation metric computed on held-out test set, not val used for tuning
```
Use this checklist explicitly in the PR review comment for notebook promotions.

### Good — ML ADR for recurring decision
```markdown
# ADR-ML-003: Feature transformations must use fitted Pipelines

Status: Accepted (2026-04-10)

Context:
Three recent PRs applied StandardScaler.fit_transform() on the full dataset before splitting,
introducing data leakage into training. The pattern appeared because ad-hoc scripting from notebooks
was copied directly into scripts.

Decision:
All feature transformations are wrapped in sklearn.pipeline.Pipeline.
fit() is called only on X_train. The same fitted object is used for transform() on val, test, and serving.
Notebook code is treated as a draft; Pipeline code is the source of truth.

Consequences:
One-time refactor of two existing training scripts (issue #234).
All new training scripts: PR checklist item added.
Leakage from scaler refitting is eliminated for all models using this convention.
```

### Bad — Tribal knowledge on leakage prevention
"Everyone knows you don't fit on the full dataset." A new hire's first PR does exactly that; three reviewers catch it in comments without writing down the rule. Next quarter: same issue from a different hire.

### Good — Mentoring through questions on an ML PR
"What happens if the val set has a category not seen in train — how does OrdinalEncoder behave?"
"If you remove this feature, how would you know if model quality dropped?"
"Where would you write the test that catches the leakage you fixed in this PR?"
The author thinks and answers; the answer is the lesson.

### Bad — Mentoring by dictation
"Just use Pipeline like this." Author copies the snippet; doesn't understand why; repeats the mistake with a different transformation two weeks later.

## Boundaries

- Owns ML code review for correctness, shape, and readability; ADRs scoped to the ML domain; mentoring on ML engineering standards.
- Does not own org-wide engineering standards beyond ML → `tech-lead`.
- Does not own performance management of the author → role manager.
- Does not own the substance of feature design decisions surfaced in review → `feature-engineering-and-validation`.
- Does not own API contract decisions surfaced in review → `model-serving-and-inference`.

## Sources

### Priority 1 — Review practice
- Google Engineering Practices: Code Review — https://google.github.io/eng-practices/review/
- ML Test Score (Breck et al., 2017) — https://research.google/pubs/pub46555/

### Priority 2 — ADR and team practice
- Michael Nygard: Documenting Architecture Decisions — https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- ADR GitHub organization — https://adr.github.io/
- Google Rules of ML — https://developers.google.com/machine-learning/guides/rules-of-ml

### Priority 3 — Mentoring background
- Camille Fournier: The Manager's Path — book reference
- Made With ML: Best Practices — https://madewithml.com/

## Handoff

- Org-wide engineering direction and cross-team standards → `tech-lead`.
- Architectural decisions across ML and backend services → `system-architect`.
- Career/performance management → role manager.
- Substance of feature design issue found in review → `feature-engineering-and-validation`.
- Substance of API/serving issue found in review → `model-serving-and-inference`.
