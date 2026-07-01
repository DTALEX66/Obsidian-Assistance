import json
from pathlib import Path
from scripts.v4.generate_canvas_map import build_canvas


def test_canvas_json_parse_demo_file():
    data = json.loads(Path("examples/v4-demo-course/01_课程地图.canvas").read_text(encoding="utf-8"))
    assert "nodes" in data and "edges" in data


def test_canvas_builder_has_nodes_edges():
    data = build_canvas({"course":"Demo","lessons":["L1"],"concepts":["C1"]})
    assert data["nodes"]
    assert isinstance(data["edges"], list)
