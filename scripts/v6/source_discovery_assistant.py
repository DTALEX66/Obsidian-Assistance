#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Discover local source-file candidates for V6 evidence work.

Read-only by default. With --apply, writes JSON and Markdown reports only.
It never copies source files, extracts media, or creates evidence.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

SOURCE_EXTENSIONS = {
    '.pdf': 'pdf',
    '.mp4': 'video', '.mov': 'video', '.mkv': 'video', '.avi': 'video', '.webm': 'video',
    '.ppt': 'slides', '.pptx': 'slides', '.key': 'slides',
    '.doc': 'document', '.docx': 'document',
    '.png': 'image', '.jpg': 'image', '.jpeg': 'image', '.webp': 'image',
}
STOP_TOKENS = {
    '课程', '训练营', '完结', '基础', '系统', '教学', '训练', '商业', '设计', '视频', '课件',
    'day', 'DAY', 'pdf', 'mp4', 'ppt', 'doc', 'png', 'jpg', 'jpeg', 'webp', 'the', 'and',
}


@dataclass
class SourceCandidate:
    course: str
    source_type: str
    path: str
    filename: str
    score: int
    matched_tokens: list[str]
    confidence: str
    status: str
    rationale: str


def normalize_text(text: str) -> str:
    return re.sub(r'\s+', '', text).lower()


def tokenize_course(course: str) -> list[str]:
    raw = re.split(r'[\s_\-—–:：/\\（）()【】\[\]「」,，.。]+', course)
    tokens: list[str] = []
    for t in raw:
        t = t.strip()
        if not t or t in STOP_TOKENS:
            continue
        if len(t) >= 2:
            tokens.append(t)
    # add full course name for exact high-confidence matches
    compact = re.sub(r'[\s_\-—–:：/\\（）()【】\[\]「」,，.。]+', '', course)
    if len(compact) >= 4:
        tokens.insert(0, compact)
    # de-dupe preserving order
    out = []
    for t in tokens:
        if t not in out:
            out.append(t)
    return out


def discover_files(roots: Iterable[Path], extensions: set[str] | None = None, max_files: int | None = None) -> list[Path]:
    exts = extensions or set(SOURCE_EXTENSIONS)
    files: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for p in root.rglob('*'):
            if p.is_file() and p.suffix.lower() in exts:
                files.append(p)
                if max_files and len(files) >= max_files:
                    return files
    return files


def score_file(course: str, path: Path) -> tuple[int, list[str]]:
    hay = normalize_text(path.as_posix())
    tokens = tokenize_course(course)
    matched = []
    score = 0
    for idx, token in enumerate(tokens):
        n = normalize_text(token)
        if not n:
            continue
        if n in hay:
            matched.append(token)
            score += 5 if idx == 0 else max(1, min(4, len(n) // 2))
    return score, matched


def confidence_for(score: int, matched: list[str]) -> str:
    if score >= 8 or (matched and len(normalize_text(matched[0])) >= 6):
        return 'B'
    if score >= 3:
        return 'C'
    return 'D'


def audit(vault: Path, roots: list[Path], limit: int | None = None, min_score: int = 2, max_files: int | None = None) -> dict:
    course_root = vault / '02_课程库'
    courses = [p.name for p in sorted(course_root.iterdir()) if p.is_dir() and (p / '00_课程总览.md').exists()]
    if limit:
        courses = courses[:limit]
    files = discover_files(roots, max_files=max_files)
    candidates: list[SourceCandidate] = []
    for course in courses:
        for f in files:
            score, matched = score_file(course, f)
            if score < min_score:
                continue
            conf = confidence_for(score, matched)
            candidates.append(SourceCandidate(
                course=course,
                source_type=SOURCE_EXTENSIONS.get(f.suffix.lower(), 'unknown'),
                path=str(f),
                filename=f.name,
                score=score,
                matched_tokens=matched,
                confidence=conf,
                status='candidate-only',
                rationale='文件名/路径与课程关键词匹配；候选不是证据，必须人工打开源文件核验后才能抽取。',
            ))
    candidates.sort(key=lambda c: (-c.score, c.course, c.filename))
    by_course: dict[str, int] = {c: 0 for c in courses}
    strong_by_course: dict[str, int] = {c: 0 for c in courses}
    for c in candidates:
        by_course[c.course] += 1
        if c.confidence == 'B':
            strong_by_course[c.course] += 1
    return {
        'generated': date.today().isoformat(),
        'vault': str(vault),
        'roots': [str(r) for r in roots],
        'courses_total': len(courses),
        'files_scanned': len(files),
        'candidates_total': len(candidates),
        'courses_with_candidates': sum(1 for v in by_course.values() if v),
        'courses_with_strong_candidates': sum(1 for v in strong_by_course.values() if v),
        'by_course': by_course,
        'strong_by_course': strong_by_course,
        'candidates': [asdict(c) for c in candidates],
    }


def markdown_report(data: dict) -> str:
    lines = [
        '# V6 Source Discovery Assistant Report',
        '',
        '> 本报告只列出本地源文件候选。候选不是证据；不得直接把路径/文件名当作课程证据。必须人工打开源文件核验归属，再使用 PDF/视频工具抽取并视觉核验。',
        '',
        f"- 生成日期：{data.get('generated')}",
        f"- 课程数：{data.get('courses_total')}",
        f"- 扫描文件数：{data.get('files_scanned')}",
        f"- 候选总数：{data.get('candidates_total')}",
        f"- 有候选课程：{data.get('courses_with_candidates')}",
        f"- 有强候选课程：{data.get('courses_with_strong_candidates')}",
        '',
        '## 课程候选概览',
        '',
        '| 课程 | 候选数 | 强候选数 |',
        '|---|---:|---:|',
    ]
    for course, count in data.get('by_course', {}).items():
        strong = data.get('strong_by_course', {}).get(course, 0)
        lines.append(f'| {course} | {count} | {strong} |')
    lines += ['', '## 候选明细', '', '| 课程 | 类型 | 分数 | 置信度 | 文件名 | 匹配词 | 路径 |', '|---|---|---:|---|---|---|---|']
    for c in data.get('candidates', []):
        matched = ', '.join(c.get('matched_tokens', []))
        lines.append(f"| {c['course']} | {c['source_type']} | {c['score']} | {c['confidence']} / {c['status']} | `{c['filename']}` | {matched} | `{c['path']}` |")
    return '\n'.join(lines).rstrip() + '\n'


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--vault', type=Path, required=True)
    parser.add_argument('--root', action='append', type=Path, required=True, help='Root to scan; repeatable')
    parser.add_argument('--limit', type=int)
    parser.add_argument('--min-score', type=int, default=2)
    parser.add_argument('--max-files', type=int)
    parser.add_argument('--output-dir', type=Path)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    data = audit(args.vault, args.root, limit=args.limit, min_score=args.min_score, max_files=args.max_files)
    if args.apply:
        if not args.output_dir:
            raise SystemExit('--output-dir is required with --apply')
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / 'v6-source-discovery.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        (args.output_dir / 'v6-source-discovery.md').write_text(markdown_report(data), encoding='utf-8')
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
