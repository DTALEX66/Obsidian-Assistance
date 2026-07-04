from pathlib import Path

BACKEND_README = Path("README.md")
SCRIPTS_README = Path("scripts/README_SCRIPTS.md")
ROOT_WORKFLOW = Path("../.github/workflows/repo-validation.yml")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_backend_readme_points_to_current_ci_and_workspace_demo_vault():
    text = read(BACKEND_README)

    assert ".github/workflows/repo-validation.yml" in text
    assert "v4-validation.yml" not in text
    assert "D:/All projects/Obsidian-Assistance/demo-vaults/OBS-V4-DEMO" in text
    assert "D:/OBS-V4-DEMO" not in text
    assert ROOT_WORKFLOW.exists()


def test_scripts_readme_is_current_v4_to_v9_operator_index():
    text = read(SCRIPTS_README)

    for section in ["V4", "V5", "V6", "V7", "V8", "V9"]:
        assert section in text
    for command in [
        "python -m pytest tests -q",
        "python scripts/v4/obsidian_v4_audit.py .",
        "--apply",
        "--dry-run",
    ]:
        assert command in text
    assert "01_scan_course_materials.ps1" not in text
    assert "D:/OBS-V4-DEMO" not in text
