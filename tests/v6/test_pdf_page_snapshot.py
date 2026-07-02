from pathlib import Path

from scripts.v6.pdf_page_snapshot import build_plan, execute, parse_pages, slugify


def assert_raises(exc_type, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except exc_type:
        return
    raise AssertionError(f"expected {exc_type.__name__}")


def test_parse_pages_supports_ranges():
    assert parse_pages('1,3-5,2') == [1, 2, 3, 4, 5]


def test_parse_pages_rejects_invalid_zero():
    assert_raises(ValueError, parse_pages, '0')


def test_parse_pages_rejects_invalid_range():
    assert_raises(ValueError, parse_pages, '3-1')


def test_slugify_keeps_chinese_course_names():
    assert slugify('版式设计 / UI') == '版式设计-UI'


def test_dry_run_does_not_write_outputs(tmp_path):
    pdf = tmp_path / 'sample.pdf'
    pdf.write_bytes(b'%PDF-1.4\n% synthetic placeholder for dry-run\n')
    out = tmp_path / 'out'
    result = execute(pdf, '版式设计', '1,2', out, apply=False)
    assert result['apply'] is False
    assert result['pages'] == [1, 2]
    assert len(result['plans']) == 2
    assert not out.exists()
    assert all('candidate' not in p['status'] for p in result['plans'])


def test_build_plan_contains_required_metadata_paths(tmp_path):
    pdf = tmp_path / 'course.pdf'
    output_dir = tmp_path / 'images'
    plan = build_plan(pdf, '记忆圣经学习力合集', [3], output_dir)[0]
    assert plan.source_type == 'pdf'
    assert plan.page == 3
    assert plan.confidence == 'B'
    assert plan.status == 'pending-verification'
    assert plan.output_path.endswith('.png')
    assert plan.metadata_path.endswith('.json')
    assert 'pdf-p003' in plan.evidence_id


def test_missing_pdf_fails_honestly(tmp_path):
    assert_raises(FileNotFoundError, execute, tmp_path / 'missing.pdf', '课程', '1', tmp_path / 'out')


def test_evidence_templates_include_no_fabrication_boundary():
    root = Path(__file__).resolve().parents[2]
    for rel in [
        'templates/obsidian/evidence/evidence-index.md',
        'templates/obsidian/evidence/evidence-gallery.md',
    ]:
        text = (root / rel).read_text(encoding='utf-8')
        assert '候选不是证据' in text or '不得添加图片占位' in text
        assert text.count('```') % 2 == 0
