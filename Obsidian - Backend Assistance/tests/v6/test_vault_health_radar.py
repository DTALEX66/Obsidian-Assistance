from pathlib import Path
import json

from scripts.v6.vault_health_radar import audit, markdown_report


def write(path: Path, text: str = ''):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def write_meta(vault: Path, course: str, name: str, source_type='pdf', status='verified'):
    p = vault / '99_附件/images' / course / 'v6-evidence' / f'{name}.json'
    data = {
        'evidence_id': name,
        'course': course,
        'source_type': source_type,
        'status': status,
        'confidence': 'A' if status == 'verified' else 'B',
        'output_path': str(p.with_suffix('.png')),
    }
    write(p, json.dumps(data, ensure_ascii=False, indent=2))


def make_course(vault: Path, course: str):
    c = vault / '02_课程库' / course
    write(c / '00_课程总览.md', '# overview')
    return c


def test_audit_detects_missing_and_multimodal_courses(tmp_path):
    vault = tmp_path / 'vault'
    c1 = make_course(vault, '课程A')
    c2 = make_course(vault, '课程B')
    write_meta(vault, '课程A', 'a-pdf', source_type='pdf', status='verified')
    write_meta(vault, '课程A', 'a-video', source_type='video', status='verified')
    write(c1 / '11_证据索引.md', '# index')
    write(c1 / '12_真实截图与关键帧.md', '# gallery')
    write(c1 / '04_关键图表与课件索引.md', '## V6 真实证据页图')
    data = audit(vault)
    assert data['courses_total'] == 2
    assert data['totals']['metadata'] == 2
    rows = {c['course']: c for c in data['courses']}
    assert rows['课程A']['status'] == 'multimodal-verified'
    assert rows['课程A']['has_index'] is True
    assert rows['课程B']['status'] == 'missing-evidence'


def test_audit_detects_candidate_only(tmp_path):
    vault = tmp_path / 'vault'
    make_course(vault, '课程A')
    write_meta(vault, '课程A', 'a-candidate', source_type='pdf', status='pending-verification')
    data = audit(vault)
    row = data['courses'][0]
    assert row['status'] == 'candidate-only'
    assert row['pending_total'] == 1


def test_markdown_report_contains_boundaries_and_table(tmp_path):
    vault = tmp_path / 'vault'
    make_course(vault, '课程A')
    write_meta(vault, '课程A', 'a-pdf')
    data = audit(vault)
    md = markdown_report(data)
    assert '不创建证据、不升格状态' in md
    assert '| 课程 | 状态 | metadata |' in md
    assert '课程A' in md
    assert md.count('```') % 2 == 0


def test_audit_limit(tmp_path):
    vault = tmp_path / 'vault'
    make_course(vault, 'A')
    make_course(vault, 'B')
    data = audit(vault, limit=1)
    assert data['courses_total'] == 1
