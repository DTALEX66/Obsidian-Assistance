#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import argparse, json
from pathlib import Path

VALID_TYPE={"course","lesson","concept","method","case","review","action","evidence","pending","report","visual"}
VALID_STATUS={"inbox","processing","verified","blocked","done"}
VALID_CONF={"high","medium","low","unknown"}
REQUIRED={"type","status","course","confidence","created","updated","cssclasses"}


def parse_frontmatter(text):
    if not text.startswith("---\n"): return None
    end=text.find("\n---",4)
    if end<0: return None
    data={}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith(" "):
            k,v=line.split(":",1); data[k.strip()]=v.strip().strip('"')
    return data


def validate_file(path):
    text=Path(path).read_text(encoding="utf-8",errors="ignore")
    fm=parse_frontmatter(text); issues=[]
    if fm is None: return ["missing_frontmatter"]
    missing=sorted(REQUIRED-set(fm))
    if missing: issues.append("missing:"+",".join(missing))
    if fm.get("type") and fm.get("type") not in VALID_TYPE and "{{" not in fm.get("type",""): issues.append("invalid_type")
    if fm.get("status") and fm.get("status") not in VALID_STATUS and "{{" not in fm.get("status",""): issues.append("invalid_status")
    if fm.get("confidence") and fm.get("confidence") not in VALID_CONF and "{{" not in fm.get("confidence",""): issues.append("invalid_confidence")
    return issues


def validate_root(root):
    result={}
    for p in Path(root).rglob("*.md"):
        if ".git" in p.parts: continue
        issues=validate_file(p)
        if issues: result[p.as_posix()]=issues
    return result


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("path"); args=ap.parse_args()
    issues=validate_root(args.path)
    print(json.dumps({"ok":not issues,"issues":issues},ensure_ascii=False,indent=2))
    raise SystemExit(0 if not issues else 1)

if __name__ == "__main__": main()
