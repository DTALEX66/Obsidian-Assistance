from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


TEXT_EXTENSIONS = {".md", ".txt", ".json", ".csv"}
SKIP_DIRS = {
    ".git",
    "__pycache__",
    "node_modules",
    ".obsidian",
    ".smart-env",
    "pdf_pages",
    "temp_audio",
    "outputs",
    "work",
}
RAW_MARKERS = (
    "transcripts",
    "web_cache",
    "source_cache",
    "memory_course_ocr_texts.json",
)
NOISE_PATTERNS = [
    re.compile(r"^\s*$"),
    re.compile(r"^\[OCR ERROR:", re.I),
    re.compile(r"Image too large", re.I),
]
EXCLUDE_TERMS = [
    "奖品",
    "获奖",
    "获奖名单",
    "作品展示",
    "Q&A 大赛",
    "活动展示",
]
ALIASES = {
    "121工作流": ["121工作流", "121 工作流", "一二一工作流", "一二一 工作流"],
    "Q&A笔记": ["Q&A笔记", "Q&A 笔记", "QA笔记"],
}


@dataclass
class Document:
    path: str
    source_type: str
    title: str
    text: str
    mtime: float


def default_db(root: Path) -> Path:
    return root / ".obsidian-assistance" / "course_evidence.sqlite"


def default_report(root: Path) -> Path:
    return root / "outputs" / "course_verifier_report.md"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


def is_noise(text: str) -> bool:
    sample = text.strip()
    if not sample:
        return True
    return any(p.search(sample) for p in NOISE_PATTERNS)


def read_text(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "gb18030"):
        try:
            return path.read_text(encoding=encoding, errors="replace")
        except UnicodeDecodeError:
            continue
    return path.read_text(errors="replace")


def flatten_json(value, prefix: str = "") -> Iterable[tuple[str, str]]:
    if isinstance(value, dict):
        title = (
            value.get("title")
            or value.get("name")
            or value.get("filename")
            or value.get("file")
            or prefix
        )
        text = value.get("text") or value.get("content") or value.get("markdown")
        if isinstance(text, str) and not is_noise(text):
            yield str(title), text
        for key, child in value.items():
            if key in {"text", "content", "markdown"}:
                continue
            yield from flatten_json(child, f"{prefix}/{key}".strip("/"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from flatten_json(child, f"{prefix}[{index}]")
    elif isinstance(value, str) and len(value.strip()) > 80 and not is_noise(value):
        yield prefix or "json_text", value


def source_type_for(path: Path) -> str:
    p = str(path).lower()
    if "web_cache" in p or "source_cache" in p:
        return "external_cache"
    if "transcripts" in p and "audio" in p:
        return "audio_asr"
    if "transcripts" in p and "video" in p:
        return "video_asr"
    if "ocr" in p or "memory_course_ocr" in p:
        return "pdf_ocr"
    return "project_text"


def should_index(path: Path) -> bool:
    p = str(path).lower()
    if any(marker.lower() in p for marker in RAW_MARKERS):
        return True
    if path.name.lower().startswith("ocr_") and path.suffix.lower() == ".txt":
        return True
    return False


def iter_files(root: Path) -> Iterable[Path]:
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        current_path = Path(current)
        for name in files:
            path = current_path / name
            if path.suffix.lower() in TEXT_EXTENSIONS and should_index(path):
                yield path


def iter_documents(root: Path) -> Iterable[Document]:
    for path in iter_files(root):
        try:
            raw = read_text(path)
        except OSError:
            continue
        rel = str(path.relative_to(root)) if path.is_relative_to(root) else str(path)
        stype = source_type_for(path)
        mtime = path.stat().st_mtime
        if path.suffix.lower() == ".json":
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                if not is_noise(raw):
                    yield Document(rel, stype, path.stem, raw, mtime)
                continue
            for title, text in flatten_json(data, path.stem):
                if not is_noise(text):
                    yield Document(rel, stype, title, text, mtime)
        elif not is_noise(raw):
            yield Document(rel, stype, path.stem, raw, mtime)


def chunk_text(text: str, max_chars: int = 1200) -> list[str]:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    paragraphs = [p.strip() for p in re.split(r"\n{2,}", text) if p.strip()]
    chunks: list[str] = []
    current = ""
    for paragraph in paragraphs:
        if len(paragraph) > max_chars:
            sentences = re.split(r"(?<=[。！？.!?])\s*", paragraph)
            for sentence in sentences:
                if not sentence.strip():
                    continue
                if len(current) + len(sentence) > max_chars and current:
                    chunks.append(current.strip())
                    current = ""
                current += sentence.strip() + " "
            continue
        if len(current) + len(paragraph) > max_chars and current:
            chunks.append(current.strip())
            current = ""
        current += paragraph + "\n\n"
    if current.strip():
        chunks.append(current.strip())
    return chunks


def connect(db: Path) -> sqlite3.Connection:
    db.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(db))
    con.execute("PRAGMA journal_mode=WAL")
    return con


def build(root: Path, db: Path) -> None:
    con = connect(db)
    con.executescript(
        """
        DROP TABLE IF EXISTS chunks;
        DROP TABLE IF EXISTS docs;
        CREATE TABLE docs (
            id INTEGER PRIMARY KEY,
            path TEXT NOT NULL,
            source_type TEXT NOT NULL,
            title TEXT NOT NULL,
            mtime REAL NOT NULL,
            sha256 TEXT NOT NULL
        );
        CREATE TABLE chunks (
            id INTEGER PRIMARY KEY,
            doc_id INTEGER NOT NULL,
            chunk_no INTEGER NOT NULL,
            text TEXT NOT NULL,
            FOREIGN KEY(doc_id) REFERENCES docs(id)
        );
        CREATE INDEX idx_docs_path ON docs(path);
        CREATE INDEX idx_docs_source_type ON docs(source_type);
        CREATE INDEX idx_chunks_doc ON chunks(doc_id);
        """
    )
    count_docs = 0
    count_chunks = 0
    for doc in iter_documents(root):
        chunks = [c for c in chunk_text(doc.text) if not is_noise(c)]
        if not chunks:
            continue
        cur = con.execute(
            "INSERT INTO docs(path, source_type, title, mtime, sha256) VALUES (?, ?, ?, ?, ?)",
            (doc.path, doc.source_type, doc.title, doc.mtime, sha256_text(doc.text)),
        )
        doc_id = cur.lastrowid
        for index, chunk in enumerate(chunks):
            con.execute(
                "INSERT INTO chunks(doc_id, chunk_no, text) VALUES (?, ?, ?)",
                (doc_id, index, chunk),
            )
            count_chunks += 1
        count_docs += 1
    con.commit()
    print(f"indexed_docs={count_docs}")
    print(f"indexed_chunks={count_chunks}")
    print(f"db={db}")


def terms_from_query(query: str) -> list[str]:
    if query in ALIASES:
        return ALIASES[query]
    parts = [p.strip() for p in re.split(r"[,，\s]+", query) if p.strip()]
    return parts or [query.strip()]


def score_text(text: str, terms: list[str]) -> int:
    lower = text.lower()
    score = 0
    for term in terms:
        if not term:
            continue
        score += lower.count(term.lower()) * 10
    if any(term.lower() in lower for term in terms if term):
        score += 30
    return score


def snippet(text: str, terms: list[str], max_chars: int = 260) -> str:
    lower = text.lower()
    positions = [lower.find(t.lower()) for t in terms if t and lower.find(t.lower()) >= 0]
    pos = min(positions) if positions else 0
    start = max(0, pos - max_chars // 3)
    end = min(len(text), start + max_chars)
    snip = re.sub(r"\s+", " ", text[start:end]).strip()
    if start > 0:
        snip = "..." + snip
    if end < len(text):
        snip += "..."
    return snip


def query_db(db: Path, query: str, top: int = 8) -> list[dict]:
    con = connect(db)
    terms = terms_from_query(query)
    rows = con.execute(
        """
        SELECT docs.path, docs.source_type, docs.title, chunks.chunk_no, chunks.text
        FROM chunks
        JOIN docs ON docs.id = chunks.doc_id
        """
    ).fetchall()
    results = []
    for path, source_type, title, chunk_no, text in rows:
        score = score_text(text, terms)
        if score <= 0:
            continue
        results.append(
            {
                "score": score,
                "path": path,
                "source_type": source_type,
                "title": title,
                "chunk_no": chunk_no,
                "snippet": snippet(text, terms),
            }
        )
    results.sort(key=lambda r: (-r["score"], r["source_type"], r["path"], r["chunk_no"]))
    return results[:top]


def classify(term: str, results: list[dict]) -> str:
    if any(x in term for x in EXCLUDE_TERMS):
        return "exclude"
    source_types = {r["source_type"] for r in results}
    if len(results) >= 2 and len(source_types) >= 2:
        return "confirmed"
    if len(results) >= 1:
        return "single_source"
    return "needs_web"


def render_query(query: str, results: list[dict]) -> str:
    lines = [f"# 查询：{query}", ""]
    if not results:
        lines.append("未找到本地证据。")
        return "\n".join(lines)
    for i, r in enumerate(results, 1):
        lines.append(f"## {i}. {r['title']}")
        lines.append("")
        lines.append(f"- score: {r['score']}")
        lines.append(f"- source_type: `{r['source_type']}`")
        lines.append(f"- path: `{r['path']}`")
        lines.append(f"- chunk: {r['chunk_no']}")
        lines.append("")
        lines.append(f"> {r['snippet']}")
        lines.append("")
    return "\n".join(lines)


def verify(db: Path, terms: list[str], output: Path, top: int = 6) -> None:
    lines = [
        "# 课程本地证据核验报告",
        "",
        f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"证据库：`{db}`",
        "",
        "## 判定规则",
        "",
        "- `confirmed`：至少两个证据或两个来源类型支持。",
        "- `single_source`：只有一个来源支持，写入时要保守。",
        "- `needs_web`：本地证据不足，才需要联网补证。",
        "- `exclude`：与课程核心知识无关，正式库排除。",
        "",
        "## 结果",
        "",
        "| 术语/主张 | 判定 | 证据数 | 来源类型 | 正式处理 |",
        "|---|---|---:|---|---|",
    ]
    detail_blocks = []
    for term in terms:
        all_results = query_db(db, term, top=max(top, 40))
        results = all_results[:top]
        decision = classify(term, all_results)
        source_types = ", ".join(sorted({r["source_type"] for r in all_results})) or "-"
        handling = {
            "confirmed": "可写入正式知识点",
            "single_source": "可写入，但避免扩展细节",
            "needs_web": "先联网或补材料，不写死",
            "exclude": "正式库删除或忽略",
        }[decision]
        lines.append(f"| {term} | {decision} | {len(all_results)} | {source_types} | {handling} |")
        detail_blocks.append(f"## {term}\n")
        detail_blocks.append(f"- 判定：`{decision}`")
        detail_blocks.append(f"- 正式处理：{handling}\n")
        if results:
            for i, r in enumerate(results, 1):
                detail_blocks.append(f"### 证据 {i}")
                detail_blocks.append(f"- source_type: `{r['source_type']}`")
                detail_blocks.append(f"- path: `{r['path']}`")
                detail_blocks.append(f"- title: {r['title']}")
                detail_blocks.append(f"> {r['snippet']}\n")
        else:
            detail_blocks.append("未找到本地证据。\n")
    lines.extend(["", "## 证据片段", ""])
    lines.extend(detail_blocks)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"report={output}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Local-first course evidence verifier.")
    parser.add_argument("--root", default=".", help="Project root")
    parser.add_argument("--db", default=None, help="SQLite evidence database")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("build", help="Build local evidence index")

    q = sub.add_parser("query", help="Query local evidence")
    q.add_argument("--q", required=True, help="Query term or phrase")
    q.add_argument("--top", type=int, default=8)

    v = sub.add_parser("verify", help="Verify comma-separated terms")
    v.add_argument("--terms", required=True, help="Comma-separated terms")
    v.add_argument("--top", type=int, default=6)
    v.add_argument("--output", default=None)

    args = parser.parse_args()
    root = Path(args.root).resolve()
    db = Path(args.db).resolve() if args.db else default_db(root)

    if args.cmd == "build":
        build(root, db)
    elif args.cmd == "query":
        results = query_db(db, args.q, top=args.top)
        print(render_query(args.q, results))
    elif args.cmd == "verify":
        terms = [t.strip() for t in re.split(r"[,，]", args.terms) if t.strip()]
        output = Path(args.output).resolve() if args.output else default_report(root)
        verify(db, terms, output, top=args.top)


if __name__ == "__main__":
    main()

