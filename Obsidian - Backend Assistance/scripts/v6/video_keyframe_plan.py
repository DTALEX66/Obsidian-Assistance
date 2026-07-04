#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Plan V6 video keyframe evidence candidates without extracting frames.

Safety:
- read-only by default;
- does not copy videos or extract frames;
- filename/path matching produces candidate-only plans, not evidence;
- optional markdown/json report output requires --output-dir and --apply;
- later extraction must record timestamp and visual verification before promoting to A/verified.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

VIDEO_EXTS = {'.mp4', '.mov', '.mkv', '.avi', '.webm', '.mpeg', '.mpg', '.m4v'}
GENERIC_TOKENS = {'课程', '教程', '训练', '训练营', '合集', '计划', '实战', '介绍', '基础', '系统'}


@dataclass
class VideoCandidate:
    course: str
    path: str
    ext: str
    size: int
    matched_tokens: list[str]
    score: int
    status: str
    confidence: str
    recommended_timestamps: list[str]
    note: str


def tokenize_course(course: str) -> list[str]:
    raw = {course}
    separators = ['与', '和', '全', 'AI', 'AIGC', '商业', '设计', '运营', '记忆', '心理学', '算法', '大模型', '新媒体', '视觉', '美术', '版式', '课程', '教程', '训练营', '训练', '实战']
    for sep in separators:
        for x in list(raw):
            for y in x.split(sep):
                if len(y) >= 2:
                    raw.add(y)
    tokens = []
    for t in raw:
        t = t.strip().lower()
        if len(t) < 2 or t in GENERIC_TOKENS:
            continue
        tokens.append(t)
    return sorted(set(tokens), key=len, reverse=True)


def iter_videos(roots: Iterable[Path]) -> list[Path]:
    videos: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for p in root.rglob('*'):
            if p.is_file() and p.suffix.lower() in VIDEO_EXTS and '.git' not in p.parts:
                videos.append(p)
    return sorted(videos)


def score_video(course: str, video: Path) -> tuple[int, list[str]]:
    hay = video.as_posix().lower()
    tokens = tokenize_course(course)
    matched = [t for t in tokens if t in hay]
    score = sum(len(t) for t in matched)
    # Strong full-name match gets a large bonus.
    if course.lower() in hay:
        score += 100
    return score, matched


def audit(courses: list[str], roots: list[Path], limit_per_course: int = 5, min_score: int = 4) -> dict:
    videos = iter_videos(roots)
    rows: list[dict] = []
    for course in courses:
        hits: list[VideoCandidate] = []
        for video in videos:
            score, matched = score_video(course, video)
            if score >= min_score:
                hits.append(VideoCandidate(
                    course=course,
                    path=video.as_posix(),
                    ext=video.suffix.lower(),
                    size=video.stat().st_size,
                    matched_tokens=matched,
                    score=score,
                    status='candidate-only',
                    confidence='C',
                    recommended_timestamps=['00:00:05', '00:01:00', '00:03:00'],
                    note='Filename/path match only. Open video and visually verify before extracting frames.',
                ))
        if hits:
            hits = sorted(hits, key=lambda x: (-x.score, x.path))[:limit_per_course]
            rows.append({'course': course, 'candidates': [asdict(h) for h in hits]})
    return {
        'generated': date.today().isoformat(),
        'video_total': len(videos),
        'matched_courses': len(rows),
        'rows': rows,
        'boundary': 'candidate-only; not evidence until timestamp extraction and visual verification',
    }


def markdown_report(data: dict) -> str:
    lines = [
        '# V6 视频关键帧候选计划',
        '',
        '> 本报告只记录本地视频候选与建议核验时间点。候选不是证据；未抽帧、未视觉核验前不得写入 `A/verified`。',
        '',
        f"- 生成日期：{data.get('generated')}",
        f"- 本地视频总数：{data.get('video_total')}",
        f"- 命中课程数：{data.get('matched_courses')}",
        '',
    ]
    for row in data.get('rows', []):
        lines += [f"## {row['course']}", '', '| 文件 | 匹配 | 建议时间点 | 状态 | 说明 |', '|---|---|---|---|---|']
        for c in row.get('candidates', []):
            lines.append(f"| `{c['path']}` | {', '.join(c['matched_tokens'])} | {', '.join(c['recommended_timestamps'])} | {c['status']} / {c['confidence']} | {c['note']} |")
        lines.append('')
    if not data.get('rows'):
        lines.append('未发现达到阈值的本地视频候选。')
    return '\n'.join(lines).rstrip() + '\n'


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--courses-file', type=Path, help='UTF-8 text file, one course per line')
    parser.add_argument('--course', action='append', default=[])
    parser.add_argument('--root', action='append', required=True)
    parser.add_argument('--min-score', type=int, default=4)
    parser.add_argument('--limit-per-course', type=int, default=5)
    parser.add_argument('--output-dir', type=Path)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    courses = list(args.course)
    if args.courses_file:
        courses += [line.strip() for line in args.courses_file.read_text(encoding='utf-8').splitlines() if line.strip()]
    data = audit(courses, [Path(r) for r in args.root], limit_per_course=args.limit_per_course, min_score=args.min_score)
    if args.apply:
        if not args.output_dir:
            raise SystemExit('--output-dir is required with --apply')
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / 'video-keyframe-plan.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        (args.output_dir / 'video-keyframe-plan.md').write_text(markdown_report(data), encoding='utf-8')
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
