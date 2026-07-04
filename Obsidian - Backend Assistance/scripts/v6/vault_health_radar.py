#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a V6 evidence health radar for an Obsidian course vault.

Read-only by default. With --apply, writes JSON and Markdown reports to --output-dir.
It summarizes existing metadata sidecars; it never creates evidence or changes course notes.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Any


@dataclass
class CourseHealth:
    course: str
    path: str
    metadata_total: int
    verified_total: int
    pending_total: int
    pdf_total: int
    video_total: int
    other_total: int
    has_index: bool
    has_gallery: bool
    has_visual_index: bool
    status: str
    recommendation: str


def discover_courses(vault: Path, limit: int | None = None) -> list[Path]:
    root = vault / '02_课程库'
    courses = [p for p in sorted(root.iterdir()) if p.is_dir() and (p / '00_课程总览.md').exists()]
    return courses[:limit] if limit else courses


def load_metadata_for_course(vault: Path, course: str) -> list[dict[str, Any]]:
    base = vault / '99_附件' / 'images' / course / 'v6-evidence'
    items: list[dict[str, Any]] = []
    if not base.exists():
        return items
    for p in sorted(base.glob('*.json')):
        try:
            data = json.loads(p.read_text(encoding='utf-8'))
        except Exception as exc:
            data = {'course': course, 'source_type': 'invalid-json', 'status': 'invalid', 'error': str(exc), 'metadata_path': str(p)}
        if data.get('course') == course:
            data.setdefault('metadata_path', str(p))
            items.append(data)
    return items


def status_for(metadata_total: int, verified_total: int, pending_total: int, pdf_total: int, video_total: int) -> tuple[str, str]:
    if metadata_total == 0:
        return 'missing-evidence', '未发现 V6 metadata；需要定位本地 PDF/视频/课件后再抽取证据。'
    if verified_total == 0:
        return 'candidate-only', '已有候选 metadata，但无 verified；需要视觉核验后再升格。'
    if pdf_total > 0 and video_total > 0:
        return 'multimodal-verified', '已有 PDF 页图和视频关键帧；下一步可扩展到更多课程或补项目转化。'
    if pdf_total > 0:
        return 'pdf-verified', '已有 PDF 页图；可继续寻找视频/课件关键帧。'
    if video_total > 0:
        return 'video-verified', '已有视频关键帧；可继续寻找 PDF/课件页图。'
    return 'verified-other', '已有 verified 证据，但类型不是 pdf/video；检查来源类型。'


def audit(vault: Path, limit: int | None = None) -> dict[str, Any]:
    courses = discover_courses(vault, limit=limit)
    rows: list[CourseHealth] = []
    totals = {'metadata': 0, 'verified': 0, 'pending': 0, 'pdf': 0, 'video': 0}
    for course_dir in courses:
        course = course_dir.name
        metas = load_metadata_for_course(vault, course)
        verified = [m for m in metas if m.get('status') == 'verified']
        pending = [m for m in metas if m.get('status') != 'verified']
        pdf = [m for m in metas if m.get('source_type') == 'pdf']
        video = [m for m in metas if m.get('source_type') == 'video']
        other = [m for m in metas if m.get('source_type') not in {'pdf', 'video'}]
        status, rec = status_for(len(metas), len(verified), len(pending), len(pdf), len(video))
        has_visual = False
        visual_path = course_dir / '04_关键图表与课件索引.md'
        if visual_path.exists():
            has_visual = '## V6 真实证据页图' in visual_path.read_text(encoding='utf-8', errors='ignore')
        row = CourseHealth(
            course=course,
            path=str(course_dir),
            metadata_total=len(metas),
            verified_total=len(verified),
            pending_total=len(pending),
            pdf_total=len(pdf),
            video_total=len(video),
            other_total=len(other),
            has_index=(course_dir / '11_证据索引.md').exists(),
            has_gallery=(course_dir / '12_真实截图与关键帧.md').exists(),
            has_visual_index=has_visual,
            status=status,
            recommendation=rec,
        )
        rows.append(row)
        totals['metadata'] += row.metadata_total
        totals['verified'] += row.verified_total
        totals['pending'] += row.pending_total
        totals['pdf'] += row.pdf_total
        totals['video'] += row.video_total
    status_counts: dict[str, int] = {}
    for row in rows:
        status_counts[row.status] = status_counts.get(row.status, 0) + 1
    return {
        'generated': date.today().isoformat(),
        'vault': str(vault),
        'courses_total': len(rows),
        'totals': totals,
        'status_counts': status_counts,
        'courses': [asdict(r) for r in rows],
    }


def markdown_report(data: dict[str, Any]) -> str:
    totals = data.get('totals', {})
    lines = [
        '# V6 Vault Health Radar',
        '',
        '> 本报告只汇总 V6 metadata sidecars，不创建证据、不升格状态。missing 表示未发现真实本地证据 metadata，不代表课程内容不存在。',
        '',
        f"- 生成日期：{data.get('generated')}",
        f"- 课程数：{data.get('courses_total')}",
        f"- metadata：{totals.get('metadata', 0)}",
        f"- verified：{totals.get('verified', 0)}",
        f"- pending/candidate：{totals.get('pending', 0)}",
        f"- PDF 页图：{totals.get('pdf', 0)}",
        f"- 视频关键帧：{totals.get('video', 0)}",
        '',
        '## 状态分布',
        '',
    ]
    for status, count in sorted(data.get('status_counts', {}).items()):
        lines.append(f'- `{status}`: {count}')
    lines += [
        '',
        '## 课程明细',
        '',
        '| 课程 | 状态 | metadata | verified | pending | PDF | video | 11 | 12 | 04 V6 | 建议 |',
        '|---|---|---:|---:|---:|---:|---:|---|---|---|---|',
    ]
    for c in data.get('courses', []):
        lines.append(
            f"| {c['course']} | `{c['status']}` | {c['metadata_total']} | {c['verified_total']} | "
            f"{c['pending_total']} | {c['pdf_total']} | {c['video_total']} | "
            f"{'✅' if c['has_index'] else '—'} | {'✅' if c['has_gallery'] else '—'} | "
            f"{'✅' if c['has_visual_index'] else '—'} | {c['recommendation']} |"
        )
    return '\n'.join(lines).rstrip() + '\n'


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--vault', type=Path, required=True)
    parser.add_argument('--limit', type=int)
    parser.add_argument('--output-dir', type=Path)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    data = audit(args.vault, limit=args.limit)
    if args.apply:
        if not args.output_dir:
            raise SystemExit('--output-dir is required with --apply')
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / 'v6-vault-health-radar.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        (args.output_dir / 'v6-vault-health-radar.md').write_text(markdown_report(data), encoding='utf-8')
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
