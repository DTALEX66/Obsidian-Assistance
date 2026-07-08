#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OBS V10 course evidence sidecar generator.

Generates verifiable sidecar artifacts for course remediation without writing
formal vault course bodies: extracted source text, PDF source-page images, media
keyframes, and optional ASR transcripts.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.v10.course_verification_audit import (  # noqa: E402
    IMAGE_EXT,
    AUDIO_EXT,
    VIDEO_EXT,
    classify_file,
    collect_explicit_source_paths,
    collect_local_vault_refs,
    extract_terms,
    extract_text_from_file,
    match_score,
    read_text,
    rel,
    scan_files,
)


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def safe_name(value: str) -> str:
    cleaned = re.sub(r"[\\/:*?\"<>|\s]+", "_", value.strip())
    cleaned = cleaned.strip("._")
    return cleaned[:120] or "course"


def command_available(name: str) -> bool:
    return subprocess.run(["which", name], text=True, capture_output=True, timeout=10).returncode == 0


def render_pdf_page_image(pdf_path: Path, output_path: Path, page_number: int = 0) -> dict[str, Any]:
    try:
        import fitz  # type: ignore

        output_path.parent.mkdir(parents=True, exist_ok=True)
        doc = fitz.open(pdf_path)
        if doc.page_count == 0:
            return {"path": str(output_path), "written": False, "error": "pdf_has_no_pages"}
        page = doc.load_page(min(page_number, doc.page_count - 1))
        pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False)
        pix.save(output_path)
        pages = doc.page_count
        doc.close()
        return {"path": str(output_path), "written": output_path.exists(), "page": page_number + 1, "pages": pages}
    except Exception as exc:
        return {"path": str(output_path), "written": False, "error": str(exc)[:200]}


def extract_keyframe(media_path: Path, output_path: Path, at_seconds: float = 0.1) -> dict[str, Any]:
    if not command_available("ffmpeg"):
        return {"path": str(output_path), "written": False, "error": "ffmpeg_missing"}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-y",
        "-ss",
        str(at_seconds),
        "-i",
        str(media_path),
        "-frames:v",
        "1",
        "-q:v",
        "2",
        str(output_path),
    ]
    proc = subprocess.run(cmd, text=True, capture_output=True, timeout=120)
    if proc.returncode != 0 or not output_path.exists():
        return {"path": str(output_path), "written": False, "error": (proc.stderr or proc.stdout)[-300:]}
    return {"path": str(output_path), "written": True, "source": str(media_path)}


def build_audio_sample_command(media_path: Path, output_path: Path, seconds: int = 45, start_seconds: int = 0) -> list[str]:
    cmd = ["ffmpeg", "-y"]
    if start_seconds > 0:
        cmd.extend(["-ss", str(start_seconds)])
    cmd.extend([
        "-i",
        str(media_path),
        "-t",
        str(seconds),
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ar",
        "16000",
        "-ac",
        "1",
        str(output_path),
    ])
    return cmd


def extract_audio_sample(media_path: Path, output_path: Path, seconds: int = 45, start_seconds: int = 0) -> dict[str, Any]:
    if not command_available("ffmpeg"):
        return {"path": str(output_path), "written": False, "error": "ffmpeg_missing"}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = build_audio_sample_command(media_path, output_path, seconds=seconds, start_seconds=start_seconds)
    proc = subprocess.run(cmd, text=True, capture_output=True, timeout=180)
    if proc.returncode != 0 or not output_path.exists():
        sample_file = output_path
        sample_file.unlink(missing_ok=True)
        return {"path": str(output_path), "written": False, "error": (proc.stderr or proc.stdout)[-300:]}
    return {"path": str(output_path), "written": True, "seconds": seconds, "start_seconds": start_seconds}


def transcribe_audio(audio_path: Path, output_path: Path, model_name: str = "tiny", language: str | None = "zh") -> dict[str, Any]:
    try:
        from faster_whisper import WhisperModel  # type: ignore
    except Exception as exc:
        return {"path": str(output_path), "written": False, "error": f"faster_whisper_missing:{exc}"}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        model = WhisperModel(model_name, device="cpu", compute_type="int8")
        segments, info = model.transcribe(str(audio_path), language=language, vad_filter=True)
        lines = []
        for segment in segments:
            text = segment.text.strip()
            if text:
                lines.append(f"[{segment.start:.2f}-{segment.end:.2f}] {text}")
        transcript = "\n".join(lines)
        output_path.write_text(transcript, encoding="utf-8")
        return {
            "path": str(output_path),
            "written": output_path.exists() and bool(transcript.strip()),
            "segments": len(lines),
            "language": getattr(info, "language", language),
            "duration": getattr(info, "duration", None),
            "model": model_name,
        }
    except Exception as exc:
        return {"path": str(output_path), "written": False, "error": str(exc)[:300], "model": model_name}


def discover_course_sources(course: str, vault: Path, source_root: Path) -> dict[str, Any]:
    course_dir = vault / "02_课程库" / course
    md_files = list(course_dir.rglob("*.md")) if course_dir.exists() else []
    formal_text = "\n".join(read_text(path, limit_chars=12000) for path in md_files)
    explicit_files = collect_explicit_source_paths(formal_text, source_root)
    raw_files = list(dict.fromkeys(explicit_files if explicit_files else [path for path in scan_files(source_root) if match_score(course, path) >= 2]))
    raw_files = sorted(raw_files, key=lambda p: (-match_score(course, p), str(p)))
    local_refs = collect_local_vault_refs(formal_text, vault)
    return {"course_dir": course_dir, "raw_files": raw_files, "local_refs": local_refs}


def build_course_sidecar(
    course: str,
    vault: Path,
    source_root: Path,
    output_root: Path,
    max_text_files: int = 3,
    max_media_files: int = 1,
    max_candidate_text_files: int = 30,
    run_asr: bool = False,
    asr_model: str = "tiny",
    asr_seconds: int = 45,
    asr_start_seconds: int = 0,
) -> dict[str, Any]:
    course_slug = safe_name(course)
    sidecar_root = output_root / course_slug
    text_dir = sidecar_root / "text"
    visual_dir = sidecar_root / "visual"
    keyframe_dir = sidecar_root / "keyframes"
    asr_dir = sidecar_root / "asr"
    sidecar_root.mkdir(parents=True, exist_ok=True)

    discovered = discover_course_sources(course, vault, source_root)
    candidates = list(discovered["local_refs"]) + list(discovered["raw_files"])
    formal_text = "\n".join(read_text(path, limit_chars=12000) for path in discovered["course_dir"].rglob("*.md")) if discovered["course_dir"].exists() else ""
    formal_terms = set(extract_terms(formal_text, limit=160))
    text_artifacts: list[dict[str, Any]] = []
    visual_artifacts: list[dict[str, Any]] = []
    keyframe_artifacts: list[dict[str, Any]] = []
    asr_artifacts: list[dict[str, Any]] = []

    extracted_candidates: list[tuple[int, Path, dict[str, Any], str]] = []
    for source in candidates:
        kind = classify_file(source)
        if kind not in {"text", "pdf"}:
            continue
        extracted = extract_text_from_file(source)
        text = extracted.get("text", "").strip()
        if text:
            source_terms = set(extract_terms(text, limit=160))
            overlap = len(formal_terms & source_terms)
            extracted_candidates.append((overlap, source, extracted, text))
        if len(extracted_candidates) >= max_candidate_text_files:
            break
    for overlap, source, extracted, text in sorted(extracted_candidates, key=lambda item: (-item[0], str(item[1])))[:max_text_files]:
        kind = classify_file(source)
        if len(text) >= 20:
            out = text_dir / f"{len(text_artifacts)+1:02d}_{safe_name(source.stem)}.txt"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(text, encoding="utf-8")
            text_artifacts.append({"source": str(source), "path": str(out), "method": extracted.get("method"), "chars": len(text), "formal_overlap_terms": overlap})
        if kind == "pdf":
            image_out = visual_dir / f"{len(visual_artifacts)+1:02d}_{safe_name(source.stem)}_p1.png"
            rendered = render_pdf_page_image(source, image_out)
            rendered["source"] = str(source)
            if rendered.get("written"):
                visual_artifacts.append(rendered)

    media_files = [p for p in discovered["raw_files"] if p.suffix.lower() in VIDEO_EXT | AUDIO_EXT]
    for source in media_files[:max_media_files]:
        if source.suffix.lower() in VIDEO_EXT:
            keyframe_out = keyframe_dir / f"{len(keyframe_artifacts)+1:02d}_{safe_name(source.stem)}.jpg"
            keyframe = extract_keyframe(source, keyframe_out)
            if keyframe.get("written"):
                keyframe_artifacts.append(keyframe)
        if run_asr:
            audio_out = asr_dir / f"{safe_name(source.stem)}_sample.wav"
            transcript_out = asr_dir / f"{safe_name(source.stem)}_transcript.txt"
            audio = extract_audio_sample(source, audio_out, seconds=asr_seconds, start_seconds=asr_start_seconds)
            if audio.get("written"):
                transcript = transcribe_audio(audio_out, transcript_out, model_name=asr_model)
                transcript["source"] = str(source)
                transcript["audio_sample_deleted"] = False
                try:
                    audio_out.unlink(missing_ok=True)
                    transcript["audio_sample_deleted"] = True
                except Exception as exc:
                    transcript["audio_sample_delete_error"] = str(exc)[:120]
                asr_artifacts.append(transcript)
            else:
                asr_artifacts.append({"source": str(source), "path": str(transcript_out), "written": False, "error": audio.get("error")})

    result = {
        "schema": "obs-course-evidence-sidecar/v1",
        "generated_at": now_iso(),
        "course": course,
        "boundary": "sidecar evidence only; no formal vault body writes",
        "inputs": {
            "vault": str(vault),
            "source_root": str(source_root),
            "raw_matches": len(discovered["raw_files"]),
            "local_refs": len(discovered["local_refs"]),
        },
        "evidence": {
            "text_sidecars": len(text_artifacts),
            "visual_sidecars": len(visual_artifacts),
            "keyframes": len(keyframe_artifacts),
            "asr_transcripts": sum(1 for item in asr_artifacts if item.get("written") and int(item.get("segments") or 0) > 0),
        },
        "artifacts": {
            "text": text_artifacts,
            "visual": visual_artifacts,
            "keyframes": keyframe_artifacts,
            "asr": asr_artifacts,
        },
    }
    manifest = sidecar_root / "manifest.json"
    manifest.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    result["manifest_path"] = str(manifest)
    return result


def to_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['course']} evidence sidecar",
        "",
        f"- schema: `{result['schema']}`",
        f"- boundary: {result['boundary']}",
        f"- manifest: `{result.get('manifest_path', '')}`",
        "",
        "## Evidence",
    ]
    for key, value in result["evidence"].items():
        lines.append(f"- {key}: `{value}`")
    lines.append("")
    lines.append("## Artifacts")
    for group, items in result["artifacts"].items():
        lines.append(f"### {group}")
        for item in items:
            lines.append(f"- `{item.get('path')}` ← `{item.get('source', '')}`")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate course evidence sidecars")
    parser.add_argument("--course", required=True)
    parser.add_argument("--vault", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, default=Path("docs/course-evidence-sidecars"))
    parser.add_argument("--max-text-files", type=int, default=3)
    parser.add_argument("--max-candidate-text-files", type=int, default=30)
    parser.add_argument("--max-media-files", type=int, default=1)
    parser.add_argument("--asr", action="store_true")
    parser.add_argument("--asr-model", default="tiny")
    parser.add_argument("--asr-seconds", type=int, default=45)
    parser.add_argument("--asr-start-seconds", type=int, default=0)
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    args = parser.parse_args()

    result = build_course_sidecar(
        course=args.course,
        vault=args.vault,
        source_root=args.source_root,
        output_root=args.output_root,
        max_text_files=args.max_text_files,
        max_candidate_text_files=args.max_candidate_text_files,
        max_media_files=args.max_media_files,
        run_asr=args.asr,
        asr_model=args.asr_model,
        asr_seconds=args.asr_seconds,
        asr_start_seconds=args.asr_start_seconds,
    )
    if args.format == "markdown":
        print(to_markdown(result), end="")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
