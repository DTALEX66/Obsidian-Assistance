from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]

REQUIRED = [
    "docs/research/obsidian-knowledgeos-upgrade-evidence.md",
    "docs/v5-obsidian-knowledgeos-upgrade-analysis.md",
    "docs/v5-talos-ai-os-dashboard-spec.md",
    "templates/obsidian/standard-note.md",
    "templates/obsidian/moc.md",
    "templates/obsidian/dashboard-home.md",
    "templates/obsidian/knowledge-health-dashboard.md",
    "templates/obsidian/course-card-wall.md",
    "templates/obsidian/domain-home.md",
    "snippets/v5/talos-dashboard.css",
    "examples/v5-talos-dashboard/README.md",
    "examples/v5-talos-dashboard/50_Dashboard/今日工作台_Talos.md",
    "examples/v5-talos-dashboard/50_Dashboard/知识库健康度_Talos.md",
    "examples/v5-talos-dashboard/40_Wiki/MOC/MOC_示例主题.md",
]

FORBIDDEN_PATTERNS = [
    re.compile(r"E:[\\/]BaiduSyncdisk[\\/]Obsidian知识库"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def is_obsidian_note(rel: str) -> bool:
    if rel.startswith("templates/obsidian/"):
        return rel.endswith(".md")
    if rel.startswith("examples/v5-talos-dashboard/") and rel.endswith(".md"):
        return not rel.endswith("README.md")
    return False


def test_required_v5_knowledgeos_assets_exist():
    missing = [rel for rel in REQUIRED if not (ROOT / rel).exists()]
    assert missing == []


def test_markdown_fences_are_balanced():
    for rel in REQUIRED:
        if rel.endswith(".md"):
            text = read(rel)
            assert text.count("```") % 2 == 0, rel


def test_templates_and_demo_notes_have_frontmatter():
    for rel in REQUIRED:
        if is_obsidian_note(rel):
            text = read(rel)
            assert text.startswith("---\n"), rel


def test_dashboard_like_assets_include_dataview_blocks():
    dashboard_files = [
        rel
        for rel in REQUIRED
        if rel.endswith(".md") and ("dashboard" in rel.lower() or "Dashboard" in rel or "Talos" in rel or "MOC" in rel)
    ]
    assert any("```dataview" in read(rel) for rel in dashboard_files)


def test_css_is_scoped_to_knowledgeos_v5():
    css = read("snippets/v5/talos-dashboard.css")
    assert ".knowledgeos-v5" in css
    assert ".talos-dashboard" in css
    assert "body {" not in css
    assert ".workspace" not in css
    assert "!important" not in css


def test_no_private_vault_paths_or_secret_like_values():
    offenders = []
    for rel in REQUIRED:
        text = read(rel)
        for pattern in FORBIDDEN_PATTERNS:
            if pattern.search(text):
                offenders.append(rel)
    assert offenders == []


def test_downloaded_reference_files_are_public_docs_only():
    downloaded = ROOT / "docs/research/downloaded"
    assert (downloaded / "dataview-readme.md").exists()
    assert (downloaded / "obsidian-sample-plugin-readme.md").exists()
    assert (downloaded / "obsidian-sample-plugin-manifest.json").exists()
    for path in downloaded.iterdir():
        assert path.suffix in {".md", ".json"}
