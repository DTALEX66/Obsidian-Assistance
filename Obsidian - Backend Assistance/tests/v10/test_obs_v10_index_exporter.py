import json
import subprocess
import sys
from pathlib import Path

from scripts.v10.obs_task_ledger import create_task
from scripts.v10.obs_v10_index_exporter import build_indexes, write_indexes


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_build_indexes_exports_lightweight_frontend_json(tmp_path):
    vault = tmp_path / "vault"
    source_root = tmp_path / "sources"
    db = tmp_path / "ledger.sqlite"
    write(vault / "02_课程库" / "课程A" / "00_课程总览.md", "# 课程A")
    write(source_root / "课程A" / "lesson.pdf", "%PDF-1.4 fake")
    create_task(
        db,
        title="课程转化补全：课程A",
        executor="course_transform",
        payload={"course": "课程A", "vault": str(vault), "dry_run": False},
        course="课程A",
    )

    indexes = build_indexes(vault=vault, source_root=source_root, ledger_db=db, limit=20)

    assert indexes["obs-v10-course-transform-index.json"]["schema"] == "obs-v10-course-transform-index/v1"
    assert indexes["obs-v10-source-manifest-index.json"]["schema"] == "obs-v10-source-manifest-index/v1"
    assert indexes["obs-v10-task-ledger-index.json"]["schema"] == "obs-v10-task-ledger-index/v1"
    assert indexes["obs-v10-course-transform-index.json"]["summary"]["courses_total"] == 1
    source_item = indexes["obs-v10-source-manifest-index.json"]["items"][0]
    assert "content" not in source_item
    assert "raw" not in json.dumps(indexes, ensure_ascii=False).lower()
    assert indexes["boundary"]["read_only"] is True


def test_write_indexes_writes_named_json_files(tmp_path):
    indexes = {
        "obs-v10-course-transform-index.json": {"schema": "obs-v10-course-transform-index/v1", "items": []},
        "boundary": {"read_only": True},
    }

    written = write_indexes(indexes, tmp_path)

    assert written == [str(tmp_path / "obs-v10-course-transform-index.json")]
    payload = json.loads((tmp_path / "obs-v10-course-transform-index.json").read_text(encoding="utf-8"))
    assert payload["schema"] == "obs-v10-course-transform-index/v1"


def test_cli_outputs_combined_json_without_writing(tmp_path):
    vault = tmp_path / "vault"
    source_root = tmp_path / "sources"
    write(vault / "02_课程库" / "课程A" / "00_课程总览.md", "# 课程A")
    write(source_root / "课程A" / "lesson.md", "# lesson")
    backend_root = Path(__file__).resolve().parents[2]

    result = subprocess.run(
        [
            sys.executable,
            "scripts/v10/obs_v10_index_exporter.py",
            "--vault",
            str(vault),
            "--source-root",
            str(source_root),
            "--limit",
            "20",
        ],
        cwd=backend_root,
        text=True,
        capture_output=True,
        timeout=30,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert "obs-v10-course-transform-index.json" in payload
    assert "written" not in payload
