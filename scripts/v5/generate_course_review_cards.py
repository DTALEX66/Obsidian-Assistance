#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate V5 active-recall review cards for formal Obsidian courses.

Safety:
- dry-run by default;
- writes only with --apply;
- writes only under 04_复习卡片/V5课程多样化 and appends links to 05_复习与检索练习.md;
- does not modify course body/source notes.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path


@dataclass
class PlannedCard:
    course: str
    path: str
    question: str
    action: str


def safe_name(text: str, max_len: int = 34) -> str:
    return re.sub(r'[\\/:*?"<>|]+', "_", text)[:max_len]


def formal_courses(vault: Path, limit: int) -> list[Path]:
    root = vault / "02_课程库"
    return [p for p in sorted(root.iterdir()) if p.is_dir() and (p / "00_课程总览.md").exists()][:limit]


def course_has_cards(review_root: Path, course: str) -> bool:
    return any(p.name.startswith(course + "_") for p in review_root.glob("*.md"))


def prompts_for(course: str) -> list[str]:
    if any(k in course for k in ["运营", "新媒体", "转岗"]):
        return ["本课程的运营闭环如何运转？", "哪些动作可以转成可量化指标？", "哪些案例或结论需要补来源验证？"]
    if any(k in course for k in ["记忆", "思维导图", "学习", "考霸", "大脑"]):
        return ["本课程的训练路径如何安排？", "如何把方法转成每日练习？", "哪些结论需要回到原素材核验？"]
    if any(k in course for k in ["设计", "视觉", "美术", "版式", "UI", "品牌", "Photoshop"]):
        return ["本课程的视觉原则如何落到作品检查？", "哪些案例需要真实图片或参考页支撑？", "如何把课程内容转成设计练习清单？"]
    if any(k in course for k in ["模型", "算法", "开发"]):
        return ["本课程的技术流程如何画成流程图？", "哪些步骤需要实验或截图验证？", "如何判断方法是否真的可复现？"]
    return ["本课程最核心的方法是什么？", "如何把本课程转成行动清单？", "哪些内容仍需来源核验？"]


def card_text(course: str, question: str) -> str:
    today = date.today().isoformat()
    return f'''---
title: "{course}：{question}"
type: review-card
course: "{course}"
status: draft
created: {today}
updated: {today}
tags:
  - review-card
  - course-review
  - knowledgeos-v5
source_note: "02_课程库/{course}/00_课程总览.md"
---

# {course}：{question}

## 正面

{course}：{question}

## 背面

先检索 [[02_课程库/{course}/00_课程总览|课程总览]]、[[02_课程库/{course}/04_关键图表与课件索引|关键图表]]、[[02_课程库/{course}/06_验证与不确定项|验证页]]，再用自己的话回答。没有真实来源或图片时标记为待核验。

## 来源与边界

- 课程：[[02_课程库/{course}/00_课程总览|{course}]]
- 主动回忆候选卡；不新增课程事实。

## 复习记录

- [ ] 第一次回忆
- [ ] 24小时后复习
- [ ] 7天后复习
'''


def generate(vault: Path, limit: int = 20, apply: bool = False, backup_dir: Path | None = None, skip_existing: bool = True) -> dict:
    review_root = vault / "04_复习卡片" / "V5课程多样化"
    planned: list[PlannedCard] = []
    for course_dir in formal_courses(vault, limit):
        course = course_dir.name
        if skip_existing and review_root.exists() and course_has_cards(review_root, course):
            continue
        links: list[str] = []
        for idx, question in enumerate(prompts_for(course), 1):
            stem = f"{course}_{idx:02d}_{safe_name(question)}"
            target = review_root / f"{stem}.md"
            action = "overwrite" if target.exists() else "create"
            planned.append(PlannedCard(course, str(target.relative_to(vault)), question, action))
            links.append(f"- [[04_复习卡片/V5课程多样化/{stem}|{course}：{question}]]")
            if apply:
                review_root.mkdir(parents=True, exist_ok=True)
                if target.exists() and backup_dir:
                    backup_dir.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(target, backup_dir / (target.name + ".before"))
                target.write_text(card_text(course, question), encoding="utf-8")
        review_page = course_dir / "05_复习与检索练习.md"
        if apply and links and review_page.exists():
            text = review_page.read_text(encoding="utf-8", errors="ignore")
            marker = "## 7. V5 独立复习卡片入口（20轮自动任务）"
            if marker not in text:
                if backup_dir:
                    backup_dir.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(review_page, backup_dir / (course + "__05.before"))
                review_page.write_text(text.rstrip() + "\n\n" + marker + "\n\n" + "\n".join(links) + "\n", encoding="utf-8")
    return {"vault": str(vault), "apply": apply, "planned_cards": [asdict(p) for p in planned]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("vault", type=Path)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--backup-dir", type=Path)
    parser.add_argument("--include-existing", action="store_true", help="Generate even if course already has V5 review cards")
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
