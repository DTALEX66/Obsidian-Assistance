#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OBS V10 local task ledger.

Adapted from Cognitive-Loop-OS `shared/sleep_loop_engine.py` real-task
ledger ideas, but rewritten as a small standalone helper-repo script:

- SQLite durable task ledger for OBS backend/course-pipeline work.
- Blocks virtual executors such as echo/heartbeat/context-pack previews.
- A task can become `done` only when its result carries verifiable evidence.
- CLI and library functions are local-only; no daemon, no network, no vault writes.

This is intentionally not a copy of the Cognitive-Loop-OS runtime engine.  It is
an OBS-safe minimum baseline for course transformation loops and future sleep
mode orchestration.
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any

TASK_PENDING = "pending"
TASK_DONE = "done"
TASK_BLOCKED = "blocked"
TASK_FAILED = "failed"

REAL_EXECUTORS = {
    "file_read",
    "safe_write",
    "source_scan",
    "vault_audit",
    "report_write",
    "course_transform",
}
NON_REAL_EXECUTORS = {
    "echo",
    "heartbeat",
    "preview",
    "context_pack_build",
    "taskpack_generate",
    "dry_run",
}


def default_db_path() -> Path:
    """Return an external local-state DB path, never inside the helper repo."""
    local = os.environ.get("LOCALAPPDATA")
    if local:
        return Path(local) / "obsidian-assistance" / "obs-task-ledger.sqlite"
    return Path.home() / ".local" / "state" / "obsidian-assistance" / "obs-task-ledger.sqlite"


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def loads(value: str | None, default: Any = None) -> Any:
    if value in (None, ""):
        return default
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return default


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def managed_connection(db_path: Path):
    """Open, commit/rollback, and always close a SQLite connection.

    The bundled mini pytest removes temporary directories immediately after each
    test. On Windows, `with sqlite3.connect(...) as conn` commits but does not
    close the file handle, so explicit close is required.
    """
    conn = connect(db_path)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_schema(db_path: Path) -> None:
    """Create the OBS task ledger schema if it does not already exist."""
    with managed_connection(db_path) as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS obs_task_ledger_tasks (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL DEFAULT '',
                course TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'pending',
                priority INTEGER NOT NULL DEFAULT 100,
                executor TEXT NOT NULL,
                payload_json TEXT NOT NULL DEFAULT '{}',
                result_json TEXT NOT NULL DEFAULT '{}',
                error TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                finished_at TEXT
            );

            CREATE INDEX IF NOT EXISTS idx_obs_task_ledger_status
                ON obs_task_ledger_tasks(status, priority, created_at);

            CREATE TABLE IF NOT EXISTS obs_task_ledger_events (
                id TEXT PRIMARY KEY,
                task_id TEXT NOT NULL DEFAULT '',
                event_type TEXT NOT NULL,
                level TEXT NOT NULL DEFAULT 'info',
                message TEXT NOT NULL,
                payload_json TEXT NOT NULL DEFAULT '{}',
                created_at TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_obs_task_ledger_events_task
                ON obs_task_ledger_events(task_id, created_at);
            """
        )


def validate_real_task(executor: str, payload: dict[str, Any] | None = None) -> tuple[bool, str]:
    """Validate whether a queued task represents real/verifiable work."""
    payload = payload or {}
    executor = str(executor or "").strip()
    if executor in NON_REAL_EXECUTORS:
        return False, f"non_real_executor_blocked:{executor}"
    if executor not in REAL_EXECUTORS:
        return False, f"executor_not_real_task:{executor or '<missing>'}"
    if payload.get("dry_run") is True:
        return False, "dry_run_task_blocked"
    if executor == "file_read" and not str(payload.get("path", "")).strip():
        return False, "file_read_requires_path_evidence"
    if executor == "safe_write":
        if payload.get("dry_run") is not False:
            return False, "safe_write_requires_dry_run_false_for_real_task"
        if not str(payload.get("path", "")).strip():
            return False, "safe_write_requires_path"
    if executor == "source_scan" and not any(str(payload.get(k, "")).strip() for k in ("root", "vault", "path")):
        return False, "source_scan_requires_root_or_vault"
    if executor == "vault_audit" and not str(payload.get("vault", "")).strip():
        return False, "vault_audit_requires_vault"
    if executor == "report_write":
        if payload.get("dry_run") is not False:
            return False, "report_write_requires_dry_run_false_for_real_task"
        if not any(str(payload.get(k, "")).strip() for k in ("path", "report_path")):
            return False, "report_write_requires_report_path"
    if executor == "course_transform":
        if payload.get("dry_run") is not False:
            return False, "course_transform_requires_dry_run_false_for_real_task"
        if not str(payload.get("course", "")).strip():
            return False, "course_transform_requires_course"
        if not any(str(payload.get(k, "")).strip() for k in ("vault", "course_path", "source_path")):
            return False, "course_transform_requires_vault_or_course_path"
    return True, "real_task_allowed"


def has_real_evidence(executor: str, result: dict[str, Any] | None = None) -> tuple[bool, str]:
    """A task can be marked done only when the result proves real execution."""
    result = result or {}
    executor = str(executor or "").strip()
    if result.get("dry_run") is True:
        return False, "dry_run_result_is_not_real"
    if executor == "file_read":
        if result.get("path") and "content" in result:
            return True, "file_read_content_evidence"
        return False, "missing_file_read_evidence"
    if executor == "safe_write":
        if result.get("written") is True and result.get("path"):
            return True, "safe_write_written_evidence"
        return False, "missing_safe_write_evidence"
    if executor == "source_scan":
        if isinstance(result.get("count"), int) and isinstance(result.get("items"), list):
            return True, "source_scan_count_evidence"
        return False, "missing_source_scan_evidence"
    if executor == "vault_audit":
        if isinstance(result.get("ok"), bool) and isinstance(result.get("issues"), list):
            return True, "vault_audit_issue_list_evidence"
        return False, "missing_vault_audit_evidence"
    if executor == "report_write":
        if result.get("written") is True and (result.get("path") or result.get("report_path")):
            return True, "report_write_written_evidence"
        return False, "missing_report_write_evidence"
    if executor == "course_transform":
        if result.get("course") and isinstance(result.get("files_written"), list) and result.get("report_path"):
            return True, "course_transform_file_report_evidence"
        return False, "missing_course_transform_evidence"
    return False, f"non_real_executor_result:{executor or '<missing>'}"


def insert_event(
    db_path: Path,
    task_id: str,
    event_type: str,
    message: str,
    payload: dict[str, Any] | None = None,
    level: str = "info",
) -> dict[str, Any]:
    init_schema(db_path)
    event = {
        "id": new_id("evt"),
        "task_id": task_id,
        "event_type": event_type,
        "level": level,
        "message": message,
        "payload_json": dumps(payload or {}),
        "created_at": now(),
    }
    with managed_connection(db_path) as conn:
        conn.execute(
            """
            INSERT INTO obs_task_ledger_events
                (id, task_id, event_type, level, message, payload_json, created_at)
            VALUES (:id, :task_id, :event_type, :level, :message, :payload_json, :created_at)
            """,
            event,
        )
    return row_to_event(event)


def create_task(
    db_path: Path,
    title: str,
    executor: str,
    payload: dict[str, Any] | None = None,
    content: str = "",
    course: str = "",
    priority: int = 100,
) -> dict[str, Any]:
    """Create a task. Non-real tasks are inserted as blocked for auditability."""
    init_schema(db_path)
    payload = payload or {}
    allowed, reason = validate_real_task(executor, payload)
    ts = now()
    task = {
        "id": new_id("task"),
        "title": title,
        "content": content,
        "course": course,
        "status": TASK_PENDING if allowed else TASK_BLOCKED,
        "priority": priority,
        "executor": executor,
        "payload_json": dumps(payload),
        "result_json": "{}",
        "error": "" if allowed else reason,
        "created_at": ts,
        "updated_at": ts,
        "finished_at": None if allowed else ts,
    }
    with managed_connection(db_path) as conn:
        conn.execute(
            """
            INSERT INTO obs_task_ledger_tasks
                (id, title, content, course, status, priority, executor, payload_json,
                 result_json, error, created_at, updated_at, finished_at)
            VALUES
                (:id, :title, :content, :course, :status, :priority, :executor, :payload_json,
                 :result_json, :error, :created_at, :updated_at, :finished_at)
            """,
            task,
        )
    insert_event(
        db_path,
        task["id"],
        "task_created" if allowed else "task_blocked",
        reason,
        {"executor": executor, "payload": payload},
        level="info" if allowed else "warn",
    )
    return row_to_task(task)


def get_task(db_path: Path, task_id: str) -> dict[str, Any] | None:
    init_schema(db_path)
    with managed_connection(db_path) as conn:
        row = conn.execute("SELECT * FROM obs_task_ledger_tasks WHERE id = ?", (task_id,)).fetchone()
    return row_to_task(dict(row)) if row else None


def record_result(db_path: Path, task_id: str, result: dict[str, Any]) -> dict[str, Any]:
    """Record task result and mark done only if evidence is verifiable."""
    task = get_task(db_path, task_id)
    if not task:
        raise KeyError(f"task not found: {task_id}")
    ok, reason = has_real_evidence(task["executor"], result)
    status = TASK_DONE if ok else TASK_BLOCKED
    ts = now()
    with managed_connection(db_path) as conn:
        conn.execute(
            """
            UPDATE obs_task_ledger_tasks
            SET status = ?, result_json = ?, error = ?, updated_at = ?, finished_at = ?
            WHERE id = ?
            """,
            (status, dumps(result), "" if ok else reason, ts, ts, task_id),
        )
    insert_event(
        db_path,
        task_id,
        "task_done" if ok else "task_blocked",
        reason,
        {"result": result},
        level="info" if ok else "warn",
    )
    updated = get_task(db_path, task_id)
    assert updated is not None
    updated["reason"] = reason
    return updated


def row_to_task(row: dict[str, Any]) -> dict[str, Any]:
    item = dict(row)
    item["payload"] = loads(item.pop("payload_json", "{}"), {})
    item["result"] = loads(item.pop("result_json", "{}"), {})
    return item


def row_to_event(row: dict[str, Any]) -> dict[str, Any]:
    item = dict(row)
    item["payload"] = loads(item.pop("payload_json", "{}"), {})
    return item


def list_tasks(db_path: Path, status: str | None = None, limit: int = 100) -> list[dict[str, Any]]:
    init_schema(db_path)
    query = "SELECT * FROM obs_task_ledger_tasks"
    params: list[Any] = []
    if status:
        query += " WHERE status = ?"
        params.append(status)
    query += " ORDER BY priority ASC, created_at ASC, id ASC LIMIT ?"
    params.append(limit)
    with managed_connection(db_path) as conn:
        rows = conn.execute(query, params).fetchall()
    return [row_to_task(dict(row)) for row in rows]


def list_events(db_path: Path, task_id: str | None = None, limit: int = 100) -> list[dict[str, Any]]:
    init_schema(db_path)
    query = "SELECT * FROM obs_task_ledger_events"
    params: list[Any] = []
    if task_id:
        query += " WHERE task_id = ?"
        params.append(task_id)
    query += " ORDER BY created_at ASC, id ASC LIMIT ?"
    params.append(limit)
    with managed_connection(db_path) as conn:
        rows = conn.execute(query, params).fetchall()
    return [row_to_event(dict(row)) for row in rows]


def status_summary(db_path: Path) -> dict[str, int]:
    init_schema(db_path)
    summary = {TASK_PENDING: 0, TASK_DONE: 0, TASK_BLOCKED: 0, TASK_FAILED: 0, "total": 0}
    with managed_connection(db_path) as conn:
        rows = conn.execute("SELECT status, COUNT(*) AS count FROM obs_task_ledger_tasks GROUP BY status").fetchall()
    for row in rows:
        summary[row["status"]] = int(row["count"])
        summary["total"] += int(row["count"])
    return summary


def markdown_report(db_path: Path) -> str:
    summary = status_summary(db_path)
    tasks = list_tasks(db_path, limit=500)
    lines = [
        "# OBS V10 本地任务账本",
        "",
        "> 从 Cognitive-Loop-OS sleep-loop 真实任务规则改造而来：只有带真实证据的任务才能标记 done。",
        "",
        "## Summary",
        "",
        f"- total: {summary['total']}",
        f"- pending: {summary[TASK_PENDING]}",
        f"- done: {summary[TASK_DONE]}",
        f"- blocked: {summary[TASK_BLOCKED]}",
        f"- failed: {summary[TASK_FAILED]}",
        "",
        "## Tasks",
        "",
        "| 状态 | 标题 | executor | course | error |",
        "|---|---|---|---|---|",
    ]
    for task in tasks:
        lines.append(
            f"| {task['status']} | {task['title']} | `{task['executor']}` | {task.get('course') or '—'} | {task.get('error') or '—'} |"
        )
    if not tasks:
        lines.append("| — | 暂无 | — | — | — |")
    lines += [
        "",
        "## Boundary",
        "",
        "- blocked 不代表失败；它表示缺少真实执行证据或任务本身是虚拟/预览任务。",
        "- echo、heartbeat、context_pack_build、taskpack_generate、preview、dry_run 不允许计入 done。",
        "- file_read 需要 path + content；safe_write/report_write 需要 written + path；source_scan 需要 count + items。",
    ]
    return "\n".join(lines).rstrip() + "\n"


def parse_jsonish(raw: str) -> dict[str, Any]:
    if not raw:
        return {}
    return json.loads(raw)


def main() -> None:
    parser = argparse.ArgumentParser(description="OBS V10 local task ledger")
    parser.add_argument("--db", type=Path, default=default_db_path())
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init")

    add = sub.add_parser("add")
    add.add_argument("--title", required=True)
    add.add_argument("--executor", required=True)
    add.add_argument("--payload", default="{}", help="JSON payload")
    add.add_argument("--content", default="")
    add.add_argument("--course", default="")
    add.add_argument("--priority", type=int, default=100)

    done = sub.add_parser("record")
    done.add_argument("--task-id", required=True)
    done.add_argument("--result", required=True, help="JSON result payload")

    listing = sub.add_parser("list")
    listing.add_argument("--status")
    listing.add_argument("--limit", type=int, default=100)

    sub.add_parser("summary")
    sub.add_parser("report")

    args = parser.parse_args()
    if args.command == "init":
        init_schema(args.db)
        print(json.dumps({"ok": True, "db": str(args.db)}, ensure_ascii=False, indent=2))
    elif args.command == "add":
        task = create_task(
            args.db,
            title=args.title,
            executor=args.executor,
            payload=parse_jsonish(args.payload),
            content=args.content,
            course=args.course,
            priority=args.priority,
        )
        print(json.dumps(task, ensure_ascii=False, indent=2))
    elif args.command == "record":
        task = record_result(args.db, args.task_id, parse_jsonish(args.result))
        print(json.dumps(task, ensure_ascii=False, indent=2))
    elif args.command == "list":
        print(json.dumps(list_tasks(args.db, status=args.status, limit=args.limit), ensure_ascii=False, indent=2))
    elif args.command == "summary":
        print(json.dumps(status_summary(args.db), ensure_ascii=False, indent=2))
    elif args.command == "report":
        print(markdown_report(args.db))


if __name__ == "__main__":
    main()
