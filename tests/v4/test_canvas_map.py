import json
import subprocess
import sys
from pathlib import Path
from scripts.v4.generate_canvas_map import build_canvas


def test_canvas_json_parse_demo_file():
    data = json.loads(Path("examples/v4-demo-course/01_课程地图.canvas").read_text(encoding="utf-8"))
    assert "nodes" in data and "edges" in data


def test_canvas_builder_has_nodes_edges():
    data = build_canvas({"course":"Demo","lessons":["L1"],"concepts":["C1"]})
    assert data["nodes"]
    assert isinstance(data["edges"], list)


def test_canvas_cli_output_defaults_to_dry_run(tmp_path):
    output = tmp_path / "map.canvas"
    result = subprocess.run(
        [sys.executable, "scripts/v4/generate_canvas_map.py", "--output", str(output)],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0
    assert not output.exists()
    assert "dry_run" in result.stdout


def test_canvas_cli_apply_writes_output(tmp_path):
    output = tmp_path / "map.canvas"
    result = subprocess.run(
        [sys.executable, "scripts/v4/generate_canvas_map.py", "--output", str(output), "--apply"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0
    assert output.exists()
    json.loads(output.read_text(encoding="utf-8"))
