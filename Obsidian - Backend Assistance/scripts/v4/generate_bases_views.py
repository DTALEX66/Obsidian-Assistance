#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import json
from pathlib import Path


def build_views(course):
    return {
        "course": course,
        "note": "Bases 格式仍在演进；本文件提供稳定视图配置草案，不强写正式 vault。",
        "views": [
            {"name": "课程章节", "filter": {"type": "lesson"}, "sort": ["priority", "updated"]},
            {"name": "知识卡片", "filter": {"type": ["concept", "method", "case"]}, "sort": ["priority"]},
            {"name": "复习中心", "filter": {"type": "review"}, "sort": ["review_level", "updated"]},
            {"name": "待确认", "filter": {"status": "blocked"}, "sort": ["priority"]},
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--course", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.apply and args.dry_run:
        raise SystemExit("--apply and --dry-run are mutually exclusive")

    out = Path(args.output)
    text = json.dumps(build_views(args.course), ensure_ascii=False, indent=2)
    if args.apply:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8", newline="\n")
        print(json.dumps({"dry_run": False, "output": str(out)}, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"dry_run": True, "output": str(out), "bytes": len(text.encode("utf-8"))}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
