#!/usr/bin/env python3
"""Compare two PRD markdown versions by logical sections."""

from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path

from prd_utils import iter_sections, read_text, section_key


def section_map(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for section in iter_sections(text):
        if section.level != 2:
            continue
        key = section_key(section.title)
        current = result.get(key, "")
        result[key] = (current + "\n\n" + f"## {section.title}\n{section.body}").strip()
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare two PRD versions")
    parser.add_argument("old_prd")
    parser.add_argument("new_prd")
    parser.add_argument("--context", type=int, default=2)
    args = parser.parse_args()

    old_path = Path(args.old_prd)
    new_path = Path(args.new_prd)
    if not old_path.exists() or not new_path.exists():
        print("ERROR: both PRD files must exist", file=sys.stderr)
        return 2

    old = section_map(read_text(old_path))
    new = section_map(read_text(new_path))
    keys = sorted(set(old) | set(new))
    changed = 0
    for key in keys:
        if old.get(key, "") == new.get(key, ""):
            continue
        changed += 1
        print(f"## Changed section: {key}")
        if key not in old:
            print("[added]")
            print(new[key])
        elif key not in new:
            print("[removed]")
            print(old[key])
        else:
            diff = difflib.unified_diff(
                old[key].splitlines(),
                new[key].splitlines(),
                fromfile=f"old:{key}",
                tofile=f"new:{key}",
                lineterm="",
                n=args.context,
            )
            print("\n".join(diff))
        print("")
    print(f"Changed sections: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
