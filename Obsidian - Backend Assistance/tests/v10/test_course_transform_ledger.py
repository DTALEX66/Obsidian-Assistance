import json
import subprocess
import sys
from pathlib import Path

from scripts.v10.course_transform_ledger import (
    build_course_transform_ledger,
    generate_tasks,
    markdown_report,
    seed_task_ledger,
)
from scripts.v10.obs_task_ledger import list_tasks, status_summary


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_build_course_transform_ledger_detects_missing_pages_reports_and_assets(tmp_path):
    vault = tmp_path / "vault"
    course = vault / "02_课程库" / "示例课程"
    write(course / "00_课程总览.md", "# 示例课程")
    write(course / "08_术语索引.md", "# 术语")
    write(vault / "93_导入报告" / "示例课程_导入报告.md", "# 报告")
    write(
        vault / "99_附件" / "verified-keyframes" / "keyframe-registry.json",
        json.dumps({"items": [{"course": "示例课程", "path": "99_附件/verified-keyframes/示例课程/p1.png"}]}, ensure_ascii=False),
    )

    ledger = build_course_transform_ledger(vault)

    assert ledger["summary"]["courses_total"] == 1
    row = ledger["courses"][0]
    assert row["course"] == "示例课程"
    assert row["has_keyframes"] is True
    assert row["report_count"] == 1
    assert "01_素材识别报告.md" in row["missing_pages"]
    assert "07_实操工作流.md" in row["missing_pages"]
    assert "12_真实截图与关键帧.md" in row["missing_pages"]


def test_generate_tasks_creates_course_transform_tasks_only_for_real_gaps(tmp_path):
    vault = tmp_path / "vault"
    complete = vault / "02_课程库" / "完整课程"
    incomplete = vault / "02_课程库" / "缺口课程"
    for name in [
        "00_课程总览.md",
        "01_素材识别报告.md",
        "07_实操工作流.md",
        "08_术语索引.md",
        "12_真实截图与关键帧.md",
        "13_项目转化.md",
        "14_开放知识交叉对比.md",
    ]:
        write(complete / name, f"# {name}")
    write(vault / "93_导入报告" / "完整课程_导入报告.md", "# 报告")
    write(
        vault / "99_附件" / "verified-keyframes" / "keyframe-registry.json",
        json.dumps(
            {"items": [{"course": "完整课程", "path": "99_附件/verified-keyframes/完整课程/p1.png"}]},
            ensure_ascii=False,
        ),
    )
    write(incomplete / "00_课程总览.md", "# 缺口课程")

    tasks = generate_tasks(build_course_transform_ledger(vault))

    assert [task["course"] for task in tasks] == ["缺口课程"]
    assert tasks[0]["executor"] == "course_transform"
    assert tasks[0]["payload"]["missing_pages"]
    assert tasks[0]["payload"]["dry_run"] is not True


def test_seed_task_ledger_creates_pending_tasks_with_verifiable_payload(tmp_path):
    vault = tmp_path / "vault"
    write(vault / "02_课程库" / "缺口课程" / "00_课程总览.md", "# 缺口课程")
    db = tmp_path / "obs-task-ledger.sqlite"

    tasks = generate_tasks(build_course_transform_ledger(vault))
    created = seed_task_ledger(db, tasks)

    assert len(created) == 1
    assert status_summary(db)["pending"] == 1
    rows = list_tasks(db)
    assert rows[0]["executor"] == "course_transform"
    assert rows[0]["payload"]["course"] == "缺口课程"


def test_seed_task_ledger_is_idempotent_for_same_pending_task(tmp_path):
    vault = tmp_path / "vault"
    write(vault / "02_课程库" / "缺口课程" / "00_课程总览.md", "# 缺口课程")
    db = tmp_path / "obs-task-ledger.sqlite"
    tasks = generate_tasks(build_course_transform_ledger(vault))

    first = seed_task_ledger(db, tasks)
    second = seed_task_ledger(db, tasks)

    assert len(first) == 1
    assert second == []
    assert status_summary(db)["pending"] == 1


def test_markdown_report_exposes_source_to_asset_to_course_page_mapping(tmp_path):
    vault = tmp_path / "vault"
    write(vault / "02_课程库" / "缺口课程" / "00_课程总览.md", "# 缺口课程")

    report = markdown_report(build_course_transform_ledger(vault))

    assert "原始来源" in report
    assert "扫描报告" in report
    assert "生成资产" in report
    assert "registry" in report
    assert "课程页" in report
    assert "下一步" in report
    assert "缺口课程" in report


def test_cli_runs_from_backend_root_without_import_path_errors(tmp_path):
    vault = tmp_path / "vault"
    write(vault / "02_课程库" / "缺口课程" / "00_课程总览.md", "# 缺口课程")
    backend_root = Path(__file__).resolve().parents[2]

    result = subprocess.run(
        [
            sys.executable,
            "scripts/v10/course_transform_ledger.py",
            "--vault",
            str(vault),
            "--tasks",
            "--limit",
            "1",
        ],
        cwd=backend_root,
        text=True,
        capture_output=True,
        timeout=30,
    )

    assert result.returncode == 0, result.stderr
    tasks = json.loads(result.stdout)
    assert tasks[0]["course"] == "缺口课程"
