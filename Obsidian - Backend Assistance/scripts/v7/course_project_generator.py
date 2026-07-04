#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate V7 course project-conversion pages from existing course notes.

Safety:
- dry-run by default;
- writes only with --apply;
- does not invent new course facts;
- uses filenames/headings as navigation signals, not as evidence claims.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Any


@dataclass
class CourseProjectPlan:
    course: str
    target: str
    source_notes: list[str]
    project_title: str
    milestones: list[str]
    deliverables: list[str]
    review_prompts: list[str]
    boundary: str


def list_course_notes(course_dir: Path) -> list[Path]:
    return [p for p in sorted(course_dir.glob('*.md')) if p.name not in {'13_项目转化.md'}]


def first_heading(path: Path) -> str:
    try:
        for line in path.read_text(encoding='utf-8', errors='ignore').splitlines():
            if line.startswith('#'):
                return line.lstrip('#').strip()
    except Exception:
        pass
    return path.stem


def classify_theme(course: str, note_names: list[str]) -> str:
    text = course + ' ' + ' '.join(note_names)
    if any(k in text for k in ['设计', '视觉', '版式', 'UI', 'Photoshop', 'AIGC', '品牌']):
        return 'design'
    if any(k in text for k in ['运营', '新媒体', '增长']):
        return 'operation'
    if any(k in text for k in ['记忆', '学习', '大脑', '知识内化', '复习']):
        return 'learning'
    if any(k in text for k in ['算法', '开发', '大模型', '全栈']):
        return 'engineering'
    return 'general'


def project_title_for(course: str, theme: str) -> str:
    suffix = {
        'design': '作品集/案例拆解项目',
        'operation': '增长实验/内容运营项目',
        'learning': '个人学习系统改造项目',
        'engineering': '可运行 Demo / 技术练习项目',
        'general': '可交付成果项目',
    }[theme]
    return f'{course}｜{suffix}'


def milestones_for(theme: str) -> list[str]:
    common = ['M1：从课程笔记中选择 3 个可执行主题', 'M2：定义一个 7 天内可完成的最小作品', 'M3：完成作品并写复盘']
    theme_extra = {
        'design': ['M4：产出前后对比图或案例拆解板', 'M5：沉淀为作品集条目'],
        'operation': ['M4：设计一次内容/渠道/转化实验', 'M5：记录数据与下一轮假设'],
        'learning': ['M4：制作主动回忆/复习流程', 'M5：连续 7 天验证并复盘'],
        'engineering': ['M4：实现一个可运行脚本/Demo', 'M5：补最小测试和 README'],
        'general': ['M4：交付一个可展示版本', 'M5：写复盘和下一步'],
    }[theme]
    return common + theme_extra


def deliverables_for(theme: str) -> list[str]:
    return {
        'design': ['案例拆解图板', '设计原则清单', '作品集条目草稿'],
        'operation': ['实验计划', '内容/渠道清单', '数据记录表与复盘'],
        'learning': ['复习流程图', '主动回忆卡组', '7天执行记录'],
        'engineering': ['可运行 Demo', 'README', '最小测试/验证记录'],
        'general': ['项目说明', '成果截图/链接', '复盘记录'],
    }[theme]


def review_prompts_for(course: str) -> list[str]:
    return [
        f'这门课《{course}》最能转化为作品的 3 个知识点是什么？',
        '哪些内容只能作为参考，不能当作已验证事实？',
        '最小可交付成果是什么？一周内如何完成？',
        '完成后如何证明自己真的掌握，而不是只读过？',
    ]


def build_plan(vault: Path, course: str) -> CourseProjectPlan:
    course_dir = vault / '02_课程库' / course
    notes = list_course_notes(course_dir)
    headings = [first_heading(p) for p in notes[:12]]
    theme = classify_theme(course, [p.name for p in notes] + headings)
    target = course_dir / '13_项目转化.md'
    return CourseProjectPlan(
        course=course,
        target=str(target),
        source_notes=[p.name for p in notes],
        project_title=project_title_for(course, theme),
        milestones=milestones_for(theme),
        deliverables=deliverables_for(theme),
        review_prompts=review_prompts_for(course),
        boundary='本页基于已有课程笔记结构生成项目化学习框架，不新增课程事实；具体内容需回到课程原文/证据页核验。',
    )


def render(plan: CourseProjectPlan) -> str:
    today = date.today().isoformat()
    source_rows = '\n'.join(f'- [[{name}]]' for name in plan.source_notes[:20]) or '- 暂无可读取课程笔记'
    milestones = '\n'.join(f'- [ ] {m}' for m in plan.milestones)
    deliverables = '\n'.join(f'- {d}' for d in plan.deliverables)
    prompts = '\n'.join(f'- {p}' for p in plan.review_prompts)
    return f'''---
title: {plan.course}｜13_项目转化
type: course-project-conversion
course: {plan.course}
status: draft
created: {today}
updated: {today}
tags:
  - v7
  - project-conversion
  - course-output
---

# {plan.project_title}

> [!warning] 边界
> {plan.boundary}

## 1. 来源笔记

{source_rows}

## 2. 最小项目目标

把本课程从“读过/整理过”推进到“能产出一个可展示作品或可执行流程”。

## 3. 里程碑

{milestones}

## 4. 交付物

{deliverables}

## 5. 主动回忆问题

{prompts}

## 6. 验收标准

- [ ] 有一个可展示成果或可执行流程
- [ ] 能说明它来自哪些课程笔记/证据页
- [ ] 能指出哪些内容仍需核验
- [ ] 有一次复盘记录

## 7. 复盘区

- 做了什么：
- 证据/链接：
- 卡住点：
- 下一步：
'''


def generate(vault: Path, course: str, apply: bool = False, backup_dir: Path | None = None) -> dict[str, Any]:
    plan = build_plan(vault, course)
    content = render(plan)
    target = Path(plan.target)
    result = {'apply': apply, 'plan': asdict(plan), 'content': content}
    if apply:
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and backup_dir:
            backup_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, backup_dir / f'{course}_13_项目转化.md.before')
        target.write_text(content, encoding='utf-8')
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--vault', type=Path, required=True)
    parser.add_argument('--course', required=True)
    parser.add_argument('--backup-dir', type=Path)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    result = generate(args.vault, args.course, apply=args.apply, backup_dir=args.backup_dir)
    print(json.dumps({k: v for k, v in result.items() if k != 'content'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
