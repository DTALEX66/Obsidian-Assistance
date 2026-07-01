#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import argparse, json
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
    for k,v in values.items(): text=text.replace("{{"+k+"}}", str(v))
    return text


def demo_values(course):
    today=date.today().isoformat()
    return {"type":"lesson","status":"done","course":course,"lesson":"第01节","title":"示例章节","date":today,"updated":today,"source_type":"demo","source_path":"examples/v4-demo-course","evidence_id":"evidence-001","confidence":"medium","tags":"knowledgeos","course_path":".","summary":"示例，不含用户真实课程内容。","content":"这是 V4 Demo 生成内容，用于验证模板、Canvas、Mermaid、Dataview 和 Tasks 结构。","pending_review":"无真实课程内容；仅用于演示。"}


def build_course_pack(course, template_dir):
    template_dir=Path(template_dir); v=demo_values(course); files={}
    mapping={"00_课程主页.md":"course-home.md","02_逐节总结/第01节_示例章节.md":"lesson-summary.md","03_知识卡片/概念_输入箱.md":"concept-card.md","03_知识卡片/方法_课程处理流程.md":"method-card.md","03_知识卡片/案例_示例案例.md":"case-card.md","04_复习卡片/Q_什么是输入箱.md":"review-card.md","06_项目行动/行动清单.md":"action-card.md","07_证据索引/evidence-index.md":"evidence-card.md","08_导入报告.md":"import-report.md"}
    type_overrides={"03_知识卡片/概念_输入箱.md":"concept","03_知识卡片/方法_课程处理流程.md":"method","03_知识卡片/案例_示例案例.md":"case","04_复习卡片/Q_什么是输入箱.md":"review","06_项目行动/行动清单.md":"action","07_证据索引/evidence-index.md":"evidence","08_导入报告.md":"report"}
    for rel,tpl in mapping.items():
        vv=dict(v); vv["type"]=type_overrides.get(rel,"lesson")
        if rel=="00_课程主页.md": vv["type"]="course"
        files[rel]=render((template_dir/tpl).read_text(encoding="utf-8"), vv)
    files["01_课程地图.canvas"]=json.dumps(build_canvas({"course":course,"lessons":["第01节"],"concepts":["输入箱"],"methods":["课程处理流程"],"cases":["示例案例"],"tasks":["完成复习"],"reviews":["什么是输入箱"],"evidence":["evidence-001"]}),ensure_ascii=False,indent=2)
    for name,content in build_graphs(course).items(): files[f"05_视觉图解/{name}"]=content
    return files


def write_to_output(files, output_root, apply):
    output_root=Path(output_root)
    if not apply: return {"dry_run":True,"files":sorted(files)}
    for rel,content in files.items():
        target=output_root/rel; target.parent.mkdir(parents=True,exist_ok=True); target.write_text(content,encoding="utf-8",newline="\n")
    return {"dry_run":False,"output":str(output_root),"files":sorted(files)}


def write_to_vault(files, vault_root, apply):
    writer=SafeVaultWriter(vault_root,dry_run=not apply)
    for rel,content in files.items(): writer.apply_write(rel,content)
    return writer.write_report()


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--course",required=True); ap.add_argument("--output"); ap.add_argument("--vault"); ap.add_argument("--template-dir",default="templates/v4"); ap.add_argument("--report-dir",default="reports"); ap.add_argument("--apply",action="store_true"); ap.add_argument("--dry-run",action="store_true"); args=ap.parse_args()
    if bool(args.output)==bool(args.vault): raise SystemExit("--output and --vault must be exactly one")
    files=build_course_pack(args.course,args.template_dir)
    result=write_to_output(files,args.output,args.apply) if args.output else write_to_vault(files,args.vault,args.apply)
    Path(args.report_dir).mkdir(parents=True,exist_ok=True); (Path(args.report_dir)/"generate-course-pack-report.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8",newline="\n")
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__ == "__main__": main()
