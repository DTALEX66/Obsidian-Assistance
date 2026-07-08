#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OBS V10 Dataview-like read-only query layer.

Adapted from Cognitive-Loop-OS `shared/dataview.py`, but rewritten for the
Obsidian-Assistance helper repo.  It queries in-memory rows produced by V10
read-only ledgers/adapters instead of a live KB database.

Supported syntax:

    FROM <table> WHERE field='value' AND n>0 SORT field DESC LIMIT 10
    LIST field FROM <table> WHERE ... LIMIT 10
    TABLE field1, field2 FROM <table> WHERE ...

Tables:
- courses: from course_transform_ledger.py
- tasks: from obs_task_ledger.py
- sources: from course_intake_adapter.py manifest
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.v10.course_intake_adapter import inventory_sources
from scripts.v10.course_transform_ledger import build_course_transform_ledger
from scripts.v10.obs_task_ledger import default_db_path, list_tasks

_QUERY_RE = re.compile(
    r"^\s*(?:(?P<mode>LIST|TABLE)\s+(?P<fields>[\w,\s]+?)\s+)?"
    r"FROM\s+(?P<table>\w+)"
    r"(?:\s+WHERE\s+(?P<where>.+?))?"
    r"(?:\s+SORT\s+(?P<sort>\w+)(?:\s+(?P<order>ASC|DESC))?)?"
    r"(?:\s+LIMIT\s+(?P<limit>\d+))?"
    r"\s*$",
    re.IGNORECASE,
)


def available_tables() -> dict[str, dict[str, Any]]:
    return {
        "courses": {
            "source": "course_transform_ledger",
            "read_only": True,
            "fields": ["course", "missing_count", "has_keyframes", "keyframe_count", "report_count", "next_action"],
        },
        "tasks": {
            "source": "obs_task_ledger",
            "read_only": True,
            "fields": ["id", "title", "course", "status", "priority", "executor", "error"],
        },
        "sources": {
            "source": "course_intake_adapter",
            "read_only": True,
            "content_included": False,
            "fields": ["path", "relative_path", "name", "format", "size_bytes", "candidate_only"],
        },
    }


def parse_query(query: str) -> dict[str, Any]:
    match = _QUERY_RE.match(query)
    if not match:
        raise ValueError(f"invalid query syntax: {query}")
    fields = []
    if match.group("fields"):
        fields = [field.strip() for field in match.group("fields").split(",") if field.strip()]
    return {
        "query": query,
        "mode": (match.group("mode") or "FROM").upper(),
        "fields": fields,
        "table": match.group("table"),
        "conditions": parse_where(match.group("where") or ""),
        "sort": match.group("sort"),
        "order": (match.group("order") or "ASC").upper(),
        "limit": int(match.group("limit") or 100),
    }


def parse_where(where: str) -> list[dict[str, Any]]:
    if not where.strip():
        return []
    return [parse_condition(part) for part in re.split(r"\s+AND\s+", where, flags=re.IGNORECASE)]


def parse_condition(text: str) -> dict[str, Any]:
    text = text.strip()
    for op in ("!=", ">=", "<=", "=", ">", "<", "~", "!~"):
        if op in text:
            key, _, value = text.partition(op)
            return {"field": key.strip(), "op": op, "value": parse_value(value.strip())}
    return {"field": text, "op": "exists", "value": ""}


def parse_value(value: str) -> Any:
    value = value.strip().strip("'\"")
    low = value.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def query_records(query: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    parsed = parse_query(query)
    matched = [row for row in rows if matches(row, parsed["conditions"])]
    if parsed["sort"]:
        sort_field = parsed["sort"]
        reverse = parsed["order"] == "DESC"
        matched.sort(key=lambda row: comparable(row.get(sort_field)), reverse=reverse)
    matched = matched[: parsed["limit"]]
    if parsed["mode"] in {"LIST", "TABLE"} and parsed["fields"]:
        matched = [{field: row.get(field) for field in parsed["fields"]} for row in matched]
    return {
        "query": query,
        "table": parsed["table"],
        "count": len(matched),
        "items": matched,
        "parsed": parsed,
        "read_only": True,
    }


def comparable(value: Any) -> tuple[int, Any]:
    if isinstance(value, bool):
        return (0, int(value))
    if isinstance(value, (int, float)):
        return (0, value)
    return (1, "" if value is None else str(value).casefold())


def matches(row: dict[str, Any], conditions: list[dict[str, Any]]) -> bool:
    for cond in conditions:
        field = cond["field"]
        op = cond["op"]
        expected = cond["value"]
        actual = row.get(field)
        if op == "exists":
            if not actual:
                return False
        elif op == "=":
            if not equal(actual, expected):
                return False
        elif op == "!=":
            if equal(actual, expected):
                return False
        elif op == "~":
            if str(expected).casefold() not in stringify(actual).casefold():
                return False
        elif op == "!~":
            if str(expected).casefold() in stringify(actual).casefold():
                return False
        elif op in {">", ">=", "<", "<="}:
            if not compare_numeric(actual, expected, op):
                return False
    return True


def equal(actual: Any, expected: Any) -> bool:
    if isinstance(expected, bool):
        return bool(actual) is expected
    if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
        return actual == expected
    return stringify(actual).casefold() == stringify(expected).casefold()


def stringify(value: Any) -> str:
    if isinstance(value, list):
        return ",".join(str(item) for item in value)
    return "" if value is None else str(value)


def compare_numeric(actual: Any, expected: Any, op: str) -> bool:
    try:
        left = float(actual)
        right = float(expected)
    except (TypeError, ValueError):
        return False
    if op == ">":
        return left > right
    if op == ">=":
        return left >= right
    if op == "<":
        return left < right
    return left <= right


def run_query(
    query: str,
    vault: str | Path | None = None,
    ledger_db: str | Path | None = None,
    source_root: str | Path | None = None,
    source_limit: int = 200,
) -> dict[str, Any]:
    parsed = parse_query(query)
    table = parsed["table"]
    rows = load_table(table, vault=vault, ledger_db=ledger_db, source_root=source_root, source_limit=source_limit)
    return query_records(query, rows)


def load_table(
    table: str,
    vault: str | Path | None = None,
    ledger_db: str | Path | None = None,
    source_root: str | Path | None = None,
    source_limit: int = 200,
) -> list[dict[str, Any]]:
    if table == "courses":
        if not vault:
            raise ValueError("courses table requires --vault")
        ledger = build_course_transform_ledger(Path(vault))
        return [flatten_course_row(row) for row in ledger["courses"]]
    if table == "tasks":
        return flatten_tasks(list_tasks(Path(ledger_db) if ledger_db else default_db_path(), limit=10_000))
    if table == "sources":
        if not source_root:
            raise ValueError("sources table requires --source-root")
        return inventory_sources(Path(source_root), limit=source_limit)["items"]
    raise ValueError(f"unknown table: {table}; available={sorted(available_tables())}")


def flatten_course_row(row: dict[str, Any]) -> dict[str, Any]:
    flat = dict(row)
    flat["missing_count"] = len(row.get("missing_pages", []))
    flat["existing_count"] = len(row.get("existing_pages", []))
    flat["status"] = "gap" if flat["missing_count"] or not row.get("has_keyframes") else "ok"
    return flat


def flatten_tasks(tasks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for task in tasks:
        row = dict(task)
        payload = row.get("payload") or {}
        row["missing_count"] = len(payload.get("missing_pages", [])) if isinstance(payload, dict) else 0
        rows.append(row)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="OBS V10 Dataview-like read-only query")
    parser.add_argument("query")
    parser.add_argument("--vault", type=Path)
    parser.add_argument("--ledger-db", type=Path)
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--source-limit", type=int, default=200)
    parser.add_argument("--tables", action="store_true")
    args = parser.parse_args()

    if args.tables:
        payload = available_tables()
    else:
        payload = run_query(
            args.query,
            vault=args.vault,
            ledger_db=args.ledger_db,
            source_root=args.source_root,
            source_limit=args.source_limit,
        )
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
