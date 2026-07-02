from pathlib import Path

from scripts.v6.source_discovery_assistant import audit, markdown_report, score_file, tokenize_course


def write(path: Path, text: str = ''):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def make_course(vault: Path, name: str):
    write(vault / '02_课程库' / name / '00_课程总览.md', '# overview')


def test_tokenize_course_adds_compact_name_and_tokens():
    tokens = tokenize_course('知识内化训练营')
    assert tokens[0] == '知识内化训练营'
    assert '知识内化训练营' in tokens


def test_score_file_matches_path_tokens(tmp_path):
    p = tmp_path / '知识内化训练营' / '06 Anki 操作.mp4'
    write(p, 'x')
    score, matched = score_file('知识内化训练营', p)
    assert score >= 5
    assert matched


def test_audit_finds_candidates_and_keeps_candidate_only(tmp_path):
    vault = tmp_path / 'vault'
    root = tmp_path / 'sources'
    make_course(vault, '知识内化训练营')
    make_course(vault, '第二课程')
    write(root / '知识内化训练营' / '讲义.pdf', 'pdf')
    write(root / 'unrelated' / 'random.pdf', 'pdf')
    data = audit(vault, [root], min_score=2)
    assert data['courses_total'] == 2
    assert data['candidates_total'] == 1
    c = data['candidates'][0]
    assert c['course'] == '知识内化训练营'
    assert c['source_type'] == 'pdf'
    assert c['status'] == 'candidate-only'


def test_markdown_report_warns_candidate_not_evidence(tmp_path):
    vault = tmp_path / 'vault'
    root = tmp_path / 'sources'
    make_course(vault, '知识内化训练营')
    write(root / '知识内化训练营' / '操作.mp4', 'video')
    md = markdown_report(audit(vault, [root]))
    assert '候选不是证据' in md
    assert '| 课程 | 类型 | 分数 |' in md
    assert md.count('```') % 2 == 0


def test_audit_limit_and_min_score(tmp_path):
    vault = tmp_path / 'vault'
    root = tmp_path / 'sources'
    make_course(vault, 'A课程')
    make_course(vault, 'B课程')
    write(root / 'A课程.pdf', 'pdf')
    data = audit(vault, [root], limit=1, min_score=99)
    assert data['courses_total'] == 1
    assert data['candidates_total'] == 0
