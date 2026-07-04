#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update course visual index (`04_关键图表与课件索引.md`) from V6 metadata sidecars.

Safety:
- dry-run by default;
- writes only with --apply;
- renders metadata as-is and never promotes confidence/status;
- only updates the dedicated `## V6 真实证据页图` section.
"""
from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SECTION_TITLE = '## V6 真实证据页图'


@dataclass
class VisualItem:
    evidence_id: str
    source_type: str
    source_file: str
    ref: str
    confidence: str
    status: str
    caption: str
    rel_image: str
    rel_metadata: str


def vault_relative(vault: Path, path_text: str, fallback_base: Path | None = None) -> str:
    p = Path(path_text)
    if not p.is_absolute() and fallback_base is not None:
        p = fallback_base / p
    try:
        return p.resolve().relative_to(vault.resolve()).as_posix()
    except Exception:
        if fallback_base is not None:
            candidate = fallback_base / Path(path_text).name
            try:
                return candidate.resolve().relative_to(vault.resolve()).as_posix()
            except Exception:
                return candidate.as_posix()
        return Path(path_text).as_posix()


def item_ref(data: dict[str, Any]) -> str:
    if data.get('page'):
        return f"p.{data['page']}"
    ref = data.get('source_ref') or {}
    if ref.get('timestamp'):
        return str(ref['timestamp'])
    if data.get('timestamp'):
        return str(data['timestamp'])
    return '待补'


def load_items(vault: Path, course: str, evidence_dir: Path, verified_only: bool = False) -> list[VisualItem]:
    items: list[VisualItem] = []
    for meta_path in sorted(evidence_dir.glob('*.json')):
        data = json.loads(meta_path.read_text(encoding='utf-8'))
        if data.get('course') != course:
            continue
        if verified_only and data.get('status') != 'verified':
            continue
        output_path = str(data.get('output_path', ''))
        items.append(VisualItem(
            evidence_id=str(data.get('evidence_id', meta_path.stem)),
            source_type=str(data.get('source_type', 'unknown')),
            source_file=Path(str(data.get('source_path', ''))).name,
            ref=item_ref(data),
            confidence=str(data.get('confidence', 'C')),
            status=str(data.get('status', 'candidate-only')),
            caption=str(data.get('caption', '')),
            rel_image=vault_relative(vault, output_path, evidence_dir),
            rel_metadata=vault_relative(vault, str(meta_path), evidence_dir),
        ))
    return sorted(items, key=lambda x: (x.source_type, x.evidence_id))


def render_section(course: str, items: list[VisualItem]) -> str:
    rows = []
    for e in items:
        rows.append(
            f"| ![[{e.rel_image}|180]] | {e.source_type} | `{e.source_file}` | {e.ref} | "
            f"{e.confidence} | {e.status} | [[02_课程库/{course}/11_证据索引|证据索引]] · "
            f"[[02_课程库/{course}/12_真实截图与关键帧|真实截图与关键帧]] |"
        )
    body = '\n'.join(rows) if rows else '| 暂无 | - | - | - | - | - | - |'
    return f'''{SECTION_TITLE}

| 图像 | 类型 | 来源 | 页码/时间点 | 置信度 | 状态 | 链接 |
|---|---|---|---:|---|---|---|
{body}

> 以上图像来自 V6 metadata sidecars。候选不是证据；本工具不会提升置信度/状态。`11_证据索引.md` 与 `12_真实截图与关键帧.md` 应由 `scripts/v6/evidence_index_builder.py` 从同一 metadata 自动生成。
'''


def replace_section(text: str, section: str) -> str:
    if SECTION_TITLE not in text:
        return text.rstrip() + '\n\n' + section
    before = text.split(SECTION_TITLE, 1)[0].rstrip()
    return before + '\n\n' + section


def update(vault: Path, course: str, evidence_dir: Path, apply: bool = False, backup_dir: Path | None = None, verified_only: bool = False) -> dict[str, Any]:
    vault = vault.resolve()
    evidence_dir = evidence_dir.resolve()
    target = vault / '02_课程库' / course / '04_关键图表与课件索引.md'
    items = load_items(vault, course, evidence_dir, verified_only=verified_only)
    section = render_section(course, items)
    old_text = target.read_text(encoding='utf-8', errors='ignore') if target.exists() else f'# {course}｜关键图表与课件索引\n'
    new_text = replace_section(old_text, section)
    result = {
        'apply': apply,
        'course': course,
        'target': str(target),
        'items': [item.__dict__ for item in items],
        'preview': new_text,
    }
    if apply:
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and backup_dir:
            backup_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, backup_dir / f'{target.name}.before')
        target.write_text(new_text, encoding='utf-8')
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--vault', type=Path, required=True)
    parser.add_argument('--course', required=True)
    parser.add_argument('--evidence-dir', type=Path, required=True)
    parser.add_argument('--backup-dir', type=Path)
    parser.add_argument('--verified-only', action='store_true')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    result = update(args.vault, args.course, args.evidence_dir, apply=args.apply, backup_dir=args.backup_dir, verified_only=args.verified_only)
    print(json.dumps({k: v for k, v in result.items() if k != 'preview'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
