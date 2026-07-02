#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract V6 video keyframes and metadata sidecars.

Safety:
- dry-run by default;
- writes only with --apply;
- never copies the source video;
- metadata starts as B / pending-verification;
- visual verification must promote status/confidence later.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shlex
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass
class KeyframePlan:
    evidence_id: str
    course: str
    source_type: str
    source_path: str
    timestamp: str
    output_path: str
    metadata_path: str
    confidence: str
    status: str
    caption: str
    extractor: str


def parse_timestamps(spec: str) -> list[str]:
    values = []
    for raw in spec.split(','):
        item = raw.strip()
        if not item:
            continue
        parts = item.split(':')
        if len(parts) != 3:
            raise ValueError(f'invalid timestamp: {item}')
        h, m, s = parts
        if not (h.isdigit() and m.isdigit() and s.isdigit()):
            raise ValueError(f'invalid timestamp: {item}')
        if int(m) >= 60 or int(s) >= 60:
            raise ValueError(f'invalid timestamp: {item}')
        values.append(f'{int(h):02d}:{int(m):02d}:{int(s):02d}')
    if not values:
        raise ValueError('no timestamps specified')
    return values


def safe_timestamp(ts: str) -> str:
    return ts.replace(':', '')


def build_plan(video: Path, course: str, timestamps: list[str], output_dir: Path, caption_prefix: str = '') -> list[KeyframePlan]:
    plans: list[KeyframePlan] = []
    video_abs = video.resolve()
    for ts in timestamps:
        h = hashlib.sha1((str(video_abs) + '|' + ts).encode('utf-8')).hexdigest()[:8]
        evidence_id = f'{course}-video-{safe_timestamp(ts)}-{h}'
        out = output_dir / f'{evidence_id}.png'
        meta = output_dir / f'{evidence_id}.json'
        caption = caption_prefix.strip() or f'{Path(video).name} @ {ts} 候选关键帧'
        plans.append(KeyframePlan(
            evidence_id=evidence_id,
            course=course,
            source_type='video',
            source_path=str(video_abs),
            timestamp=ts,
            output_path=str(out),
            metadata_path=str(meta),
            confidence='B',
            status='pending-verification',
            caption=caption,
            extractor='scripts/v6/video_keyframe_extract.py + ffmpeg',
        ))
    return plans


def run_ffmpeg(video: Path, timestamp: str, output_path: Path, ffmpeg_bin: str = 'ffmpeg') -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = shlex.split(ffmpeg_bin) + ['-y', '-ss', timestamp, '-i', str(video), '-frames:v', '1', '-q:v', '2', str(output_path)]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr[-2000:])


def metadata_for(plan: KeyframePlan) -> dict[str, Any]:
    data = asdict(plan)
    data['source_ref'] = {'timestamp': plan.timestamp}
    data['notes'] = [
        'Extracted from local course video.',
        'Pending visual verification; do not treat as A/verified until reviewed.',
    ]
    return data


def extract(video: Path, course: str, timestamps: str, output_dir: Path, apply: bool = False, caption_prefix: str = '', ffmpeg_bin: str = 'ffmpeg') -> dict[str, Any]:
    if not video.exists():
        raise FileNotFoundError(video)
    ts_values = parse_timestamps(timestamps)
    plans = build_plan(video, course, ts_values, output_dir, caption_prefix=caption_prefix)
    result = {'apply': apply, 'video': str(video.resolve()), 'course': course, 'plans': [asdict(p) for p in plans]}
    if apply:
        output_dir.mkdir(parents=True, exist_ok=True)
        for plan in plans:
            run_ffmpeg(video, plan.timestamp, Path(plan.output_path), ffmpeg_bin=ffmpeg_bin)
            Path(plan.metadata_path).write_text(json.dumps(metadata_for(plan), ensure_ascii=False, indent=2), encoding='utf-8')
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('video', type=Path)
    parser.add_argument('--course', required=True)
    parser.add_argument('--timestamps', required=True, help='Comma-separated HH:MM:SS values')
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--caption-prefix', default='')
    parser.add_argument('--ffmpeg-bin', default='ffmpeg')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    result = extract(args.video, args.course, args.timestamps, args.output_dir, apply=args.apply, caption_prefix=args.caption_prefix, ffmpeg_bin=args.ffmpeg_bin)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
