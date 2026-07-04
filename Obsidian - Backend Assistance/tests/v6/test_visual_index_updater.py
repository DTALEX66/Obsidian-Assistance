from pathlib import Path
import json

from scripts.v6.visual_index_updater import load_items, render_section, replace_section, update


def write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def make_meta(vault: Path, course: str, suffix: str, source_type='pdf', status='verified', confidence='A'):
    img = vault / '99_附件' / 'images' / course / 'v6-evidence' / f'{suffix}.png'
    img.parent.mkdir(parents=True, exist_ok=True)
    img.write_bytes(b'png')
    meta = img.with_suffix('.json')
    data = {
        'evidence_id': suffix,
        'course': course,
        'source_type': source_type,
        'source_path': f'D:/source/{suffix}.{source_type}',
        'output_path': str(img),
        'confidence': confidence,
        'status': status,
        'caption': f'caption {suffix}',
    }
    if source_type == 'pdf':
        data['page'] = 1
    else:
        data['source_ref'] = {'timestamp': '00:00:10'}
    write_json(meta, data)
    return meta


def test_load_items_filters_course_and_verified_only(tmp_path):
    vault = tmp_path / 'vault'
    make_meta(vault, '课程A', 'a1', status='verified')
    make_meta(vault, '课程A', 'a2', status='pending-verification', confidence='B')
    make_meta(vault, '课程B', 'b1')
    evidence_dir = vault / '99_附件/images/课程A/v6-evidence'
    all_items = load_items(vault, '课程A', evidence_dir)
    verified = load_items(vault, '课程A', evidence_dir, verified_only=True)
    assert len(all_items) == 2
    assert len(verified) == 1
    assert verified[0].status == 'verified'


def test_render_section_has_boundaries_and_links(tmp_path):
    vault = tmp_path / 'vault'
    make_meta(vault, '课程A', 'a1')
    items = load_items(vault, '课程A', vault / '99_附件/images/课程A/v6-evidence')
    text = render_section('课程A', items)
    assert '## V6 真实证据页图' in text
    assert '候选不是证据' in text
    assert '[[02_课程库/课程A/11_证据索引|证据索引]]' in text
    assert '![[99_附件/images/课程A/v6-evidence/a1.png|180]]' in text
    assert text.count('```') % 2 == 0


def test_replace_section_replaces_old_v6_section_only():
    old = '# Title\n\nIntro\n\n## V6 真实证据页图\nold rows\n'
    new = replace_section(old, '## V6 真实证据页图\nnew rows\n')
    assert 'Intro' in new
    assert 'new rows' in new
    assert 'old rows' not in new


def test_update_dry_run_does_not_write(tmp_path):
    vault = tmp_path / 'vault'
    course_dir = vault / '02_课程库/课程A'
    course_dir.mkdir(parents=True, exist_ok=True)
    target = course_dir / '04_关键图表与课件索引.md'
    target.write_text('# old\n', encoding='utf-8')
    make_meta(vault, '课程A', 'a1')
    result = update(vault, '课程A', vault / '99_附件/images/课程A/v6-evidence', apply=False)
    assert result['apply'] is False
    assert len(result['items']) == 1
    assert target.read_text(encoding='utf-8') == '# old\n'
    assert 'a1.png' in result['preview']


def test_update_apply_writes_and_backs_up(tmp_path):
    vault = tmp_path / 'vault'
    course_dir = vault / '02_课程库/课程A'
    course_dir.mkdir(parents=True, exist_ok=True)
    target = course_dir / '04_关键图表与课件索引.md'
    target.write_text('# old\n', encoding='utf-8')
    make_meta(vault, '课程A', 'a1', source_type='video')
    backup = tmp_path / 'backup'
    result = update(vault, '课程A', vault / '99_附件/images/课程A/v6-evidence', apply=True, backup_dir=backup)
    assert result['apply'] is True
    text = target.read_text(encoding='utf-8')
    assert '00:00:10' in text
    assert 'video' in text
    assert (backup / '04_关键图表与课件索引.md.before').exists()
