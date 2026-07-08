from scripts.v10.obs_task_ledger import (
    create_task,
    has_real_evidence,
    init_schema,
    list_tasks,
    record_result,
    status_summary,
    validate_real_task,
)


def test_validate_real_task_blocks_virtual_or_dry_run_tasks():
    assert validate_real_task("echo", {"message": "done"}) == (False, "non_real_executor_blocked:echo")
    assert validate_real_task("safe_write", {"path": "x.md", "dry_run": True}) == (False, "dry_run_task_blocked")
    assert validate_real_task("file_read", {"path": "x.md"}) == (True, "real_task_allowed")


def test_has_real_evidence_requires_verifiable_result_payload():
    assert has_real_evidence("file_read", {"path": "x.md", "content": "hello"}) == (True, "file_read_content_evidence")
    assert has_real_evidence("file_read", {"path": "x.md"}) == (False, "missing_file_read_evidence")
    assert has_real_evidence("safe_write", {"written": True, "path": "x.md"}) == (True, "safe_write_written_evidence")
    assert has_real_evidence("source_scan", {"count": 2, "items": [{"path": "a.pdf"}]}) == (True, "source_scan_count_evidence")


def test_ledger_marks_task_done_only_after_real_evidence(tmp_path):
    db = tmp_path / "obs-task-ledger.sqlite"
    init_schema(db)
    task = create_task(db, title="读取课程处理工作台", executor="file_read", payload={"path": "02_课程库/01_课程处理工作台.md"})

    blocked = record_result(db, task["id"], {"path": "02_课程库/01_课程处理工作台.md"})
    assert blocked["status"] == "blocked"
    assert blocked["reason"] == "missing_file_read_evidence"

    done = record_result(db, task["id"], {"path": "02_课程库/01_课程处理工作台.md", "content": "# 工作台"})
    assert done["status"] == "done"
    assert done["reason"] == "file_read_content_evidence"

    rows = list_tasks(db)
    assert rows[0]["status"] == "done"
    assert status_summary(db)["done"] == 1


def test_create_task_blocks_non_real_executor_immediately(tmp_path):
    db = tmp_path / "obs-task-ledger.sqlite"
    init_schema(db)
    task = create_task(db, title="虚假心跳", executor="echo", payload={"message": "done"})

    assert task["status"] == "blocked"
    assert "non_real_executor_blocked" in task["error"]
    assert status_summary(db)["blocked"] == 1
