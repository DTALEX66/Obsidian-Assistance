from pathlib import Path
import json

from scripts.v5.course_image_evidence_audit import audit, markdown_report


def write(path: Path, text: str = ""):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_image_evidence_audit_counts_direct_and_referenced_images(tmp_path):
    vault = tmp_path / "vault"
    c1 = vault / "02_课程库" / "视觉课程"
    c2 = vault / "02_课程库" / "纯文字课程"
    write(c1 / "00_课程总览.md", "# 视觉课程\n![[shot.png]]\n")
    write(c1 / "shot.png", "fake image bytes")
    write(c2 / "00_课程总览.md", "# 纯文字课程\n")
    data = audit(vault, limit=20)
    assert data["audited_courses"] == 2
    assert data["total_vault_images"] == 1
    rows = {c["course"]: c for c in data["courses"]}
    assert rows["视觉课程"]["status"] == "has-real-images"
    assert rows["视觉课程"]["direct_images"] == 1
    assert rows["视觉课程"]["referenced_images"] == 1
    assert rows["纯文字课程"]["status"] == "missing-real-images"


def test_image_evidence_markdown_report_is_balanced(tmp_path):
    vault = tmp_path / "vault"
    c = vault / "02_课程库" / "Demo"
    write(c / "00_课程总览.md", "# Demo\n")
    data = audit(vault, limit=20)
    md = markdown_report(data)
    assert "课程图片证据与关键帧采集清单" in md
    assert "不从互联网随便找图" in md
    assert md.count("```") % 2 == 0
