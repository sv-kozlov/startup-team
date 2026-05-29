#!/usr/bin/env python3
"""Build a lightweight PRD traceability matrix."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from prd_utils import extract_metrics, extract_risks, extract_stories, first_nonempty_line, read_text, section_text, write_csv


def rows_for(text: str) -> list[dict[str, str]]:
    goals = "; ".join(line.strip("-* ") for line in section_text(text, "goals").splitlines() if line.strip().startswith(("-", "*")))
    if not goals:
        goals = first_nonempty_line(section_text(text, "goals"))
    metrics = "; ".join(f"{mid}: {body}" if mid else body for mid, body in extract_metrics(text))
    risks = "; ".join(f"{rid}: {body}" if rid else body for rid, body in extract_risks(text))
    rows = []
    for story in extract_stories(text):
        rows.append(
            {
                "goal": goals,
                "story_id": story.story_id,
                "story_title": story.title,
                "story": story.story,
                "acceptance_criteria_ids": "; ".join(ac_id for ac_id, _ in story.acceptance_criteria if ac_id),
                "acceptance_criteria": " | ".join(body for _, body in story.acceptance_criteria),
                "metrics": metrics,
                "risks": risks,
                "priority": story.priority,
            }
        )
    if not rows:
        rows.append(
            {
                "goal": goals,
                "story_id": "",
                "story_title": "",
                "story": "",
                "acceptance_criteria_ids": "",
                "acceptance_criteria": "",
                "metrics": metrics,
                "risks": risks,
                "priority": "",
            }
        )
    return rows


def print_markdown(rows: list[dict[str, str]]) -> None:
    fields = ["story_id", "story_title", "story", "acceptance_criteria_ids", "metrics", "risks"]
    print("| " + " | ".join(fields) + " |")
    print("| " + " | ".join("---" for _ in fields) + " |")
    for row in rows:
        values = [row[field].replace("|", "\\|").replace("\n", " ") for field in fields]
        print("| " + " | ".join(values) + " |")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build PRD traceability matrix")
    parser.add_argument("prd_file")
    parser.add_argument("--format", choices=["markdown", "csv"], default="markdown")
    parser.add_argument("--output", "-o")
    args = parser.parse_args()

    path = Path(args.prd_file)
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2
    rows = rows_for(read_text(path))
    if args.format == "csv":
        if not args.output:
            print("ERROR: --output is required for csv", file=sys.stderr)
            return 2
        fields = list(rows[0].keys())
        write_csv(args.output, fields, rows)
        print(f"Wrote {args.output}")
    else:
        print_markdown(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

