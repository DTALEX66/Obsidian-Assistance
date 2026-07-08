import json
import subprocess
import sys
from pathlib import Path

from scripts.v10.obs_task_ledger import create_task
from scripts.v10.obs_dataview_query import available_tables, query_records, run_query


def test_query_records_filters_sorts_limits_and_projects_fields():
    rows = [
        {"course": "A", "missing_count": 3, "has_keyframes": False, "status": "pending"},
        {"course": "B", "missing_count": 1, "has_keyframes": True, "status": "done"},
        {"course": "C", "missing_count": 2, "has_keyframes": False, "status": "pending"},
    ]

    result = query_records(
        "TABLE course, missing_count FROM courses WHERE status='pending' AND has_keyframes=false SORT missing_count DESC LIMIT 1",
        rows,
    )

    assert result["count"] == 1
    assert result["items"] == [{"course": "A", "missing_count": 3}]
    assert result["parsed"]["table"] == "courses"


def test_run_query_can_read_course_transform_ledger_table(tmp_path):
    vault = tmp_path / "vault"
    course = vault / "02_课程库" / "缺口课程"
    course.mkdir(parents=True)
    (course / "00_课程总览.md").write_text("# 缺口课程", encoding="utf-8")

    result = run_query(
        "FROM courses WHERE missing_count>0 SORT missing_count DESC LIMIT 5",
        vault=vault,
    )

    assert result["table"] == "courses"
    assert result["count"] == 1
    assert result["items"][0]["course"] == "缺口课程"
    assert result["items"][0]["missing_count"] > 0


def test_run_query_can_read_task_ledger_table(tmp_path):
    db = tmp_path / "ledger.sqlite"
    create_task(
        db,
        title="课程转化补全：缺口课程",
        executor="course_transform",
        payload={"course": "缺口课程", "vault": "vault", "dry_run": False},
        course="缺口课程",
        priority=10,
    )

    result = run_query("LIST course FROM tasks WHERE status='pending' LIMIT 10", ledger_db=db)

    assert result["table"] == "tasks"
    assert result["items"] == [{"course": "缺口课程"}]


def test_available_tables_documents_safe_read_only_sources():
    tables = available_tables()

    assert "courses" in tables
    assert "tasks" in tables
    assert "sources" in tables
    assert tables["sources"]["content_included"] is False


def test_cli_outputs_json_from_backend_root(tmp_path):
    vault = tmp_path / "vault"
    course = vault / "02_课程库" / "缺口课程"
    course.mkdir(parents=True)
    (course / "00_课程总览.md").write_text("# 缺口课程", encoding="utf-8")
    backend_root = Path(__file__).resolve().parents[2]

    result = subprocess.run(
        [
            sys.executable,
            "scripts/v10/obs_dataview_query.py",
            "--vault",
            str(vault),
            "FROM courses WHERE missing_count>0 LIMIT 1",
        ],
        cwd=backend_root,
        text=True,
        capture_output=True,
        timeout=30,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["items"][0]["course"] == "缺口课程"
