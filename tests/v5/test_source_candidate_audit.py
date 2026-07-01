from pathlib import Path

from scripts.v5.source_candidate_audit import audit, markdown_report


def write(path: Path, text: str = ''):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def test_source_candidate_audit_matches_course_names(tmp_path):
    vault = tmp_path / 'vault'
    write(vault / '02_课程库' / '版式设计' / '00_课程总览.md', '# 版式设计')
    root = tmp_path / 'sources'
    write(root / '设计资料' / '版式设计案例.pdf', 'x')
    write(root / 'other' / 'unrelated.pdf', 'x')
    data = audit(vault, [root], limit=20)
    assert data['files_scanned'] == 2
    assert data['courses'][0]['course'] == '版式设计'
    assert data['courses'][0]['candidates']
    md = markdown_report(data)
    assert '候选未核验' in md
    assert '版式设计案例.pdf' in md
