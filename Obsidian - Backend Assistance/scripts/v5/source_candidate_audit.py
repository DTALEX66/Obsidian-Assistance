#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Find local source-file candidates for Obsidian course keyframes.

Conservative: filename/path matching only. Results are candidates, not evidence.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

EXTS = {'.pdf', '.mp4', '.mov', '.mkv', '.avi', '.ppt', '.pptx', '.docx', '.png', '.jpg', '.jpeg', '.webp'}


def formal_courses(vault: Path, limit: int) -> list[Path]:
    root = vault / '02_课程库'
    return [p for p in sorted(root.iterdir()) if p.is_dir() and (p / '00_课程总览.md').exists()][:limit]


def tokens(course: str) -> list[str]:
    parts = {course.lower()}
    for sep in ['与', '和', '全', 'AI', 'AIGC', '训练', '设计', '运营', '记忆', '课程']:
        for item in list(parts):
            parts.update(x.lower() for x in item.split(sep) if len(x) >= 2)
    return sorted(parts, key=len, reverse=True)


def collect_files(roots: list[Path], max_files: int = 20000) -> list[Path]:
    found: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for p in root.rglob('*'):
            if p.is_file() and p.suffix.lower() in EXTS and '.git' not in p.parts:
                found.append(p)
                if len(found) >= max_files:
                    return found
    return found


def audit(vault: Path, roots: list[Path], limit: int = 20, max_files: int = 20000) -> dict:
    files = collect_files(roots, max_files=max_files)
    courses = []
    for course_dir in formal_courses(vault, limit):
        course = course_dir.name
        toks = tokens(course)
        hits = []
        for f in files:
            path = f.as_posix().lower()
            score = sum(1 for t in toks if t in path)
            if score:
                hits.append({'path': f.as_posix(), 'ext': f.suffix.lower(), 'score': score})
        hits = sorted(hits, key=lambda x: (-x['score'], x['path']))[:20]
        courses.append({'course': course, 'candidates': hits})
    return {'vault': str(vault), 'roots': [str(r) for r in roots], 'files_scanned': len(files), 'courses': courses}


def markdown_report(data: dict) -> str:
    lines = ['# 本地源文件候选扫描', '', '> 文件名/路径匹配结果只是候选未核验，不是课程证据。', '']
    for r in data['courses']:
        lines.append(f"## {r['course']}")
        if not r['candidates']:
            lines.append('- 未发现明显候选。')
        else:
            for h in r['candidates'][:10]:
                lines.append(f"- `{h['path']}` · score={h['score']}")
        lines.append('')
    return '\n'.join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('vault', type=Path)
    parser.add_argument('--root', action='append', type=Path, required=True)
    parser.add_argument('--limit', type=int, default=20)
    parser.add_argument('--max-files', type=int, default=20000)
    parser.add_argument('--report-dir', type=Path)
    args = parser.parse_args()
    data = audit(args.vault, args.root, limit=args.limit, max_files=args.max_files)
    print(json.dumps(data, ensure_ascii=False, indent=2))
    if args.report_dir:
        args.report_dir.mkdir(parents=True, exist_ok=True)
        (args.report_dir / 'source-candidates.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        (args.report_dir / 'source-candidates.md').write_text(markdown_report(data), encoding='utf-8')


if __name__ == '__main__':
    main()
