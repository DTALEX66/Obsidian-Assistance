from pathlib import Path
import json

from scripts.v5.generate_course_diversity_pack import generate


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_vault(tmp_path: Path) -> Path:
    vault = tmp_path / "vault"
    course = vault / "02_课程库" / "UI系统全能班"
    write(course / "00_课程总览.md", "# UI系统全能班\n\n- 设计系统\n- 组件规范\n")
    write(course / "03_模块总结.md", "# 模块总结\n\n- 原子组件：按钮、输入框、卡片。\n- 设计规范：颜色、字号、间距。\n")
    write(course / "07_实操工作流.md", "# 工作流\n\n- 建立组件库\n- 输出设计规范\n")
    return vault


def test_dry_run_does_not_write(tmp_path):
    vault = make_vault(tmp_path)
    result = generate(vault, limit=20, apply=False, backup_dir=None)
    assert result["courses"] == 1
    assert len(result["planned_writes"]) == 4
    course = vault / "02_课程库" / "UI系统全能班"
    assert not (course / "04_关键图表与课件索引.md").exists()


def test_apply_writes_diversity_pack_and_valid_canvas(tmp_path):
    vault = make_vault(tmp_path)
    backup = tmp_path / "backup"
    result = generate(vault, limit=20, apply=True, backup_dir=backup)
    course = vault / "02_课程库" / "UI系统全能班"
    for name in ["02_课程地图.canvas", "04_关键图表与课件索引.md", "05_复习与检索练习.md", "06_验证与不确定项.md"]:
        assert (course / name).exists(), name
    canvas = json.loads((course / "02_课程地图.canvas").read_text(encoding="utf-8"))
    assert canvas["nodes"]
    assert canvas["edges"]
    visual = (course / "04_关键图表与课件索引.md").read_text(encoding="utf-8")
    assert "```mermaid" in visual
    assert "不编造图片" in visual
    assert result["planned_writes"][0]["action"] == "create"


def test_second_apply_backs_up_overwrites(tmp_path):
    vault = make_vault(tmp_path)
    backup = tmp_path / "backup"
    generate(vault, limit=20, apply=True, backup_dir=backup)
    generate(vault, limit=20, apply=True, backup_dir=backup)
    backups = list(backup.glob("*.before"))
    assert backups
    assert any("04_关键图表" in p.name for p in backups)


def test_generated_markdown_fences_are_balanced(tmp_path):
    vault = make_vault(tmp_path)
    backup = tmp_path / "backup"
    generate(vault, limit=20, apply=True, backup_dir=backup)
    for p in (vault / "02_课程库" / "UI系统全能班").glob("*.md"):
        text = p.read_text(encoding="utf-8")
        assert text.count("```") % 2 == 0, p
