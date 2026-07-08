import json
import subprocess
import sys
from pathlib import Path

from scripts.v10.course_pipeline_candidate import (
    cross_reference_sources,
    detect_contradictions,
    run_candidate_pipeline,
    score_credibility,
)

TEXT = """
RAG 依赖向量数据库和知识库检索。AI Agent 使用工具调用完成任务编排。
Python was created by Guido van Rossum. RAG depends on vector databases.
"""


def test_score_credibility_rates_oer_and_unknown_sources():
    trusted = score_credibility(
        {"url": "https://arxiv.org/abs/2401.00001", "content": "References DOI citation author"}
    )
    unknown = score_credibility({"url": "https://random-blog.example/post", "content": "个人经验"})

    assert trusted["score"] > unknown["score"]
    assert trusted["level"] in {"high", "medium"}
    assert "domain" in trusted["factors"]
    assert trusted["candidate_only"] is True


def test_detect_contradictions_groups_subject_predicate_conflicts():
    facts = [
        {"subject": "RAG", "predicate": "depends_on", "object": "vector database", "source": "a"},
        {"subject": "RAG", "predicate": "depends_on", "object": "keyword search", "source": "b"},
    ]

    conflicts = detect_contradictions(facts)

    assert conflicts
    assert conflicts[0]["subject"] == "rag"
    assert conflicts[0]["predicate"] == "depends_on"
    assert set(conflicts[0]["conflicting_objects"]) == {"vector database", "keyword search"}


def test_cross_reference_requires_two_sources_and_compares_candidates():
    one = cross_reference_sources([{"title": "one", "content": TEXT}])
    assert one["error"] == "need at least 2 sources to cross-reference"

    result = cross_reference_sources(
        [
            {"title": "A", "url": "https://arxiv.org/abs/x", "content": TEXT},
            {"title": "B", "url": "https://docs.python.org/3/", "content": TEXT.replace("向量数据库", "知识图谱")},
        ]
    )

    assert result["candidate_only"] is True
    assert result["source_count"] == 2
    assert "credibility" in result
    assert "agreement_count" in result


def test_run_candidate_pipeline_is_read_only_and_json_serializable(tmp_path):
    note = tmp_path / "note.md"
    note.write_text(TEXT, encoding="utf-8")

    result = run_candidate_pipeline("file", str(note), root=tmp_path)

    assert result["candidate_only"] is True
    assert result["verified"] is False
    assert result["writes"] == []
    assert result["stages"]["extract"]["chars"] > 0
    assert result["stages"]["tag"]["keywords"]
    assert result["stages"]["summarize"]["executive"]
    assert result["stages"]["facts"]["count"] >= 1
    json.dumps(result, ensure_ascii=False)


def test_run_candidate_pipeline_blocks_paths_outside_root(tmp_path):
    outside = tmp_path.parent / "outside-course-note.md"
    outside.write_text(TEXT, encoding="utf-8")
    try:
        try:
            run_candidate_pipeline("file", str(outside), root=tmp_path)
            assert False, "expected ValueError"
        except ValueError as exc:
            assert "outside root" in str(exc)
    finally:
        outside.unlink(missing_ok=True)


def test_cli_text_outputs_candidate_json_from_backend_root():
    backend_root = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        [sys.executable, "scripts/v10/course_pipeline_candidate.py", "text", "--text", TEXT],
        cwd=backend_root,
        text=True,
        capture_output=True,
        timeout=30,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["candidate_only"] is True
    assert payload["writes"] == []
