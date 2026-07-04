from pathlib import Path

from scripts.v5.generate_course_review_cards import generate


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_vault(tmp_path: Path) -> Path:
    vault = tmp_path / "vault"
    course = vault / "02_课程库" / "UI系统全能班"
    write(course / "00_课程总览.md", "# UI系统全能班\n")
    write(course / "05_复习与检索练习.md", "# 复习\n")
    return vault


def test_dry_run_does_not_write(tmp_path):
    vault = make_vault(tmp_path)
    result = generate(vault, apply=False)
    assert len(result["planned_cards"]) == 3
    assert not (vault / "04_复习卡片" / "V5课程多样化").exists()


def test_apply_writes_cards_and_backlinks(tmp_path):
    vault = make_vault(tmp_path)
    backup = tmp_path / "backup"
    result = generate(vault, apply=True, backup_dir=backup)
    cards = list((vault / "04_复习卡片" / "V5课程多样化").glob("*.md"))
    assert len(cards) == 3
    for card in cards:
        text = card.read_text(encoding="utf-8")
        assert text.startswith("---")
        assert "主动回忆候选卡" in text
        assert "真实来源" in text
    review = (vault / "02_课程库" / "UI系统全能班" / "05_复习与检索练习.md").read_text(encoding="utf-8")
    assert "V5 独立复习卡片入口" in review


def test_skip_existing_cards(tmp_path):
    vault = make_vault(tmp_path)
    generate(vault, apply=True, backup_dir=tmp_path / "backup")
    result = generate(vault, apply=False, skip_existing=True)
    assert result["planned_cards"] == []
