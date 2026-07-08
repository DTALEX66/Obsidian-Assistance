from pathlib import Path

from scripts.v10.cognitive_vault_garden import (
    audit,
    detect_atomicity,
    extract_keywords,
    markdown_report,
    parse_links,
    suggest_tags,
)


def write(path: Path, text: str = ""):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_auto_tagger_extracts_keywords_tags_and_atomicity():
    text = """# Obsidian AI 课程管道

Obsidian vault 使用 Markdown、Dataview、wikilink 和 evidence pipeline 管理课程。"""
    keywords = extract_keywords(text, top_k=5)
    tags = suggest_tags(text, max_tags=5)
    atomic = detect_atomicity(text)

    assert keywords
    assert "obsidian" in tags
    assert atomic["is_atomic"] is True


def test_parse_links_handles_wikilinks_embeds_and_local_markdown_links():
    refs = parse_links("See [[课程A|A]] and ![[img.png]] plus [local](docs/page.md) and [web](https://example.com)")
    targets = {r.target for r in refs}

    assert "课程A" in targets
    assert "img.png" in targets
    assert "docs/page.md" in targets
    assert "https://example.com" not in targets
    assert any(r.is_embed for r in refs if r.target == "img.png")


def test_audit_finds_orphans_unresolved_links_and_suggestions(tmp_path):
    vault = tmp_path / "vault"
    write(
        vault / "02_课程库" / "课程A" / "00_课程总览.md",
        """---
tags: [obsidian, pipeline]
---
# 课程A

Obsidian pipeline evidence index dataview automation. [[不存在的课程]]
""",
    )
    write(
        vault / "02_课程库" / "课程B" / "00_课程总览.md",
        """---
tags:
  - obsidian
  - pipeline
---
# 课程B

Obsidian pipeline evidence index automation review.
""",
    )
    write(vault / "03_知识卡片" / "卡片C.md", "# 卡片C\n\nCompletely isolated note.")

    data = audit(vault, include_dirs=["02_课程库", "03_知识卡片"])

    assert data["notes_total"] == 3
    assert data["unresolved_notes"] == 1
    assert any("不存在的课程" in item["targets"] for item in data["unresolved_links"])
    assert data["orphans_total"] >= 1
    assert data["connection_suggestions"]


def test_markdown_report_contains_candidate_boundary(tmp_path):
    vault = tmp_path / "vault"
    write(vault / "02_课程库" / "课程A" / "00_课程总览.md", "# 课程A\n\n[[课程B]]")
    write(vault / "02_课程库" / "课程B" / "00_课程总览.md", "# 课程B\n\nObsidian Dataview")

    md = markdown_report(audit(vault, include_dirs=["02_课程库"]))

    assert "candidate-only" in md
    assert "不修改正式笔记" in md
    assert "V10 Cognitive Vault Garden Audit" in md
    assert md.count("```") % 2 == 0
