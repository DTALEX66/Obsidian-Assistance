from pathlib import Path

from scripts.v6.video_keyframe_plan import audit, markdown_report, tokenize_course


def test_tokenize_course_keeps_meaningful_tokens():
    tokens = tokenize_course('思维导图与记忆宫殿教程')
    assert '思维导图' in tokens
    assert '记忆宫殿' in tokens
    assert '教程' not in tokens


def test_audit_video_candidates_are_candidate_only(tmp_path):
    root = tmp_path / 'media'
    video = root / '思维导图与记忆宫殿教程' / '01_记忆宫殿入门.mp4'
    video.parent.mkdir(parents=True, exist_ok=True)
    video.write_bytes(b'fake video bytes for filename audit only')
    data = audit(['思维导图与记忆宫殿教程'], [root], min_score=4)
    assert data['video_total'] == 1
    assert data['matched_courses'] == 1
    candidate = data['rows'][0]['candidates'][0]
    assert candidate['status'] == 'candidate-only'
    assert candidate['confidence'] == 'C'
    assert '00:00:05' in candidate['recommended_timestamps']


def test_audit_does_not_match_unrelated_videos(tmp_path):
    root = tmp_path / 'media'
    video = root / 'random' / 'cat.mp4'
    video.parent.mkdir(parents=True, exist_ok=True)
    video.write_bytes(b'x')
    data = audit(['牛客算法直通套餐'], [root], min_score=4)
    assert data['video_total'] == 1
    assert data['matched_courses'] == 0


def test_markdown_report_states_candidate_boundary(tmp_path):
    root = tmp_path / 'media'
    video = root / '牛客算法直通套餐' / '牛客算法01.mp4'
    video.parent.mkdir(parents=True, exist_ok=True)
    video.write_bytes(b'x')
    data = audit(['牛客算法直通套餐'], [root], min_score=4)
    md = markdown_report(data)
    assert '候选不是证据' in md
    assert 'candidate-only' in md
    assert md.count('```') % 2 == 0
