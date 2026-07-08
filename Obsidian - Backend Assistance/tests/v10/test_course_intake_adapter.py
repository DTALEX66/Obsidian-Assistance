import json

from scripts.v10.course_intake_adapter import (
    convert_file,
    detect_format,
    inventory_sources,
    optional_engine_status,
)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_detect_format_covers_course_source_types():
    assert detect_format("lesson.pdf") == "pdf"
    assert detect_format("deck.pptx") == "pptx"
    assert detect_format("notes.docx") == "docx"
    assert detect_format("page.html") == "html"
    assert detect_format("frame.png") == "image"
    assert detect_format("audio.mp3") == "audio"
    assert detect_format("video.mp4") == "video"
    assert detect_format("unknown.bin") == "unknown"


def test_inventory_sources_returns_manifest_without_file_content(tmp_path):
    write(tmp_path / "course" / "a.md", "# A")
    write(tmp_path / "course" / "b.pdf", "%PDF fake")
    write(tmp_path / "course" / "ignore.bin", "x")

    manifest = inventory_sources(tmp_path, limit=10)

    assert manifest["root"] == tmp_path.as_posix()
    assert manifest["count"] == 2
    assert sorted(item["format"] for item in manifest["items"]) == ["md", "pdf"]
    assert all("content" not in item for item in manifest["items"])


def test_convert_file_passthrough_for_md_and_txt(tmp_path):
    md = tmp_path / "note.md"
    txt = tmp_path / "transcript.txt"
    write(md, "# 标题\n内容")
    write(txt, "逐字稿")

    md_result = convert_file(md)
    txt_result = convert_file(txt)

    assert md_result["ok"] is True
    assert md_result["engine"] == "passthrough"
    assert "# 标题" in md_result["content"]
    assert txt_result["ok"] is True
    assert txt_result["format"] == "txt"


def test_convert_file_unknown_is_candidate_only_error(tmp_path):
    path = tmp_path / "raw.bin"
    write(path, "x")

    result = convert_file(path)

    assert result["ok"] is False
    assert result["candidate_only"] is True
    assert result["error"] == "unsupported_format"


def test_optional_engine_status_is_json_serializable():
    status = optional_engine_status()

    assert {"markitdown", "docling", "trafilatura"}.issubset(status)
    json.dumps(status, ensure_ascii=False)
