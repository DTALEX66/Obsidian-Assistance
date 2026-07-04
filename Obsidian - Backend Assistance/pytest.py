#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tiny pytest-compatible runner for environments without pytest.

This is intentionally minimal and only supports the V4 repository tests:
- discover test_*.py under provided paths
- run functions named test_*
- provide tmp_path fixture when requested

It exists so `python -m pytest tests -q` works in offline/local agent
environments without installing packages. If real pytest is installed outside
this repository, prefer running it from outside the repo root or remove this
compat shim.
"""
from __future__ import annotations

import importlib.util
import inspect
import sys
import tempfile
import traceback
from pathlib import Path


def discover(paths):
    files = []
    for raw in paths or ["tests"]:
        if raw.startswith("-"):
            continue
        p = Path(raw)
        if p.is_file() and p.name.startswith("test_") and p.suffix == ".py":
            files.append(p)
        elif p.exists():
            files.extend(sorted(p.rglob("test_*.py")))
    return files


def load_module(path: Path):
    name = "_mini_pytest_" + "_".join(path.with_suffix("").parts)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.path.insert(0, str(Path.cwd()))
    spec.loader.exec_module(module)
    return module


def run_test(func):
    sig = inspect.signature(func)
    kwargs = {}
    with tempfile.TemporaryDirectory() as d:
        if "tmp_path" in sig.parameters:
            kwargs["tmp_path"] = Path(d)
        func(**kwargs)


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    quiet = "-q" in argv
    paths = [a for a in argv if not a.startswith("-")]
    files = discover(paths)
    total = 0
    failed = []
    for path in files:
        try:
            module = load_module(path)
        except Exception:
            failed.append((str(path), "<import>", traceback.format_exc()))
            continue
        for name, obj in sorted(vars(module).items()):
            if name.startswith("test_") and callable(obj):
                total += 1
                try:
                    run_test(obj)
                    if not quiet:
                        print(f"PASS {path}::{name}")
                except Exception:
                    failed.append((str(path), name, traceback.format_exc()))
                    if not quiet:
                        print(f"FAIL {path}::{name}")
    if failed:
        for path, name, tb in failed:
            print(f"FAILED {path}::{name}")
            print(tb)
        print(f"{len(failed)} failed, {total-len(failed)} passed")
        return 1
    print(f"{total} passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
