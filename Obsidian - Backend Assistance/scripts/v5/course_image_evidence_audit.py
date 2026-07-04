#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit real image evidence for Obsidian courses.

This tool is intentionally conservative: it only counts images that physically exist
inside the vault and are directly under a course folder (or already referenced by
course markdown). It never creates fake image embeds.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}
IMAGE_EMBED_RE = re.compile(r"!\[\[([^\]]+)\]\]|!\[[^\]]*\]\(([^)]+)\)")


@dataclass
class CourseImageEvidence:
    course: str
    path: str
    direct_images: int
    referenced_images: int
    examples: list[str]
    status: str
    recommendation: str


def formal_courses(vault: Path, limit: int) -> list[Path]:
    root = vault / "02_课程库"
    return [p for p in sorted(root.iterdir()) if p.is_dir() and (p / "00_课程总览.md").exists()][:limit]


def all_vault_images(vault: Path) -> list[Path]:
    return [p for p in vault.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTS and ".git" not in p.parts]


def referenced_images(course: Path) -> list[str]:
    refs: list[str] = []
    for md in course.glob("*.md"):
        text = md.read_text(encoding="utf-8", errors="ignore")
        for m in IMAGE_EMBED_RE.finditer(text):
            ref = m.group(1) or m.group(2)
            if ref and Path(ref.split("|")[0]).suffix.lower() in IMAGE_EXTS:
                refs.append(ref)
    return refs


def audit(vault: Path, limit: int = 20) -> dict:
    images = all_vault_images(vault)
    rows: list[CourseImageEvidence] = []
    for c in formal_courses(vault, limit):
        direct = [p for p in images if c in p.parents]
        refs = referenced_images(c)
        total = len(direct) + len(refs)
        status = "has-real-images" if total else "missing-real-images"
        recommendation = (
            "已有真实图片/引用，下一步检查来源标注。"
            if total
            else "未发现可直接归属的真实图片；后续只能从本地课程视频/PDF/课件抽取关键帧，不能编造图片。"
        )
        examples = [str(p.relative_to(vault)) for p in direct[:5]] + refs[:5]
        rows.append(CourseImageEvidence(c.name, str(c.relative_to(vault)), len(direct), len(refs), examples[:8], status, recommendation))
    return {
        "vault": str(vault),
        "total_vault_images": len(images),
        "sample_images": [str(p.relative_to(vault)) for p in images[:30]],
        "audited_courses": len(rows),
        "courses_with_real_images": sum(1 for r in rows if r.status == "has-real-images"),
        "courses_missing_real_images": sum(1 for r in rows if r.status == "missing-real-images"),
        "courses": [asdict(r) for r in rows],
    }


def markdown_report(data: dict) -> str:
    lines = [
        "# 课程图片证据与关键帧采集清单",
        "",
        "> 只统计真实存在或真实引用的图片。没有图片就标记待采集，不用占位图伪装。",
        "",
        "## 总览",
        "",
        f"- vault 图片总数：{data['total_vault_images']}",
        f"- 审计课程数：{data['audited_courses']}",
        f"- 有真实图片课程：{data['courses_with_real_images']}",
        f"- 缺真实图片课程：{data['courses_missing_real_images']}",
        "",
        "## 图片样本",
        "",
    ]
    for p in data["sample_images"]:
        lines.append(f"- `{p}`")
    lines += ["", "## 课程明细", "", "| 课程 | 目录图片 | 引用图片 | 状态 | 建议 |", "|---|---:|---:|---|---|"]
    for c in data["courses"]:
        lines.append(f"| {c['course']} | {c['direct_images']} | {c['referenced_images']} | {c['status']} | {c['recommendation']} |")
    lines += [
        "",
        "## 采集原则",
        "",
        "- 只从本地课程视频、PDF、课件或已授权附件抽取。",
        "- 不从互联网随便找图冒充课程材料。",
        "- 不采集个人隐私、二维码、联系方式、学员名单。",
        "- 每张图应标明来源和用途。",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("vault", type=Path)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--report-dir", type=Path)
    args = parser.parse_args()
    data = audit(args.vault, args.limit)
    if args.report_dir:
        args.report_dir.mkdir(parents=True, exist_ok=True)
        (args.report_dir / "course-image-evidence.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        (args.report_dir / "course-image-evidence.md").write_text(markdown_report(data), encoding="utf-8")
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
