#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate V5 keyframe collection task notes for formal Obsidian courses.

This does not extract or fabricate images. It creates task notes that instruct the
operator to collect real keyframes from local videos/PDF/courseware.
"""
from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path


@dataclass
class PlannedTask:
    course: str
    path: str
    action: str


def formal_courses(vault: Path, limit: int) -> list[Path]:
    root = vault / "02_课程库"
    return [p for p in sorted(root.iterdir()) if p.is_dir() and (p / "00_课程总览.md").exists()][:limit]


def task_text(course: str) -> str:
    today = date.today().isoformat()
    return f'''---
title: "{course} 关键帧采集任务单"
type: keyframe-task
course: "{course}"
status: todo
created: {today}
updated: {today}
tags:
  - keyframe
  - course-evidence
  - knowledgeos-v5
---

# {course} 关键帧采集任务单

> [!warning] 真实性边界
> 本页不是图片证据本身，只是采集任务单。没有打开本地课程视频/PDF/课件并核验前，不能添加截图、占位图或互联网图片。

## 1. 优先采集对象

| 类型 | 应采集内容 | 状态 |
|---|---|---|
| 课程视频 | 讲师展示流程/案例/操作界面/板书 | 待找源 |
| PDF/课件 | 章节结构图、关键表格、案例页 | 待找源 |
| 实操/案例 | 前后对比、成品、错误示例 | 待找源 |

## 2. 采集记录

| 序号 | 来源文件 | 页码/时间点 | 内容说明 | 可否入库 | 备注 |
|---:|---|---|---|---|---|
| 1 | 待补 | 待补 | 待补 | 待核验 | 不编造 |

## 3. 入库路径建议

- 附件目录：`99_附件/course-keyframes/{course}/`
- 视觉索引：[[04_关键图表与课件索引]]
- 验证页：[[06_验证与不确定项]]

## 4. 采集后必须更新

- [ ] 把真实图片写入附件目录。
- [ ] 在 `04_关键图表与课件索引.md` 写明来源。
- [ ] 在 `06_验证与不确定项.md` 标记核验状态。
- [ ] 重跑图片证据审计。
'''


def generate(vault: Path, limit: int = 20, apply: bool = False, backup_dir: Path | None = None, skip_existing: bool = True) -> dict:
    planned: list[PlannedTask] = []
    for course_dir in formal_courses(vault, limit):
        course = course_dir.name
        target = course_dir / "10_关键帧采集任务单.md"
        if skip_existing and target.exists():
            continue
        action = "overwrite" if target.exists() else "create"
        planned.append(PlannedTask(course, str(target.relative_to(vault)), action))
        if apply:
            if target.exists() and backup_dir:
                backup_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(target, backup_dir / (course + "__10.before"))
            target.write_text(task_text(course), encoding="utf-8")
            visual = course_dir / "04_关键图表与课件索引.md"
            if visual.exists():
                text = visual.read_text(encoding="utf-8", errors="ignore")
                if "关键帧采集任务单" not in text:
                    if backup_dir:
                        backup_dir.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(visual, backup_dir / (course + "__04.before"))
                    visual.write_text(text.rstrip() + f"\n\n## 8. 关键帧采集任务\n\n- [[10_关键帧采集任务单|{course} 关键帧采集任务单]]\n- 说明：本课程仍缺真实课程图片，必须从本地视频/PDF/课件抽取。\n", encoding="utf-8")
    return {"vault": str(vault), "apply": apply, "planned_tasks": [asdict(p) for p in planned]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("vault", type=Path)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--backup-dir", type=Path)
    parser.add_argument("--include-existing", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    data = generate(args.vault, args.limit, args.apply, args.backup_dir, skip_existing=not args.include_existing)
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
