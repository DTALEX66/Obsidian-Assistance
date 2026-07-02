#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate TALOS OER/open-knowledge crosswalk pages for an Obsidian course.

Safety:
- dry-run by default;
- writes only with --apply;
- only writes inside the selected course directory unless an explicit report dir is used;
- backs up overwritten files when --backup-dir is supplied;
- never creates/claims V6 verified evidence;
- derives structure from existing course notes and marks evidence gaps honestly.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Any

COURSE_ROOT = Path('02_课程库')
OER_ROOT = Path('50_领域知识/开放知识与OER')

TERM_RE = re.compile(r"^- \[\[([^\]]+)\]\]", re.MULTILINE)
HEADING_RE = re.compile(r"^##\s+(.+?)(?:\s+\^[\w-]+)?\s*$", re.MULTILINE)

TECH_TERMS = {
    'rag', 'embedding', 'prompt', 'agent', 'function calling', 'langchain',
    'transformer', 'topk', 'rerank', '向量', '大模型', '模型幻觉', 'llm'
}
LEARNING_TERMS = {'anki', '主动回想', '间断重复', '复习', '卡片', '阅读', '记忆', '费曼'}
DESIGN_TERMS = {'ui', '设计', '版式', '视觉', '组件', '色彩', '排版'}


@dataclass
class CourseAnalysis:
    course: str
    course_dir: str
    overview: str | None
    workflow: str | None
    terms_page: str | None
    project_page: str | None
    evidence_index: str | None
    review_page: str | None
    headings: list[str]
    terms: list[str]
    profile: str
    has_v6_verified: bool
    boundary: str


@dataclass
class GenerationPlan:
    course: str
    apply: bool
    overwrite: bool
    crosswalk_path: str
    faq_path: str
    sample_path: str | None
    analysis: CourseAnalysis
    writes: list[str]


def safe_child(root: Path, child: Path) -> Path:
    root_resolved = root.resolve()
    child_resolved = child.resolve()
    try:
        child_resolved.relative_to(root_resolved)
    except ValueError as exc:
        raise ValueError(f'Unsafe path outside root: {child}') from exc
    return child_resolved


def rel(vault: Path, path: Path | None) -> str | None:
    if path is None or not path.exists():
        return None
    return path.relative_to(vault).as_posix()


def read_text(path: Path | None) -> str:
    if path is None or not path.exists():
        return ''
    return path.read_text(encoding='utf-8', errors='ignore')


def first_existing(paths: list[Path]) -> Path | None:
    for p in paths:
        if p.exists():
            return p
    return None


def classify(text: str, terms: list[str]) -> str:
    lower = text.lower()
    score = { 'techdocs': 0, 'learning': 0, 'design': 0, 'general': 1 }
    for token in TECH_TERMS:
        if token.lower() in lower or any(token.lower() in t.lower() for t in terms):
            score['techdocs'] += 1
    for token in LEARNING_TERMS:
        if token.lower() in lower or any(token.lower() in t.lower() for t in terms):
            score['learning'] += 1
    for token in DESIGN_TERMS:
        if token.lower() in lower or any(token.lower() in t.lower() for t in terms):
            score['design'] += 1
    return max(score, key=score.get)


def analyze_course(vault: Path, course: str) -> CourseAnalysis:
    course_root = safe_child(vault, vault / COURSE_ROOT)
    course_dir = safe_child(course_root, course_root / course)
    if not course_dir.exists():
        raise FileNotFoundError(f'course directory not found: {course_dir}')
    overview = course_dir / '00_课程总览.md'
    if not overview.exists():
        raise FileNotFoundError(f'course overview not found: {overview}')
    workflow = first_existing([
        course_dir / '07_实操工作流.md',
        course_dir / '07_RAG实操工作流.md',
        course_dir / '07_工作流.md',
    ])
    terms_page = course_dir / '08_术语索引.md'
    project_page = course_dir / '13_项目转化.md'
    evidence_index = course_dir / '11_证据索引.md'
    review_page = course_dir / '05_复习与检索练习.md'
    corpus = '\n'.join(read_text(p) for p in [overview, workflow, terms_page, project_page, review_page])
    headings = [h.strip() for h in HEADING_RE.findall(corpus)][:16]
    terms = list(dict.fromkeys(t.strip() for t in TERM_RE.findall(read_text(terms_page))))[:24]
    profile = classify(corpus, terms)
    has_v6_verified = evidence_index.exists() and 'verified' in read_text(evidence_index).lower()
    boundary = '已有 V6 verified 证据，可回链证据索引；外部开放知识仍只作结构参考。' if has_v6_verified else '本课程未检测到 V6 verified 证据；不得伪造截图/关键帧/外部核验。'
    return CourseAnalysis(
        course=course,
        course_dir=rel(vault, course_dir) or str(course_dir),
        overview=rel(vault, overview),
        workflow=rel(vault, workflow),
        terms_page=rel(vault, terms_page),
        project_page=rel(vault, project_page),
        evidence_index=rel(vault, evidence_index),
        review_page=rel(vault, review_page),
        headings=headings,
        terms=terms,
        profile=profile,
        has_v6_verified=has_v6_verified,
        boundary=boundary,
    )


def wiki(path: str | None, label: str) -> str:
    if not path:
        return f'{label}（缺失）'
    stem = path[:-3] if path.endswith('.md') else path
    return f'[[{stem}|{label}]]'


def profile_matrix(profile: str) -> list[tuple[str, str, str, str]]:
    if profile == 'techdocs':
        return [
            ('技术文档', 'MDN Web Docs', '概念、架构、步骤、示例、常见错误、参考', '把工作流文档化为可执行技术说明'),
            ('问答知识库', 'Stack Exchange', '问题、上下文、答案线索、标签、采纳标准', '把复习题升级成可检索 FAQ'),
            ('知识图谱', 'Wikidata', '实体、别名、上位概念、关系、来源', '把术语索引实体化'),
            ('课程作业', 'MIT OCW / Wikiversity', 'Assignment、Project、Rubric、Retro', '把项目页改成作业制交付'),
            ('证据/许可', 'Commons / Wikisource', '来源、作者、许可、版本、时间戳', '仅记录证据状态，不伪造 verified'),
        ]
    if profile == 'learning':
        return [
            ('开放教材', 'OpenStax / Wikibooks', '学习目标、章节、练习、术语表', '把课程改造成教材型学习包'),
            ('课程包', 'MIT OCW / Wikiversity', 'Syllabus、Assignment、Project、Exam', '把学习路线转成任务包'),
            ('问答知识库', 'Stack Exchange', '问题、答案、标签、采纳标准', '把主动回想题沉淀成 FAQ'),
            ('知识图谱', 'Wikidata', '实体、别名、关系、来源', '把术语/方法实体化'),
            ('证据/许可', 'Commons / Wikisource', '来源、许可、版本、媒体元数据', '只引用本地证据或开放许可来源'),
        ]
    if profile == 'design':
        return [
            ('教材结构', 'OpenStax / LibreTexts', '章节、学习目标、练习', '组织设计基础知识'),
            ('开放媒体', 'Wikimedia Commons / Openverse', '作者、许可、来源、媒体元数据', '建立素材授权意识'),
            ('问答知识库', 'Stack Exchange', '问题、答案、标签、采纳标准', '沉淀设计判断 FAQ'),
            ('知识图谱', 'Wikidata', '实体、属性、关系', '组织风格/组件/原则关系'),
            ('课程包', 'MIT OCW / Wikiversity', '作业、项目、Rubric', '把设计练习项目化'),
        ]
    return [
        ('百科模式', 'Wikipedia', '条目、分类、引用、版本历史', '课程概念条目化'),
        ('教材模式', 'OpenStax / Wikibooks', '章节、目标、练习、术语表', '学习结构化'),
        ('课程模式', 'MIT OCW / Wikiversity', 'Syllabus、Assignment、Project', '任务/项目化'),
        ('问答模式', 'Stack Exchange', '问题、答案、标签、采纳标准', '复习问题化'),
        ('图谱模式', 'Wikidata', '实体、属性、关系、来源', '跨课程关系化'),
    ]


def render_crosswalk(analysis: CourseAnalysis, created: str | None = None) -> str:
    created = created or date.today().isoformat()
    rows = '\n'.join(
        f'| {dim} | {site} | {fields} | {action} |'
        for dim, site, fields, action in profile_matrix(analysis.profile)
    )
    term_preview = '、'.join(analysis.terms[:8]) if analysis.terms else '待从术语索引补齐'
    heading_preview = '\n'.join(f'- {h}' for h in analysis.headings[:8]) or '- 待从章节总结补齐'
    return f'''---
type: course-open-knowledge-crosswalk
status: active
course: {analysis.course}
created: {created}
profile: {analysis.profile}
tags:
  - OER
  - open-knowledge
  - generated
---

# {analysis.course} · 开放知识交叉对比

> [!warning] 边界
> {analysis.boundary}

## 来源入口

- 课程总览：{wiki(analysis.overview, '00_课程总览')}
- 工作流：{wiki(analysis.workflow, '工作流')}
- 术语索引：{wiki(analysis.terms_page, '08_术语索引')}
- 复习练习：{wiki(analysis.review_page, '05_复习与检索练习')}
- V7 项目页：{wiki(analysis.project_page, '13_项目转化')}
- V6 证据页：{wiki(analysis.evidence_index, '11_证据索引')}

## 结构对齐矩阵

| 维度 | 参考开放知识模式 | 可吸收字段 | 本课程下一步 |
|---|---|---|---|
{rows}

## 课程结构摘要

{heading_preview}

## 术语实体候选

{term_preview}

## 执行动作

- [ ] 选 3 个核心概念，补“定义 / 上位概念 / 关联术语 / 使用场景”。
- [ ] 选 3 个复习问题，补“上下文 / 答案线索 / 标签 / 采纳标准”。
- [ ] 选 1 个最小项目动作，补“交付物 / 验收标准 / 复盘”。
- [ ] 如缺 V6 evidence，只标记待核验，不升级为 verified。
'''


def render_faq(analysis: CourseAnalysis, created: str | None = None) -> str:
    created = created or date.today().isoformat()
    seeds = analysis.terms[:6] or analysis.headings[:6] or [analysis.course]
    rows = []
    for seed in seeds[:6]:
        rows.append(f'| 如何理解“{seed}”并把它用于一个项目？ | {wiki(analysis.overview, "课程总览")} / {wiki(analysis.terms_page, "术语索引")} | 用课程已有笔记回答；缺证据则标待核验 | {seed} / OER / 复习 | 能给出定义、例子、下一步动作 |')
    rows_text = '\n'.join(rows)
    return f'''---
type: course-faq-hub
status: active
course: {analysis.course}
created: {created}
profile: {analysis.profile}
tags:
  - FAQ
  - StackExchange
  - generated
---

# {analysis.course} · FAQ 问题驱动入口

> [!warning] 边界
> {analysis.boundary}

| 问题 | 上下文 | 答案线索 | 标签 | 采纳标准 |
|---|---|---|---|---|
{rows_text}

## 下一步

- [ ] 把 3 个问题转成复习卡。
- [ ] 为 1 个问题补来源段落或证据链接。
- [ ] 把 1 个问题推进到 V7 项目页的最小交付物。
'''


def render_sample(analysis: CourseAnalysis, created: str | None = None) -> str:
    created = created or date.today().isoformat()
    return f'''---
type: open-knowledge-course-crosswalk-sample
status: active
created: {created}
course: {analysis.course}
profile: {analysis.profile}
tags:
  - OER
  - sample
  - generated
---

# {analysis.course} · OER交叉对比样板

## Profile

- profile: `{analysis.profile}`
- V6 verified: `{analysis.has_v6_verified}`
- boundary: {analysis.boundary}

## 可复制结构

- 交叉对比页：`14_开放知识交叉对比.md`
- FAQ 入口：`15_FAQ问题驱动入口.md`
- 字段：维度、参考模式、可吸收字段、课程下一步、证据边界。
'''


def backup_existing(path: Path, backup_dir: Path | None, vault: Path) -> None:
    if not path.exists() or backup_dir is None:
        return
    rel_path = path.relative_to(vault)
    target = backup_dir / rel_path
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)


def generate(vault: Path, course: str, apply: bool = False, overwrite: bool = False,
             backup_dir: Path | None = None, sample: bool = False) -> dict[str, Any]:
    analysis = analyze_course(vault, course)
    course_dir = safe_child(vault, vault / analysis.course_dir)
    crosswalk = safe_child(course_dir, course_dir / '14_开放知识交叉对比.md')
    faq = safe_child(course_dir, course_dir / '15_FAQ问题驱动入口.md')
    sample_path = None
    if sample:
        sample_dir = safe_child(vault, vault / OER_ROOT)
        sample_dir.mkdir(parents=True, exist_ok=True) if apply else None
        sample_path = safe_child(sample_dir, sample_dir / f'{course}_OER交叉对比样板.md')
    writes = [str(crosswalk), str(faq)] + ([str(sample_path)] if sample_path else [])
    plan = GenerationPlan(
        course=course,
        apply=apply,
        overwrite=overwrite,
        crosswalk_path=str(crosswalk),
        faq_path=str(faq),
        sample_path=str(sample_path) if sample_path else None,
        analysis=analysis,
        writes=writes,
    )
    outputs = {
        str(crosswalk): render_crosswalk(analysis),
        str(faq): render_faq(analysis),
    }
    if sample_path:
        outputs[str(sample_path)] = render_sample(analysis)
    if apply:
        for raw_path, content in outputs.items():
            p = Path(raw_path)
            if p.exists() and not overwrite:
                raise FileExistsError(f'target exists; pass --overwrite to replace: {p}')
            backup_existing(p, backup_dir, vault)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding='utf-8')
    return {'plan': asdict(plan), 'contents': outputs}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--vault', type=Path, required=True)
    parser.add_argument('--course', required=True)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--overwrite', action='store_true')
    parser.add_argument('--backup-dir', type=Path)
    parser.add_argument('--sample', action='store_true', help='also generate a reusable sample under 50_领域知识/开放知识与OER')
    args = parser.parse_args()
    result = generate(args.vault, args.course, apply=args.apply, overwrite=args.overwrite, backup_dir=args.backup_dir, sample=args.sample)
    printable = result['plan']
    print(json.dumps(printable, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
