#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V10 Cognitive Vault Garden audit.

Adapted from Cognitive-Loop-OS shared modules:
- shared/auto_tagger.py: zero-dependency keyword/tag/atomicity helpers
- shared/backlinks.py: Obsidian-style wikilink/embed/markdown-link parsing
- shared/knowledge_gardener.py: orphan detection, connection suggestions, thin-topic radar

This script is tailored for Obsidian-Assistance:
- read-only by default;
- with --apply it writes JSON/Markdown reports only;
- it never edits notes, creates evidence, deletes files, or scans source media by default.
"""
from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Any, Iterable

DEFAULT_INCLUDE_DIRS = (
    "02_课程库",
    "03_知识卡片",
    "04_复习卡片",
    "50_领域知识",
    "80_索引数据库",
)
SKIP_DIR_NAMES = {
    ".git",
    ".obsidian",
    "__pycache__",
    "node_modules",
    "backups",
    ".pytest_cache",
    ".ruff_cache",
}
MEDIA_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
    ".svg",
    ".pdf",
    ".mp3",
    ".mp4",
    ".mov",
    ".mkv",
    ".avi",
    ".wav",
    ".ppt",
    ".pptx",
}
STOP_WORDS = {
    "the",
    "a",
    "an",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "have",
    "has",
    "had",
    "do",
    "does",
    "did",
    "will",
    "would",
    "could",
    "should",
    "may",
    "might",
    "can",
    "shall",
    "to",
    "of",
    "in",
    "for",
    "on",
    "with",
    "at",
    "by",
    "from",
    "as",
    "into",
    "through",
    "during",
    "before",
    "after",
    "above",
    "below",
    "between",
    "under",
    "again",
    "further",
    "then",
    "once",
    "here",
    "there",
    "when",
    "where",
    "why",
    "how",
    "all",
    "both",
    "each",
    "few",
    "more",
    "most",
    "other",
    "some",
    "such",
    "no",
    "nor",
    "not",
    "only",
    "own",
    "same",
    "so",
    "than",
    "too",
    "very",
    "just",
    "because",
    "but",
    "and",
    "or",
    "if",
    "while",
    "this",
    "that",
    "these",
    "those",
    "it",
    "its",
    "he",
    "she",
    "they",
    "them",
    "we",
    "you",
    "i",
    "me",
    "my",
    "your",
    "our",
    "his",
    "her",
    "的",
    "了",
    "在",
    "是",
    "我",
    "有",
    "和",
    "就",
    "不",
    "人",
    "都",
    "一",
    "一个",
    "上",
    "也",
    "很",
    "到",
    "说",
    "要",
    "去",
    "你",
    "会",
    "着",
    "没有",
    "看",
    "好",
    "自己",
    "这",
    "他",
    "她",
    "它",
    "们",
    "那",
    "什么",
    "怎么",
    "如果",
    "因为",
    "所以",
    "但是",
    "可以",
    "这个",
    "那个",
    "已经",
    "还是",
    "或者",
    "虽然",
    "然后",
    "并且",
    "而且",
    "不过",
    "只是",
    "就是",
    "的话",
    "不能",
    "不要",
    "课程",
    "知识",
    "学习",
    "训练",
    "总结",
    "索引",
    "报告",
    "项目",
    "复习",
    "卡片",
}
DOMAIN_SIGNALS: dict[str, list[str]] = {
    "machine-learning": ["neural", "training", "model", "gradient", "loss", "dataset", "机器学习", "模型", "训练"],
    "programming": ["function", "class", "code", "api", "import", "def ", "return", "编程", "代码", "接口"],
    "design": ["color", "layout", "typography", "ui", "ux", "font", "spacing", "设计", "视觉", "版式", "组件"],
    "psychology": ["cognitive", "behavior", "memory", "learning", "bias", "emotion", "记忆", "认知", "心理"],
    "data-science": ["data", "analysis", "visualization", "statistics", "pipeline", "数据", "分析", "可视化"],
    "devops": ["docker", "deploy", "ci", "cd", "pipeline", "kubernetes", "部署", "流水线"],
    "obsidian": ["obsidian", "markdown", "dataview", "wikilink", "vault", "双链", "笔记"],
}
WIKILINK_RE = re.compile(r"(?<!!)\[\[([^\]|#]+?)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]")
EMBED_RE = re.compile(r"!\[\[([^\]|#]+?)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]")
MD_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


@dataclass
class LinkRef:
    target: str
    alias: str
    is_embed: bool
    link_type: str


@dataclass
class NoteRecord:
    path: str
    title: str
    chars: int
    tags: list[str]
    suggested_tags: list[str]
    keywords: list[str]
    outgoing: list[str]
    embeds: list[str]
    md_links: list[str]
    unresolved: list[str]
    incoming_count: int
    outgoing_count: int
    is_atomic: bool
    topic_count: int
    confidence: float


def tokenize(text: str) -> list[str]:
    tokens = re.findall(r"[a-zA-Z\u4e00-\u9fff]+", text.lower())
    return [t for t in tokens if len(t) > 1 and t not in STOP_WORDS]


def extract_keywords(text: str, top_k: int = 10) -> list[dict[str, Any]]:
    tokens = tokenize(text)
    if not tokens:
        return []
    tf = Counter(tokens)
    total = len(tokens)
    keywords = []
    for word, count in tf.most_common(top_k * 2):
        score = (count / total) * (1 + math.log(len(word)))
        keywords.append({"keyword": word, "score": round(score, 4), "count": count})
    keywords.sort(key=lambda k: k["score"], reverse=True)
    return keywords[:top_k]


def suggest_tags(text: str, max_tags: int = 8) -> list[str]:
    keywords = extract_keywords(text, top_k=15)
    tags = [k["keyword"] for k in keywords[:max_tags]]
    lower = text.lower()
    for domain, signals in DOMAIN_SIGNALS.items():
        if any(signal in lower for signal in signals):
            tags.insert(0, domain)
    return list(dict.fromkeys(tags))[:max_tags]


def detect_atomicity(text: str) -> dict[str, Any]:
    tokens = tokenize(text)
    headings = len(re.findall(r"^#{1,6}\s+", text, flags=re.MULTILINE))
    shift_markers = len(re.findall(r"\b(however|meanwhile|另外|同时|但是|另一方面|其次|第三)\b", text, flags=re.IGNORECASE))
    topic_count = max(1, min(10, headings + shift_markers))
    is_atomic = len(tokens) < 220 and topic_count <= 2
    confidence = 0.85 if is_atomic else 0.55
    suggestions = []
    if headings > 2:
        suggestions.append("multiple_headings")
    if shift_markers > 1:
        suggestions.append("multiple_topic_shifts")
    if len(tokens) >= 220:
        suggestions.append("long_note")
    return {
        "is_atomic": is_atomic,
        "topic_count": topic_count,
        "suggested_splits": suggestions,
        "confidence": confidence,
    }


def progressive_summarize(text: str) -> dict[str, str]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    first = paragraphs[0] if paragraphs else text.strip()
    keywords = [k["keyword"] for k in extract_keywords(text, top_k=5)]
    executive = first[:260].replace("\n", " ")
    if len(first) > 260:
        executive += "..."
    return {
        "layer_1_full": text[:2000],
        "layer_2_bold": "; ".join(keywords),
        "layer_3_highlight": " / ".join(keywords[:3]),
        "layer_4_executive": executive,
    }


def parse_links(content: str) -> list[LinkRef]:
    refs: list[LinkRef] = []
    for match in WIKILINK_RE.finditer(content):
        target = match.group(1).strip().replace("%20", " ")
        alias = (match.group(2) or target).strip()
        refs.append(LinkRef(target=target, alias=alias, is_embed=False, link_type="wikilink"))
    for match in EMBED_RE.finditer(content):
        target = match.group(1).strip().replace("%20", " ")
        alias = (match.group(2) or target).strip()
        refs.append(LinkRef(target=target, alias=alias, is_embed=True, link_type="embed"))
    for match in MD_LINK_RE.finditer(content):
        label = match.group(1).strip()
        url = match.group(2).strip()
        if url and not url.startswith(("http://", "https://", "#")):
            refs.append(LinkRef(target=url, alias=label or url, is_embed=False, link_type="md_link"))
    return refs


def first_heading(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def parse_frontmatter_tags(text: str) -> list[str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return []
    fm = match.group(1)
    tags: list[str] = []
    in_tags = False
    for raw in fm.splitlines():
        line = raw.rstrip()
        if re.match(r"^tags\s*:", line):
            value = line.split(":", 1)[1].strip()
            in_tags = True
            if value.startswith("[") and value.endswith("]"):
                tags.extend(t.strip().strip("'\"") for t in value.strip("[]").split(",") if t.strip())
            elif value:
                tags.extend(t.strip() for t in re.split(r"[,\s]+", value) if t.strip())
            continue
        if in_tags and line.lstrip().startswith("-"):
            tags.append(line.split("-", 1)[1].strip().strip("'\""))
            continue
        if in_tags and raw and not raw.startswith(" "):
            in_tags = False
    return list(dict.fromkeys(t for t in tags if t))


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def markdown_files(vault: Path, include_dirs: Iterable[str], limit: int | None = None) -> list[Path]:
    files: list[Path] = []
    for include in include_dirs:
        root = vault / include
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.md")):
            if should_skip(path):
                continue
            files.append(path)
            if limit and len(files) >= limit:
                return files
    return files


def rel(vault: Path, path: Path) -> str:
    return path.relative_to(vault).as_posix()


def canonical_target(target: str) -> str:
    cleaned = target.strip().replace("\\", "/")
    if cleaned.endswith(".md"):
        cleaned = cleaned[:-3]
    return cleaned.strip("/")


def build_note_index(vault: Path, files: list[Path]) -> dict[str, str]:
    index: dict[str, str] = {}
    for path in files:
        r = rel(vault, path)
        no_ext = r[:-3] if r.endswith(".md") else r
        index[no_ext] = r
        index[path.stem] = r
        index[path.name] = r
    return index


def resolve_target(target: str, note_index: dict[str, str]) -> str | None:
    candidate = canonical_target(target)
    if candidate in note_index:
        return note_index[candidate]
    stem = Path(candidate).stem
    if stem in note_index:
        return note_index[stem]
    return None


def is_media_target(target: str) -> bool:
    suffix = Path(target.split("|", 1)[0]).suffix.lower()
    return suffix in MEDIA_EXTENSIONS


def note_record(vault: Path, path: Path, note_index: dict[str, str]) -> NoteRecord:
    text = path.read_text(encoding="utf-8", errors="ignore")
    links = parse_links(text)
    outgoing: list[str] = []
    embeds: list[str] = []
    md_links: list[str] = []
    unresolved: list[str] = []
    for ref in links:
        if ref.is_embed:
            embeds.append(ref.target)
        elif ref.link_type == "md_link":
            md_links.append(ref.target)
        else:
            outgoing.append(ref.target)
        if ref.link_type == "md_link" or is_media_target(ref.target):
            continue
        if resolve_target(ref.target, note_index) is None:
            unresolved.append(ref.target)
    atomic = detect_atomicity(text)
    return NoteRecord(
        path=rel(vault, path),
        title=first_heading(text, path.stem),
        chars=len(text),
        tags=parse_frontmatter_tags(text),
        suggested_tags=suggest_tags(text, max_tags=6),
        keywords=[k["keyword"] for k in extract_keywords(text, top_k=10)],
        outgoing=outgoing,
        embeds=embeds,
        md_links=md_links,
        unresolved=sorted(set(unresolved)),
        incoming_count=0,
        outgoing_count=len(outgoing),
        is_atomic=bool(atomic["is_atomic"]),
        topic_count=int(atomic["topic_count"]),
        confidence=float(atomic["confidence"]),
    )


def connection_suggestions(records: list[NoteRecord], max_items: int = 25) -> list[dict[str, Any]]:
    kw_by_path = {r.path: set(r.keywords) for r in records}
    linked_pairs = {(r.path, resolve_like) for r in records for resolve_like in r.outgoing}
    suggestions: list[dict[str, Any]] = []
    for src in records:
        if not src.keywords:
            continue
        scored = []
        for dst in records:
            if src.path == dst.path:
                continue
            overlap = kw_by_path[src.path] & kw_by_path[dst.path]
            if len(overlap) < 2:
                continue
            if (src.path, dst.title) in linked_pairs or (src.path, dst.path) in linked_pairs:
                continue
            scored.append(
                {
                    "source": src.path,
                    "target": dst.path,
                    "target_title": dst.title,
                    "overlap": sorted(overlap),
                    "score": round(len(overlap) / max(len(kw_by_path[src.path]), 1), 3),
                    "status": "candidate-only",
                }
            )
        scored.sort(key=lambda item: (-item["score"], item["target"]))
        suggestions.extend(scored[:2])
    suggestions.sort(key=lambda item: (-item["score"], item["source"], item["target"]))
    return suggestions[:max_items]


def audit(vault: Path, include_dirs: list[str] | None = None, limit: int | None = None) -> dict[str, Any]:
    include = include_dirs or list(DEFAULT_INCLUDE_DIRS)
    files = markdown_files(vault, include, limit=limit)
    note_index = build_note_index(vault, files)
    records = [note_record(vault, path, note_index) for path in files]

    incoming: dict[str, int] = defaultdict(int)
    for record in records:
        for target in record.outgoing:
            resolved = resolve_target(target, note_index)
            if resolved:
                incoming[resolved] += 1
    for record in records:
        record.incoming_count = incoming.get(record.path, 0)

    orphans = [
        {
            "path": r.path,
            "title": r.title,
            "reason": "no incoming and no outgoing note links",
            "suggested_tags": r.suggested_tags[:4],
        }
        for r in records
        if r.incoming_count == 0 and r.outgoing_count == 0
    ]
    unresolved = [
        {"path": r.path, "title": r.title, "targets": r.unresolved}
        for r in records
        if r.unresolved
    ]
    tag_counts = Counter(tag for r in records for tag in (r.tags or r.suggested_tags) if tag)
    thin_topics = [
        {"topic": topic, "count": count, "status": "thin"}
        for topic, count in sorted(tag_counts.items(), key=lambda item: (item[1], item[0]))
        if count <= 2
    ][:30]
    non_atomic = [
        {"path": r.path, "title": r.title, "topic_count": r.topic_count, "chars": r.chars}
        for r in records
        if not r.is_atomic
    ][:30]
    suggestions = connection_suggestions(records)

    return {
        "generated": date.today().isoformat(),
        "vault": str(vault),
        "include_dirs": include,
        "notes_total": len(records),
        "links_total": sum(r.outgoing_count for r in records),
        "embeds_total": sum(len(r.embeds) for r in records),
        "unresolved_notes": len(unresolved),
        "orphans_total": len(orphans),
        "atomic_notes": sum(1 for r in records if r.is_atomic),
        "non_atomic_notes": sum(1 for r in records if not r.is_atomic),
        "topics_total": len(tag_counts),
        "thin_topics_total": len(thin_topics),
        "top_topics": [{"topic": t, "count": c} for t, c in tag_counts.most_common(20)],
        "orphans": orphans[:50],
        "unresolved_links": unresolved[:50],
        "thin_topics": thin_topics,
        "non_atomic": non_atomic,
        "connection_suggestions": suggestions,
        "notes": [asdict(r) for r in records],
        "boundary": "Read-only audit. Connection/tag suggestions are candidate-only and must be reviewed before editing notes.",
    }


def wikilink(path: str, label: str | None = None) -> str:
    target = path[:-3] if path.endswith(".md") else path
    return f"[[{target}|{label or Path(target).name}]]"


def markdown_report(data: dict[str, Any]) -> str:
    orphans = data.get("orphans", [])[:20]
    unresolved = data.get("unresolved_links", [])[:20]
    suggestions = data.get("connection_suggestions", [])[:20]
    thin = data.get("thin_topics", [])[:20]
    non_atomic = data.get("non_atomic", [])[:20]

    lines = [
        "# V10 Cognitive Vault Garden Audit",
        "",
        "> 本报告吸收 Cognitive-Loop-OS 的 auto-tagging、backlinks、knowledge-gardener 思路，但在 OBS 后端中保持只读。所有标签、连接、拆分建议均为 candidate-only，不能自动写入正式课程页。",
        "",
        f"- 生成日期：{data.get('generated')}",
        f"- 扫描笔记：{data.get('notes_total')}",
        f"- 笔记链接：{data.get('links_total')}",
        f"- 嵌入附件：{data.get('embeds_total')}",
        f"- 孤岛笔记：{data.get('orphans_total')}",
        f"- 未解析链接笔记：{data.get('unresolved_notes')}",
        f"- Atomic / Non-atomic：{data.get('atomic_notes')} / {data.get('non_atomic_notes')}",
        f"- 薄弱主题：{data.get('thin_topics_total')}",
        "",
        "## Top topics",
        "",
    ]
    lines.extend(f"- {item['topic']}: {item['count']}" for item in data.get("top_topics", [])[:15])
    if not data.get("top_topics"):
        lines.append("- 暂无")

    lines += ["", "## Orphan candidates", "", "| 笔记 | 建议标签 | 说明 |", "|---|---|---|"]
    for item in orphans:
        tags = ", ".join(item.get("suggested_tags", [])) or "—"
        lines.append(f"| {wikilink(item['path'], item['title'])} | {tags} | {item['reason']} |")
    if not orphans:
        lines.append("| — | — | 暂无 |")

    lines += ["", "## Unresolved note links", "", "| 笔记 | 未解析目标 |", "|---|---|"]
    for item in unresolved:
        targets = ", ".join(f"`{target}`" for target in item.get("targets", []))
        lines.append(f"| {wikilink(item['path'], item['title'])} | {targets} |")
    if not unresolved:
        lines.append("| — | 暂无 |")

    lines += ["", "## Connection suggestions", "", "| 来源 | 建议连接 | 重叠关键词 | 分数 |", "|---|---|---|---:|"]
    for item in suggestions:
        overlap = ", ".join(item.get("overlap", []))
        lines.append(
            f"| {wikilink(item['source'])} | {wikilink(item['target'], item['target_title'])} | {overlap} | {item['score']} |"
        )
    if not suggestions:
        lines.append("| — | — | — | 0 |")

    lines += ["", "## Thin topics", "", "| Topic | Count | Status |", "|---|---:|---|"]
    for item in thin:
        lines.append(f"| {item['topic']} | {item['count']} | {item['status']} |")
    if not thin:
        lines.append("| — | 0 | 暂无 |")

    lines += ["", "## Non-atomic notes", "", "| 笔记 | topic_count | chars |", "|---|---:|---:|"]
    for item in non_atomic:
        lines.append(f"| {wikilink(item['path'], item['title'])} | {item['topic_count']} | {item['chars']} |")
    if not non_atomic:
        lines.append("| — | 0 | 0 |")

    lines += [
        "",
        "## Boundary",
        "",
        "- 本脚本不读取原始媒体，不复制课程资料，不创建 verified 证据。",
        "- 本脚本不修改正式笔记；`--apply` 只写审计 JSON/Markdown。",
        "- 连接建议、标签建议、拆分建议都只是候选，需要后续课程管道核验。",
    ]
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", type=Path, required=True)
    parser.add_argument("--include", action="append", help="Vault subdirectory to scan; repeatable")
    parser.add_argument("--limit", type=int, help="Limit number of Markdown files scanned")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    data = audit(args.vault, include_dirs=args.include, limit=args.limit)
    if args.apply:
        if not args.output_dir:
            raise SystemExit("--output-dir is required with --apply")
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / "v10-cognitive-vault-garden.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        (args.output_dir / "v10-cognitive-vault-garden.md").write_text(
            markdown_report(data), encoding="utf-8"
        )
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
