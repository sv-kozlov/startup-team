#!/usr/bin/env python3
"""Create a compact PRD context pack for future agent turns."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from prd_utils import (
    bullet_items,
    extract_metrics,
    extract_open_items,
    extract_risks,
    extract_stories,
    first_nonempty_line,
    read_text,
    section_text,
)


def clip(value: str, limit: int = 180) -> str:
    value = " ".join(value.split())
    return value if len(value) <= limit else value[: limit - 3].rstrip() + "..."


def top_items(text: str, limit: int) -> list[str]:
    items = bullet_items(text)
    if not items and text.strip():
        items = [first_nonempty_line(text)]
    return [clip(item) for item in items[:limit] if item]


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a compact PRD context pack")
    parser.add_argument("prd_file")
    parser.add_argument("--max-items", type=int, default=5)
    args = parser.parse_args()

    path = Path(args.prd_file)
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2
    text = read_text(path)
    stories = extract_stories(text)[: args.max_items]
    metrics = extract_metrics(text)[: args.max_items]
    risks = extract_risks(text)[: args.max_items]
    questions = extract_open_items(text)[: args.max_items]

    print(f"# Context Pack: {path.name}")
    print("")
    print("## Problem")
    print(clip(first_nonempty_line(section_text(text, "problem") or section_text(text, "executive_summary"))))
    print("")
    print("## Scope")
    for item in top_items(section_text(text, "scope"), args.max_items):
        print(f"- {item}")
    print("")
    print("## Stories")
    for story in stories:
        prefix = f"{story.story_id}: " if story.story_id else ""
        print(f"- {prefix}{clip(story.story)}")
    print("")
    print("## Metrics")
    for metric_id, metric in metrics:
        prefix = f"{metric_id}: " if metric_id else ""
        print(f"- {prefix}{clip(metric)}")
    print("")
    print("## Risks")
    for risk_id, risk in risks:
        prefix = f"{risk_id}: " if risk_id else ""
        print(f"- {prefix}{clip(risk)}")
    print("")
    print("## Open Questions")
    for _, item in questions:
        print(f"- {clip(item)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
