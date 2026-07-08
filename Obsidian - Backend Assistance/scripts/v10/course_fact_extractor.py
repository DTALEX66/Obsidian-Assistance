#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OBS V10 course fact/entity candidate extractor.

Adapted from Cognitive-Loop-OS `shared/fact_extractor.py`, with Chinese course
material patterns and OBS safety boundaries.  Output is always candidate-only:
terms/facts/graph edges are suggestions for course processing and OER review,
not verified facts.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

EN_PHRASE_RE = re.compile(r"\b(?:[A-Z][A-Za-z0-9]*)(?:[ -][A-Z][A-Za-z0-9]*){0,3}\b")
CN_TOKEN_RE = re.compile(r"[\u4e00-\u9fffA-Za-z0-9][\u4e00-\u9fffA-Za-z0-9 +#._/-]{1,24}")

STOP_TERMS = {
    "本页内容",
    "候选抽取",
    "人工核验",
    "正式课程事实",
    "课程包含",
    "使用工具",
    "完成任务",
    "需要人工核验后才能进入正式课程事实",
}

CN_FACT_PATTERNS: list[tuple[str, str]] = [
    (r"(?P<subject>[^。；\n]{2,40}?)包含\s*(?P<object>[^。；\n]{2,80})", "contains"),
    (r"(?P<subject>[^。；\n]{2,40}?)依赖\s*(?P<object>[^。；\n]{2,80})", "depends_on"),
    (r"(?P<subject>[^。；\n]{2,40}?)使用\s*(?P<object>[^。；\n]{2,80})", "uses"),
    (r"(?P<subject>[^。；\n]{2,40}?)用于\s*(?P<object>[^。；\n]{2,80})", "used_for"),
    (r"(?P<subject>[^。；\n]{2,40}?)生成\s*(?P<object>[^。；\n]{2,80})", "generates"),
]

EN_FACT_PATTERNS: list[tuple[str, str]] = [
    (r"(?P<subject>[A-Z][A-Za-z0-9 -]{1,50})\s+(?:uses|use)\s+(?P<object>[^.。；\n]{2,80})", "uses"),
    (r"(?P<subject>[A-Z][A-Za-z0-9 -]{1,50})\s+(?:requires|depends on)\s+(?P<object>[^.。；\n]{2,80})", "depends_on"),
    (r"(?P<subject>[A-Z][A-Za-z0-9 -]{1,50})\s+(?:contains|includes)\s+(?P<object>[^.。；\n]{2,80})", "contains"),
]


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def clean_entity(text: str) -> str:
    text = normalize_space(text)
    text = text.strip(" ，,。.;；：:、()（）[]【】\"'")
    for prefix in ("和 ", "以及 ", "并且 "):
        if text.startswith(prefix):
            text = text[len(prefix) :]
    return text[:80].strip()


def split_objects(text: str) -> list[str]:
    parts = re.split(r"[、,，]|\s+和\s+|\s+以及\s+|\s+and\s+", text)
    return [clean_entity(part) for part in parts if len(clean_entity(part)) >= 2]


def extract_candidate_terms(text: str, top_k: int = 20) -> list[dict[str, Any]]:
    counts: Counter[str] = Counter()
    for match in EN_PHRASE_RE.finditer(text):
        term = clean_entity(match.group(0))
        if len(term) >= 2 and term.upper() not in {"THE", "AND"}:
            counts[term] += 3
    for match in CN_TOKEN_RE.finditer(text):
        raw = clean_entity(match.group(0))
        for term in split_cn_candidate(raw):
            if term and term not in STOP_TERMS:
                counts[term] += 1
    results = []
    for term, score in counts.most_common(top_k):
        results.append(
            {
                "term": term,
                "score": score,
                "type": classify_term(term),
                "candidate_only": True,
                "confidence": min(0.85, 0.35 + score * 0.05),
            }
        )
    return results


def split_cn_candidate(raw: str) -> list[str]:
    raw = clean_entity(raw)
    if not raw:
        return []
    candidates = [raw]
    for marker in ("课程", "知识库", "向量数据库", "工具调用", "任务编排", "检索增强生成", "大模型"):
        if marker in raw:
            candidates.append(marker)
    return unique_keep_order([item for item in candidates if len(item) >= 2])


def classify_term(term: str) -> str:
    if re.search(r"[A-Z]", term):
        return "technical_term"
    if any(key in term for key in ("课程", "工作流", "方法", "工具", "数据库", "知识库")):
        return "course_concept"
    return "concept"


def extract_candidate_facts(text: str, max_facts: int = 30) -> list[dict[str, Any]]:
    facts: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    for patterns in (CN_FACT_PATTERNS, EN_FACT_PATTERNS):
        for pattern, predicate in patterns:
            for match in re.finditer(pattern, text, flags=re.IGNORECASE):
                subject = clean_entity(match.group("subject"))
                objects = split_objects(match.group("object")) or [clean_entity(match.group("object"))]
                for obj in objects:
                    if len(facts) >= max_facts:
                        return facts
                    if not subject or not obj or subject == obj:
                        continue
                    key = (subject, predicate, obj)
                    if key in seen:
                        continue
                    seen.add(key)
                    facts.append(
                        {
                            "subject": subject,
                            "predicate": predicate,
                            "object": obj,
                            "confidence": 0.62,
                            "candidate_only": True,
                            "needs_human_review": True,
                        }
                    )
    return facts


def text_to_candidate_graph(text: str) -> dict[str, Any]:
    terms = extract_candidate_terms(text, top_k=30)
    facts = extract_candidate_facts(text, max_facts=50)
    nodes: dict[str, dict[str, Any]] = {}
    for term in terms:
        nodes.setdefault(term["term"], {"id": term["term"], "label": term["term"], "type": term["type"], "candidate_only": True})
    edges = []
    for fact in facts:
        for name in (fact["subject"], fact["object"]):
            nodes.setdefault(name, {"id": name, "label": name, "type": "concept", "candidate_only": True})
        edges.append(
            {
                "source": fact["subject"],
                "target": fact["object"],
                "relation": fact["predicate"],
                "confidence": fact["confidence"],
                "candidate_only": True,
            }
        )
    return {
        "candidate_only": True,
        "needs_human_review": True,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "nodes": list(nodes.values()),
        "edges": edges,
        "terms": terms,
        "facts": facts,
    }


def unique_keep_order(items: list[str]) -> list[str]:
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="OBS V10 candidate-only course fact extractor")
    parser.add_argument("path", type=Path)
    parser.add_argument("--mode", choices=["terms", "facts", "graph"], default="graph")
    parser.add_argument("--limit", type=int, default=30)
    args = parser.parse_args()

    text = args.path.read_text(encoding="utf-8", errors="replace")
    if args.mode == "terms":
        payload: Any = {"candidate_only": True, "items": extract_candidate_terms(text, top_k=args.limit)}
    elif args.mode == "facts":
        payload = {"candidate_only": True, "items": extract_candidate_facts(text, max_facts=args.limit)}
    else:
        payload = text_to_candidate_graph(text)
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
