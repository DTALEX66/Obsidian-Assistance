#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OBS V10 local course verification audit.

Runs a conservative multi-method audit across formal course pages, raw source
matches, reports, visual assets, and OER/public-knowledge notes.  This script
never claims absolute zero hallucination.  It marks a course as
`verified_by_available_methods` only when available local evidence agrees across
multiple independent channels; otherwise it remains `needs_review`.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".bmp"}
VIDEO_EXT = {".mp4", ".mov", ".mkv", ".avi", ".wmv", ".flv", ".webm", ".m4v", ".mpg", ".mpeg", ".sz"}
AUDIO_EXT = {".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg"}
TEXT_EXT = {".md", ".txt", ".csv", ".json", ".html", ".htm"}
DOC_EXT = {".pdf", ".docx", ".doc", ".pptx", ".ppt", ".xlsx", ".xls"}
SUPPORTED_EXT = IMAGE_EXT | VIDEO_EXT | AUDIO_EXT | TEXT_EXT | DOC_EXT
STOPWORDS = {
    "课程", "总结", "内容", "学习", "方法", "工具", "知识", "系统", "使用", "需要", "可以", "进行",
    "the", "and", "for", "with", "from", "this", "that", "into", "course", "lesson",
}
GENERIC_PATH_TOKENS = {
    "ai",
    "ui",
    "ux",
    "llm",
    "rag",
    "agent",
    "skills",
    "github",
    "obsidian",
    "ocr",
    "pdf",
    "cn",
    "com",
    "net",
    "org",
    "www",
    "awesome",
    "课程",
    "教程",
    "资料",
    "素材",
    "完结",
    "实战课",
    "实战班",
    "训练营",
}
COURSE_ALIASES = {
    "品牌全案AI设计实战班": ["卢帅", "品牌全案", "AI设计实战班", "AIGC篇"],
    "网易视觉设计师养成计划": ["网易", "视觉设计师养成计划", "大河", "合成电商"],
    "AI Agent Skills 实战课": ["AI Agent技能库", "awesome-skills-cn", "agent skills"],
    "AI LLM工具生态与Skill工程": ["AI Agent技能库", "awesome-skills-cn", "Skill工程"],
    "AI研究搜索与OER交叉验证": ["AI Agent技能库", "awesome-skills-cn", "OER", "research"],
    "Agent技能安全审计": ["AI Agent技能库", "awesome-skills-cn", "安全审计"],
    "Obsidian与PKM自动化实战": ["PKM", "AI Agent技能库", "awesome-skills-cn"],
    "多Agent工程与任务编排": ["multi-agent", "多Agent", "AI Agent技能库", "awesome-skills-cn"],
    "文档OCR与课程入库自动化": ["课程入库", "AI Agent技能库", "awesome-skills-cn"],
    "浏览器自动化与桌面控制": ["browser", "computer-use", "浏览器自动化", "AI Agent技能库"],
    "GitHub自动化与代码审查工作流": ["代码审查", "awesome-skills-cn"],
    "新媒体高阶运营增长实战训练": ["新媒体", "运营增长", "增长实战"],
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path, limit_chars: int | None = None) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""
    return text[:limit_chars] if limit_chars else text


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except Exception:
        return str(path).replace("\\", "/")


def tokenize_name(name: str) -> list[str]:
    parts = re.split(r"[\s\-_—/|·：:（）()【】\[\]、,，]+", name.lower())
    tokens = [part for part in parts if len(part) >= 2 and part not in GENERIC_PATH_TOKENS]
    for alias in COURSE_ALIASES.get(name, []):
        tokens.extend(
            part
            for part in re.split(r"[\s\-_—/|·：:（）()【】\[\]、,，]+", alias.lower())
            if len(part) >= 2 and part not in GENERIC_PATH_TOKENS
        )
    if len(name) >= 4:
        tokens.append(name.lower())
    return list(dict.fromkeys(tokens))


def extract_terms(text: str, limit: int = 80) -> list[str]:
    chinese = re.findall(r"[\u4e00-\u9fff]{2,12}", text)
    english = re.findall(r"[A-Za-z][A-Za-z0-9_+\-]{2,30}", text)
    counts: Counter[str] = Counter()
    for token in chinese + english:
        normalized = token.strip().lower()
        if normalized in STOPWORDS:
            continue
        counts[normalized] += 1
    return [term for term, _ in counts.most_common(limit)]


def classify_file(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in IMAGE_EXT:
        return "image"
    if ext in VIDEO_EXT:
        return "video"
    if ext in AUDIO_EXT:
        return "audio"
    if ext == ".pdf":
        return "pdf"
    if ext in {".ppt", ".pptx"}:
        return "slides"
    if ext in {".doc", ".docx"}:
        return "word"
    if ext in TEXT_EXT:
        return "text"
    return "doc"


def scan_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    found: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {".git", ".obsidian", "node_modules", "__pycache__", ".venv"}]
        base = Path(dirpath)
        for filename in filenames:
            path = base / filename
            if path.suffix.lower() in SUPPORTED_EXT:
                found.append(path)
    return found


def match_score(course: str, path: Path) -> int:
    path_text = str(path).lower().replace("\\", "/")
    score = 0
    if course.lower() in path_text:
        score += 5
    for token in tokenize_name(course):
        if token and token in path_text:
            score += 1
    return score


def collect_local_vault_refs(text: str, vault: Path) -> list[Path]:
    """Collect local vault references mentioned in course pages/reports.

    These are not external raw media, but they are useful local source indexes
    for generated/OER courses that originate from `50_领域知识` or prior verified
    reports rather than an external raw-course directory.
    """
    candidates: list[str] = []
    for match in re.findall(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]", text):
        candidates.append(match.strip())
    for match in re.findall(r"((?:50_领域知识|93_导入报告)/[^`\]\)\n]+)", text):
        candidates.append(match.strip())

    found: list[Path] = []
    for candidate in candidates:
        normalized = candidate.replace("\\", "/").strip()
        if not normalized.startswith(("50_领域知识/", "93_导入报告/")):
            continue
        path = vault / normalized
        possible = [path]
        if path.suffix == "":
            possible.append(path.with_suffix(".md"))
        for item in possible:
            if item.exists() and item.is_file():
                found.append(item)
                break
    return list(dict.fromkeys(found))


def normalize_possible_windows_path(value: str) -> Path:
    cleaned = value.strip().strip('"\'`').replace("\\", "/")
    return Path(cleaned)


def is_broad_source_root_candidate(path: Path, source_root: Path) -> bool:
    """Return True when a recorded path is only the global scan root.

    Course pages sometimes record `source_root: E:\学习数据` as metadata. Treating
    that as an explicit course source expands to the whole disk slice and causes
    cross-course sidecar sampling. Only concrete subdirectories/files under the
    root should be considered explicit course evidence.
    """
    candidate = str(path).replace("\\", "/").rstrip("/").lower()
    root = str(source_root).replace("\\", "/").rstrip("/").lower()
    return candidate == root


def collect_explicit_source_paths(text: str, source_root: Path) -> list[Path]:
    """Collect explicit source_path / 来源目录 records from course pages."""
    candidates: list[str] = []
    patterns = [
        r"source_path:\s*[\"']?([^\"'\n]+)[\"']?",
        r"source_root:\s*[\"']?([^\"'\n]+)[\"']?",
        r"来源目录[:：]\s*`([^`]+)`",
        r"资料位置[:：]\s*`([^`]+)`",
        r"素材目录[:：]\s*`([^`]+)`",
    ]
    for pattern in patterns:
        candidates.extend(match.strip() for match in re.findall(pattern, text))
    found: list[Path] = []
    for candidate in candidates:
        path = normalize_possible_windows_path(candidate)
        if is_broad_source_root_candidate(path, source_root):
            continue
        if path.exists():
            if path.is_file() and path.suffix.lower() in SUPPORTED_EXT:
                found.append(path)
            elif path.is_dir():
                found.extend(scan_files(path))
            continue
        root_text = str(source_root).replace("\\", "/").rstrip("/")
        cand_text = str(path).replace("\\", "/")
        if cand_text.rstrip("/").lower() == root_text.lower():
            continue
        if cand_text.startswith(root_text):
            fallback = source_root / cand_text[len(root_text):].lstrip("/")
            if fallback.exists():
                if fallback.is_file() and fallback.suffix.lower() in SUPPORTED_EXT:
                    found.append(fallback)
                elif fallback.is_dir():
                    found.extend(scan_files(fallback))
    return list(dict.fromkeys(found))


def safe_name(value: str) -> str:
    cleaned = re.sub(r"[\\/:*?\"<>|\s]+", "_", value.strip())
    cleaned = cleaned.strip("._")
    return cleaned[:120] or "course"


def load_sidecar_manifest(course: str, sidecar_root: Path | None) -> dict[str, Any]:
    if not sidecar_root:
        return {"evidence": {}, "artifacts": {}}
    candidates = [sidecar_root / safe_name(course) / "manifest.json", sidecar_root / course / "manifest.json"]
    for path in candidates:
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception as exc:
                return {"error": str(exc)[:120], "evidence": {}, "artifacts": {}}
    return {"evidence": {}, "artifacts": {}}


def has_oer_sidecar(course: str, oer_sidecar_root: Path | None) -> bool:
    if not oer_sidecar_root:
        return False
    return any((oer_sidecar_root / name).exists() for name in [f"{safe_name(course)}.md", f"{course}.md"])


def extract_text_from_file(path: Path, max_chars: int = 6000) -> dict[str, Any]:
    ext = path.suffix.lower()
    if ext in TEXT_EXT:
        return {"method": "text-read", "text": read_text(path, max_chars), "path": str(path)}
    if ext == ".pdf":
        via_fitz = extract_pdf_with_pymupdf(path, max_chars=max_chars)
        if via_fitz.get("text"):
            return via_fitz
        via_pdftotext = extract_pdf_with_pdftotext(path, max_chars=max_chars)
        if via_pdftotext.get("text"):
            return via_pdftotext
        return {"method": "pdf-no-text", "text": "", "path": str(path), "needs_ocr": True}
    if ext == ".doc":
        return extract_doc_with_antiword(path, max_chars=max_chars)
    if ext == ".docx":
        return extract_docx_with_zip(path, max_chars=max_chars)
    return {"method": "unsupported-text-extraction", "text": "", "path": str(path)}


def extract_doc_with_antiword(path: Path, max_chars: int) -> dict[str, Any]:
    try:
        result = subprocess.run(["antiword", str(path)], text=True, capture_output=True, timeout=30)
        if result.returncode == 0 and result.stdout.strip():
            return {"method": "antiword", "text": result.stdout[:max_chars], "path": str(path)}
        return {"method": "antiword-error", "text": "", "path": str(path), "error": (result.stderr or result.stdout)[:120]}
    except Exception as exc:
        return {"method": "antiword-error", "text": "", "path": str(path), "error": str(exc)[:120]}


def extract_docx_with_zip(path: Path, max_chars: int) -> dict[str, Any]:
    try:
        with zipfile.ZipFile(path) as docx:
            xml = docx.read("word/document.xml").decode("utf-8", errors="ignore")
        text = re.sub(r"<[^>]+>", "", xml)
        text = re.sub(r"\s+", " ", text).strip()
        return {"method": "docx-zip", "text": text[:max_chars], "path": str(path)}
    except Exception as exc:
        return {"method": "docx-zip-error", "text": "", "path": str(path), "error": str(exc)[:120]}


def extract_pdf_with_pymupdf(path: Path, max_chars: int) -> dict[str, Any]:
    try:
        import fitz  # type: ignore

        pieces: list[str] = []
        with fitz.open(path) as doc:
            for page in doc[: min(3, len(doc))]:
                pieces.append(page.get_text("text"))
                if sum(len(piece) for piece in pieces) >= max_chars:
                    break
        return {"method": "pymupdf", "text": "\n".join(pieces)[:max_chars], "path": str(path)}
    except Exception as exc:
        return {"method": "pymupdf-error", "text": "", "path": str(path), "error": str(exc)[:120]}


def extract_pdf_with_pdftotext(path: Path, max_chars: int) -> dict[str, Any]:
    try:
        result = subprocess.run(["pdftotext", "-f", "1", "-l", "3", str(path), "-"], text=True, capture_output=True, timeout=30)
        if result.returncode == 0:
            return {"method": "pdftotext", "text": result.stdout[:max_chars], "path": str(path)}
        return {"method": "pdftotext-error", "text": "", "path": str(path), "error": result.stderr[:120]}
    except Exception as exc:
        return {"method": "pdftotext-error", "text": "", "path": str(path), "error": str(exc)[:120]}


def build_verification_audit(
    vault: Path,
    source_root: Path,
    limit: int = 10000,
    sample_limit: int = 3,
    sidecar_root: Path | None = None,
    oer_sidecar_root: Path | None = None,
) -> dict[str, Any]:
    course_root = vault / "02_课程库"
    report_root = vault / "93_导入报告"
    attach_root = vault / "99_附件"
    oer_root = vault / "50_领域知识"
    courses = sorted([p for p in course_root.iterdir() if p.is_dir()], key=lambda p: p.name)[:limit] if course_root.exists() else []
    source_files = scan_files(source_root)
    report_files = [p for p in report_root.rglob("*") if p.is_file() and p.suffix.lower() in {".md", ".json"}] if report_root.exists() else []
    asset_files = [p for p in attach_root.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXT | {".json"}] if attach_root.exists() else []
    oer_files = [p for p in oer_root.rglob("*.md") if p.is_file()] if oer_root.exists() else []

    rows = [audit_course(course_dir, vault, source_root, source_files, report_files, asset_files, oer_files, sample_limit, sidecar_root, oer_sidecar_root) for course_dir in courses]
    summary = summarize(rows, source_files, report_files, asset_files, oer_files)
    return {
        "schema": "obs-course-local-verification-audit/v1",
        "generated_at": now_iso(),
        "boundary": {
            "absolute_zero_error_claim": False,
            "rule": "Only courses with multiple agreeing evidence channels are marked verified_by_available_methods; all others remain needs_review.",
            "no_vault_body_write": True,
            "network_oer_not_substitute_for_local_source": True,
        },
        "environment": detect_environment(),
        "summary": summary,
        "courses": rows,
    }


def audit_course(
    course_dir: Path,
    vault: Path,
    source_root: Path,
    source_files: list[Path],
    report_files: list[Path],
    asset_files: list[Path],
    oer_files: list[Path],
    sample_limit: int,
    sidecar_root: Path | None = None,
    oer_sidecar_root: Path | None = None,
) -> dict[str, Any]:
    course = course_dir.name
    md_files = list(course_dir.rglob("*.md"))
    formal_text = "\n".join(read_text(path) for path in md_files)
    formal_terms = set(extract_terms(formal_text, limit=120))
    explicit_source_files = collect_explicit_source_paths(formal_text, source_root)
    raw_candidates = explicit_source_files if explicit_source_files else [path for path in source_files if match_score(course, path) >= 2]
    raw_matches = sorted(list(dict.fromkeys(raw_candidates)), key=lambda p: (-match_score(course, p), str(p)))
    reports = sorted([path for path in report_files if match_score(course, path) > 0], key=str)
    report_text = "\n".join(read_text(path, limit_chars=12000) for path in reports[:10])
    local_source_refs = collect_local_vault_refs(formal_text + "\n" + report_text, vault)
    sidecar = load_sidecar_manifest(course, sidecar_root)
    sidecar_evidence = sidecar.get("evidence") if isinstance(sidecar.get("evidence"), dict) else {}
    sidecar_artifacts = sidecar.get("artifacts") if isinstance(sidecar.get("artifacts"), dict) else {}
    assets = sorted([path for path in asset_files if match_score(course, path) > 0], key=str)
    oer = sorted([path for path in oer_files if match_score(course, path) > 0], key=str)
    oer_sidecar = has_oer_sidecar(course, oer_sidecar_root)
    embedded_visuals = count_visual_embeds(formal_text)
    source_type_counts = Counter(classify_file(path) for path in raw_matches)
    text_samples = []
    for item in list(sidecar_artifacts.get("text") or []) + list(sidecar_artifacts.get("asr") or []):
        path_text = str(item.get("path", "")).strip()
        if not path_text:
            continue
        path = Path(path_text)
        if path.exists() and path.is_file():
            sample = extract_text_from_file(path)
            sample["sidecar_reference"] = True
            text_samples.append(sample)
            if len(text_samples) >= sample_limit:
                break
    for path in local_source_refs:
        sample = extract_text_from_file(path)
        sample["local_vault_reference"] = True
        text_samples.append(sample)
        if len(text_samples) >= sample_limit:
            break
    for path in raw_matches:
        if len(text_samples) >= sample_limit:
            break
        if classify_file(path) in {"text", "pdf"}:
            sample = extract_text_from_file(path)
            text_samples.append(sample)
    sampled_text = "\n".join(sample.get("text", "") for sample in text_samples)
    source_terms = set(extract_terms(sampled_text, limit=120))
    overlap = sorted(formal_terms & source_terms)
    text_consistency = {
        "sample_count": len(text_samples),
        "methods": sorted({sample.get("method", "unknown") for sample in text_samples}),
        "overlap_terms": len(overlap),
        "overlap_sample": overlap[:15],
        "checked": bool(text_samples),
    }
    evidence = {
        "formal_markdown": len(md_files) > 0,
        "raw_source_match": len(raw_matches) > 0 or len(local_source_refs) > 0 or int(sidecar_evidence.get("text_sidecars") or 0) > 0,
        "raw_text_consistency": len(overlap) >= 3,
        "report_match": len(reports) > 0,
        "visual_evidence": bool(assets or embedded_visuals or source_type_counts["image"] or int(sidecar_evidence.get("visual_sidecars") or 0) > 0 or int(sidecar_evidence.get("keyframes") or 0) > 0),
        "oer_crosscheck": bool(oer or (course_dir / "14_开放知识交叉对比.md").exists() or oer_sidecar),
        "audio_video_present": bool(source_type_counts["audio"] or source_type_counts["video"]),
        "pdf_present": bool(source_type_counts["pdf"]),
    }
    risks = []
    if not evidence["raw_source_match"]:
        risks.append("missing_raw_source")
    if not evidence["raw_text_consistency"]:
        risks.append("raw_text_not_cross_confirmed")
    if not evidence["report_match"]:
        risks.append("missing_report")
    if not evidence["visual_evidence"]:
        risks.append("missing_visual_evidence")
    if not evidence["oer_crosscheck"]:
        risks.append("missing_oer_crosscheck")
    env = detect_environment()
    if evidence["audio_video_present"] and not evidence["raw_text_consistency"] and int(sidecar_evidence.get("asr_transcripts") or 0) == 0:
        if sidecar_artifacts.get("asr"):
            risks.append("audio_video_asr_unusable")
        else:
            risks.append("audio_video_asr_pending")
    if evidence["pdf_present"] and any(sample.get("needs_ocr") for sample in text_samples) and not env["tesseract_available"]:
        risks.append("scanned_pdf_ocr_not_available")
    evidence_methods = sum(bool(value) for key, value in evidence.items() if key not in {"audio_video_present", "pdf_present"})
    status = "verified_by_available_methods" if evidence_methods >= 5 and evidence["raw_text_consistency"] and not any(r in risks for r in ["missing_raw_source", "missing_visual_evidence", "missing_oer_crosscheck"]) else "needs_review"
    return {
        "course": course,
        "status": status,
        "evidence_methods": evidence_methods,
        "evidence": evidence,
        "hallucination_risks": risks,
        "source_type_counts": dict(source_type_counts),
        "raw_matches": len(raw_matches),
        "explicit_source_files": len(explicit_source_files),
        "local_source_refs": len(local_source_refs),
        "reports": len(reports),
        "visual_assets": len(assets),
        "embedded_visuals": embedded_visuals,
        "sidecar_evidence": sidecar_evidence,
        "oer_matches": len(oer),
        "oer_sidecar": oer_sidecar,
        "text_consistency": text_consistency,
        "sample_raw_sources": [rel(path, source_root) for path in raw_matches[:5]],
        "sample_local_sources": [rel(path, vault) for path in local_source_refs[:5]],
        "sample_reports": [rel(path, vault) for path in reports[:5]],
        "sample_visual_assets": [rel(path, vault) for path in assets[:5]],
        "sample_oer": [rel(path, vault) for path in oer[:5]],
    }


def count_visual_embeds(text: str) -> int:
    return len(re.findall(r"!\[\[|!\[[^\]]*\]\(|\.(?:png|jpg|jpeg|webp|gif|svg)", text, flags=re.IGNORECASE))


def detect_environment() -> dict[str, Any]:
    def has_command(name: str) -> bool:
        try:
            return subprocess.run(["which", name], text=True, capture_output=True, timeout=5).returncode == 0
        except Exception:
            return False

    return {
        "pymupdf_available": import_available("fitz"),
        "markitdown_available": import_available("markitdown"),
        "pdftotext_available": has_command("pdftotext"),
        "ffmpeg_available": has_command("ffmpeg"),
        "tesseract_available": has_command("tesseract"),
        "whisper_available": has_command("whisper") or import_available("whisper") or import_available("faster_whisper"),
    }


def import_available(name: str) -> bool:
    try:
        __import__(name)
        return True
    except Exception:
        return False


def summarize(rows: list[dict[str, Any]], source_files: list[Path], report_files: list[Path], asset_files: list[Path], oer_files: list[Path]) -> dict[str, Any]:
    statuses = Counter(row["status"] for row in rows)
    risks = Counter(risk for row in rows for risk in row["hallucination_risks"])
    return {
        "courses_total": len(rows),
        "verified_by_available_methods": statuses.get("verified_by_available_methods", 0),
        "needs_review": statuses.get("needs_review", 0),
        "source_files_total": len(source_files),
        "report_files_total": len(report_files),
        "asset_files_total": len(asset_files),
        "oer_files_total": len(oer_files),
        "risk_counts": dict(risks),
    }


def markdown_report(audit: dict[str, Any]) -> str:
    lines = ["# 全课程本地转化多源交叉识别核验报告", ""]
    lines.append("> 结论口径：不声称绝对零错误；只有本地源、二次文本抽取、报告、视觉资产、OER 等多种方法互相印证时，才标 `verified_by_available_methods`。")
    lines.append("")
    lines.append("## 环境")
    for key, value in audit["environment"].items():
        lines.append(f"- {key}: `{value}`")
    lines.append("")
    lines.append("## 总览")
    for key, value in audit["summary"].items():
        lines.append(f"- **{key}**: `{value}`")
    lines.append("")
    lines.append("## 课程核验矩阵")
    lines.append("| 课程 | 状态 | 方法数 | 风险 | 原始源 | 本地来源索引 | Sidecar | 报告 | 视觉 | OER | 文本交叉 | 样例源 |")
    lines.append("|---|---|---:|---|---:|---:|---|---:|---:|---:|---|---|")
    ordered = sorted(audit["courses"], key=lambda r: (r["status"] == "verified_by_available_methods", -len(r["hallucination_risks"]), r["course"]))
    for row in ordered:
        text_cross = f"{row['text_consistency']['overlap_terms']} terms / {','.join(row['text_consistency']['methods'])}"
        sample_items = row["sample_raw_sources"][:2] or row.get("sample_local_sources", [])[:2]
        sample = "<br>".join(sample_items)
        sidecar = row.get("sidecar_evidence", {})
        sidecar_label = "/".join(str(sidecar.get(k, 0)) for k in ["text_sidecars", "visual_sidecars", "keyframes", "asr_transcripts"])
        lines.append(
            f"| {row['course']} | {row['status']} | {row['evidence_methods']} | {'、'.join(row['hallucination_risks']) or 'OK'} | {row['raw_matches']} | {row.get('local_source_refs', 0)} | {sidecar_label} | {row['reports']} | {row['visual_assets'] + row['embedded_visuals']} | {row['oer_matches'] + int(bool(row.get('oer_sidecar')))} | {text_cross} | {sample} |"
        )
    lines.append("")
    lines.append("## 后续规则")
    lines.append("- `needs_review` 课程不能宣称无幻觉/无识别错误。")
    lines.append("- 视频/音频课程在 whisper/faster-whisper 缺失时，只能做文件级存在验证，不能做内容级 ASR 核验。")
    lines.append("- 扫描 PDF 在 tesseract/marker 缺失时，只能做可复制文本 PDF 的 PyMuPDF/pdftotext 核验，不能做图像 OCR 核验。")
    lines.append("- 网络/OER 只能校对公共知识，不能替代本地课程源。")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit local course conversion with multiple evidence methods")
    parser.add_argument("--vault", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=10000)
    parser.add_argument("--sample-limit", type=int, default=3)
    parser.add_argument("--sidecar-root", type=Path)
    parser.add_argument("--oer-sidecar-root", type=Path)
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    audit = build_verification_audit(args.vault, args.source_root, args.limit, args.sample_limit, args.sidecar_root, args.oer_sidecar_root)
    content = json.dumps(audit, ensure_ascii=False, indent=2) + "\n" if args.format == "json" else markdown_report(audit)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content, encoding="utf-8")
    print(content)


if __name__ == "__main__":
    main()
