#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate V5 diversity supplement pages for formal Obsidian courses.

Safety:
- Dry-run by default.
- Writes only when --apply is provided.
- Only creates/updates the supplement files inside formal course folders:
  02_课程地图.canvas, 04_关键图表与课件索引.md, 05_复习与检索练习.md, 06_验证与不确定项.md.
- Backs up overwritten files to --backup-dir.
- Never deletes or moves course source/body files.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from dataclasses import dataclass, asdict
from datetime import date
from pathlib import Path

SUPPLEMENT_FILES = [
    "02_课程地图.canvas",
    "04_关键图表与课件索引.md",
    "05_复习与检索练习.md",
    "06_验证与不确定项.md",
]

TYPE_HINTS = [
    (re.compile(r"UI|设计|视觉|Photoshop|品牌|版式|美术|AIGC", re.I), "design"),
    (re.compile(r"模型|AI|算法|编程|RAG|开发", re.I), "technical"),
    (re.compile(r"运营|增长|新媒体|转岗", re.I), "growth"),
    (re.compile(r"记忆|学习|考霸|大脑|心理|思维导图", re.I), "learning"),
]

@dataclass
class PlannedWrite:
    course: str
    path: str
    action: str
    bytes: int


def infer_course_type(name: str) -> str:
    for pattern, kind in TYPE_HINTS:
        if pattern.search(name):
            return kind
    return "general"


def formal_course_dirs(course_root: Path, limit: int) -> list[Path]:
    dirs = [p for p in sorted(course_root.iterdir()) if p.is_dir() and (p / "00_课程总览.md").exists()]
    return dirs[:limit]


def read_note(course_dir: Path, filename: str) -> str:
    p = course_dir / filename
    return p.read_text(encoding="utf-8", errors="ignore") if p.exists() else ""


def extract_bullets(text: str, limit: int = 8) -> list[str]:
    candidates: list[str] = []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("---") or s.startswith("#"):
            continue
        if s.startswith(('-', '*', '1.', '2.', '3.', '4.', '5.')):
            s = re.sub(r"^[-*]\s*|^\d+\.\s*", "", s).strip()
            if 8 <= len(s) <= 80:
                candidates.append(s)
        elif "：" in s and len(s) <= 80:
            candidates.append(s)
        if len(candidates) >= limit:
            break
    return candidates[:limit]


def canvas_json(course: str, kind: str) -> str:
    nodes = [
        {"id":"course","type":"text","text":course,"x":0,"y":0,"width":260,"height":80,"color":"1"},
        {"id":"overview","type":"file","file":f"02_课程库/{course}/00_课程总览.md","x":-360,"y":150,"width":300,"height":80,"color":"2"},
        {"id":"summary","type":"text","text":"深度文字层\n03_模块总结 / 逐节总结","x":0,"y":150,"width":280,"height":90,"color":"3"},
        {"id":"visual","type":"file","file":f"02_课程库/{course}/04_关键图表与课件索引.md","x":360,"y":150,"width":320,"height":90,"color":"4"},
        {"id":"review","type":"file","file":f"02_课程库/{course}/05_复习与检索练习.md","x":-180,"y":330,"width":320,"height":90,"color":"5"},
        {"id":"verify","type":"file","file":f"02_课程库/{course}/06_验证与不确定项.md","x":220,"y":330,"width":320,"height":90,"color":"6"},
        {"id":"type","type":"text","text":f"课程类型：{kind}\n目标：从纯文字升级为可视化+复习+验证闭环","x":0,"y":500,"width":420,"height":100,"color":"1"},
    ]
    edges = [
        {"id":"e1","fromNode":"course","fromSide":"bottom","toNode":"overview","toSide":"top"},
        {"id":"e2","fromNode":"course","fromSide":"bottom","toNode":"summary","toSide":"top"},
        {"id":"e3","fromNode":"course","fromSide":"bottom","toNode":"visual","toSide":"top"},
        {"id":"e4","fromNode":"summary","fromSide":"bottom","toNode":"review","toSide":"top"},
        {"id":"e5","fromNode":"visual","fromSide":"bottom","toNode":"verify","toSide":"top"},
        {"id":"e6","fromNode":"review","fromSide":"bottom","toNode":"type","toSide":"top"},
        {"id":"e7","fromNode":"verify","fromSide":"bottom","toNode":"type","toSide":"top"},
    ]
    return json.dumps({"nodes":nodes,"edges":edges}, ensure_ascii=False, indent=2) + "\n"


def visual_index(course: str, kind: str, bullets: list[str]) -> str:
    today = date.today().isoformat()
    type_advice = {
        "design":"优先补作品截图、前后对比、视觉原则表、案例拆解图。",
        "technical":"优先补系统流程图、代码/实验步骤、错误排查表。",
        "growth":"优先补漏斗图、指标表、案例拆解、运营动作清单。",
        "learning":"优先补训练路径图、记忆宫殿/复习节奏图、练习表。",
        "general":"优先补课程结构图、关键表格、案例索引。",
    }[kind]
    bullet_rows = "\n".join(f"| {i+1} | {b} | 待补图/表/流程 |" for i,b in enumerate(bullets[:6])) or "| 1 | 待从模块总结抽取 | 待补图/表/流程 |"
    return f'''---
title: "{course} 关键图表与课件索引"
type: visual-index
course: "{course}"
status: draft
created: {today}
updated: {today}
tags:
  - course-visual
  - knowledgeos-v5
  - generated
---

# {course} 关键图表与课件索引

> [!note] 生成说明
> 此页是课程多样化补丁包生成的“视觉层入口”。它不编造图片；没有真实截图时先放索引、表格和 Mermaid 占位，后续再补真实附件。

## 1. 课程类型建议

- 推断类型：`{kind}`
- 升级重点：{type_advice}

## 2. 关键内容候选

| 序号 | 候选内容 | 建议表达形态 |
|---:|---|---|
{bullet_rows}

## 3. 课程结构流程图

```mermaid
flowchart TD
  A[课程输入/素材] --> B[核心概念]
  B --> C[方法步骤]
  C --> D[案例/练习]
  D --> E[复习与行动]
  E --> F[验证与不确定项]
```

## 4. 真实图像/附件索引

| 图像/附件 | 来源 | 说明 | 状态 |
|---|---|---|---|
| 待补充 | 课程截图/课件/PDF | 不编造，等待真实素材 | 待补 |

## 5. 待补视觉材料

- [ ] 课程关键截图
- [ ] 模块关系图
- [ ] 方法流程图
- [ ] 案例对比图/表
'''


def review_practice(course: str, kind: str, bullets: list[str]) -> str:
    today = date.today().isoformat()
    questions = bullets[:5] or ["本课程最核心的概念是什么？", "本课程最可执行的方法是什么？", "如何把课程内容应用到一个真实项目？"]
    q_text = "\n".join(f"### Q{i+1}. {q}\n\n答案：\n" for i,q in enumerate(questions))
    return f'''---
title: "{course} 复习与检索练习"
type: review
course: "{course}"
status: draft
created: {today}
updated: {today}
tags:
  - course-review
  - knowledgeos-v5
  - generated
---

# {course} 复习与检索练习

> 目标：让课程从“看过”变成“能回忆、能复现、能应用”。

## 1. 快速回忆

- [ ] 不看笔记，说出本课程 3 个核心概念。
- [ ] 写下一个最重要的方法步骤。
- [ ] 举一个真实应用场景。

## 2. 检索练习题

{q_text}
## 3. Anki 候选卡

| 正面 | 背面 | 标签 |
|---|---|---|
| {course} 的核心目标是什么？ | 待根据课程总览补充 | {course} |
| {course} 最重要的一个行动步骤是什么？ | 待根据实操工作流补充 | {course} |

## 4. 行动清单

- [ ] 选择一个模块做 15 分钟复盘。
- [ ] 输出一张流程图或表格。
- [ ] 把一个知识点改写成 Anki 卡。
'''


def verification(course: str) -> str:
    today = date.today().isoformat()
    return f'''---
title: "{course} 验证与不确定项"
type: verification
course: "{course}"
status: draft
created: {today}
updated: {today}
tags:
  - course-verification
  - knowledgeos-v5
  - generated
---

# {course} 验证与不确定项

> [!warning] 原则
> 没有素材证据的内容只标记为待核验；不编造来源、截图、课件或外部结论。

## 1. 已有来源入口

- [[01_素材识别报告]]
- [[00_课程总览]]
- [[03_模块总结]] / 逐节总结
- [[07_实操工作流]]
- [[08_术语索引]]

## 2. 来源覆盖表

| 来源类型 | 是否存在 | 覆盖范围 | 可信度 |
|---|---|---|---|
| 课程总览 | 待检查 | 课程定位/模块 | 中 |
| 素材识别报告 | 待检查 | 文件/素材来源 | 中 |
| 模块/逐节总结 | 待检查 | 知识内容 | 中 |
| 课件截图/附件 | 待补 | 视觉证据 | 待核验 |

## 3. 不确定项

> [!warning] 待人工/后续素材确认
> - 是否存在真实课件截图或视频关键帧。
> - 是否有缺失模块、缺失章节或来源不明断言。
> - 是否需要补充外部公开资料交叉验证。

## 4. 过滤记录

| 内容类型 | 处理方式 | 原因 |
|---|---|---|
| 个人信息/营销/二维码 | 过滤或摘要化 | 保护隐私与降低噪音 |
'''


def plan_course(course_dir: Path, vault: Path) -> dict[str, str]:
    course = course_dir.name
    kind = infer_course_type(course)
    source = "\n".join([read_note(course_dir, "00_课程总览.md"), read_note(course_dir, "03_模块总结.md"), read_note(course_dir, "03_课程完整总结.md"), read_note(course_dir, "07_实操工作流.md")])
    bullets = extract_bullets(source)
    return {
        "02_课程地图.canvas": canvas_json(course, kind),
        "04_关键图表与课件索引.md": visual_index(course, kind, bullets),
        "05_复习与检索练习.md": review_practice(course, kind, bullets),
        "06_验证与不确定项.md": verification(course),
    }


def backup_file(path: Path, vault: Path, backup_dir: Path) -> None:
    rel = path.relative_to(vault).as_posix().replace("/", "__")
    backup_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, backup_dir / (rel + ".before"))


def generate(vault: Path, limit: int, apply: bool, backup_dir: Path | None) -> dict:
    course_root = vault / "02_课程库"
    planned: list[PlannedWrite] = []
    dirs = formal_course_dirs(course_root, limit)
    for course_dir in dirs:
        files = plan_course(course_dir, vault)
        for filename, content in files.items():
            target = course_dir / filename
            action = "create" if not target.exists() else "overwrite"
            planned.append(PlannedWrite(course_dir.name, str(target.relative_to(vault)), action, len(content.encode("utf-8"))))
            if apply:
                if target.exists():
                    if backup_dir is None:
                        raise SystemExit("--backup-dir is required when applying over existing files")
                    backup_file(target, vault, backup_dir)
                target.write_text(content, encoding="utf-8")
    return {"vault": str(vault), "apply": apply, "courses": len(dirs), "planned_writes": [asdict(p) for p in planned]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("vault", type=Path)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--backup-dir", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = generate(args.vault, args.limit, args.apply, args.backup_dir)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
