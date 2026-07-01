from pathlib import Path
import json

from scripts.v5.course_diversity_audit import audit_vault, markdown_report


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_course_diversity_audit_detects_text_heavy_and_rich_courses(tmp_path):
    vault = tmp_path / "vault"
    text_course = vault / "02_课程库" / "纯文字课程"
    rich_course = vault / "02_课程库" / "丰富课程"
    write(text_course / "00_课程总览.md", "# 纯文字课程\n\n来源：素材识别。\n复习问题：什么是核心概念？\n")
    write(rich_course / "00_课程总览.md", """# 丰富课程

> [!note] 重点
> 这是一门 demo。

![[image.png]]

| 模块 | 输出 |
|---|---|
| A | B |

```mermaid
flowchart TD
A --> B
```

```dataview
TABLE status
FROM ""
```

- [ ] 完成练习

课程地图.canvas
来源：视频/OCR/PDF 已核验。
复习题：请解释流程。
行动清单：完成案例。
""")
    result = audit_vault(vault, limit=20)
    assert result["audited_courses"] == 2
    rows = {c["course"]: c for c in result["courses"]}
    assert rows["纯文字课程"]["coverage_level"] == "text-heavy"
    assert rows["丰富课程"]["diversity_score"] >= 8
    assert rows["丰富课程"]["coverage_level"] == "rich"


def test_markdown_report_contains_minimum_standard(tmp_path):
    vault = tmp_path / "vault"
    course = vault / "02_课程库" / "Demo课程"
    write(course / "00_课程总览.md", "# Demo\n纯文字。\n")
    result = audit_vault(vault, limit=20)
    md = markdown_report(result)
    assert "课程内容验证与多样化审计报告" in md
    assert "推荐最低标准" in md
    assert "02_课程地图.canvas" in md


def test_course_diversity_templates_are_scoped_and_structured():
    root = Path(__file__).resolve().parents[2]
    for rel in [
        "templates/obsidian/course-diversity/review-practice.md",
        "templates/obsidian/course-diversity/visual-index.md",
        "templates/obsidian/course-diversity/verification.md",
    ]:
        text = (root / rel).read_text(encoding="utf-8")
        assert text.startswith("---\n"), rel
        assert "{{course}}" in text
        assert "```" not in text or text.count("```") % 2 == 0
