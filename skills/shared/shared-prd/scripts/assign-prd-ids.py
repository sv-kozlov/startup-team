#!/usr/bin/env python3
"""Assign stable IDs to common PRD elements without replacing existing IDs."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


PREFIXES = ["REQ", "STORY", "AC", "METRIC", "RISK", "GOAL"]


def collect_existing(text: str) -> set[str]:
    return {m.group(1).upper() for m in re.finditer(r"\b((?:REQ|STORY|AC|METRIC|RISK|GOAL)-\d{3}(?:-\d{2})?)\b", text, re.I)}


def next_id(existing: set[str], prefix: str, counters: dict[str, int]) -> str:
    while True:
        value = f"{prefix}-{counters[prefix]:03d}"
        counters[prefix] += 1
        if value not in existing:
            existing.add(value)
            return value


def assign(text: str) -> str:
    existing = collect_existing(text)
    counters = {prefix: 1 for prefix in PREFIXES}
    out: list[str] = []
    in_ac = False
    in_metrics = False
    in_risks = False
    story_counter = 0
    ac_counter = 1
    active_story_heading = False

    for line in text.splitlines():
        stripped = line.strip()
        lower = stripped.lower()
        new_line = line

        if re.match(r"^#{2,6}\s+", stripped):
            in_ac = False
            in_metrics = bool(re.search(r"\b(metrics|kpi|метрики|критерии успеха)\b", stripped, re.I))
            in_risks = bool(re.search(r"\b(risks?|риски)\b", stripped, re.I))
            if re.search(r"\b(story|истори|сценар)\b", stripped, re.I) and "STORY-" not in stripped.upper():
                story_id = next_id(existing, "STORY", counters)
                story_counter += 1
                ac_counter = 1
                active_story_heading = True
                new_line = re.sub(r"^(#{2,6}\s+)", rf"\1{story_id}: ", line)
            elif re.search(r"\b(story|истори|сценар|STORY-\d{3})\b", stripped, re.I):
                active_story_heading = True
            else:
                active_story_heading = False

        if re.search(r"acceptance criteria|критерии при[её]мки", stripped, re.I):
            in_ac = True

        if not re.match(r"^#{2,6}\s+", stripped):
            if re.search(r"\bas\s+an?\s+.+?\bi\s+want\b.+?\bso\s+that\b", stripped, re.I) or re.search(
                r"\bкак\s+.+?\s+я\s+хочу\b.+?\bчтобы\b", stripped, re.I
            ):
                if "STORY-" not in stripped.upper() and not active_story_heading:
                    story_id = next_id(existing, "STORY", counters)
                    story_counter += 1
                    ac_counter = 1
                    new_line = f"{story_id}: {line}"
            elif in_ac and re.match(r"^\s*[-*]\s+", line) and "AC-" not in stripped.upper():
                if story_counter == 0:
                    story_counter = 1
                ac_id = f"AC-{story_counter:03d}-{ac_counter:02d}"
                while ac_id in existing:
                    ac_counter += 1
                    ac_id = f"AC-{story_counter:03d}-{ac_counter:02d}"
                existing.add(ac_id)
                ac_counter += 1
                new_line = re.sub(r"^(\s*[-*]\s+(?:\[[ xX]\]\s*)?)", rf"\1{ac_id}: ", line)
            elif in_metrics and "METRIC-" not in stripped.upper() and stripped and not stripped.startswith("|"):
                metric_id = next_id(existing, "METRIC", counters)
                if re.match(r"^\s*[-*]\s+", line):
                    new_line = re.sub(r"^(\s*[-*]\s+(?:\[[ xX]\]\s*)?)", rf"\1{metric_id}: ", line)
                else:
                    new_line = f"{metric_id}: {line}"
            elif re.match(r"^\s*[-*]\s+", line) and "METRIC-" not in stripped.upper() and re.search(
                r"\b(metric|kpi|baseline|target|метрик|цель|измер)\w*", lower, re.I
            ):
                new_line = re.sub(r"^(\s*[-*]\s+(?:\[[ xX]\]\s*)?)", rf"\1{next_id(existing, 'METRIC', counters)}: ", line)
            elif in_risks and re.match(r"^\s*[-*]\s+", line) and "RISK-" not in stripped.upper():
                new_line = re.sub(r"^(\s*[-*]\s+(?:\[[ xX]\]\s*)?)", rf"\1{next_id(existing, 'RISK', counters)}: ", line)
            elif re.match(r"^\s*[-*]\s+", line) and "RISK-" not in stripped.upper() and re.search(
                r"\b(risk|риск|угроз)\w*", lower, re.I
            ):
                new_line = re.sub(r"^(\s*[-*]\s+(?:\[[ xX]\]\s*)?)", rf"\1{next_id(existing, 'RISK', counters)}: ", line)

        out.append(new_line)

    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def main() -> int:
    parser = argparse.ArgumentParser(description="Assign stable IDs to PRD elements")
    parser.add_argument("prd_file")
    parser.add_argument("--output", "-o", help="Output file. Defaults to stdout")
    args = parser.parse_args()

    path = Path(args.prd_file)
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2
    result = assign(path.read_text(encoding="utf-8"))
    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        print(result, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
