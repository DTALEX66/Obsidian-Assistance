#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit generated V4 files for private data and structural issues."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

FORBIDDEN_EXT = {".mp3", ".mp4", ".wav", ".flac", ".ape", ".m4a", ".mov", ".avi", ".mkv", ".pdf", ".ppt", ".pptx", ".zip", ".rar", ".7z", ".sqlite"}
SECRET_RE = re.compile(r"(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|Bearer\s+[A-Za-z0-9._-]{20,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)")
FORMAL_PATH_RE = re.compile(r"E:[\\/]BaiduSyncdisk[\\/]Obsidian知识库|E:/BaiduSyncdisk/Obsidian知识库")


def audit(root: Path):
    issues = []
    for p in root.rglob("*"):
        if ".git" in p.parts or "__pycache__" in p.parts:
            continue
        rel = p.relative_to(root).as_posix()
        if p.is_file() and p.suffix.lower() in FORBIDDEN_EXT:
            issues.append({"file": rel, "issue": "forbidden_ext"})
        if p.is_file() and p.stat().st_size <= 1_000_000:
            text = p.read_text(encoding="utf-8", errors="ignore")
            if SECRET_RE.search(text):
                issues.append({"file": rel, "issue": "secret_like_value"})
            if FORMAL_PATH_RE.search(text):
                issues.append({"file": rel, "issue": "hardcoded_formal_vault_path"})
    return {"root": str(root), "issues": issues, "ok": not issues}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    result = audit(Path(args.root).resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
