import subprocess
import sys
from pathlib import Path
from scripts.v4.generate_mermaid_graph import build_graphs


def test_build_mermaid_graphs_have_blocks():
    graphs = build_graphs("Demo课程")
    assert len(graphs) == 3
    for content in graphs.values():
        assert "```mermaid" in content


def test_demo_mermaid_files_have_blocks():
    for p in Path("examples/v4-demo-course/05_视觉图解").glob("*.md"):
        assert "```mermaid" in p.read_text(encoding="utf-8")


def test_mermaid_cli_output_defaults_to_dry_run(tmp_path):
    output = tmp_path / "graphs"
    result = subprocess.run(
        [sys.executable, "scripts/v4/generate_mermaid_graph.py", "--course", "Demo", "--output", str(output)],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0
    assert not output.exists()
    assert "dry_run" in result.stdout


def test_mermaid_cli_apply_writes_output(tmp_path):
    output = tmp_path / "graphs"
    result = subprocess.run(
        [sys.executable, "scripts/v4/generate_mermaid_graph.py", "--course", "Demo", "--output", str(output), "--apply"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0
    assert (output / "课程流程图.md").exists()
    assert "```mermaid" in (output / "课程流程图.md").read_text(encoding="utf-8")
