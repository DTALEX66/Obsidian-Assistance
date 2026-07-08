#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OBS V10 read-only candidate pipeline.

OBS-safe adaptation of Cognitive-Loop-OS `shared/pipeline.py` and
`shared/cross_reference.py`.

It deliberately does not ingest, index, write vault files, write SQLite rows,
start services, fetch network data, or claim verified evidence.  Output is a
candidate JSON object for course processing/OER review.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.v10.cognitive_vault_garden import (  # noqa: E402
    detect_atomicity,
    extract_keywords,
    progressive_summarize,
    suggest_tags,
)
from scripts.v10.course_fact_extractor import extract_candidate_facts  # noqa: E402
from scripts.v10.course_intake_adapter import convert_file  # noqa: E402

BOUNDARY = "read-only candidate analysis; no vault write, no DB/log/cache/secret copy"
TRUSTED_DOMAINS = {
    "arxiv.org",
    "github.com",
    "wikipedia.org",
    "docs.python.org",
    "developer.mozilla.org",
    "pypi.org",
    "nature.com",
    "science.org",
    "ieee.org",
    "acm.org",
    "mit.edu",
    "stanford.edu",
    "berkeley.edu",
    "cmu.edu",
    "openai.com",
    "anthropic.com",
    "huggingface.co",
    "openstax.org",
    "ocw.mit.edu",
    "wikibooks.org",
    "wikiversity.org",
    "mdn.github.io",
}
CRED_SIGNALS = {
    "peer-reviewed": 0.3,
    "citation": 0.15,
    "reference": 0.1,
    "references": 0.1,
    "bibliography": 0.1,
    "doi": 0.2,
    "arxiv": 0.15,
    "license": 0.05,
    "version": 0.05,
    "last updated": 0.1,
    "author": 0.1,
    "affiliation": 0.1,
}
BLOCKED_PARTS = {".git", ".obsidian", "__pycache__", "logs", "cache", "node_modules"}
BLOCKED_SUFFIXES = {".sqlite", ".db", ".env", ".log", ".pyc", ".pyo"}


def domain_trust(domain: str) -> float:
    domain = domain.lower().replace("www.", "")
    if domain in TRUSTED_DOMAINS:
        return 0.8
    if domain.endswith(".edu"):
        return 0.7
    if domain.endswith(".gov"):
        return 0.9
    if domain.endswith(".org"):
        return 0.5
    if "blog" in domain or "medium" in domain:
        return 0.3
    if not domain:
        return 0.25
    return 0.3


def score_credibility(source: dict[str, Any]) -> dict[str, Any]:
    content = source.get("content", "") or ""
    url = source.get("url", "") or source.get("source", "") or ""
    title = source.get("title", "") or ""
    domain = ""
    parsed = urlparse(url)
    if parsed.netloc:
        domain = parsed.netloc
    elif "://" in url:
        domain = url.split("://", 1)[1].split("/", 1)[0]

    score = domain_trust(domain)
    factors: dict[str, float] = {"domain": round(score, 2)}
    lower = f"{title} {content}".lower()
    for signal, weight in CRED_SIGNALS.items():
        if signal in lower:
            contribution = min(weight, 1.0 - score)
            score += contribution
            factors[signal] = round(contribution, 2)
    score = min(1.0, round(score, 2))
    level = "high" if score >= 0.7 else "medium" if score >= 0.4 else "low"
    return {
        "score": score,
        "level": level,
        "domain": domain,
        "factors": factors,
        "candidate_only": True,
        "verified": False,
    }


def detect_contradictions(fact_list: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for fact in fact_list:
        subject = str(fact.get("subject", "")).casefold()
        predicate = str(fact.get("predicate", "")).casefold()
        if not subject or not predicate:
            continue
        groups.setdefault((subject, predicate), []).append(fact)

    contradictions = []
    for (subject, predicate), facts in groups.items():
        objects = {str(f.get("object", "")).casefold() for f in facts if f.get("object")}
        if len(objects) > 1:
            contradictions.append(
                {
                    "subject": subject,
                    "predicate": predicate,
                    "conflicting_objects": sorted(objects),
                    "sources": [f.get("source", "") for f in facts],
                    "candidate_only": True,
                }
            )
    return contradictions


def cross_reference_sources(sources: list[dict[str, Any]]) -> dict[str, Any]:
    if len(sources) < 2:
        return {"error": "need at least 2 sources to cross-reference", "candidate_only": True, "verified": False}

    facts_by_source: dict[int, list[dict[str, Any]]] = {}
    keywords_by_source: dict[int, set[str]] = {}
    for index, src in enumerate(sources):
        text = f"{src.get('title', '')}\n{src.get('content', '')}"
        facts = extract_candidate_facts(text, max_facts=12)
        for fact in facts:
            fact["source"] = src.get("title") or src.get("url") or str(index)
        facts_by_source[index] = facts
        keywords_by_source[index] = {k["keyword"] for k in extract_keywords(text, top_k=15)}

    agreements: list[dict[str, Any]] = []
    contradictions: list[dict[str, Any]] = []
    unique_keywords: dict[str, list[str]] = {str(i): [] for i in range(len(sources))}
    for i in range(len(sources)):
        for j in range(i + 1, len(sources)):
            for left in facts_by_source[i]:
                for right in facts_by_source[j]:
                    if same_fact_key(left, right):
                        if str(left.get("object", "")).casefold() == str(right.get("object", "")).casefold():
                            agreements.append({"fact": left, "source_a": i, "source_b": j, "type": "exact_match"})
                        else:
                            contradictions.append(
                                {"fact_a": left, "fact_b": right, "source_a": i, "source_b": j, "type": "object_differs"}
                            )
            shared = keywords_by_source[i] & keywords_by_source[j]
            unique_keywords[str(i)].extend(sorted((keywords_by_source[i] - shared))[:5])
            unique_keywords[str(j)].extend(sorted((keywords_by_source[j] - shared))[:5])

    all_facts = [fact for facts in facts_by_source.values() for fact in facts]
    contradictions.extend(detect_contradictions(all_facts))
    return {
        "candidate_only": True,
        "verified": False,
        "source_count": len(sources),
        "agreement_count": len(agreements),
        "contradiction_count": len(contradictions),
        "agreements": agreements[:10],
        "contradictions": contradictions[:10],
        "unique_keywords": {key: list(dict.fromkeys(values))[:5] for key, values in unique_keywords.items()},
        "credibility": {str(i): score_credibility(src) for i, src in enumerate(sources)},
    }


def same_fact_key(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return (
        str(left.get("subject", "")).casefold() == str(right.get("subject", "")).casefold()
        and str(left.get("predicate", "")).casefold() == str(right.get("predicate", "")).casefold()
    )


def fuse_sources(sources: list[dict[str, Any]]) -> dict[str, Any]:
    combined = "\n\n".join(f"{s.get('title', '')}\n{s.get('content', '')}" for s in sources)
    summary = progressive_summarize(combined) if combined.strip() else {}
    return {
        "candidate_only": True,
        "verified": False,
        "source_count": len(sources),
        "keywords": extract_keywords(combined, top_k=12),
        "summary": summary.get("layer_4_executive", ""),
        "contradictions": detect_contradictions(extract_candidate_facts(combined, max_facts=40)),
    }


def run_candidate_pipeline(
    source: str,
    input_data: str,
    actions: list[str] | None = None,
    root: Path | None = None,
    include_content: bool = False,
) -> dict[str, Any]:
    actions = actions or ["extract", "tag", "summarize", "facts", "crossref"]
    result: dict[str, Any] = {
        "candidate_only": True,
        "verified": False,
        "source": source,
        "stages": {},
        "writes": [],
        "boundary": BOUNDARY,
    }
    title = ""
    content = ""

    if "extract" in actions:
        extracted = extract_input(source, input_data, root=root, include_content=include_content)
        content = extracted.pop("content", "")
        title = extracted.get("title", "")
        result["stages"]["extract"] = extracted
    else:
        content = input_data

    if not content:
        return result

    if "tag" in actions:
        keywords = extract_keywords(content, top_k=10)
        result["stages"]["tag"] = {
            "tags": suggest_tags(content, max_tags=8),
            "keywords": [item["keyword"] for item in keywords[:8]],
            "atomicity": detect_atomicity(content),
            "candidate_only": True,
        }
    if "summarize" in actions:
        summary = progressive_summarize(content)
        result["stages"]["summarize"] = {
            "executive": summary.get("layer_4_executive", ""),
            "highlight": summary.get("layer_3_highlight", ""),
            "candidate_only": True,
        }
    if "facts" in actions:
        facts = extract_candidate_facts(content, max_facts=15)
        result["stages"]["facts"] = {"count": len(facts), "sample": facts[:8], "candidate_only": True}
    if "crossref" in actions:
        result["stages"]["crossref"] = score_credibility({"title": title, "content": content, "url": input_data})
    if include_content:
        result["content_preview"] = content[:1000]
    return result


def extract_input(source: str, input_data: str, root: Path | None = None, include_content: bool = False) -> dict[str, Any]:
    if source == "text":
        return {"engine": "passthrough", "chars": len(input_data), "title": "inline-text", "content": input_data}
    if source != "file":
        raise ValueError(f"unsupported source: {source}; use file or text")
    path = safe_input_path(Path(input_data), root=root)
    converted = convert_file(path)
    content = converted.get("content") or ""
    if not content and path.suffix.lower() in {".md", ".markdown", ".txt"}:
        content = path.read_text(encoding="utf-8", errors="replace")
    payload = {
        "engine": converted.get("engine", "file-read"),
        "format": converted.get("format", path.suffix.lower().lstrip(".")),
        "path": str(path),
        "chars": len(content),
        "title": path.stem,
        "candidate_only": True,
    }
    payload["content"] = content
    if include_content:
        payload["content_preview"] = content[:1000]
    return payload


def safe_input_path(path: Path, root: Path | None = None) -> Path:
    resolved = path.resolve()
    if root is not None:
        root_resolved = root.resolve()
        try:
            resolved.relative_to(root_resolved)
        except ValueError as exc:
            raise ValueError(f"input path outside root: {path}") from exc
    if any(part in BLOCKED_PARTS for part in resolved.parts):
        raise ValueError(f"blocked runtime/cache path: {path}")
    if resolved.suffix.lower() in BLOCKED_SUFFIXES or resolved.name.lower() == ".env":
        raise ValueError(f"blocked runtime/secret file: {path}")
    return resolved


def load_source(path: Path, root: Path | None = None) -> dict[str, Any]:
    safe = safe_input_path(path, root=root)
    text = safe.read_text(encoding="utf-8", errors="replace")
    return {"title": safe.stem, "source": str(safe), "content": text}


def main() -> None:
    parser = argparse.ArgumentParser(description="OBS V10 read-only candidate pipeline")
    sub = parser.add_subparsers(dest="command", required=True)

    text = sub.add_parser("text")
    text.add_argument("--text", required=True)
    text.add_argument("--actions", default="extract,tag,summarize,facts,crossref")

    file_cmd = sub.add_parser("file")
    file_cmd.add_argument("--path", required=True, type=Path)
    file_cmd.add_argument("--root", type=Path)
    file_cmd.add_argument("--include-content", action="store_true")
    file_cmd.add_argument("--actions", default="extract,tag,summarize,facts,crossref")

    cross = sub.add_parser("crossref")
    cross.add_argument("--root", type=Path)
    cross.add_argument("--paths", nargs="+", type=Path, required=True)

    args = parser.parse_args()
    if args.command == "text":
        payload = run_candidate_pipeline("text", args.text, actions=split_actions(args.actions))
    elif args.command == "file":
        payload = run_candidate_pipeline(
            "file",
            str(args.path),
            actions=split_actions(args.actions),
            root=args.root,
            include_content=args.include_content,
        )
    else:
        sources = [load_source(path, root=args.root) for path in args.paths]
        payload = cross_reference_sources(sources)
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    print()


def split_actions(actions: str) -> list[str]:
    return [item.strip() for item in actions.split(",") if item.strip()]


if __name__ == "__main__":
    main()
