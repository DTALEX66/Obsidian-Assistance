#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import argparse, json
from pathlib import Path


def build_views(course):
    return {"course":course,"note":"Bases 格式仍在演进；本文件提供稳定视图配置草案，不强写正式 vault。","views":[{"name":"课程章节","filter":{"type":"lesson"},"sort":["priority","updated"]},{"name":"知识卡片","filter":{"type":["concept","method","case"]},"sort":["priority"]},{"name":"复习中心","filter":{"type":"review"},"sort":["review_level","updated"]},{"name":"待确认","filter":{"status":"blocked"},"sort":["priority"]}]}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--course",required=True); ap.add_argument("--output",required=True); args=ap.parse_args()
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(build_views(args.course),ensure_ascii=False,indent=2),encoding="utf-8",newline="\n"); print(out)

if __name__ == "__main__": main()
