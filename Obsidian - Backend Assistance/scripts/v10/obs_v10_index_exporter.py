#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Export OBS V10 lightweight JSON indexes for frontend / Bridge / Open Design.

The exporter turns V10 read-only backend ledgers into explicit JSON files:

- obs-v10-course-transform-index.json
- obs-v10-source-manifest-index.json
- obs-v10-task-ledger-index.json

Default prints JSON to stdout and writes nothing.  `--output-dir` writes only the
named JSON files into the explicit directory.  No vault notes/media are modified.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.v10.course_intake_adapter import inventory_sources  # noqa: E402
from scripts.v10.course_transform_ledger import build_course_transform_ledger, generate_tasks  # noqa: E402
from scripts.v10.obs_task_ledger import default_db_path, list_tasks  # noqa: E402

INDEX_NAMES = {
    "course": "obs-v10-course-transform-index.json",
    "source": "obs-v10-source-manifest-index.json",
    "task": "obs-v10-task-ledger-index.json",
}
BOUNDARY = {
    "read_only": True,
    "candidate_only": True,
    "no_vault_write": True,
    "no_body_content": True,
    "no_verified_evidence_claim": True,
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def build_indexes(
    vault: Path | None = None,
    source_root: Path | None = None,
    ledger_db: Path | None = None,
    limit: int = 200,
) -> dict[str, Any]:
    generated_at = now_iso()
    indexes: dict[str, Any] = {"boundary": BOUNDARY, "generated_at": generated_at}
    if vault is not None:
        ledger = build_course_transform_ledger(vault, limit=limit)
        courses = [sanitize_course(row) for row in ledger["courses"]]
        indexes[INDEX_NAMES["course"]] = {
            "schema": "obs-v10-course-transform-index/v1",
            "generated_at": generated_at,
            "boundary": BOUNDARY,
            "storage_map": ledger.get("storage_map", {}),
            "required_pages": ledger.get("required_pages", []),
            "summary": ledger.get("summary", {}),
            "courses": courses,
            "items": courses,
        }
        tasks = generate_tasks(ledger, limit=limit)
        indexes[INDEX_NAMES["task"]] = {
            "schema": "obs-v10-task-ledger-index/v1",
            "generated_at": generated_at,
            "boundary": BOUNDARY,
            "source": "course_transform_ledger.generate_tasks",
            "summary": {"task_count": len(tasks)},
            "items": tasks,
        }
    if source_root is not None:
        manifest = inventory_sources(source_root, limit=limit)
        indexes[INDEX_NAMES["source"]] = {
            "schema": "obs-v10-source-manifest-index/v1",
            "generated_at": generated_at,
            "boundary": BOUNDARY,
            "root": manifest.get("root"),
            "summary": {"count": manifest.get("count", 0)},
            "items": [sanitize_source(item) for item in manifest.get("items", [])],
        }
    if ledger_db is not None and ledger_db.exists():
        rows = [sanitize_task(row) for row in list_tasks(ledger_db, limit=limit)]
        indexes[INDEX_NAMES["task"]] = {
            "schema": "obs-v10-task-ledger-index/v1",
            "generated_at": generated_at,
            "boundary": BOUNDARY,
            "source": "obs_task_ledger.list_tasks",
            "summary": summarize_task_rows(rows),
            "items": rows,
        }
    elif ledger_db is None and default_db_path().exists() and INDEX_NAMES["task"] not in indexes:
        rows = [sanitize_task(row) for row in list_tasks(default_db_path(), limit=limit)]
        indexes[INDEX_NAMES["task"]] = {
            "schema": "obs-v10-task-ledger-index/v1",
            "generated_at": generated_at,
            "boundary": BOUNDARY,
            "source": "obs_task_ledger.default_db_path",
            "summary": summarize_task_rows(rows),
            "items": rows,
        }
    return indexes


def sanitize_course(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "course": row.get("course"),
        "course_path": row.get("course_path"),
        "existing_pages": row.get("existing_pages", []),
        "missing_pages": row.get("missing_pages", []),
        "missing_count": len(row.get("missing_pages", [])),
        "has_keyframes": bool(row.get("has_keyframes")),
        "keyframe_count": int(row.get("keyframe_count", 0)),
        "report_count": int(row.get("report_count", 0)),
        "next_action": row.get("next_action"),
        "candidate_only": True,
    }


def sanitize_source(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "path": item.get("path"),
        "relative_path": item.get("relative_path"),
        "name": item.get("name"),
        "format": item.get("format"),
        "size_bytes": item.get("size_bytes"),
        "candidate_only": True,
    }


def sanitize_task(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row.get("id"),
        "title": row.get("title"),
        "course": row.get("course"),
        "status": row.get("status"),
        "priority": row.get("priority"),
        "executor": row.get("executor"),
        "error": row.get("error"),
        "candidate_only": True,
    }


def summarize_task_rows(rows: list[dict[str, Any]]) -> dict[str, int]:
    summary = {"total": len(rows), "pending": 0, "done": 0, "blocked": 0, "failed": 0}
    for row in rows:
        status = row.get("status")
        if status in summary:
            summary[status] += 1
    return summary


def write_indexes(indexes: dict[str, Any], output_dir: Path) -> list[str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for name, payload in indexes.items():
        if not name.endswith(".json"):
            continue
        path = output_dir / name
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        written.append(str(path))
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description="Export OBS V10 lightweight JSON indexes")
    parser.add_argument("--vault", type=Path)
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--ledger-db", type=Path)
    parser.add_argument("--limit", type=int, default=200)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    indexes = build_indexes(vault=args.vault, source_root=args.source_root, ledger_db=args.ledger_db, limit=args.limit)
    if args.output_dir:
        payload: dict[str, Any] = {"written": write_indexes(indexes, args.output_dir), "boundary": BOUNDARY}
    else:
        payload = indexes
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
