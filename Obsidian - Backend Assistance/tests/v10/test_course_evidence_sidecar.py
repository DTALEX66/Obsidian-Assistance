import json
import subprocess
import sys
from pathlib import Path

import scripts.v10.course_evidence_sidecar as sidecar
from scripts.v10.course_evidence_sidecar import build_audio_sample_command, build_course_sidecar


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def create_pdf_placeholder(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"%PDF-1.4\n% placeholder fixture\n")


def test_build_sidecar_extracts_pdf_text_and_page_image(tmp_path):
    vault = tmp_path / "vault"
    source_root = tmp_path / "sources"
    out = tmp_path / "sidecars"
    course = vault / "02_课程库" / "RAG实战课"
    write(course / "00_课程总览.md", "# RAG实战课\nRAG vector database")
    create_pdf_placeholder(source_root / "RAG实战课" / "lesson.pdf")

    original_extract = sidecar.extract_text_from_file
    original_render = sidecar.render_pdf_page_image
    try:
        sidecar.extract_text_from_file = lambda path, max_chars=6000: {"method": "fixture-pdf", "text": "RAG vector database evidence", "path": str(path)}

        def fake_render_pdf_page_image(pdf_path: Path, output_path: Path, page_number: int = 0) -> dict:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(b"fake-png")
            return {"path": str(output_path), "written": True, "page": page_number + 1, "pages": 1, "source": str(pdf_path)}

        sidecar.render_pdf_page_image = fake_render_pdf_page_image
        result = build_course_sidecar(
            course="RAG实战课",
            vault=vault,
            source_root=source_root,
            output_root=out,
            max_text_files=1,
            max_media_files=0,
            run_asr=False,
        )
    finally:
        sidecar.extract_text_from_file = original_extract
        sidecar.render_pdf_page_image = original_render

    assert result["course"] == "RAG实战课"
    assert result["evidence"]["text_sidecars"] == 1
    assert result["evidence"]["visual_sidecars"] == 1
    text_path = Path(result["artifacts"]["text"][0]["path"])
    image_path = Path(result["artifacts"]["visual"][0]["path"])
    assert text_path.exists()
    assert image_path.exists()
    assert "vector database" in text_path.read_text(encoding="utf-8")


def test_build_sidecar_extracts_video_keyframe_when_ffmpeg_available(tmp_path):
    if subprocess.run(["which", "ffmpeg"], capture_output=True, text=True).returncode != 0:
        return
    vault = tmp_path / "vault"
    source_root = tmp_path / "sources"
    out = tmp_path / "sidecars"
    course = vault / "02_课程库" / "视频课"
    write(course / "00_课程总览.md", "# 视频课")
    video = source_root / "视频课" / "lesson.mp4"
    video.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=blue:s=160x90:d=1", "-frames:v", "5", str(video)],
        check=True,
        capture_output=True,
        text=True,
    )

    result = build_course_sidecar(
        course="视频课",
        vault=vault,
        source_root=source_root,
        output_root=out,
        max_text_files=0,
        max_media_files=1,
        run_asr=False,
    )

    assert result["evidence"]["keyframes"] == 1
    keyframe = Path(result["artifacts"]["keyframes"][0]["path"])
    assert keyframe.exists()
    assert keyframe.suffix == ".jpg"


def test_cli_writes_manifest(tmp_path):
    vault = tmp_path / "vault"
    source_root = tmp_path / "sources"
    out = tmp_path / "sidecars"
    course = vault / "02_课程库" / "文本课"
    write(course / "00_课程总览.md", "# 文本课")
    write(source_root / "文本课" / "lesson.md", "文本课 evidence text")

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/v10/course_evidence_sidecar.py",
            "--course",
            "文本课",
            "--vault",
            str(vault),
            "--source-root",
            str(source_root),
            "--output-root",
            str(out),
            "--max-text-files",
            "1",
            "--max-media-files",
            "0",
            "--format",
            "json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(completed.stdout)
    assert data["manifest_path"]
    assert Path(data["manifest_path"]).exists()


def test_audio_sample_command_supports_mid_video_start_offset(tmp_path):
    cmd = build_audio_sample_command(tmp_path / "lesson.mp4", tmp_path / "sample.wav", seconds=90, start_seconds=300)

    assert cmd[:4] == ["ffmpeg", "-y", "-ss", "300"]
    assert "-t" in cmd
    assert cmd[cmd.index("-t") + 1] == "90"
