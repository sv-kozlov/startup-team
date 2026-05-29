#!/usr/bin/env python3
"""Regression tests for the PRD skill scripts."""

from __future__ import annotations

import csv
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def run(script: str, *args: object) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, str(SCRIPTS / script), *map(str, args)],
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )


def assert_ok(result: subprocess.CompletedProcess[str]) -> None:
    assert result.returncode == 0, result.stdout + result.stderr


def write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def main() -> int:
    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    for match in re.finditer(r"(references|scripts|tests)/[A-Za-z0-9_.-]+\.(?:md|py)", skill_text):
        referenced = ROOT / match.group(0)
        assert referenced.exists(), f"Missing referenced file: {match.group(0)}"

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        old = write(
            tmp / "old-prd.md",
            """# PRD: Smart Search

## Executive Summary
Smart search finds cited answers.

## Goals and Non-Goals
- Reduce support escalations by 20%.
- Non-goal: voice search.

## Scope
### MVP / P0
- Search documentation.

## User Stories and Acceptance Criteria
### Story: Search docs
As a support specialist, I want to ask a question, So that I can answer customers.
Acceptance Criteria:
- Given indexed docs, when I ask a question, then I receive a cited answer.

## Success Metrics
**Metric:** Citation accuracy
**Target:** 90%

## Risks and Mitigations
- Incorrect answer: human feedback loop.

## Open Questions
- Which repositories are indexed?
""",
        )
        new = write(old.with_name("new-prd.md"), old.read_text(encoding="utf-8").replace("90%", "95%") + "\n## Functional Requirements\n- The system must return source citations.\n")
        with_ids = tmp / "with-ids.md"

        result = run("assign-prd-ids.py", new, "--output", with_ids)
        assert_ok(result)
        ids_text = with_ids.read_text(encoding="utf-8")
        assert "STORY-001" in ids_text
        assert "AC-001-01" in ids_text
        assert "METRIC-001" in ids_text
        assert "RISK-001" in ids_text

        second = tmp / "with-ids-second.md"
        assert_ok(run("assign-prd-ids.py", with_ids, "--output", second))
        assert with_ids.read_text(encoding="utf-8") == second.read_text(encoding="utf-8")

        context = run("prd-context-pack.py", with_ids, "--max-items", "5")
        assert_ok(context)
        assert context.stdout.count("Search documentation.") == 1, context.stdout
        assert len(context.stdout.split()) < 450

        section = run("extract-prd-section.py", with_ids, "--section", "metrics")
        assert_ok(section)
        assert "Citation accuracy" in section.stdout

        trace_file = tmp / "trace.csv"
        assert_ok(run("build-traceability-matrix.py", with_ids, "--format", "csv", "--output", trace_file))
        trace_rows = list(csv.DictReader(trace_file.open(encoding="utf-8")))
        assert trace_rows and trace_rows[0]["story_id"] == "STORY-001"
        assert "AC-001-01" in trace_rows[0]["acceptance_criteria_ids"]

        backlog_file = tmp / "backlog.csv"
        assert_ok(run("prd-to-backlog.py", with_ids, "--output", backlog_file))
        backlog_rows = list(csv.DictReader(backlog_file.open(encoding="utf-8")))
        assert backlog_rows and backlog_rows[0]["story_id"] == "STORY-001"

        diff = run("compare-prd-versions.py", old, new, "--context", "1")
        assert_ok(diff)
        assert "## Changed section: metrics" in diff.stdout
        assert "## Changed section: functional" in diff.stdout
        assert "prd-smart-search" not in diff.stdout
        assert "Changed sections: 2" in diff.stdout

        id_diff = run("compare-prd-versions.py", new, with_ids, "--context", "1")
        assert_ok(id_diff)
        assert "story-search-docs" not in id_diff.stdout

        ru = write(
            tmp / "ru-prd.md",
            """# PRD: Тест

## Резюме
Кратко.

## Проблема
Пользователи не видят статус.

## Цели и задачи
- Снизить обращения на 20%.

## Пользователи
Операторы поддержки.

## Объем
- MVP: показать статус.

## Пользовательские истории
Как оператор, я хочу видеть статус заявки, чтобы быстрее отвечать клиенту.

Критерии приемки:
- Дано открытая заявка, когда я смотрю карточку, тогда вижу статус.

## Функциональные требования
- Система показывает статус.

## Метрики
- Целевое значение: минус 20% обращений.

## Риски
- Риск неверного статуса.

## Открытые вопросы
- Кто владелец статуса?
""",
        )
        assert_ok(run("validate-prd.py", ru, "--lang", "ru"))
        assert_ok(run("score-prd.py", ru, "--lang", "ru"))
        questions = run("extract-open-questions.py", ru)
        assert_ok(questions)
        assert "Кто владелец статуса?" in questions.stdout

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
