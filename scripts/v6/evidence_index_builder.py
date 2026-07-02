#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build V6 evidence index/gallery notes from metadata sidecars.

Safety:
- dry-run by default;
- writes only with --apply;
- reads metadata JSON under a caller-provided evidence directory;
- does not extract images or copy source files;
- never promotes confidence/status; it renders what metadata already says.
"""
from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


@dataclass
class EvidenceItem:
    evidence_id: str
    course: str
    source_type: str
    source_path: str
    page: int | None
    timestamp: str | None
    output_path: str
    metadata_path: str
    confidence: str
    status: str
    caption: str
    rel_image: str
    rel_metadata: str
    source_file: str


def vault_relative(vault: Path, path_text: str, fallback_base: Path | None = None) -> str:
    p = Path(path_text)
    if not p.is_absolute() and fallback_base is not None:
        p = fallback_base / p
    try:
        return p.resolve().relative_to(vault.resolve()).as_posix()
    except Exception:
        # Windows absolute paths on MSYS may not resolve cleanly; fallback to name under evidence dir.
        if fallback_base is not None:
            candidate = fallback_base / Path(path_text).name
            try:
                return candidate.resolve().relative_to(vault.resolve()).as_posix()
            except Exception:
                return candidate.as_posix()
        return Path(path_text).as_posix()


def load_items(vault: Path, course: str, evidence_dir: Path) -> list[EvidenceItem]:
    items: list[EvidenceItem] = []
    for meta_path in sorted(evidence_dir.glob('*.json')):
        data: dict[str, Any] = json.loads(meta_path.read_text(encoding='utf-8'))
        if data.get('course') != course:
            continue
        output_path = str(data.get('output_path', ''))
        image_rel = vault_relative(vault, output_path, evidence_dir)
        meta_rel = vault_relative(vault, str(meta_path), evidence_dir)
        source_ref = data.get('source_ref') or {}
        page = data.get('page') or source_ref.get('page')
        timestamp = source_ref.get('timestamp')
        items.append(EvidenceItem(
            evidence_id=str(data.get('evidence_id', meta_path.stem)),
            course=course,
            source_type=str(data.get('source_type', 'unknown')),
            source_path=str(data.get('source_path', '')),
            page=int(page) if isinstance(page, int) or (isinstance(page, str) and page.isdigit()) else None,
            timestamp=str(timestamp) if timestamp else None,
            output_path=output_path,
            metadata_path=str(meta_path),
            confidence=str(data.get('confidence', 'C')),
            status=str(data.get('status', 'candidate-only')),
            caption=str(data.get('caption', '待核验')),
            rel_image=image_rel,
            rel_metadata=meta_rel,
            source_file=Path(str(data.get('source_path', ''))).name,
        ))
    return sorted(items, key=lambda x: x.evidence_id)


def ref_text(item: EvidenceItem) -> str:
    if item.page is not None:
        return f"p.{item.page}"
    if item.timestamp:
        return item.timestamp
    return "待补"


def render_index(course: str, items: list[EvidenceItem]) -> str:
    rows = []
    for e in items:
        rows.append(
            f"| `{e.evidence_id}` | {e.source_type} | `{e.source_path}` | {ref_text(e)} | "
            f"`![[{e.rel_image}|180]]` | {e.confidence} | {e.status} | {e.caption} |"
        )
    metadata = '\n'.join(f"- `{e.rel_metadata}`" for e in items) or "- 暂无"
    return f'''---
title: {course}｜11_证据索引
type: evidence-index
course: "{course}"
status: active
created: {date.today().isoformat()}
updated: {date.today().isoformat()}
tags:
  - evidence
  - v6
  - course-verification
---

# {course}｜11_证据索引

> [!warning] 证据边界
> 本页由 V6 metadata sidecars 生成。候选源文件不是证据；只有 metadata 标记为 `verified` 的条目才可视为已核验证据。

## 证据表

| ID | 类型 | 来源 | 页码/时间点 | 输出图片 | 置信度 | 状态 | 说明 |
|---|---|---|---|---|---|---|---|
{chr(10).join(rows)}

## Metadata

{metadata}

## 后续

- [ ] 对 `pending-verification` 或 `candidate-only` 条目继续人工/视觉核验。
- [ ] 将 A/B 级证据回链到课程 Canvas 与关键图表索引。
'''


def render_gallery(course: str, items: list[EvidenceItem]) -> str:
    rows = []
    for e in items:
        rows.append(
            f"| ![[{e.rel_image}|320]] | `{e.source_file}` | {ref_text(e)} | "
            f"{e.confidence} | {e.caption} | `{e.rel_metadata}` |"
        )
    return f'''---
title: {course}｜12_真实截图与关键帧
type: evidence-gallery
course: "{course}"
status: active
created: {date.today().isoformat()}
updated: {date.today().isoformat()}
tags:
  - keyframe
  - screenshot
  - v6
---

# {course}｜12_真实截图与关键帧

> [!important] 不伪造规则
> 本页只嵌入来自本地课程视频/PDF/课件的真实截图或关键帧。条目的置信度/状态来自 metadata sidecar，生成器不会自动升格。

## 已登记图片

| 图片 | 来源 | 页码/时间点 | 置信度 | 用途 | Metadata |
|---|---|---|---|---|---|
{chr(10).join(rows)}
'''


def build(vault: Path, course: str, evidence_dir: Path, apply: bool = False, backup_dir: Path | None = None) -> dict[str, Any]:
    vault = vault.resolve()
    evidence_dir = evidence_dir.resolve()
    course_dir = vault / '02_课程库' / course
    items = load_items(vault, course, evidence_dir)
    index_text = render_index(course, items)
    gallery_text = render_gallery(course, items)
    outputs = {
        'index': course_dir / '11_证据索引.md',
        'gallery': course_dir / '12_真实截图与关键帧.md',
    }
    result = {
        'apply': apply,
        'course': course,
        'evidence_dir': str(evidence_dir),
        'items': [item.__dict__ for item in items],
        'outputs': {k: str(v) for k, v in outputs.items()},
        'previews': {'index': index_text, 'gallery': gallery_text},
    }
    if apply:
        course_dir.mkdir(parents=True, exist_ok=True)
        if backup_dir:
            backup_dir.mkdir(parents=True, exist_ok=True)
        for key, path in outputs.items():
            if path.exists() and backup_dir:
                shutil.copy2(path, backup_dir / f"{path.name}.before")
            path.write_text(index_text if key == 'index' else gallery_text, encoding='utf-8')
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--vault', type=Path, required=True)
    parser.add_argument('--course', required=True)
    parser.add_argument('--evidence-dir', type=Path, required=True)
    parser.add_argument('--backup-dir', type=Path)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    result = build(args.vault, args.course, args.evidence_dir, apply=args.apply, backup_dir=args.backup_dir)
    # Avoid dumping full markdown in normal CLI output; keep machine-readable summary.
    print(json.dumps({k: v for k, v in result.items() if k != 'previews'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
