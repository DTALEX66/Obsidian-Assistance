#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import argparse
from pathlib import Path
from datetime import date


def frontmatter(course):
    today=date.today().isoformat()
    return "\n".join([
        "---", "type: visual", "status: done", f"course: \"{course}\"", "lesson: \"\"",
        "source_type: generated", "source_path: \"\"", "evidence_id: generated", "confidence: medium",
        "review_level: new", "difficulty: 1", "priority: 1", f"created: \"{today}\"", f"updated: \"{today}\"",
        "tags:", "  - knowledgeos", "aliases: []", "links:", "  concepts: []", "  methods: []", "  cases: []",
        "cssclasses:", "  - knowledgeos-v4", "---", ""
    ])


def build_graphs(course):
    fm=frontmatter(course)
    return {
        "课程流程图.md": fm+f"# {course}｜课程流程图\n\n```mermaid\nflowchart TD\n  A[输入素材] --> B[素材识别]\n  B --> C[核验]\n  C --> D[生成学习卡片]\n  D --> E[复习与行动]\n```\n",
        "课程思维导图.md": fm+f"# {course}｜课程思维导图\n\n```mermaid\nmindmap\n  root(({course}))\n    概念\n    方法\n    案例\n    复习\n    行动\n```\n",
        "课程时间线.md": fm+f"# {course}｜课程时间线\n\n```mermaid\ntimeline\n  title {course} 学习时间线\n  阶段一 : 素材识别\n  阶段二 : 内容核验\n  阶段三 : 卡片生成\n  阶段四 : 复习行动\n```\n",
    }


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--course",required=True); ap.add_argument("--output",required=True); args=ap.parse_args()
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    graphs=build_graphs(args.course)
    for name,content in graphs.items(): (out/name).write_text(content,encoding="utf-8",newline="\n")
    print(f"wrote {len(graphs)} mermaid files to {out}")

if __name__ == "__main__":
    main()
