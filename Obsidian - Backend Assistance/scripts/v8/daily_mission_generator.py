#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate TALOS V8 Daily Mission notes for an Obsidian vault.

Safety:
- dry-run by default;
- writes only with --apply;
- never creates course facts or evidence;
- links to existing course/V6/V7/V8 pages only when they exist;
- protects existing mission notes unless --overwrite is passed.
"""
from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Any


@dataclass
class DailyMissionPlan:
    mission_date: str
    course: str
    target: str
    course_overview: str
    project_page: str | None
    evidence_index: str | None
    active_training_center: str | None
    execution_log: str | None
    status: str
    boundary: str


def rel(root: Path, path: Path | None) -> str | None:
    if path is None:
        return None
    return path.relative_to(root).as_posix()


def first_existing(paths: list[Path]) -> Path | None:
    for p in paths:
        if p.exists():
            return p
    return None


def build_plan(vault: Path, course: str, mission_date: str | None = None, output_dir: Path | None = None) -> DailyMissionPlan:
    mission_date = mission_date or date.today().isoformat()
    course_dir = vault / '02_课程库' / course
    overview = course_dir / '00_课程总览.md'
    if not overview.exists():
        raise FileNotFoundError(f'course overview not found: {overview}')
    project = course_dir / '13_项目转化.md'
    evidence = course_dir / '11_证据索引.md'
    output_dir = output_dir or vault / '00_主页' / '12_TALOS_Daily_Missions'
    target = output_dir / f'{mission_date}.md'
    return DailyMissionPlan(
        mission_date=mission_date,
        course=course,
        target=str(target),
        course_overview=rel(vault, overview) or str(overview),
        project_page=rel(vault, project) if project.exists() else None,
        evidence_index=rel(vault, evidence) if evidence.exists() else None,
        active_training_center=rel(vault, first_existing([vault / '00_主页/09_TALOS主动训练中心.md'])),
        execution_log=rel(vault, first_existing([vault / '00_主页/11_TALOS执行日志.md'])),
        status='ready-to-write',
        boundary='Daily Mission 是执行日志模板，不新增课程事实；证据任务必须回链真实 V6 或课程原文。',
    )


def link(path: str | None, label: str) -> str:
    if not path:
        return f'{label}（缺失）'
    stem = path[:-3] if path.endswith('.md') else path
    return f'[[{stem}|{label}]]'


def render(plan: DailyMissionPlan) -> str:
    project_task = '从项目页选择一个 25 分钟可完成的最小动作。' if plan.project_page else '先创建/检查本课程 V7 项目页，再选择最小动作。'
    evidence_task = '从 V6 证据索引选 1 个真实证据点并复述。' if plan.evidence_index else '本课程缺 V6 证据页：只能回链课程原文，不得伪造截图/关键帧。'
    return f'''---
title: TALOS Daily Mission {plan.mission_date}
type: talos-daily-mission
status: active
mission_date: {plan.mission_date}
course: {plan.course}
tags:
  - talos
  - v8
  - daily-mission
  - execution-log
---

# TALOS Daily Mission — {plan.mission_date}

> [!warning] 边界
> {plan.boundary}

## 0. Mission Links

- 课程总览：{link(plan.course_overview, plan.course + '｜课程总览')}
- V7 项目页：{link(plan.project_page, '13_项目转化')}
- V6 证据页：{link(plan.evidence_index, '11_证据索引')}
- 主动训练中心：{link(plan.active_training_center, 'TALOS 主动训练中心')}
- 执行日志：{link(plan.execution_log, 'TALOS 执行日志')}

## 1. Evidence / 证据

- [ ] {evidence_task}
- 选择的证据/原文链接：
- 我能复述出的关键点：

## 2. Recall / 主动回忆

- [ ] 不看答案，写出 3 个问题和回答。
- 问题 1：
- 回答 1：
- 问题 2：
- 回答 2：
- 问题 3：
- 回答 3：
- 对照后修正：

## 3. Project / 项目动作

- [ ] {project_task}
- 今日 25 分钟动作：
- 可见产出：
- 产出链接/截图/文件：

## 4. Log / 复盘

- 做了什么：
- 证据/链接：
- 卡住点：
- 明天下一步：

## 5. Done Criteria

- [ ] 有一个真实链接或可见产出。
- [ ] 有一条主动回忆修正。
- [ ] 没有把缺失证据伪装成 V6 verified。
'''


def generate(vault: Path, course: str, mission_date: str | None = None, output_dir: Path | None = None,
             apply: bool = False, overwrite: bool = False, backup_dir: Path | None = None) -> dict[str, Any]:
    plan = build_plan(vault, course, mission_date=mission_date, output_dir=output_dir)
    content = render(plan)
    target = Path(plan.target)
    exists = target.exists()
    result: dict[str, Any] = {'apply': apply, 'exists': exists, 'plan': asdict(plan), 'content': content}
    if apply:
        if exists and not overwrite:
            raise FileExistsError(f'target exists; pass --overwrite to replace: {target}')
        target.parent.mkdir(parents=True, exist_ok=True)
        if exists and backup_dir:
            backup_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, backup_dir / f'{target.stem}.before.md')
        target.write_text(content, encoding='utf-8')
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--vault', type=Path, required=True)
    parser.add_argument('--course', required=True)
    parser.add_argument('--date', dest='mission_date')
    parser.add_argument('--output-dir', type=Path)
    parser.add_argument('--backup-dir', type=Path)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    result = generate(
        args.vault,
        args.course,
        mission_date=args.mission_date,
        output_dir=args.output_dir,
        apply=args.apply,
        overwrite=args.overwrite,
        backup_dir=args.backup_dir,
    )
    print(json.dumps({k: v for k, v in result.items() if k != 'content'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
