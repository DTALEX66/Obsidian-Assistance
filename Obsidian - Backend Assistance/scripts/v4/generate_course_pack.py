#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

try:
    from scripts.v4.safe_vault_writer import SafeVaultWriter
    from scripts.v4.generate_canvas_map import build_canvas
    from scripts.v4.generate_mermaid_graph import build_graphs
except ModuleNotFoundError:
    from safe_vault_writer import SafeVaultWriter
    from generate_canvas_map import build_canvas
    from generate_mermaid_graph import build_graphs


def render(text, values):
    for k, v in values.items():
        text = text.replace("{{" + k + "}}", str(v))
    return text


def safe_name(value):
    return "".join(c if c not in '<>:"/\\|?*' else "_" for c in str(value)).strip() or "未命名"


def load_spec(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("course spec must be a JSON object")
    if not data.get("course"):
        raise ValueError("course spec requires a non-empty 'course' field")
    return data


def demo_spec(course):
    return {
        "course": course,
        "status": "done",
        "source_type": "demo",
        "source_path": "examples/v4-demo-course",
        "confidence": "medium",
        "lessons": [
            {"lesson": "第01节", "title": "示例章节", "summary": "示例，不含用户真实课程内容。", "content": "这是 V4 Demo 生成内容，用于验证模板、Canvas、Mermaid、Dataview 和 Tasks 结构。"}
        ],
        "concepts": [{"title": "输入箱", "summary": "用于收集待处理学习材料的入口。", "content": "示例概念卡，不含真实课程内容。"}],
        "methods": [{"title": "课程处理流程", "summary": "从素材识别到复习行动的处理流程。", "content": "示例方法卡，不含真实课程内容。"}],
        "cases": [{"title": "示例案例", "summary": "用于验证案例卡渲染。", "content": "示例案例卡，不含真实课程内容。"}],
        "reviews": [{"title": "什么是输入箱", "summary": "输入箱的用途是什么？", "content": "输入箱用于暂存待处理学习材料。"}],
        "actions": [{"title": "行动清单", "summary": "Demo 行动任务。", "content": "完成 V4 Demo 课程包验证。"}],
        "evidence": [{"id": "evidence-001", "title": "Demo evidence", "summary": "示例证据，不含用户真实课程内容。"}],
        "pending_review": "无真实课程内容；仅用于演示。",
    }


def base_values(spec, item=None, item_type="lesson"):
    today = date.today().isoformat()
    item = item or {}
    evidence_id = item.get("evidence_id") or item.get("id") or spec.get("evidence_id") or "evidence-001"
    return {
        "type": item_type,
        "status": item.get("status", spec.get("status", "done")),
        "course": spec["course"],
        "lesson": item.get("lesson", ""),
        "title": item.get("title", item.get("lesson", spec["course"])),
        "date": item.get("created", spec.get("created", today)),
        "updated": item.get("updated", spec.get("updated", today)),
        "source_type": item.get("source_type", spec.get("source_type", "demo")),
        "source_path": item.get("source_path", spec.get("source_path", "")),
        "evidence_id": evidence_id,
        "confidence": item.get("confidence", spec.get("confidence", "medium")),
        "tags": "knowledgeos",
        "course_path": spec.get("course_path", "."),
        "summary": item.get("summary", spec.get("summary", "示例，不含用户真实课程内容。")),
        "content": item.get("content", spec.get("content", "示例内容，不含用户真实课程内容。")),
        "pending_review": item.get("pending_review", spec.get("pending_review", "无")),
    }


def first_or_default(items, default):
    return items[0] if isinstance(items, list) and items else default


def build_course_pack(course, template_dir, spec=None):
    template_dir = Path(template_dir)
    spec = dict(spec or demo_spec(course))
    spec.setdefault("course", course)
    files = {}

    # Course home
    files["00_课程主页.md"] = render((template_dir / "course-home.md").read_text(encoding="utf-8"), base_values(spec, item_type="course"))

    # Lessons
    lessons = spec.get("lessons") or demo_spec(spec["course"])["lessons"]
    for idx, lesson in enumerate(lessons, 1):
        lesson = dict(lesson)
        lesson.setdefault("lesson", f"第{idx:02d}节")
        lesson.setdefault("title", lesson["lesson"])
        rel = f"02_逐节总结/{safe_name(lesson['lesson'])}_{safe_name(lesson['title'])}.md"
        files[rel] = render((template_dir / "lesson-summary.md").read_text(encoding="utf-8"), base_values(spec, lesson, "lesson"))

    card_groups = [
        ("concepts", "concept-card.md", "concept", "03_知识卡片/概念_{title}.md"),
        ("methods", "method-card.md", "method", "03_知识卡片/方法_{title}.md"),
        ("cases", "case-card.md", "case", "03_知识卡片/案例_{title}.md"),
        ("reviews", "review-card.md", "review", "04_复习卡片/Q_{title}.md"),
        ("actions", "action-card.md", "action", "06_项目行动/{title}.md"),
    ]
    fallback = demo_spec(spec["course"])
    for key, template_name, item_type, rel_tpl in card_groups:
        items = spec.get(key) or fallback[key]
        for item in items:
            title = safe_name(item.get("title", item.get("lesson", item_type)))
            rel = rel_tpl.format(title=title)
            files[rel] = render((template_dir / template_name).read_text(encoding="utf-8"), base_values(spec, item, item_type))

    evidence_items = spec.get("evidence") or fallback["evidence"]
    for item in evidence_items:
        evidence_id = safe_name(item.get("id", item.get("evidence_id", "evidence-001")))
        files[f"07_证据索引/{evidence_id}.md"] = render((template_dir / "evidence-card.md").read_text(encoding="utf-8"), base_values(spec, item, "evidence"))

    report_item = {"title": "导入报告", "summary": spec.get("summary", "课程包生成报告。"), "content": "生成文件数量：待由运行报告确认。", "pending_review": spec.get("pending_review", "无")}
    files["08_导入报告.md"] = render((template_dir / "import-report.md").read_text(encoding="utf-8"), base_values(spec, report_item, "report"))

    canvas_data = {
        "course": spec["course"],
        "lessons": [i.get("title", i.get("lesson", "章节")) for i in lessons],
        "concepts": [i.get("title", "概念") for i in (spec.get("concepts") or fallback["concepts"])],
        "methods": [i.get("title", "方法") for i in (spec.get("methods") or fallback["methods"])],
        "cases": [i.get("title", "案例") for i in (spec.get("cases") or fallback["cases"])],
        "tasks": [i.get("title", "行动") for i in (spec.get("actions") or fallback["actions"])],
        "reviews": [i.get("title", "复习") for i in (spec.get("reviews") or fallback["reviews"])],
        "evidence": [i.get("id", i.get("evidence_id", "evidence")) for i in evidence_items],
    }
    files["01_课程地图.canvas"] = json.dumps(build_canvas(canvas_data), ensure_ascii=False, indent=2)
    for name, content in build_graphs(spec["course"]).items():
        files[f"05_视觉图解/{name}"] = content
    return files


def write_to_output(files, output_root, apply):
    output_root = Path(output_root)
    if not apply:
        return {"dry_run": True, "files": sorted(files)}
    for rel, content in files.items():
        target = output_root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")
    return {"dry_run": False, "output": str(output_root), "files": sorted(files)}


def write_to_vault(files, vault_root, apply):
    writer = SafeVaultWriter(vault_root, dry_run=not apply)
    for rel, content in files.items():
        writer.apply_write(rel, content)
    return writer.write_report()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--course", help="Course name. Optional when --spec provides course.")
    ap.add_argument("--spec", help="Path to a JSON course specification file.")
    ap.add_argument("--output")
    ap.add_argument("--vault")
    ap.add_argument("--template-dir", default="templates/v4")
    ap.add_argument("--report-dir", default="reports")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if args.apply and args.dry_run:
        raise SystemExit("--apply and --dry-run are mutually exclusive")
    if bool(args.output) == bool(args.vault):
        raise SystemExit("--output and --vault must be exactly one")
    spec = load_spec(args.spec) if args.spec else None
    course = args.course or (spec or {}).get("course")
    if not course:
        raise SystemExit("--course is required unless --spec provides course")
    files = build_course_pack(course, args.template_dir, spec=spec)
    result = write_to_output(files, args.output, args.apply) if args.output else write_to_vault(files, args.vault, args.apply)
    Path(args.report_dir).mkdir(parents=True, exist_ok=True)
    (Path(args.report_dir) / "generate-course-pack-report.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
