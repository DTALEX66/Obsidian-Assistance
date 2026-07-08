import json
import subprocess
import sys
from pathlib import Path

from scripts.v10.course_fact_extractor import (
    extract_candidate_facts,
    extract_candidate_terms,
    text_to_candidate_graph,
)


SAMPLE = """
大模型应用开发介绍课程包含 Prompt Engineering、RAG 检索增强生成和 AI Agent 工作流。
RAG 依赖向量数据库和知识库检索。AI Agent 使用工具调用完成任务编排。
本页内容为候选抽取，需要人工核验后才能进入正式课程事实。
"""


def test_extract_candidate_terms_supports_chinese_and_english_terms():
    terms = extract_candidate_terms(SAMPLE, top_k=10)
    names = {item["term"] for item in terms}

    assert "RAG" in names
    assert "AI Agent" in names
    assert any("大模型" in name or "知识库" in name for name in names)
    assert all(item["candidate_only"] is True for item in terms)


def test_extract_candidate_facts_extracts_chinese_relation_patterns():
    facts = extract_candidate_facts(SAMPLE, max_facts=10)

    assert any(f["predicate"] == "contains" and "大模型应用开发介绍课程" in f["subject"] for f in facts)
    assert any(f["predicate"] == "depends_on" and "RAG" in f["subject"] for f in facts)
    assert all(f["candidate_only"] is True for f in facts)
    assert all(f["confidence"] < 1 for f in facts)


def test_text_to_candidate_graph_returns_nodes_edges_and_candidate_boundary():
    graph = text_to_candidate_graph(SAMPLE)

    assert graph["candidate_only"] is True
    assert graph["node_count"] >= 2
    assert graph["edge_count"] >= 1
    assert any(edge["relation"] in {"contains", "depends_on", "uses"} for edge in graph["edges"])


def test_cli_outputs_candidate_json_from_backend_root(tmp_path):
    source = tmp_path / "sample.md"
    source.write_text(SAMPLE, encoding="utf-8")
    backend_root = Path(__file__).resolve().parents[2]

    result = subprocess.run(
        [sys.executable, "scripts/v10/course_fact_extractor.py", str(source), "--mode", "graph"],
        cwd=backend_root,
        text=True,
        capture_output=True,
        timeout=30,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["candidate_only"] is True
    assert payload["edge_count"] >= 1
