#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import json
from pathlib import Path


def build_canvas(data):
    nodes = []
    edges = []
    nodes.append({"id": "course", "type": "text", "text": data.get("course", "Demo课程"), "x": 0, "y": 0, "width": 260, "height": 80})
    groups = [("lessons", "章节", -260), ("concepts", "概念", -120), ("methods", "方法", 20), ("cases", "案例", 160), ("reviews", "复习", 300), ("tasks", "行动", 440), ("evidence", "证据", 580)]
    for key, label, y in groups:
        for idx, name in enumerate(data.get(key, []) or []):
            nid = f"{key}-{idx + 1}"
            nodes.append({"id": nid, "type": "text", "text": f"{label}: {name}", "x": 360 + idx * 40, "y": y, "width": 240, "height": 80})
            edges.append({"id": f"edge-{nid}", "fromNode": "course", "fromSide": "right", "toNode": nid, "toSide": "left"})
    return {"nodes": nodes, "edges": edges}


def demo_data():
    return {
        "course": "Demo课程",
        "lessons": ["第01节"],
        "concepts": ["输入箱"],
        "methods": ["课程处理流程"],
        "cases": ["示例案例"],
        "tasks": ["完成复习"],
        "reviews": ["什么是输入箱"],
        "evidence": ["evidence-001"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input")
    parser.add_argument("--output")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.apply and args.dry_run:
        raise SystemExit("--apply and --dry-run are mutually exclusive")

    data = json.loads(Path(args.input).read_text(encoding="utf-8")) if args.input else demo_data()
    text = json.dumps(build_canvas(data), ensure_ascii=False, indent=2)
    if args.output:
        if args.apply:
            out = Path(args.output)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(text, encoding="utf-8", newline="\n")
            print(json.dumps({"dry_run": False, "output": str(out)}, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({"dry_run": True, "output": args.output, "bytes": len(text.encode("utf-8"))}, ensure_ascii=False, indent=2))
    else:
        print(text)


if __name__ == "__main__":
    main()
