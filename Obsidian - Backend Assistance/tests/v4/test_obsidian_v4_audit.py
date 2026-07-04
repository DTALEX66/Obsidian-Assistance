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


def test_audit_skips_own_script_and_tests_from_nested_repo_root(tmp_path):
    audit_script = tmp_path / "Obsidian - Backend Assistance" / "scripts" / "v4" / "obsidian_v4_audit.py"
    audit_script.parent.mkdir(parents=True)
    audit_script.write_text("DANGEROUS_DELETE_RE = 'rm -rf'\n", encoding="utf-8")

    test_file = tmp_path / "Obsidian - Backend Assistance" / "tests" / "v4" / "test_obsidian_v4_audit.py"
    test_file.parent.mkdir(parents=True)
    test_file.write_text("def test_example():\n    assert 'rm -rf'\n", encoding="utf-8")

    result = audit(tmp_path)
    assert result["ok"] is True
    assert result["issues"] == []


def test_audit_flags_open_design_artifact_metadata(tmp_path):
    artifact = tmp_path / "index.html.artifact.json"
    artifact.write_text('{"tool": "open-design"}\n', encoding="utf-8")
    assert "open_design_artifact_metadata" in issues_for(tmp_path)


def test_audit_flags_open_design_artifact_metadata_case_insensitive(tmp_path):
    artifact = tmp_path / "preview.HTML.ARTIFACT.JSON"
    artifact.write_text('{"tool": "open-design"}\n', encoding="utf-8")
    assert "open_design_artifact_metadata" in issues_for(tmp_path)


def test_audit_does_not_skip_unrelated_same_named_audit_script(tmp_path):
    bad = tmp_path / "other_project" / "scripts" / "v4" / "obsidian_v4_audit.py"
    bad.parent.mkdir(parents=True)
    bad.write_text("import shutil\nshutil.rmtree('somewhere')\n", encoding="utf-8")
    assert "dangerous_delete_logic" in issues_for(tmp_path)


def test_audit_flags_tracked_obsidian_runtime_paths(tmp_path):
    snippet = tmp_path / "pack" / ".obsidian" / "snippets" / "demo.css"
    snippet.parent.mkdir(parents=True)
    snippet.write_text("body {}\n", encoding="utf-8")
    assert "obsidian_runtime_path" in issues_for(tmp_path)
