#!/usr/bin/env python3
"""Shared helpers for PRD scripts."""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path


RU = "ru"
EN = "en"
BOTH = "both"
AUTO = "auto"


@dataclass
class Check:
    name: str
    passed: bool
    detail: str = ""
    critical: bool = False


@dataclass
class Section:
    title: str
    level: int
    start_line: int
    end_line: int
    body: str


@dataclass
class Story:
    story_id: str
    title: str
    story: str
    priority: str
    acceptance_criteria: list[tuple[str, str]]


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def strip_markdown_noise(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)
    return text


def word_count(text: str) -> int:
    return len(re.findall(r"[\wА-Яа-яЁё-]+", strip_markdown_noise(text), flags=re.U))


def headings(text: str) -> list[str]:
    return [m.group(2).strip() for m in re.finditer(r"^(#{1,6})\s+(.+)$", text, flags=re.M)]


def iter_sections(text: str) -> list[Section]:
    lines = text.splitlines()
    matches = []
    for index, line in enumerate(lines):
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if match:
            matches.append((index, len(match.group(1)), match.group(2).strip()))

    sections: list[Section] = []
    for idx, (start, level, title) in enumerate(matches):
        end = len(lines)
        for next_start, next_level, _ in matches[idx + 1 :]:
            if next_level <= level:
                end = next_start
                break
        body = "\n".join(lines[start + 1 : end]).strip()
        sections.append(Section(title=title, level=level, start_line=start + 1, end_line=end, body=body))
    return sections


def section_key(title: str) -> str:
    clean = re.sub(r"^[A-Z]+-\d+(?:-\d+)?\s*[:.-]?\s*", "", title.strip(), flags=re.I)
    for key, patterns in SECTION_PATTERNS.items():
        if has_any("## " + clean, patterns):
            return key
    lowered = clean.lower()
    if any(word in lowered for word in ["mvp", "scope", "объем", "рамки"]):
        return "scope"
    return re.sub(r"[^a-zа-я0-9]+", "-", lowered, flags=re.I).strip("-") or "section"


def find_sections(text: str, key: str) -> list[Section]:
    return [section for section in iter_sections(text) if section_key(section.title) == key]


def section_text(text: str, key: str) -> str:
    sections = iter_sections(text)
    matched = [section for section in sections if section_key(section.title) == key]
    unique: list[str] = []
    seen: set[str] = set()
    for section in matched:
        body_lines = []
        for line in section.body.splitlines():
            heading = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
            if heading and len(heading.group(1)) > section.level:
                continue
            body_lines.append(line)
        body = "\n".join(body_lines).strip()
        if body and body not in seen:
            seen.add(body)
            unique.append(body)
    return "\n\n".join(unique).strip()


def has_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, flags=re.I | re.M | re.U) for pattern in patterns)


def count_any(text: str, patterns: list[str]) -> int:
    return sum(len(re.findall(pattern, text, flags=re.I | re.M | re.U)) for pattern in patterns)


def slug(text: str) -> str:
    value = re.sub(r"[^A-Za-zА-Яа-яЁё0-9]+", "-", text.lower(), flags=re.U).strip("-")
    return value[:80] or "item"


def first_nonempty_line(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip(" -*#")
        if stripped:
            return stripped
    return ""


def bullet_items(text: str) -> list[str]:
    return [m.group(1).strip() for m in re.finditer(r"^\s*[-*]\s+(?:\[[ xX]\]\s*)?(.+?)\s*$", text, flags=re.M)]


def numbered_or_bullet_items(text: str) -> list[str]:
    return [
        m.group(1).strip()
        for m in re.finditer(r"^\s*(?:[-*]|\d+[.)])\s+(?:\[[ xX]\]\s*)?(.+?)\s*$", text, flags=re.M)
    ]


def detect_language(text: str) -> str:
    latin = len(re.findall(r"[A-Za-z]", text))
    cyrillic = len(re.findall(r"[А-Яа-яЁё]", text))
    if latin and cyrillic and min(latin, cyrillic) / max(latin, cyrillic) > 0.12:
        return BOTH
    if cyrillic > latin:
        return RU
    return EN


def language_check(text: str, expected: str) -> Check:
    if expected == AUTO:
        return Check("Language", True, f"detected: {detect_language(text)}")
    detected = detect_language(text)
    if expected == BOTH:
        passed = detected == BOTH
        detail = "contains meaningful Russian and English text" if passed else f"detected: {detected}"
        return Check("Language: both", passed, detail, critical=True)
    passed = detected in {expected, BOTH}
    return Check(f"Language: {expected}", passed, f"detected: {detected}", critical=True)


SECTION_PATTERNS = {
    "executive_summary": [
        r"^##+\s+(executive summary|резюме|краткое резюме|краткое описание)\b",
    ],
    "problem": [
        r"^##+\s+(problem statement|problem|проблема|постановка проблемы)\b",
    ],
    "goals": [
        r"^##+\s+(goals|goals and objectives|цели|цели и задачи)\b",
    ],
    "users": [
        r"^##+\s+(users|user personas|personas|пользователи|персоны|целевые пользователи)\b",
    ],
    "scope": [
        r"^##+\s+(scope|mvp|объем|рамки|границы|состав работ)\b",
    ],
    "stories": [
        r"^##+\s+(user stories|user stories and acceptance criteria|stories|пользовательские истории|сценарии|истории пользователей)\b",
    ],
    "functional": [
        r"^##+\s+(functional requirements|requirements|функциональные требования|требования)\b",
    ],
    "non_functional": [
        r"^##+\s+(non-functional requirements|nfr|нефункциональные требования)\b",
    ],
    "metrics": [
        r"^##+\s+(success metrics|metrics|kpi|метрики|критерии успеха)\b",
    ],
    "risks": [
        r"^##+\s+(risks|risks and mitigations|risk assessment|риски|риски и митигации)\b",
    ],
    "dependencies": [
        r"^##+\s+(dependencies|dependencies and assumptions|зависимости|допущения)\b",
    ],
    "open_questions": [
        r"^##+\s+(open questions|questions|открытые вопросы|вопросы)\b",
    ],
}


def has_section(text: str, key: str) -> bool:
    return has_any(text, SECTION_PATTERNS[key])


def next_id(existing: set[str], prefix: str, counter: int) -> tuple[str, int]:
    while True:
        value = f"{prefix}-{counter:03d}"
        counter += 1
        if value not in existing:
            return value, counter


def extract_id(text: str, prefix: str) -> str:
    match = re.search(rf"\b({re.escape(prefix)}-\d{{3}}(?:-\d{{2}})?)\b", text, flags=re.I)
    return match.group(1).upper() if match else ""


def extract_stories(text: str) -> list[Story]:
    lines = text.splitlines()
    stories: list[Story] = []
    current: dict[str, object] | None = None
    current_ac: list[tuple[str, str]] = []
    in_ac = False

    def flush() -> None:
        nonlocal current, current_ac, in_ac
        if not current:
            return
        story_text = str(current.get("story", "")).strip()
        title = str(current.get("title", "")).strip() or story_text[:80]
        story_id = extract_id(title + " " + story_text, "STORY") or str(current.get("story_id", ""))
        if story_text or story_id:
            stories.append(
                Story(
                    story_id=story_id,
                    title=re.sub(r"^STORY-\d{3}\s*[:.-]?\s*", "", title, flags=re.I),
                    story=story_text,
                    priority=str(current.get("priority", "")),
                    acceptance_criteria=current_ac[:],
                )
            )
        current = None
        current_ac = []
        in_ac = False

    for line in lines:
        stripped = line.strip()
        heading = re.match(r"^#{2,6}\s+(.+)$", stripped)
        story_heading = bool(heading and re.search(r"\b(story|истори|сценар|STORY-\d{3})\b", heading.group(1), re.I))
        story_inline = has_any(stripped, STORY_PATTERNS)
        if current is not None and story_inline and not current.get("story"):
            current["story"] = stripped
            continue
        if story_heading or story_inline:
            flush()
            current = {
                "title": heading.group(1).strip() if heading else stripped[:80],
                "story": stripped if story_inline else "",
                "story_id": extract_id(stripped, "STORY"),
                "priority": "",
            }
            continue

        if current is None:
            continue

        if not current.get("story") and story_inline:
            current["story"] = stripped
            continue
        if re.search(r"\bpriority\b|приоритет", stripped, re.I):
            current["priority"] = stripped.split(":", 1)[-1].strip() if ":" in stripped else stripped
            continue
        if re.search(r"acceptance criteria|критерии при[её]мки", stripped, re.I):
            in_ac = True
            continue
        if in_ac:
            item = re.match(r"^\s*[-*]\s+(?:\[[ xX]\]\s*)?(.+)$", line)
            if item:
                body = item.group(1).strip()
                ac_id = extract_id(body, "AC")
                current_ac.append((ac_id, body))
            elif stripped and re.match(r"^#{1,6}\s+", stripped):
                in_ac = False

    flush()
    return stories


def extract_metrics(text: str) -> list[tuple[str, str]]:
    metrics_text = section_text(text, "metrics")
    items = numbered_or_bullet_items(metrics_text)
    rows = []
    for item in items:
        if has_any(item, METRIC_PATTERNS):
            rows.append((extract_id(item, "METRIC"), re.sub(r"^METRIC-\d{3}\s*[:.-]?\s*", "", item, flags=re.I)))
    if not rows and metrics_text:
        for line in metrics_text.splitlines():
            if has_any(line, METRIC_PATTERNS):
                rows.append((extract_id(line, "METRIC"), re.sub(r"^METRIC-\d{3}\s*[:.-]?\s*", "", line.strip(), flags=re.I)))
    return rows


def extract_risks(text: str) -> list[tuple[str, str]]:
    risk_text = section_text(text, "risks")
    items = numbered_or_bullet_items(risk_text)
    rows = [
        (extract_id(item, "RISK"), re.sub(r"^RISK-\d{3}\s*[:.-]?\s*", "", item, flags=re.I))
        for item in items
        if item and not item.startswith("|")
    ]
    if not rows and risk_text:
        for line in risk_text.splitlines():
            stripped = line.strip()
            if stripped.startswith("|") and not re.search(r"---|risk|риск", stripped, re.I):
                rows.append((extract_id(stripped, "RISK"), stripped.strip("| ")))
    return rows


def extract_open_items(text: str) -> list[tuple[int, str]]:
    results: list[tuple[int, str]] = []
    in_open_section = False
    current_heading_level = 0

    for line_no, line in enumerate(text.splitlines(), start=1):
        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            title = heading.group(2).strip().lower()
            level = len(heading.group(1))
            if re.search(r"(open questions|questions|открытые вопросы|вопросы)", title):
                in_open_section = True
                current_heading_level = level
                continue
            if in_open_section and level <= current_heading_level:
                in_open_section = False

        stripped = line.strip()
        if not stripped:
            continue

        if in_open_section and re.match(r"^[-*]\s+", stripped):
            results.append((line_no, re.sub(r"^[-*]\s+\[?\s*\]?\s*", "", stripped)))
            continue

        for pattern in OPEN_QUESTION_PATTERNS:
            match = re.search(pattern, line, flags=re.I | re.U)
            if match:
                results.append((line_no, match.group(1).strip()))
                break

    deduped: list[tuple[int, str]] = []
    seen: set[str] = set()
    for line_no, item in results:
        key = item.lower()
        if key not in seen:
            seen.add(key)
            deduped.append((line_no, item))
    return deduped


def write_csv(path: str | Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


STORY_PATTERNS = [
    r"\bas\s+an?\s+.+?i\s+want\s+.+?so\s+that\b",
    r"\bwhen\s+.+?i\s+want\s+.+?so\s+i\s+can\b",
    r"\bкак\s+.+?\s+я\s+хочу\s+.+?\s+чтобы\b",
    r"\bкогда\s+.+?\s+я\s+хочу\s+.+?\s+чтобы\b",
]

AC_PATTERNS = [
    r"\bgiven\s+.+?\bwhen\s+.+?\bthen\b",
    r"\bдано\s+.+?\bкогда\s+.+?\bтогда\b",
    r"acceptance criteria",
    r"критерии приемки",
    r"критерии приёмки",
]

METRIC_PATTERNS = [
    r"\b(kpi|metric|baseline|target|measurement|north star|okr)\b",
    r"\b(метрик|kpi|базов|целев|измер|цель|результат)\w*",
    r"\d+\s*(%|percent|процент|сек|ms|мс|мин|day|дн|hour|час)",
]

PLACEHOLDER_PATTERNS = [
    r"\[(?!\s?[xX]\s?\])\s*(?:tbd|todo|add|insert|name|date|metric|placeholder|описать|добавить|указать|заполнить|.+?1.+?)\s*\]",
    r"<[^>\n]{2,80}>",
    r"\b(TBD|TODO|FIXME)\b",
]

OPEN_QUESTION_PATTERNS = [
    r"^\s*[-*]\s+\[?\s*\]?\s*(.+\?)\s*$",
    r"^\s*[-*]\s+\[?\s*\]?\s*((?:TBD|TODO|FIXME)\b.*)$",
    r"^\s*[-*]\s+\[?\s*\]?\s*((?:Нужно уточнить|Уточнить|Вопрос|Открытый вопрос)\b.*)$",
]

VAGUE_WORDS = [
    "fast",
    "easy",
    "simple",
    "intuitive",
    "modern",
    "user-friendly",
    "quick",
    "быстро",
    "удобно",
    "просто",
    "интуитивно",
    "современно",
    "качественно",
    "эффективно",
]


def build_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("prd_file", help="Path to PRD markdown file")
    parser.add_argument(
        "--lang",
        choices=[AUTO, RU, EN, BOTH],
        default=AUTO,
        help="Expected PRD language. Default: auto",
    )
    return parser
