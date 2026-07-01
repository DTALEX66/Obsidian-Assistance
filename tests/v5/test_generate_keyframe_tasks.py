from pathlib import Path

from scripts.v5.generate_keyframe_tasks import generate


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_vault(tmp_path: Path) -> Path:
    vault = tmp_path / "vault"
    course = vault / "02_课程库" / "UI系统全能班"
    write(course / "00_课程总览.md", "# UI系统全能班\n")
    write(course / "04_关键图表与课件索引.md", "# 视觉索引\n")
    return vault


def test_dry_run_does_not_write(tmp_path):
    vault = make_vault(tmp_path)
    result = generate(vault, apply=False)
    assert len(result["planned_tasks"]) == 1
    assert not (vault / "02_课程库" / "UI系统全能班" / "10_关键帧采集任务单.md").exists()


def test_apply_writes_task_and_visual_link(tmp_path):
    vault = make_vault(tmp_path)
    result = generate(vault, apply=True, backup_dir=tmp_path / "backup")
    task = vault / "02_课程库" / "UI系统全能班" / "10_关键帧采集任务单.md"
    assert task.exists()
    text = task.read_text(encoding="utf-8")
    assert "不能添加截图、占位图或互联网图片" in text
    visual = (vault / "02_课程库" / "UI系统全能班" / "04_关键图表与课件索引.md").read_text(encoding="utf-8")
    assert "关键帧采集任务" in visual


def test_skip_existing_tasks(tmp_path):
    vault = make_vault(tmp_path)
    generate(vault, apply=True, backup_dir=tmp_path / "backup")
    result = generate(vault, apply=False, skip_existing=True)
    assert result["planned_tasks"] == []
