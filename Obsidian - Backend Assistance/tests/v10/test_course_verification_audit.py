import json
import zipfile
from pathlib import Path

from scripts.v10.course_verification_audit import build_verification_audit, classify_file, collect_explicit_source_paths, extract_text_from_file


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_verified_course_requires_multiple_evidence_methods(tmp_path):
    vault = tmp_path / "vault"
    sources = tmp_path / "sources"
    course = vault / "02_课程库" / "RAG实战课"
    write(course / "00_课程总览.md", "# RAG实战课\nRAG 依赖 向量数据库 和 知识库检索，适合 Agent 工具调用。\n![[99_附件/course-reference-images/RAG实战课/ref.png]]")
    write(course / "14_开放知识交叉对比.md", "# OER\nRAG 与 retrieval augmented generation 对照。")
    write(vault / "93_导入报告" / "RAG实战课_导入报告.md", "RAG实战课 已从真实源文件生成，包含向量数据库和知识库检索。")
    write(vault / "99_附件" / "course-reference-images" / "RAG实战课" / "ref.png", "fake-image")
    write(vault / "50_领域知识" / "RAG实战课.md", "RAG 公开资料交叉。")
    write(sources / "RAG实战课" / "lesson.md", "RAG 依赖 向量数据库 和 知识库检索，Agent 使用工具调用完成任务。")

    result = build_verification_audit(vault=vault, source_root=sources, limit=10, sample_limit=2)
    row = result["courses"][0]

    assert row["course"] == "RAG实战课"
    assert row["status"] == "verified_by_available_methods"
    assert row["evidence_methods"] >= 5
    assert row["text_consistency"]["overlap_terms"] >= 3
    assert not row["hallucination_risks"]


def test_text_only_course_is_not_marked_verified(tmp_path):
    vault = tmp_path / "vault"
    sources = tmp_path / "sources"
    course = vault / "02_课程库" / "纯文字课"
    write(course / "00_课程总览.md", "# 纯文字课\n只有总结，没有来源、图片、报告或公开资料。")

    result = build_verification_audit(vault=vault, source_root=sources, limit=10, sample_limit=2)
    row = result["courses"][0]

    assert row["status"] == "needs_review"
    assert "missing_raw_source" in row["hallucination_risks"]
    assert "missing_visual_evidence" in row["hallucination_risks"]
    assert "missing_oer_crosscheck" in row["hallucination_risks"]


def test_local_source_index_wikilink_counts_as_available_source(tmp_path):
    vault = tmp_path / "vault"
    sources = tmp_path / "sources"
    course = vault / "02_课程库" / "AI Agent Skills 实战课"
    write(
        course / "00_课程总览.md",
        "# AI Agent Skills 实战课\n来源索引：[[50_领域知识/AI Agent技能库/04_课程化吸收总控|AI Agent 技能库课程化吸收总控]]\nAgent 技能库 包含 工具调用 和 任务编排。",
    )
    write(vault / "50_领域知识" / "AI Agent技能库" / "04_课程化吸收总控.md", "Agent 技能库 包含 工具调用 和 任务编排。")

    result = build_verification_audit(vault=vault, source_root=sources, limit=10, sample_limit=2)
    row = result["courses"][0]

    assert row["local_source_refs"] == 1
    assert row["evidence"]["raw_source_match"] is True
    assert "missing_raw_source" not in row["hallucination_risks"]


def test_single_generic_or_english_token_does_not_create_raw_source_match(tmp_path):
    vault = tmp_path / "vault"
    sources = tmp_path / "sources"
    course = vault / "02_课程库" / "AI Agent Skills 实战课"
    write(course / "00_课程总览.md", "# AI Agent Skills 实战课\n只有课程页。")
    write(sources / "design" / "This contains an image of Totally Awesome Ideas.txt", "unrelated design material")

    result = build_verification_audit(vault=vault, source_root=sources, limit=10, sample_limit=2)
    row = result["courses"][0]

    assert row["raw_matches"] == 0
    assert "missing_raw_source" in row["hallucination_risks"]


def test_sidecar_manifest_counts_as_visual_and_text_evidence(tmp_path):
    vault = tmp_path / "vault"
    sources = tmp_path / "sources"
    sidecars = tmp_path / "sidecars"
    course = vault / "02_课程库" / "传统文化与术数"
    write(course / "00_课程总览.md", "# 传统文化与术数\n三命通会 八字 命理")
    sidecar_dir = sidecars / "传统文化与术数"
    text_path = sidecar_dir / "text" / "sample.txt"
    image_path = sidecar_dir / "visual" / "page.png"
    write(text_path, "三命通会 八字 命理 格局")
    image_path.parent.mkdir(parents=True, exist_ok=True)
    image_path.write_bytes(b"png-evidence")
    write(
        sidecar_dir / "manifest.json",
        json.dumps(
            {
                "course": "传统文化与术数",
                "evidence": {"text_sidecars": 1, "visual_sidecars": 1, "keyframes": 0, "asr_transcripts": 0},
                "artifacts": {"text": [{"path": str(text_path)}], "visual": [{"path": str(image_path)}], "keyframes": [], "asr": []},
            },
            ensure_ascii=False,
        ),
    )

    result = build_verification_audit(vault=vault, source_root=sources, limit=10, sample_limit=2, sidecar_root=sidecars)
    row = result["courses"][0]

    assert row["sidecar_evidence"]["text_sidecars"] == 1
    assert row["evidence"]["visual_evidence"] is True
    assert row["text_consistency"]["overlap_terms"] >= 3


def test_asr_attempt_without_segments_is_not_marked_pending(tmp_path):
    vault = tmp_path / "vault"
    sources = tmp_path / "sources"
    sidecars = tmp_path / "sidecars"
    course = vault / "02_课程库" / "视频课"
    write(course / "00_课程总览.md", "# 视频课\n品牌 全案 设计")
    video = sources / "视频课" / "lesson.mp4"
    video.parent.mkdir(parents=True, exist_ok=True)
    video.write_bytes(b"not-real-video")
    sidecar_dir = sidecars / "视频课"
    write(
        sidecar_dir / "manifest.json",
        json.dumps(
            {
                "course": "视频课",
                "evidence": {"text_sidecars": 0, "visual_sidecars": 0, "keyframes": 1, "asr_transcripts": 0},
                "artifacts": {"text": [], "visual": [], "keyframes": [{"path": "frame.jpg"}], "asr": [{"written": False, "segments": 0}]},
            },
            ensure_ascii=False,
        ),
    )

    result = build_verification_audit(vault=vault, source_root=sources, limit=10, sample_limit=2, sidecar_root=sidecars)
    row = result["courses"][0]

    assert "audio_video_asr_pending" not in row["hallucination_risks"]
    assert "audio_video_asr_unusable" in row["hallucination_risks"]


def test_extract_text_from_markdown_source(tmp_path):
    path = tmp_path / "lesson.md"
    write(path, "# 课程\n向量数据库 知识库检索")

    extracted = extract_text_from_file(path)

    assert extracted["method"] == "text-read"
    assert "向量数据库" in extracted["text"]


def test_extract_text_from_docx_without_external_dependency(tmp_path):
    path = tmp_path / "lesson.docx"
    with zipfile.ZipFile(path, "w") as docx:
        docx.writestr("word/document.xml", "<w:document><w:body><w:t>品牌全案 AIGC 视觉设计</w:t></w:body></w:document>")

    extracted = extract_text_from_file(path)

    assert extracted["method"] == "docx-zip"
    assert "品牌全案" in extracted["text"]


def test_sz_is_treated_as_video_source():
    assert classify_file(Path("lesson.sz")) == "video"


def test_explicit_source_root_metadata_does_not_expand_whole_scan_root(tmp_path):
    source_root = tmp_path / "source"
    source_root.mkdir()
    write(source_root / "unrelated.txt", "无关文件")
    real_course = source_root / "real-course"
    write(real_course / "lesson.txt", "真实课程文件")

    metadata = f"source_root: {source_root}\nsource_path: {real_course}\n"

    paths = collect_explicit_source_paths(metadata, source_root)

    assert source_root / "unrelated.txt" not in paths
    assert real_course / "lesson.txt" in paths


def test_explicit_source_path_takes_precedence_over_global_name_match(tmp_path):
    vault = tmp_path / "vault"
    sources = tmp_path / "sources"
    course = vault / "02_课程库" / "新媒体运营与增长"
    explicit = sources / "explicit-course"
    write(
        course / "00_课程总览.md",
        f"# 新媒体运营与增长\nsource_path: {explicit}\n运营增长 KPI 用户 生命周期",
    )
    write(explicit / "lesson.md", "运营增长 KPI 用户 生命周期")
    write(sources / "unrelated" / "新媒体运营模板.md", "这是不该被显式 source_path 课程采样的全盘同名资料")

    result = build_verification_audit(vault=vault, source_root=sources, limit=10, sample_limit=5)
    row = result["courses"][0]

    assert row["explicit_source_files"] == 1
    assert row["raw_matches"] == 1
    assert row["sample_raw_sources"] == ["explicit-course/lesson.md"]
