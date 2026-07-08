#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OBS V10 sleep-mode course remediation batch runner.

Runs bounded batches of evidence-sidecar generation, then refreshes the
verification audit and writes a short batch report. It intentionally does not
write formal vault course bodies.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.v10.course_evidence_sidecar import build_course_sidecar  # noqa: E402
from scripts.v10.course_verification_audit import build_verification_audit, markdown_report  # noqa: E402

DEFAULT_VAULT = Path(os.environ.get("OBS_VAULT", ""))
DEFAULT_SOURCE = Path(os.environ.get("OBS_SOURCE_ROOT", ""))
DEFAULT_SIDECAR_ROOT = Path("docs/course-evidence-sidecars")
DEFAULT_OER_SIDECAR_ROOT = Path("docs/course-oer-sidecars")
DEFAULT_AUDIT_JSON = Path("docs/course-local-verification-audit-2026-07-07.json")
DEFAULT_AUDIT_MD = Path("docs/course-local-verification-audit-2026-07-07.md")
DEFAULT_REMEDIATION = Path("docs/course-verification-remediation-queue-2026-07-07.md")
DEFAULT_BATCH_DIR = Path("docs/course-sleep-mode-batches")


def now_stamp() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H%M%S")


def load_latest_audit(path: Path) -> dict[str, Any]:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"courses": [], "summary": {}, "environment": {}}


def select_batch(courses: list[dict[str, Any]], batch_size: int, only_courses: list[str] | None = None) -> list[dict[str, Any]]:
    if only_courses:
        wanted = set(only_courses)
        return [row for row in courses if row["course"] in wanted]
    needs = [row for row in courses if row.get("status") == "needs_review"]

    def priority(row: dict[str, Any]) -> tuple[int, int, str]:
        risks = set(row.get("hallucination_risks") or [])
        sidecar = row.get("sidecar_evidence") or {}
        score = 0
        if "missing_raw_source" in risks:
            score += 90
        if "audio_video_asr_pending" in risks and int(sidecar.get("asr_transcripts") or 0) == 0:
            score += 70
        if "missing_visual_evidence" in risks:
            score += 60
        if "raw_text_not_cross_confirmed" in risks:
            score += 40
        if "missing_oer_crosscheck" in risks:
            score += 20
        if not sidecar:
            score += 10
        return (-score, -len(risks), row["course"])

    return sorted(needs, key=priority)[:batch_size]


def sidecar_for_row(row: dict[str, Any], vault: Path, source_root: Path, sidecar_root: Path, asr_seconds: int, max_text_files: int, max_media_files: int, max_candidate_text_files: int, asr_start_seconds: int) -> dict[str, Any]:
    risks = set(row.get("hallucination_risks") or [])
    run_asr = "audio_video_asr_pending" in risks or (
        "raw_text_not_cross_confirmed" in risks and bool(row.get("evidence", {}).get("audio_video_present"))
    )
    return build_course_sidecar(
        course=row["course"],
        vault=vault,
        source_root=source_root,
        output_root=sidecar_root,
        max_text_files=max_text_files,
        max_media_files=max_media_files,
        max_candidate_text_files=max_candidate_text_files,
        run_asr=run_asr,
        asr_model="tiny",
        asr_seconds=asr_seconds,
        asr_start_seconds=asr_start_seconds,
    )


def refresh_audit(vault: Path, source_root: Path, sidecar_root: Path, oer_sidecar_root: Path, audit_json: Path, audit_md: Path, sample_limit: int) -> dict[str, Any]:
    audit = build_verification_audit(vault=vault, source_root=source_root, sidecar_root=sidecar_root, oer_sidecar_root=oer_sidecar_root, sample_limit=sample_limit)
    audit_json.parent.mkdir(parents=True, exist_ok=True)
    audit_json.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    audit_md.parent.mkdir(parents=True, exist_ok=True)
    audit_md.write_text(markdown_report(audit), encoding="utf-8")
    return audit


def write_remediation_queue(audit: dict[str, Any], output: Path) -> None:
    needs = [r for r in audit["courses"] if r["status"] == "needs_review"]
    lines = [
        "# 课程核验问题修复队列（2026-07-07）",
        "",
        "> 只记录待办，不把未核验课程标完成。所有课程必须有真实 evidence 后才可关闭任务。",
        "",
        "## 最新状态",
        f"- verified_by_available_methods: `{audit['summary']['verified_by_available_methods']}`",
        f"- needs_review: `{audit['summary']['needs_review']}`",
        f"- environment: `tesseract={audit['environment']['tesseract_available']}`, `whisper={audit['environment']['whisper_available']}`",
        f"- risk_counts: `{audit['summary']['risk_counts']}`",
        "",
        "## 修复队列",
        "| 课程 | 优先动作 | 风险 | 原始源 | 本地索引 | Sidecar(text/visual/keyframe/asr) | OER | 视觉 | 文本交叉 |",
        "|---|---|---|---:|---:|---|---:|---:|---|",
    ]
    for row in sorted(needs, key=lambda x: (-len(x["hallucination_risks"]), x["course"])):
        risks = row["hallucination_risks"]
        actions: list[str] = []
        if "missing_raw_source" in risks:
            actions.append("source_match")
        if "raw_text_not_cross_confirmed" in risks:
            actions.append("text_crosscheck")
        if "missing_oer_crosscheck" in risks:
            actions.append("oer_crosscheck")
        if "missing_visual_evidence" in risks:
            actions.append("visual_evidence")
        if "audio_video_asr_pending" in risks:
            actions.append("asr_run")
        if not actions:
            actions.append("manual_review")
        side = row.get("sidecar_evidence", {})
        side_label = "/".join(str(side.get(k, 0)) for k in ["text_sidecars", "visual_sidecars", "keyframes", "asr_transcripts"])
        text_cross = f"{row['text_consistency']['overlap_terms']} terms / {','.join(row['text_consistency']['methods'])}"
        lines.append(
            f"| {row['course']} | {', '.join(actions)} | {'、'.join(risks)} | {row['raw_matches']} | {row.get('local_source_refs', 0)} | {side_label} | {row['oer_matches']} | {row['visual_assets'] + row['embedded_visuals']} | {text_cross} |"
        )
    lines += [
        "",
        "## 关闭条件",
        "- 不能用预览、dry-run、echo、上下文打包结果关闭。",
        "- 每门课至少提供：原始源或本地来源索引、二次抽取文本重叠、视觉/关键帧或截图、OER/官方资料交叉、报告路径。",
    ]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_guard_checks(workdir: Path) -> dict[str, Any]:
    checks = []
    commands = [
        [sys.executable, "-m", "pytest", "tests/v10", "-q"],
        [sys.executable, "scripts/v4/obsidian_v4_audit.py", "."],
    ]
    for cmd in commands:
        proc = subprocess.run(cmd, cwd=workdir, text=True, capture_output=True, timeout=300)
        checks.append({"cmd": " ".join(cmd), "returncode": proc.returncode, "stdout": proc.stdout[-2000:], "stderr": proc.stderr[-1000:]})
    wav_count = len(list(workdir.rglob("*.wav")))
    sqlite_count = len(list(workdir.rglob("*.sqlite")))
    return {"checks": checks, "wav_count": wav_count, "sqlite_count": sqlite_count, "ok": all(c["returncode"] == 0 for c in checks) and wav_count == 0 and sqlite_count == 0}


def write_batch_report(path: Path, before: dict[str, Any], after: dict[str, Any], sidecars: list[dict[str, Any]], guard: dict[str, Any]) -> None:
    lines = [
        f"# 睡觉模式批次报告 {path.stem}",
        "",
        "## 边界",
        "- 只写 helper repo 证据、报告、批次日志；不写正式 vault 正文。",
        "- 未通过多源核验的课程仍保持 needs_review。",
        "",
        "## Summary before/after",
        f"- before: `{before.get('summary', {})}`",
        f"- after: `{after.get('summary', {})}`",
        "",
        "## Sidecars",
        "| 课程 | text | visual | keyframes | asr | manifest |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for item in sidecars:
        ev = item.get("evidence", {})
        lines.append(f"| {item['course']} | {ev.get('text_sidecars', 0)} | {ev.get('visual_sidecars', 0)} | {ev.get('keyframes', 0)} | {ev.get('asr_transcripts', 0)} | `{item.get('manifest_path', '')}` |")
    lines += [
        "",
        "## Guard checks",
        f"- ok: `{guard['ok']}`",
        f"- wav_count: `{guard['wav_count']}`",
        f"- sqlite_count: `{guard['sqlite_count']}`",
    ]
    for check in guard["checks"]:
        lines.append(f"- `{check['cmd']}` → `{check['returncode']}`")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run bounded OBS sleep-mode remediation batch")
    parser.add_argument("--vault", type=Path, default=DEFAULT_VAULT)
    parser.add_argument("--source-root", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--sidecar-root", type=Path, default=DEFAULT_SIDECAR_ROOT)
    parser.add_argument("--oer-sidecar-root", type=Path, default=DEFAULT_OER_SIDECAR_ROOT)
    parser.add_argument("--audit-json", type=Path, default=DEFAULT_AUDIT_JSON)
    parser.add_argument("--audit-md", type=Path, default=DEFAULT_AUDIT_MD)
    parser.add_argument("--remediation", type=Path, default=DEFAULT_REMEDIATION)
    parser.add_argument("--batch-dir", type=Path, default=DEFAULT_BATCH_DIR)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--sample-limit", type=int, default=4)
    parser.add_argument("--max-text-files", type=int, default=3)
    parser.add_argument("--max-candidate-text-files", type=int, default=30)
    parser.add_argument("--max-media-files", type=int, default=1)
    parser.add_argument("--asr-seconds", type=int, default=35)
    parser.add_argument("--asr-start-seconds", type=int, default=0)
    parser.add_argument("--course", action="append", help="Specific course to process; may repeat")
    args = parser.parse_args()
    if not str(args.vault) or not args.vault.exists():
        raise SystemExit("--vault is required or set OBS_VAULT")
    if not str(args.source_root) or not args.source_root.exists():
        raise SystemExit("--source-root is required or set OBS_SOURCE_ROOT")

    before = load_latest_audit(args.audit_json)
    if not before.get("courses"):
        before = refresh_audit(args.vault, args.source_root, args.sidecar_root, args.oer_sidecar_root, args.audit_json, args.audit_md, args.sample_limit)
    selected = select_batch(before["courses"], args.batch_size, args.course)
    sidecars = []
    for row in selected:
        sidecars.append(sidecar_for_row(row, args.vault, args.source_root, args.sidecar_root, args.asr_seconds, args.max_text_files, args.max_media_files, args.max_candidate_text_files, args.asr_start_seconds))
    after = refresh_audit(args.vault, args.source_root, args.sidecar_root, args.oer_sidecar_root, args.audit_json, args.audit_md, args.sample_limit)
    write_remediation_queue(after, args.remediation)
    guard = run_guard_checks(PROJECT_ROOT)
    report = args.batch_dir / f"batch-{now_stamp()}.md"
    write_batch_report(report, before, after, sidecars, guard)
    print(json.dumps({"selected": [r["course"] for r in selected], "sidecars": [s.get("evidence") for s in sidecars], "report": str(report), "after_summary": after.get("summary"), "guard_ok": guard["ok"]}, ensure_ascii=False, indent=2))
    return 0 if guard["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
