#!/usr/bin/env python3
"""Extract open questions, TBDs, TODOs, and unresolved assumptions from a PRD."""

from __future__ import annotations

import sys
from pathlib import Path

from prd_utils import build_parser, extract_open_items, read_text


def main() -> int:
    parser = build_parser("Extract open questions and unresolved PRD items")
    args = parser.parse_args()
    path = Path(args.prd_file)
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2

    items = extract_open_items(read_text(path))
    print(f"Open items: {len(items)}")
    for line_no, item in items:
        print(f"- line {line_no}: {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
