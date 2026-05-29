#!/usr/bin/env python3
"""Validate a PRD markdown document for broad completeness and quality."""

from __future__ import annotations

import sys
import re
from pathlib import Path

from prd_utils import (
    AC_PATTERNS,
    METRIC_PATTERNS,
    PLACEHOLDER_PATTERNS,
    STORY_PATTERNS,
    VAGUE_WORDS,
    Check,
    build_parser,
    count_any,
    has_any,
    has_section,
    language_check,
    normalize,
    read_text,
    word_count,
)


REQUIRED_SECTIONS = [
    ("executive_summary", "Executive summary / резюме"),
    ("problem", "Problem statement / проблема"),
    ("goals", "Goals and non-goals / цели и нецели"),
    ("users", "Users or personas / пользователи"),
    ("scope", "Scope / объем"),
    ("stories", "User stories / пользовательские истории"),
    ("functional", "Functional requirements / функциональные требования"),
    ("metrics", "Success metrics / метрики"),
    ("risks", "Risks / риски"),
    ("open_questions", "Open questions / открытые вопросы"),
]

RECOMMENDED_SECTIONS = [
    ("non_functional", "Non-functional requirements / НФТ"),
    ("dependencies", "Dependencies and assumptions / зависимости"),
]


def validate(text: str, lang: str) -> list[Check]:
    checks: list[Check] = [language_check(text, lang)]

    for key, label in REQUIRED_SECTIONS:
        checks.append(Check(label, has_section(text, key), "required section", critical=True))

    for key, label in RECOMMENDED_SECTIONS:
        checks.append(Check(label, has_section(text, key), "recommended section", critical=False))

    stories = count_any(text, STORY_PATTERNS)
    checks.append(Check("User story format", stories > 0, f"found: {stories}", critical=True))

    ac = count_any(text, AC_PATTERNS)
    checks.append(Check("Acceptance criteria", ac > 0, f"found signals: {ac}", critical=True))

    metric_hits = count_any(text, METRIC_PATTERNS)
    checks.append(Check("Measurable metrics", metric_hits >= 2, f"found signals: {metric_hits}", critical=True))

    placeholders = count_any(text, PLACEHOLDER_PATTERNS)
    checks.append(Check("No placeholders/TBD", placeholders == 0, f"found: {placeholders}", critical=False))

    normalized = normalize(text)
    vague = [
        w
        for w in VAGUE_WORDS
        if re.search(rf"(?<![\wА-Яа-яЁё-]){re.escape(w)}(?![\wА-Яа-яЁё-])", normalized)
    ]
    checks.append(
        Check(
            "Vague wording bounded",
            len(vague) == 0,
            "found: " + ", ".join(sorted(set(vague))) if vague else "",
            critical=False,
        )
    )

    wc = word_count(text)
    checks.append(Check("Document length", wc >= 400, f"words: {wc}", critical=False))
    return checks


def main() -> int:
    parser = build_parser("Validate a PRD markdown document")
    parser.add_argument("--strict", action="store_true", help="Return non-zero for warnings too")
    args = parser.parse_args()

    path = Path(args.prd_file)
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2

    checks = validate(read_text(path), args.lang)
    critical = [c for c in checks if not c.passed and c.critical]
    warnings = [c for c in checks if not c.passed and not c.critical]

    print(f"PRD validation: {path}")
    print(f"Critical issues: {len(critical)}")
    print(f"Warnings: {len(warnings)}")
    print("")

    for check in checks:
        status = "PASS" if check.passed else ("FAIL" if check.critical else "WARN")
        detail = f" - {check.detail}" if check.detail else ""
        print(f"[{status}] {check.name}{detail}")

    if critical:
        return 1
    if warnings and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
