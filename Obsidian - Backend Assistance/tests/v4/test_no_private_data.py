import re
from pathlib import Path

SECRET_RE = re.compile(r"(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|Bearer\s+[A-Za-z0-9._-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)")
FORMAL_PATH_RE = re.compile("E:" + r"[\\/]" + "BaiduSyncdisk" + r"[\\/]" + "Obsidian知识库")
FORBIDDEN_EXT = {".mp3", ".mp4", ".pdf", ".zip", ".rar", ".7z", ".sqlite"}
SCAN_DIRS = ["docs", "templates/v4", "snippets/v4", "scripts/v4", "examples/v4-demo-course", "tests/v4", "reports"]


def iter_files():
    for d in SCAN_DIRS:
        root = Path(d)
        if root.is_file():
            yield root
        elif root.exists():
            for p in root.rglob("*"):
                if p.is_file() and "__pycache__" not in p.parts:
                    yield p


def test_no_forbidden_binary_or_media_files():
    bad = [str(p) for p in iter_files() if p.suffix.lower() in FORBIDDEN_EXT]
    assert bad == []


def test_no_real_secret_values():
    hits = []
    for p in iter_files():
        if p.stat().st_size > 1_000_000:
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        if SECRET_RE.search(text):
            hits.append(str(p))
    assert hits == []


def test_no_formal_vault_path_in_v4_outputs():
    hits = []
    for p in iter_files():
        text = p.read_text(encoding="utf-8", errors="ignore")
        if FORMAL_PATH_RE.search(text):
            hits.append(str(p))
    assert hits == []
