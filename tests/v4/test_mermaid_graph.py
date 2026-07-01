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
