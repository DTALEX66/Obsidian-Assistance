#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OBS V10 course transformation ledger.

Build a read-only ledger that maps formal course folders to the processing
artifacts around them:

    原始来源 → 扫描报告 → 生成资产 → registry → 课程页 → 下一步

The script is designed as the bridge between course-processing reality and the
V10 `obs_task_ledger.py` real-task ledger.  It does not modify course notes and
only writes to the SQLite task ledger when `--seed-ledger` is explicitly passed.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.v10.obs_task_ledger import TASK_PENDING, create_task, default_db_path, list_tasks

REQUIRED_COURSE_PAGES = [
    "00_课程总览.md",
    "01_素材识别报告.md",
    "07_实操工作流.md",
    "08_术语索引.md",
    "12_真实截图与关键帧.md",
    "13_项目转化.md",
    "14_开放知识交叉对比.md",
]

STORAGE_MAP = {
    "source_root": "E:/学习数据",
    "reports": "93_导入报告",
    "verified_keyframes": "99_附件/verified-keyframes",
    "reference_images": "99_附件/course-reference-images",
    "visuals": "99_附件/course-visuals",
    "course_root": "02_课程库",
}


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return None


def iter_course_dirs(vault: Path) -> list[Path]:
    root = vault / "02_课程库"
    if not root.exists():
        return []
    return sorted([p for p in root.iterdir() if p.is_dir()], key=lambda p: p.name.casefold())


def normalize_items(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        for key in ("items", "records", "keyframes", "assets"):
            value = data.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
        # Some registries are course -> list/dict maps.
        items: list[dict[str, Any]] = []
        for course, value in data.items():
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        merged = {"course": course}
                        merged.update(item)
                        items.append(merged)
            elif isinstance(value, dict):
                merged = {"course": course}
                merged.update(value)
                items.append(merged)
        return items
    return []


def item_course(item: dict[str, Any]) -> str:
    for key in ("course", "course_name", "courseName", "course_title", "title"):
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    path = str(item.get("path") or item.get("assetPath") or item.get("file") or "")
    parts = [part for part in path.replace("\\", "/").split("/") if part]
    if "verified-keyframes" in parts:
        idx = parts.index("verified-keyframes")
        if idx + 1 < len(parts):
            return parts[idx + 1]
    return ""


def load_keyframe_index(vault: Path) -> dict[str, list[dict[str, Any]]]:
    registry = vault / "99_附件" / "verified-keyframes" / "keyframe-registry.json"
    by_course: dict[str, list[dict[str, Any]]] = {}
    for item in normalize_items(read_json(registry)):
        course = item_course(item)
        if course:
            by_course.setdefault(course, []).append(item)
    return by_course


def scan_report_matches(vault: Path, course_name: str) -> list[str]:
    report_root = vault / "93_导入报告"
    if not report_root.exists():
        return []
    matches: list[str] = []
    for path in report_root.rglob("*"):
        if course_name in path.name:
            try:
                matches.append(path.relative_to(vault).as_posix())
            except ValueError:
                matches.append(path.as_posix())
    return sorted(matches)[:20]


def course_row(vault: Path, course_dir: Path, keyframes: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    existing = [name for name in REQUIRED_COURSE_PAGES if (course_dir / name).exists()]
    missing = [name for name in REQUIRED_COURSE_PAGES if name not in existing]
    course = course_dir.name
    kf_items = keyframes.get(course, [])
    report_matches = scan_report_matches(vault, course)
    return {
        "course": course,
        "course_path": course_dir.relative_to(vault).as_posix(),
        "existing_pages": existing,
        "missing_pages": missing,
        "has_keyframes": bool(kf_items),
        "keyframe_count": len(kf_items),
        "report_count": len(report_matches),
        "report_matches": report_matches,
        "next_action": next_action(missing, bool(kf_items), bool(report_matches)),
    }


def next_action(missing_pages: list[str], has_keyframes: bool, has_reports: bool) -> str:
    if missing_pages:
        return "补齐课程缺口页并生成导入/处理报告"
    if not has_keyframes:
        return "定位本地源并补真实截图/关键帧证据"
    if not has_reports:
        return "补处理/导入报告，形成可追溯总账"
    return "已具备基础闭环，进入质量审计/复习增强"


def build_course_transform_ledger(vault: Path | str, limit: int | None = None) -> dict[str, Any]:
    vault = Path(vault)
    keyframes = load_keyframe_index(vault)
    courses = [course_row(vault, path, keyframes) for path in iter_course_dirs(vault)]
    if limit is not None:
        courses = courses[: max(0, int(limit))]
    with_missing = [row for row in courses if row["missing_pages"]]
    without_keyframes = [row for row in courses if not row["has_keyframes"]]
    without_reports = [row for row in courses if row["report_count"] == 0]
    return {
        "vault": vault.as_posix(),
        "storage_map": STORAGE_MAP,
        "required_pages": REQUIRED_COURSE_PAGES,
        "summary": {
            "courses_total": len(courses),
            "courses_with_missing_pages": len(with_missing),
            "courses_without_keyframes": len(without_keyframes),
            "courses_without_reports": len(without_reports),
        },
        "courses": courses,
    }


def generate_tasks(ledger: dict[str, Any], limit: int | None = None) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    vault = ledger.get("vault", "")
    for row in ledger.get("courses", []):
        if not row.get("missing_pages") and row.get("has_keyframes") and row.get("report_count", 0) > 0:
            continue
        course = row["course"]
        tasks.append(
            {
                "title": f"课程转化补全：{course}",
                "course": course,
                "executor": "course_transform",
                "priority": priority_for(row),
                "payload": {
                    "course": course,
                    "vault": vault,
                    "dry_run": False,
                    "course_path": row.get("course_path"),
                    "missing_pages": row.get("missing_pages", []),
                    "has_keyframes": row.get("has_keyframes", False),
                    "report_count": row.get("report_count", 0),
                    "next_action": row.get("next_action", ""),
                },
            }
        )
    tasks.sort(key=lambda item: (item["priority"], item["course"]))
    if limit is not None:
        tasks = tasks[: max(0, int(limit))]
    return tasks


def priority_for(row: dict[str, Any]) -> int:
    score = 100
    missing = set(row.get("missing_pages", []))
    if "01_素材识别报告.md" in missing:
        score -= 30
    if "07_实操工作流.md" in missing:
        score -= 20
    if "12_真实截图与关键帧.md" in missing or not row.get("has_keyframes"):
        score -= 20
    if "14_开放知识交叉对比.md" in missing:
        score -= 5
    if row.get("report_count", 0) == 0:
        score -= 10
    return max(score, 1)


def seed_task_ledger(db_path: Path | str, tasks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    created: list[dict[str, Any]] = []
    db = Path(db_path)
    existing_keys = {task_identity(row) for row in list_tasks(db, status=TASK_PENDING, limit=10_000)}
    for task in tasks:
        key = task_identity(task)
        if key in existing_keys:
            continue
        created.append(
            create_task(
                db,
                title=task["title"],
                executor=task["executor"],
                payload=task["payload"],
                course=task.get("course", ""),
                priority=int(task.get("priority", 100)),
            )
        )
        existing_keys.add(key)
    return created


def task_identity(task: dict[str, Any]) -> tuple[str, str, str, str]:
    payload = task.get("payload") or {}
    missing = ",".join(sorted(str(item) for item in payload.get("missing_pages", [])))
    return (
        str(task.get("executor") or ""),
        str(task.get("course") or payload.get("course") or ""),
        str(payload.get("course_path") or ""),
        missing,
    )


def markdown_report(ledger: dict[str, Any]) -> str:
    summary = ledger["summary"]
    lines = [
        "# 课程转化与处理产物总账",
        "",
        "> 只读生成：映射原始来源、扫描报告、生成资产、registry、课程页和下一步任务。",
        "",
        "## 总览",
        "",
        f"- courses_total: {summary['courses_total']}",
        f"- courses_with_missing_pages: {summary['courses_with_missing_pages']}",
        f"- courses_without_keyframes: {summary['courses_without_keyframes']}",
        f"- courses_without_reports: {summary['courses_without_reports']}",
        "",
        "## 存储链路",
        "",
        f"- 原始来源: `{ledger['storage_map']['source_root']}`",
        f"- 扫描报告: `{ledger['storage_map']['reports']}`",
        f"- 生成资产: `{ledger['storage_map']['verified_keyframes']}`, `{ledger['storage_map']['reference_images']}`, `{ledger['storage_map']['visuals']}`",
        "- registry: `99_附件/verified-keyframes/keyframe-registry.json`",
        f"- 课程页: `{ledger['storage_map']['course_root']}/<课程名>/`",
        "",
        "## 课程明细",
        "",
        "| 课程 | 缺口页 | 关键帧 | 报告 | 下一步 |",
        "|---|---:|---:|---:|---|",
    ]
    for row in ledger.get("courses", []):
        lines.append(
            "| {course} | {missing} | {keyframes} | {reports} | {action} |".format(
                course=row["course"],
                missing=len(row.get("missing_pages", [])),
                keyframes=row.get("keyframe_count", 0),
                reports=row.get("report_count", 0),
                action=row.get("next_action", ""),
            )
        )
    if not ledger.get("courses"):
        lines.append("| — | 0 | 0 | 0 | 未发现课程目录 |")
    lines.extend(
        [
            "",
            "## 下一步",
            "",
            "1. 对缺口页生成 `course_transform` 账本任务。",
            "2. 从 `E:/学习数据` 定位课程真实源文件。",
            "3. 用 V6 证据工具补关键帧/PDF 源页图。",
            "4. 写入导入报告后，用真实 `report_path`/`files_written` 证据关闭任务。",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build OBS course transformation ledger")
    parser.add_argument("--vault", type=Path, required=True)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    parser.add_argument("--tasks", action="store_true", help="Output generated task payloads instead of the ledger")
    parser.add_argument("--seed-ledger", action="store_true", help="Create pending tasks in obs_task_ledger SQLite DB")
    parser.add_argument("--ledger-db", type=Path, default=default_db_path())
    parser.add_argument("--output", type=Path, help="Optional report output path")
    args = parser.parse_args()

    ledger = build_course_transform_ledger(args.vault, limit=args.limit)
    tasks = generate_tasks(ledger, limit=args.limit) if args.tasks or args.seed_ledger else []
    payload: Any
    if args.seed_ledger:
        payload = {"created": seed_task_ledger(args.ledger_db, tasks), "task_count": len(tasks)}
    elif args.tasks:
        payload = tasks
    else:
        payload = ledger

    text = markdown_report(ledger) if args.format == "markdown" and not (args.tasks or args.seed_ledger) else json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
