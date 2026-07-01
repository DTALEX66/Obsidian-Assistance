from pathlib import Path

from scripts.v4.obsidian_v4_audit import audit


def issues_for(root):
    return {item["issue"] for item in audit(Path(root))["issues"]}


def test_audit_flags_dangerous_python_delete_logic(tmp_path):
    bad = tmp_path / "bad_delete.py"
    bad.write_text("import shutil\nshutil.rmtree('somewhere')\n", encoding="utf-8")
    assert "dangerous_delete_logic" in issues_for(tmp_path)


def test_audit_flags_dangerous_shell_delete_logic(tmp_path):
    bad = tmp_path / "bad_delete.sh"
    bad.write_text("rm -rf ./somewhere\n", encoding="utf-8")
    assert "dangerous_delete_logic" in issues_for(tmp_path)


def test_audit_allows_safe_text(tmp_path):
    safe = tmp_path / "safe.py"
    safe.write_text("print('no delete here')\n", encoding="utf-8")
    result = audit(tmp_path)
    assert result["ok"] is True
    assert result["issues"] == []
