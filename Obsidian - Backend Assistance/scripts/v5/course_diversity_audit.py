#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit Obsidian course notes for evidence coverage and content diversity.

Read-only by default. Generates JSON/Markdown reports when --report-dir is set.
This script never edits course files.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

PATTERNS = {
    "images": re.compile(r"!\[\[|!\[[^\]]*\]\("),
    "tables": re.compile(r"^\s*\|.+\|\s*$", re.M),
    "mermaid": re.compile(r"```mermaid"),
    "dataview": re.compile(r"```dataview"),
    "tasks": re.compile(r"^\s*- \[[ xX]\]", re.M),
    "callouts": re.compile(r"^> \[![A-Za-z]", re.M),
    "canvas_links": re.compile(r"\.canvas\b|Canvas|白板"),
    "code_blocks": re.compile(r"```(?!dataview|mermaid)"),
    "review_questions": re.compile(r"复习|Anki|测试|习题|问题|Quiz|选择题|填空|自测|检索练习"),
    "source_evidence": re.compile(r"素材|来源|证据|转写|OCR|PDF|音频|视频|验证|核验|引用"),
    "action_items": re.compile(r"行动|清单|步骤|练习|实操|作业|任务"),
}

RECOMMENDED_MODALITIES = [
    "images",
    "tables",
    "mermaid",
    "dataview",
    "tasks",
    "callouts",
    "canvas_links",
    "review_questions",
    "source_evidence",
    "action_items",
]


@dataclass
class CourseAudit:
    course: str
    path: str
    files: int
    chars: int
    diversity_score: int
    coverage_level: str
    missing_modalities: list[str]
    recommendations: list[str]
    counts: dict[str, int]


def read_course_text(course_dir: Path) -> tuple[str, list[Path]]:
    files = sorted(course_dir.glob("*.md"))
    text = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in files)
    return text, files


def course_dirs(course_root: Path) -> list[Path]:
    # Prefer formal course folders with a 00_课程总览.md file.
    dirs = [p for p in sorted(course_root.iterdir()) if p.is_dir() and (p / "00_课程总览.md").exists()]
    return dirs


def classify(score: int) -> str:
    if score >= 8:
        return "rich"
    if score >= 5:
        return "mixed"
    if score >= 3:
        return "thin"
    return "text-heavy"


def recommendations_for(counts: dict[str, int]) -> list[str]:
    recs: list[str] = []
    if counts.get("images", 0) == 0:
        recs.append("补充课件截图/关键帧/附件索引，至少在总览或配图页中引用。")
    if counts.get("mermaid", 0) == 0:
        recs.append("补充 Mermaid 流程图/时间线/概念关系图，降低纯文字阅读负担。")
    if counts.get("canvas_links", 0) == 0:
        recs.append("补充 Canvas/白板课程地图，展示模块、概念和实践路径。")
    if counts.get("callouts", 0) == 0:
        recs.append("用 callout 区分重点、风险、待验证、不确定来源。")
    if counts.get("tasks", 0) == 0:
        recs.append("加入可执行练习清单，避免课程只停留在摘要。")
    if counts.get("tables", 0) == 0:
        recs.append("加入对照表/模块表/工具表/案例表，提升扫描效率。")
    if counts.get("review_questions", 0) == 0:
        recs.append("补充复习题/检索练习/Anki 卡片入口。")
    if counts.get("source_evidence", 0) == 0:
        recs.append("补充来源/证据/核验说明，标记不确定内容。")
    return recs


def audit_course(course_dir: Path, root: Path) -> CourseAudit:
    text, files = read_course_text(course_dir)
    counts = {name: len(pattern.findall(text)) for name, pattern in PATTERNS.items()}
    score = sum(1 for name in RECOMMENDED_MODALITIES if counts.get(name, 0) > 0)
    missing = [name for name in RECOMMENDED_MODALITIES if counts.get(name, 0) == 0]
    return CourseAudit(
        course=course_dir.name,
        path=str(course_dir.relative_to(root)),
        files=len(files),
        chars=len(text),
        diversity_score=score,
        coverage_level=classify(score),
        missing_modalities=missing,
        recommendations=recommendations_for(counts),
        counts=counts,
    )


def audit_vault(vault: Path, limit: int = 20) -> dict:
    course_root = vault / "02_课程库"
    if not course_root.exists():
        raise SystemExit(f"course root not found: {course_root}")
    dirs = course_dirs(course_root)[:limit]
    audits = [audit_course(d, vault) for d in dirs]
    summary = {
        "vault": str(vault),
        "course_root": str(course_root.relative_to(vault)),
        "course_dirs_total": len(course_dirs(course_root)),
        "audited_courses": len(audits),
        "avg_diversity_score": round(sum(a.diversity_score for a in audits) / len(audits), 2) if audits else 0,
        "coverage_counts": {level: sum(1 for a in audits if a.coverage_level == level) for level in ["rich", "mixed", "thin", "text-heavy"]},
        "courses": [asdict(a) for a in audits],
    }
    return summary


def markdown_report(result: dict) -> str:
    lines = [
        "# 课程内容验证与多样化审计报告",
        "",
        "> 只读审计报告：用于判断课程是否过度依赖纯文字，以及需要补充哪些内容形态。",
        "",
        "## 总览",
        "",
        f"- 审计课程数：{result['audited_courses']}",
        f"- 课程目录总数：{result['course_dirs_total']}",
        f"- 平均多样化分：{result['avg_diversity_score']} / {len(RECOMMENDED_MODALITIES)}",
        f"- 覆盖等级：{result['coverage_counts']}",
        "",
        "## 结论",
        "",
    ]
    text_heavy = result["coverage_counts"].get("text-heavy", 0) + result["coverage_counts"].get("thin", 0)
    if result["audited_courses"] and text_heavy / result["audited_courses"] >= 0.6:
        lines.append("- 当前课程库明显偏纯文字：大多数课程缺少图像、流程图、Canvas、callout、任务清单等结构化形态。")
        lines.append("- 这不适合作为长期 KnowledgeOS 形态；课程至少应具备“来源核验 + 课程地图 + 图表/流程 + 复习/行动”四类辅助结构。")
    else:
        lines.append("- 当前课程库已有一定多样化，但仍可按课程类型补强视觉化和复习结构。")
    lines += ["", "## 课程明细", ""]
    lines.append("| 课程 | 分数 | 等级 | 文件 | 字符 | 缺失重点 |")
    lines.append("|---|---:|---|---:|---:|---|")
    for c in result["courses"]:
        missing = ", ".join(c["missing_modalities"][:5])
        lines.append(f"| {c['course']} | {c['diversity_score']} | {c['coverage_level']} | {c['files']} | {c['chars']} | {missing} |")
    lines += ["", "## 每门课建议", ""]
    for c in result["courses"]:
        lines.append(f"### {c['course']}")
        lines.append(f"- 路径：`{c['path']}`")
        lines.append(f"- 多样化分：{c['diversity_score']} / {len(RECOMMENDED_MODALITIES)}（{c['coverage_level']}）")
        lines.append("- 形态计数：`" + json.dumps(c["counts"], ensure_ascii=False) + "`")
        if c["recommendations"]:
            for rec in c["recommendations"][:6]:
                lines.append(f"  - {rec}")
        else:
            lines.append("  - 当前形态较丰富，建议进一步做课程级 Canvas 和复习闭环。")
        lines.append("")
    lines += [
        "## 推荐最低标准",
        "",
        "每门正式课程至少应具备：",
        "",
        "1. `00_课程总览.md`：课程定位、模块、来源、适用人群。",
        "2. `02_课程地图.canvas` 或 Mermaid：模块/概念/实践路径关系。",
        "3. `03_模块总结.md` 或逐节总结：保留文字深度。",
        "4. `04_关键图表与课件索引.md`：截图/附件/表格/关键帧入口。",
        "5. `05_复习与检索练习.md`：问题、Anki、行动清单。",
        "6. `06_验证与不确定项.md`：来源、证据、待人工确认。",
    ]
    return "\n".join(lines) + "\n"


def write_reports(result: dict, report_dir: Path) -> dict:
    report_dir.mkdir(parents=True, exist_ok=True)
    json_path = report_dir / "course-diversity-audit.json"
    md_path = report_dir / "course-diversity-audit.md"
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(markdown_report(result), encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("vault", type=Path)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--report-dir", type=Path)
    args = parser.parse_args()
    result = audit_vault(args.vault, limit=args.limit)
    if args.report_dir:
        result["reports"] = write_reports(result, args.report_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
