#!/usr/bin/env python3
"""Export PRD user stories to a backlog CSV."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from prd_utils import extract_stories, read_text, write_csv


def main() -> int:
    parser = argparse.ArgumentParser(description="Export PRD stories to backlog CSV")
    parser.add_argument("prd_file")
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()

    path = Path(args.prd_file)
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2

    rows = []
    for story in extract_stories(read_text(path)):
        rows.append(
            {
                "story_id": story.story_id,
                "title": story.title,
                "story": story.story,
                "priority": story.priority,
                "acceptance_criteria": "\n".join(body for _, body in story.acceptance_criteria),
                "acceptance_criteria_ids": "; ".join(ac_id for ac_id, _ in story.acceptance_criteria if ac_id),
            }
        )

    write_csv(args.output, ["story_id", "title", "story", "priority", "acceptance_criteria_ids", "acceptance_criteria"], rows)
    print(f"Wrote {args.output} ({len(rows)} stories)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

