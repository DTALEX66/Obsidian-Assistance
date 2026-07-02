#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build TALOS V8 training streak radar from Daily Mission notes.

Read-only by default. With --apply, writes JSON and Markdown reports only.
It never changes Daily Mission notes or marks tasks done.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Any

TASK_RE = re.compile(r"^- \[( |x|X)\]", re.MULTILINE)
COURSE_RE = re.compile(r"^course:\s*(.+?)\s*$", re.MULTILINE)
DATE_RE = re.compile(r"^mission_date:\s*(\d{4}-\d{2}-\d{2})\s*$", re.MULTILINE)


@dataclass
class MissionStats:
    date: str
    course: str
    path: str
    tasks_total: int
    tasks_done: int
    completion_rate: float
    has_evidence_section: bool
    has_recall_section: bool
    has_project_section: bool
    has_log_section: bool


def parse_mission(path: Path, vault: Path) -> MissionStats:
    text = path.read_text(encoding='utf-8', errors='ignore')
    mission_date = None
    m = DATE_RE.search(text)
    if m:
        mission_date = m.group(1)
    else:
        mission_date = path.stem
    c = COURSE_RE.search(text)
    course = c.group(1).strip().strip('"') if c else '未标注课程'
    marks = TASK_RE.findall(text)
    total = len(marks)
    done = sum(1 for x in marks if x.lower() == 'x')
    return MissionStats(
        date=mission_date,
        course=course,
        path=path.relative_to(vault).as_posix(),
        tasks_total=total,
        tasks_done=done,
        completion_rate=round(done / total, 4) if total else 0.0,
        has_evidence_section='## 1. Evidence / 证据' in text,
        has_recall_section='## 2. Recall / 主动回忆' in text,
        has_project_section='## 3. Project / 项目动作' in text,
        has_log_section='## 4. Log / 复盘' in text,
    )


def streak_days(dates: list[str], today: str | None = None) -> int:
    if not dates:
        return 0
    parsed = {date.fromisoformat(d) for d in dates}
    cursor = date.fromisoformat(today) if today else max(parsed)
    streak = 0
    while cursor in parsed:
        streak += 1
        cursor -= timedelta(days=1)
    return streak


def audit(vault: Path, today: str | None = None) -> dict[str, Any]:
    mission_dir = vault / '00_主页' / '12_TALOS_Daily_Missions'
    missions = []
    if mission_dir.exists():
        for path in sorted(mission_dir.glob('*.md')):
            missions.append(parse_mission(path, vault))
    dates = [m.date for m in missions]
    task_total = sum(m.tasks_total for m in missions)
    task_done = sum(m.tasks_done for m in missions)
    course_counts = Counter(m.course for m in missions)
    missing_sections = []
    for m in missions:
        missing = []
        if not m.has_evidence_section: missing.append('Evidence')
        if not m.has_recall_section: missing.append('Recall')
        if not m.has_project_section: missing.append('Project')
        if not m.has_log_section: missing.append('Log')
        if missing:
            missing_sections.append({'path': m.path, 'missing': missing})
    return {
        'missions': len(missions),
        'tasks_total': task_total,
        'tasks_done': task_done,
        'completion_rate': round(task_done / task_total, 4) if task_total else 0.0,
        'streak_days': streak_days(dates, today=today),
        'latest_date': max(dates) if dates else None,
        'course_counts': dict(course_counts),
        'missing_sections': missing_sections,
        'items': [asdict(m) for m in missions],
    }


def markdown_report(data: dict[str, Any]) -> str:
    rows = []
    for item in data['items']:
        rows.append(
            f"| [[{item['path'][:-3]}|{item['date']}]] | {item['course']} | {item['tasks_done']}/{item['tasks_total']} | {item['completion_rate']:.0%} |"
        )
    rows_text = '\n'.join(rows) if rows else '| 暂无 | 暂无 | 0/0 | 0% |'
    courses = '\n'.join(f"- {k}: {v}" for k, v in sorted(data['course_counts'].items())) or '- 暂无'
    missing = '\n'.join(f"- `{x['path']}` 缺少: {', '.join(x['missing'])}" for x in data['missing_sections']) or '- 无'
    return f'''# TALOS V8 训练复盘 / 连续打卡雷达

## 总览

- Daily Mission 数量：{data['missions']}
- 任务完成：{data['tasks_done']} / {data['tasks_total']}
- 完成率：{data['completion_rate']:.0%}
- 连续打卡：{data['streak_days']} 天
- 最新任务日期：{data['latest_date'] or '暂无'}

## 课程分布

{courses}

## Daily Mission 明细

| 日期 | 课程 | 完成 | 完成率 |
|---|---|---:|---:|
{rows_text}

## 结构缺口

{missing}

## 判读

- 连续打卡只统计存在 Daily Mission 文件的日期；不会自动把未完成任务算作完成。
- 完成率来自 Markdown 复选框 `- [x]`，工具不修改任务状态。
- 若 V6 证据缺失，应记录为缺口，不得伪造成 verified。
'''


def write_reports(data: dict[str, Any], output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / 'v8-training-streak-radar.json'
    md_path = output_dir / 'v8-training-streak-radar.md'
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    md_path.write_text(markdown_report(data), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--vault', type=Path, required=True)
    parser.add_argument('--today')
    parser.add_argument('--output-dir', type=Path)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    data = audit(args.vault, today=args.today)
    out = None
    if args.apply:
        if not args.output_dir:
            raise SystemExit('--output-dir is required with --apply')
        out = write_reports(data, args.output_dir)
    print(json.dumps({'apply': args.apply, 'output': out, **{k: v for k, v in data.items() if k != 'items'}}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
