#!/usr/bin/env python3
"""Score PRD readiness on a 100-point scale."""

from __future__ import annotations

import sys
from pathlib import Path

from prd_utils import (
    AC_PATTERNS,
    METRIC_PATTERNS,
    STORY_PATTERNS,
    build_parser,
    count_any,
    has_section,
    language_check,
    read_text,
)


def score(text: str, lang: str) -> tuple[int, list[tuple[str, int, int, str]]]:
    rows: list[tuple[str, int, int, str]] = []

    def add(name: str, points: int, earned: int, detail: str) -> None:
        rows.append((name, points, min(points, earned), detail))

    business = 0
    business += 8 if has_section(text, "problem") else 0
    business += 7 if has_section(text, "goals") else 0
    business += 5 if has_section(text, "executive_summary") else 0
    business += 5 if any(word in text.lower() for word in ["why now", "почему сейчас", "impact", "влияние"]) else 0
    add("Business value and goals", 25, business, "problem, goals, impact, why now")

    functional = 0
    functional += 7 if has_section(text, "functional") else 0
    functional += 8 if count_any(text, STORY_PATTERNS) > 0 else 0
    functional += 7 if count_any(text, AC_PATTERNS) > 0 else 0
    functional += 3 if any(word in text.lower() for word in ["edge", "error", "empty", "ошиб", "пуст"]) else 0
    add("Functional scope", 25, functional, "requirements, stories, acceptance criteria, edge cases")

    ux = 0
    ux += 8 if has_section(text, "users") else 0
    ux += 4 if any(word in text.lower() for word in ["journey", "flow", "screen", "сценар", "экран", "путь"]) else 0
    ux += 3 if any(word in text.lower() for word in ["accessibility", "wcag", "доступност"]) else 0
    add("Users and UX", 15, ux, "personas, flows, accessibility")

    metrics = 0
    metric_hits = count_any(text, METRIC_PATTERNS)
    metrics += 7 if has_section(text, "metrics") else 0
    metrics += 4 if metric_hits >= 2 else 0
    metrics += 2 if any(word in text.lower() for word in ["baseline", "базов"]) else 0
    metrics += 2 if any(word in text.lower() for word in ["target", "целев"]) else 0
    add("Metrics and validation", 15, metrics, "KPIs, baseline, target, measurement method")

    technical = 0
    technical += 5 if has_section(text, "non_functional") else 0
    technical += 4 if has_section(text, "dependencies") else 0
    technical += 3 if any(word in text.lower() for word in ["security", "privacy", "compliance", "безопас", "персональн"]) else 0
    technical += 3 if any(word in text.lower() for word in ["api", "integration", "интеграц", "данн"]) else 0
    add("Technical and delivery constraints", 15, technical, "NFR, dependencies, security, integrations")

    risks = 0
    risks += 3 if has_section(text, "risks") else 0
    risks += 1 if has_section(text, "open_questions") else 0
    risks += 1 if any(word in text.lower() for word in ["non-goal", "out of scope", "нецель", "вне"]) else 0
    add("Risks and boundaries", 5, risks, "risks, open questions, non-goals")

    lang_check = language_check(text, lang)
    if not lang_check.passed:
        add("Language match", 0, 0, lang_check.detail)

    total = sum(row[2] for row in rows)
    return total, rows


def main() -> int:
    parser = build_parser("Score PRD readiness")
    args = parser.parse_args()
    path = Path(args.prd_file)
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2

    total, rows = score(read_text(path), args.lang)
    print(f"Readiness score: {total}/100")
    print("")
    for name, points, earned, detail in rows:
        print(f"- {name}: {earned}/{points} ({detail})")

    if total < 60:
        print("\nVerdict: weak draft; continue discovery before PRD handoff.")
    elif total < 80:
        print("\nVerdict: usable draft with important gaps.")
    else:
        print("\nVerdict: ready for review; resolve warnings and open questions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

