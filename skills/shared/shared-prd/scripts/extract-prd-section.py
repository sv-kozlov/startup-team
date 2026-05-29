#!/usr/bin/env python3
"""Extract one logical PRD section to reduce context size."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from prd_utils import find_sections, iter_sections, read_text, section_key


ALIASES = {
    "summary": "executive_summary",
    "problem": "problem",
    "goals": "goals",
    "users": "users",
    "scope": "scope",
    "stories": "stories",
    "requirements": "functional",
    "functional": "functional",
    "nfr": "non_functional",
    "non-functional": "non_functional",
    "metrics": "metrics",
    "risks": "risks",
    "dependencies": "dependencies",
    "open-questions": "open_questions",
    "questions": "open_questions",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract a PRD section")
    parser.add_argument("prd_file")
    parser.add_argument("--section", required=True, help="Section key, e.g. scope, stories, metrics, risks")
    args = parser.parse_args()

    path = Path(args.prd_file)
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2
    text = read_text(path)
    key = ALIASES.get(args.section.lower(), args.section.lower().replace("_", "-"))
    sections = find_sections(text, key)
    if not sections:
        available = ", ".join(f"{section_key(s.title)}:{s.title}" for s in iter_sections(text))
        print(f"ERROR: section not found: {args.section}", file=sys.stderr)
        print(f"Available: {available}", file=sys.stderr)
        return 1
    for idx, section in enumerate(sections):
        if idx:
            print("\n---\n")
        print(f"{'#' * section.level} {section.title}")
        print(section.body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

