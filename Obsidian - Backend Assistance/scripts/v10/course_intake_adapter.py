#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OBS V10 course intake adapter.

Lightweight, local-first adaptation of Cognitive-Loop-OS
`app/ingestion/multi_format.py`.  It gives OBS a single manifest/adapter layer
for course source files without forcing heavyweight OCR/PDF dependencies.

Default safety:
- inventory mode never includes file content;
- unknown/heavy formats return candidate-only errors when no optional engine exists;
- no writes to the formal vault;
- optional engines are imported lazily.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Callable

FORMAT_BY_EXT = {
    ".pdf": "pdf",
    ".docx": "docx",
    ".doc": "docx",
    ".pptx": "pptx",
    ".ppt": "pptx",
    ".xlsx": "xlsx",
    ".xls": "xlsx",
    ".html": "html",
    ".htm": "html",
    ".md": "md",
    ".markdown": "md",
    ".txt": "txt",
    ".csv": "csv",
    ".png": "image",
    ".jpg": "image",
    ".jpeg": "image",
    ".webp": "image",
    ".bmp": "image",
    ".gif": "image",
    ".mp3": "audio",
    ".m4a": "audio",
    ".wav": "audio",
    ".flac": "audio",
    ".mp4": "video",
    ".mov": "video",
    ".mkv": "video",
    ".avi": "video",
}

SUPPORTED_INVENTORY_FORMATS = {
    "pdf",
    "docx",
    "pptx",
    "xlsx",
    "html",
    "md",
    "txt",
    "csv",
    "image",
    "audio",
    "video",
}


def detect_format(file_path: str | Path) -> str:
    return FORMAT_BY_EXT.get(Path(file_path).suffix.lower(), "unknown")


def optional_engine_status() -> dict[str, dict[str, Any]]:
    modules = {
        "markitdown": "markitdown",
        "docling": "docling.document_converter",
        "trafilatura": "trafilatura",
        "pymupdf": "fitz",
        "paddleocr": "paddleocr",
        "faster_whisper": "faster_whisper",
        "scenedetect": "scenedetect",
    }
    status = {}
    for engine, module in modules.items():
        try:
            available = importlib.util.find_spec(module) is not None
        except ModuleNotFoundError:
            available = False
        status[engine] = {"available": available, "module": module}
    return status


def inventory_sources(root: str | Path, limit: int = 200) -> dict[str, Any]:
    root = Path(root)
    items: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*"), key=lambda p: p.as_posix().casefold()):
        if len(items) >= limit:
            break
        if not path.is_file():
            continue
        fmt = detect_format(path)
        if fmt not in SUPPORTED_INVENTORY_FORMATS:
            continue
        try:
            rel = path.relative_to(root).as_posix()
        except ValueError:
            rel = path.as_posix()
        items.append(
            {
                "path": path.as_posix(),
                "relative_path": rel,
                "name": path.name,
                "format": fmt,
                "suffix": path.suffix.lower(),
                "size_bytes": path.stat().st_size,
                "candidate_only": True,
            }
        )
    return {"root": root.as_posix(), "count": len(items), "items": items}


def _read_text(file_path: Path) -> str:
    return file_path.read_text(encoding="utf-8", errors="replace")


def _via_markitdown(file_path: Path) -> str:
    from markitdown import MarkItDown

    result = MarkItDown().convert(str(file_path))
    return result.text_content


def _via_docling(file_path: Path) -> str:
    from docling.document_converter import DocumentConverter

    result = DocumentConverter().convert(str(file_path))
    return result.document.export_to_markdown()


def _via_trafilatura_html(file_path: Path) -> str:
    import trafilatura

    extracted = trafilatura.extract(_read_text(file_path), output_format="markdown")
    if not extracted:
        raise RuntimeError("trafilatura returned empty text")
    return extracted


def engine_chain(fmt: str) -> list[tuple[str, Callable[[Path], str]]]:
    if fmt in {"md", "txt"}:
        return [("passthrough", _read_text)]
    if fmt == "html":
        return [("trafilatura", _via_trafilatura_html), ("markitdown", _via_markitdown)]
    if fmt == "pdf":
        return [("docling", _via_docling), ("markitdown", _via_markitdown)]
    if fmt in {"docx", "pptx", "xlsx", "csv", "image"}:
        return [("markitdown", _via_markitdown)]
    return []


def convert_file(file_path: str | Path, fmt: str | None = None) -> dict[str, Any]:
    path = Path(file_path)
    fmt = fmt or detect_format(path)
    if fmt == "unknown":
        return base_result(path, fmt, ok=False, error="unsupported_format")
    errors: list[str] = []
    for engine, fn in engine_chain(fmt):
        try:
            content = fn(path)
            return {
                **base_result(path, fmt, ok=True, error=""),
                "engine": engine,
                "content": content,
                "content_chars": len(content),
                "candidate_only": fmt not in {"md", "txt"},
            }
        except ImportError as exc:
            errors.append(f"{engine}: not_installed:{exc.__class__.__name__}")
        except Exception as exc:
            errors.append(f"{engine}: {exc}")
    return {
        **base_result(path, fmt, ok=False, error="no_available_engine"),
        "engine_errors": errors,
    }


def base_result(path: Path, fmt: str, ok: bool, error: str) -> dict[str, Any]:
    return {
        "path": path.as_posix(),
        "format": fmt,
        "ok": ok,
        "error": error,
        "candidate_only": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="OBS V10 course intake adapter")
    sub = parser.add_subparsers(dest="command", required=True)

    inv = sub.add_parser("inventory")
    inv.add_argument("root", type=Path)
    inv.add_argument("--limit", type=int, default=200)

    conv = sub.add_parser("convert")
    conv.add_argument("path", type=Path)
    conv.add_argument("--format")

    sub.add_parser("engines")
    args = parser.parse_args()

    if args.command == "inventory":
        payload = inventory_sources(args.root, limit=args.limit)
    elif args.command == "convert":
        payload = convert_file(args.path, fmt=args.format)
    else:
        payload = optional_engine_status()
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
