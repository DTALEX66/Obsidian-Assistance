import json
import subprocess
import sys
from scripts.v4.generate_bases_views import build_views


def test_build_bases_views_has_expected_views():
    data = build_views("Demo课程")
    names = [view["name"] for view in data["views"]]
    assert "课程章节" in names
    assert "知识卡片" in names
    assert data["course"] == "Demo课程"


def test_bases_cli_output_defaults_to_dry_run(tmp_path):
    output = tmp_path / "bases.json"
    result = subprocess.run(
        [sys.executable, "scripts/v4/generate_bases_views.py", "--course", "Demo", "--output", str(output)],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0
    assert not output.exists()
    assert "dry_run" in result.stdout


def test_bases_cli_apply_writes_output(tmp_path):
    output = tmp_path / "bases.json"
    result = subprocess.run(
        [sys.executable, "scripts/v4/generate_bases_views.py", "--course", "Demo", "--output", str(output), "--apply"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0
    assert output.exists()
    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["course"] == "Demo"
