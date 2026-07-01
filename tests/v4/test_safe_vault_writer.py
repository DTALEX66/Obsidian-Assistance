from pathlib import Path
from scripts.v4.safe_vault_writer import SafeVaultWriter


def test_dry_run_does_not_write(tmp_path):
    root = tmp_path / "测试库"
    root.mkdir()
    writer = SafeVaultWriter(root, dry_run=True)
    writer.apply_write("A/示例.md", "hello")
    assert not (root / "A/示例.md").exists()


def test_apply_writes_and_backup_existing(tmp_path):
    root = tmp_path / "vault"
    root.mkdir()
    target = root / "A.md"
    target.write_text("old", encoding="utf-8")
    backup = tmp_path / "backup"
    writer = SafeVaultWriter(root, backup_root=backup, dry_run=False)
    writer.apply_write("A.md", "new")
    writer.write_report()
    assert target.read_text(encoding="utf-8") == "new"
    assert (backup / "A.md").exists()
    assert (backup / "write-plan.json").exists()
    assert (backup / "write-report.md").exists()


def test_path_traversal_blocked(tmp_path):
    root = tmp_path / "vault"
    root.mkdir()
    writer = SafeVaultWriter(root, dry_run=True)
    try:
        writer.resolve_inside_vault("../outside.md")
    except ValueError:
        return
    raise AssertionError("path traversal should be blocked")
