from pathlib import Path
import json

from scripts.v6.evidence_index_builder import build, load_items, render_gallery, render_index


def write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def test_load_items_filters_course_and_preserves_metadata(tmp_path):
    vault = tmp_path / 'vault'
    evidence_dir = vault / '99_附件' / 'images' / '课程A' / 'v6-evidence'
    img = evidence_dir / 'a.png'
    img.parent.mkdir(parents=True, exist_ok=True)
    img.write_bytes(b'png')
    write_json(evidence_dir / 'a.json', {
        'evidence_id': 'course-a-p001',
        'course': '课程A',
        'source_type': 'pdf',
        'source_path': 'D:/source/a.pdf',
        'page': 1,
        'output_path': str(img),
        'confidence': 'A',
        'status': 'verified',
        'caption': '可见标题A',
    })
    write_json(evidence_dir / 'b.json', {'course': '课程B', 'output_path': str(img)})
    items = load_items(vault, '课程A', evidence_dir)
    assert len(items) == 1
    assert items[0].confidence == 'A'
    assert items[0].status == 'verified'
    assert items[0].rel_image.endswith('a.png')


def test_render_index_and_gallery_include_boundaries(tmp_path):
    vault = tmp_path / 'vault'
    evidence_dir = vault / '99_附件' / 'images' / '课程A'
    img = evidence_dir / 'a.png'
    img.parent.mkdir(parents=True, exist_ok=True)
    img.write_bytes(b'png')
    write_json(evidence_dir / 'a.json', {
        'evidence_id': 'course-a-p001',
        'course': '课程A',
        'source_type': 'pdf',
        'source_path': 'D:/source/a.pdf',
        'source_ref': {'page': 1},
        'output_path': str(img),
        'confidence': 'B',
        'status': 'pending-verification',
        'caption': '待核验图',
    })
    items = load_items(vault, '课程A', evidence_dir)
    index = render_index('课程A', items)
    gallery = render_gallery('课程A', items)
    assert '候选源文件不是证据' in index
    assert '生成器不会自动升格' in gallery
    assert 'pending-verification' in index
    assert '![[99_附件/images/课程A/a.png|320]]' in gallery
    assert index.count('```') % 2 == 0
    assert gallery.count('```') % 2 == 0


def test_build_dry_run_does_not_write(tmp_path):
    vault = tmp_path / 'vault'
    course_dir = vault / '02_课程库' / '课程A'
    evidence_dir = vault / '99_附件' / 'images' / '课程A'
    img = evidence_dir / 'a.png'
    img.parent.mkdir(parents=True, exist_ok=True)
    img.write_bytes(b'png')
    write_json(evidence_dir / 'a.json', {
        'evidence_id': 'course-a-p001',
        'course': '课程A',
        'source_type': 'pdf',
        'source_path': 'D:/source/a.pdf',
        'page': 1,
        'output_path': str(img),
        'confidence': 'A',
        'status': 'verified',
        'caption': '已核验',
    })
    result = build(vault, '课程A', evidence_dir, apply=False)
    assert result['apply'] is False
    assert len(result['items']) == 1
    assert not (course_dir / '11_证据索引.md').exists()
    assert '已核验' in result['previews']['index']


def test_build_apply_writes_and_backs_up(tmp_path):
    vault = tmp_path / 'vault'
    course_dir = vault / '02_课程库' / '课程A'
    course_dir.mkdir(parents=True, exist_ok=True)
    (course_dir / '11_证据索引.md').write_text('old index', encoding='utf-8')
    evidence_dir = vault / '99_附件' / 'images' / '课程A'
    img = evidence_dir / 'a.png'
    img.parent.mkdir(parents=True, exist_ok=True)
    img.write_bytes(b'png')
    write_json(evidence_dir / 'a.json', {
        'evidence_id': 'course-a-p001',
        'course': '课程A',
        'source_type': 'pdf',
        'source_path': 'D:/source/a.pdf',
        'page': 1,
        'output_path': str(img),
        'confidence': 'A',
        'status': 'verified',
        'caption': '已核验',
    })
    backup = tmp_path / 'backup'
    result = build(vault, '课程A', evidence_dir, apply=True, backup_dir=backup)
    assert result['apply'] is True
    assert (course_dir / '11_证据索引.md').exists()
    assert (course_dir / '12_真实截图与关键帧.md').exists()
    assert (backup / '11_证据索引.md.before').exists()
    assert '已核验' in (course_dir / '12_真实截图与关键帧.md').read_text(encoding='utf-8')
