#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Safe Vault Writer for Obsidian-Assistance V4.

Default mode is dry-run. Explicit --apply is required to write files.
This module never deletes files. Existing targets are copied to backup_root
before overwrite.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import shutil
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional


@dataclass
class WriteItem:
    relative_path: str
    target_path: str
    bytes: int
    action: str
    backup_path: Optional[str] = None


class SafeVaultWriter:
    def __init__(self, vault_root, backup_root=None, dry_run=True):
        self.vault_root = Path(vault_root).expanduser().resolve()
        if not self.vault_root.exists():
            raise ValueError(f"vault_root does not exist: {self.vault_root}")
        self.backup_root = Path(backup_root).expanduser().resolve() if backup_root else self.vault_root / "93_导入报告" / ("V4_备份_" + _dt.datetime.now().strftime("%Y%m%d_%H%M%S"))
        self.dry_run = dry_run
        self.items: List[WriteItem] = []

    def resolve_inside_vault(self, relative_path):
        rel = Path(relative_path)
        if rel.is_absolute():
            raise ValueError("relative_path must not be absolute")
        target = (self.vault_root / rel).resolve()
        try:
            target.relative_to(self.vault_root)
        except ValueError as exc:
            raise ValueError(f"path traversal blocked: {relative_path}") from exc
        return target

    def plan_write(self, relative_path, content):
        target = self.resolve_inside_vault(relative_path)
        action = "overwrite" if target.exists() else "create"
        item = WriteItem(str(relative_path), str(target), len(content.encode("utf-8")), action)
        self.items.append(item)
        return item

    def backup_existing(self, target_path):
        target = Path(target_path).resolve()
        try:
            rel = target.relative_to(self.vault_root)
        except ValueError as exc:
            raise ValueError("backup target outside vault") from exc
        backup = (self.backup_root / rel).resolve()
        if not self.dry_run:
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, backup)
        return backup

    def apply_write(self, relative_path, content):
        target = self.resolve_inside_vault(relative_path)
        action = "overwrite" if target.exists() else "create"
        backup_path = None
        if target.exists():
            backup_path = str(self.backup_existing(target))
        item = WriteItem(str(relative_path), str(target), len(content.encode("utf-8")), action, backup_path)
        self.items.append(item)
        if not self.dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8", newline="\n")
        return item

    def write_report(self):
        plan = {
            "dry_run": self.dry_run,
            "vault_root": str(self.vault_root),
            "backup_root": str(self.backup_root),
            "items": [asdict(i) for i in self.items],
        }
        plan_path = self.backup_root / "write-plan.json"
        report_path = self.backup_root / "write-report.md"
        if not self.dry_run:
            self.backup_root.mkdir(parents=True, exist_ok=True)
            plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
            lines = ["# V4 Write Report", "", f"dry_run: `{self.dry_run}`", "", "| Action | Relative Path | Bytes | Backup |", "|---|---|---:|---|"]
            for i in self.items:
                lines.append(f"| {i.action} | `{i.relative_path}` | {i.bytes} | `{i.backup_path or ''}` |")
            report_path.write_text("\n".join(lines)+"\n", encoding="utf-8", newline="\n")
        return {"plan": plan, "plan_path": str(plan_path), "report_path": str(report_path)}


def main():
    parser = argparse.ArgumentParser(description="Safe writer for V4 Obsidian outputs")
    parser.add_argument("--vault", required=True)
    parser.add_argument("--relative-path", required=True)
    parser.add_argument("--content-file", required=True)
    parser.add_argument("--backup-root")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    content = Path(args.content_file).read_text(encoding="utf-8")
    writer = SafeVaultWriter(args.vault, backup_root=args.backup_root, dry_run=not args.apply)
    writer.apply_write(args.relative_path, content)
    result = writer.write_report()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
