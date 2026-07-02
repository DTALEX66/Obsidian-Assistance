from pathlib import Path
import json
import sys

from scripts.v6.video_keyframe_extract import build_plan, extract, metadata_for, parse_timestamps


def assert_raises(exc_type, fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except exc_type:
        return
    raise AssertionError(f'{exc_type.__name__} was not raised')


def test_parse_timestamps_normalizes_and_rejects_bad_values():
    assert parse_timestamps('0:1:2,00:03:00') == ['00:01:02', '00:03:00']
    assert_raises(ValueError, parse_timestamps, '00:70:00')
    assert_raises(ValueError, parse_timestamps, 'abc')


def test_build_plan_is_pending_verification(tmp_path):
    video = tmp_path / 'demo.mp4'
    video.write_bytes(b'fake')
    plans = build_plan(video, '课程A', ['00:00:10'], tmp_path / 'out', caption_prefix='demo')
    assert len(plans) == 1
    p = plans[0]
    assert p.source_type == 'video'
    assert p.confidence == 'B'
    assert p.status == 'pending-verification'
    assert p.output_path.endswith('.png')
    assert p.metadata_path.endswith('.json')


def test_metadata_contains_timestamp_boundary(tmp_path):
    video = tmp_path / 'demo.mp4'
    video.write_bytes(b'fake')
    plan = build_plan(video, '课程A', ['00:00:10'], tmp_path / 'out')[0]
    data = metadata_for(plan)
    assert data['source_ref']['timestamp'] == '00:00:10'
    assert data['status'] == 'pending-verification'
    assert 'Pending visual verification' in ' '.join(data['notes'])


def test_extract_dry_run_does_not_write(tmp_path):
    video = tmp_path / 'demo.mp4'
    video.write_bytes(b'fake')
    out = tmp_path / 'out'
    result = extract(video, '课程A', '00:00:10,00:00:20', out, apply=False)
    assert result['apply'] is False
    assert len(result['plans']) == 2
    assert not out.exists()


def test_extract_apply_uses_fake_ffmpeg_and_writes_metadata(tmp_path):
    video = tmp_path / 'demo.mp4'
    video.write_bytes(b'fake')
    fake = tmp_path / 'fake_ffmpeg.py'
    fake.write_text("""
import sys
from pathlib import Path
out = Path(sys.argv[-1])
out.parent.mkdir(parents=True, exist_ok=True)
out.write_bytes(b'png')
""".strip(), encoding='utf-8')
    out = tmp_path / 'out'
    result = extract(video, '课程A', '00:00:10', out, apply=True, ffmpeg_bin=f'"{sys.executable}" "{fake}"')
    assert result['apply'] is True
    plan = result['plans'][0]
    assert Path(plan['output_path']).exists()
    meta = Path(plan['metadata_path'])
    assert meta.exists()
    data = json.loads(meta.read_text(encoding='utf-8'))
    assert data['status'] == 'pending-verification'
    assert data['source_ref']['timestamp'] == '00:00:10'
