#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate TALOS V8 retro summaries from Daily Mission notes and outputs.

Read-only by default. With --apply, writes JSON and Markdown reports only.
It never marks tasks done, edits missions, or invents evidence.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Any

try:
    from scripts.v8.training_streak_radar import is_daily_mission_text, parse_mission
except ModuleNotFoundError:  # direct script execution from repo root still works
    from training_streak_radar import is_daily_mission_text, parse_mission  # type: ignore

LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]")
SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


@dataclass
class OutputItem:
    path: str
    title: str
    mission_date: str | None
    course: str | None
    status: str | None


@dataclass
class MissionRetro:
    date: str
    course: str
    path: str
    tasks_done: int
    tasks_total: int
    completion_rate: float
    output_links: list[str]
    evidence_links: list[str]
    next_actions: list[str]
    blockers: list[str]


def frontmatter_value(text: str, key: str) -> str | None:
    m = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", text, flags=re.MULTILINE)
    if not m:
        return None
    return m.group(1).strip().strip('"')


def first_heading(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith('# '):
            return line[2:].strip()
    return fallback


def rel(vault: Path, path: Path) -> str:
    return path.relative_to(vault).as_posix()


def extract_section(text: str, heading_prefix: str) -> str:
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith('## ') and line[3:].strip().startswith(heading_prefix):
            start = i + 1
            break
    if start is None:
        return ''
    end = len(lines)
    for j in range(start, len(lines)):
        if lines[j].startswith('## '):
            end = j
            break
    return '\n'.join(lines[start:end]).strip()


def nonempty_payload_lines(section: str) -> list[str]:
    out = []
    for raw in section.splitlines():
        line = raw.strip()
        if not line or line.startswith('- ['):
            continue
        if line.endswith('：') or line.endswith(':'):
            continue
        if line.startswith('- '):
            out.append(line[2:].strip())
        else:
            out.append(line)
    return out


def collect_outputs(vault: Path) -> list[OutputItem]:
    outputs_dir = vault / '00_主页' / '12_TALOS_Daily_Missions' / 'outputs'
    items: list[OutputItem] = []
    if not outputs_dir.exists():
        return items
    for path in sorted(outputs_dir.glob('*.md')):
        text = path.read_text(encoding='utf-8', errors='ignore')
        items.append(OutputItem(
            path=rel(vault, path),
            title=first_heading(text, path.stem),
            mission_date=frontmatter_value(text, 'mission_date'),
            course=frontmatter_value(text, 'course'),
            status=frontmatter_value(text, 'status'),
        ))
    return items


def mission_retro(vault: Path, path: Path) -> MissionRetro:
    text = path.read_text(encoding='utf-8', errors='ignore')
    stats = parse_mission(path, vault)
    output_links: list[str] = []
    evidence_links: list[str] = []
    for target, label in LINK_RE.findall(text):
        if '12_TALOS_Daily_Missions/outputs/' in target:
            output_links.append(target)
        if '11_证据索引' in target or 'v6-evidence' in target:
            evidence_links.append(target)
    log_section = extract_section(text, '4. Log')
    next_actions = [x for x in nonempty_payload_lines(log_section) if '明天下一步' in x or '下一步' in x]
    blockers = [x for x in nonempty_payload_lines(log_section) if '卡住点' in x or '未声称' in x or '不能' in x]
    return MissionRetro(
        date=stats.date,
        course=stats.course,
        path=stats.path,
        tasks_done=stats.tasks_done,
        tasks_total=stats.tasks_total,
        completion_rate=stats.completion_rate,
        output_links=sorted(set(output_links)),
        evidence_links=sorted(set(evidence_links)),
        next_actions=next_actions,
        blockers=blockers,
    )


def audit(vault: Path) -> dict[str, Any]:
    mission_dir = vault / '00_主页' / '12_TALOS_Daily_Missions'
    retros: list[MissionRetro] = []
    if mission_dir.exists():
        for path in sorted(mission_dir.glob('*.md')):
            text = path.read_text(encoding='utf-8', errors='ignore')
            if is_daily_mission_text(text):
                retros.append(mission_retro(vault, path))
    outputs = collect_outputs(vault)
    tasks_total = sum(r.tasks_total for r in retros)
    tasks_done = sum(r.tasks_done for r in retros)
    course_counts = Counter(r.course for r in retros)
    output_by_date = Counter(o.mission_date or '未标注日期' for o in outputs)
    return {
        'generated_on': date.today().isoformat(),
        'missions': len(retros),
        'outputs': len(outputs),
        'tasks_total': tasks_total,
        'tasks_done': tasks_done,
        'completion_rate': round(tasks_done / tasks_total, 4) if tasks_total else 0.0,
        'course_counts': dict(course_counts),
        'output_by_date': dict(output_by_date),
        'missions_items': [asdict(r) for r in retros],
        'outputs_items': [asdict(o) for o in outputs],
    }


def wikilink(path: str, label: str | None = None) -> str:
    stem = path[:-3] if path.endswith('.md') else path
    return f"[[{stem}|{label or Path(stem).name}]]"


def markdown_report(data: dict[str, Any]) -> str:
    mission_rows = []
    for item in data['missions_items']:
        outputs = ', '.join(wikilink(x) for x in item['output_links']) or '—'
        evidence = ', '.join(wikilink(x) for x in item['evidence_links']) or '—'
        mission_rows.append(
            f"| {wikilink(item['path'], item['date'])} | {item['course']} | {item['tasks_done']}/{item['tasks_total']} | {item['completion_rate']:.0%} | {evidence} | {outputs} |"
        )
    outputs = []
    for item in data['outputs_items']:
        outputs.append(f"- {wikilink(item['path'], item['title'])}｜{item.get('course') or '未标注课程'}｜{item.get('status') or 'unknown'}")
    next_actions = []
    blockers = []
    for item in data['missions_items']:
        next_actions.extend(item['next_actions'])
        blockers.extend(item['blockers'])
    course_lines = '\n'.join(f"- {k}: {v}" for k, v in sorted(data['course_counts'].items())) or '- 暂无'
    return f'''# TALOS V8 自动复盘汇总

## 总览

- Daily Mission：{data['missions']}
- 可见产出：{data['outputs']}
- 任务完成：{data['tasks_done']} / {data['tasks_total']}
- 完成率：{data['completion_rate']:.0%}

## 课程分布

{course_lines}

## Mission 明细

| 日期 | 课程 | 完成 | 完成率 | 证据链接 | 产出链接 |
|---|---|---:|---:|---|---|
{chr(10).join(mission_rows) if mission_rows else '| 暂无 | 暂无 | 0/0 | 0% | — | — |'}

## 可见产出清单

{chr(10).join(outputs) if outputs else '- 暂无'}

## 下一步候选

{chr(10).join('- ' + x for x in next_actions) if next_actions else '- 暂无'}

## 边界 / 卡住点

{chr(10).join('- ' + x for x in blockers) if blockers else '- 暂无'}

## 规则

- 本报告只汇总已经存在的 Daily Mission 和 outputs，不自动勾选任务。
- outputs 必须放在 `00_主页/12_TALOS_Daily_Missions/outputs/`，避免被训练雷达误算为 mission。
- V6 verified 只能来自真实证据页，不得由复盘报告生成。
'''


def write_reports(data: dict[str, Any], output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    jp = output_dir / 'v8-retro-summary.json'
    mp = output_dir / 'v8-retro-summary.md'
    jp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    mp.write_text(markdown_report(data), encoding='utf-8')
    return {'json': str(jp), 'markdown': str(mp)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--vault', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    data = audit(args.vault)
    output = None
    if args.apply:
        if not args.output_dir:
            raise SystemExit('--output-dir is required with --apply')
        output = write_reports(data, args.output_dir)
    print(json.dumps({'apply': args.apply, 'output': output, **{k: v for k, v in data.items() if not k.endswith('_items')}}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
