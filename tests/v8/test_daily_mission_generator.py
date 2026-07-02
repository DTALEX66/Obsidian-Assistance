from pathlib import Path

from scripts.v8.daily_mission_generator import build_plan, generate, render


def write(path: Path, text: str = ''):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def make_vault(tmp_path: Path, course: str = '知识内化训练营') -> Path:
    vault = tmp_path / 'vault'
    course_dir = vault / '02_课程库' / course
    write(course_dir / '00_课程总览.md', '# 总览')
    write(course_dir / '13_项目转化.md', '# 项目')
    write(course_dir / '11_证据索引.md', '# 证据')
    write(vault / '00_主页/09_TALOS主动训练中心.md', '# 主动训练')
    write(vault / '00_主页/11_TALOS执行日志.md', '# 执行日志')
    return vault


def assert_raises(exc_type, fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except exc_type:
        return
    raise AssertionError(f'expected {exc_type.__name__}')


def test_build_plan_links_existing_pages(tmp_path):
    vault = make_vault(tmp_path)
    plan = build_plan(vault, '知识内化训练营', mission_date='2026-07-02')
    assert plan.course == '知识内化训练营'
    assert plan.project_page == '02_课程库/知识内化训练营/13_项目转化.md'
    assert plan.evidence_index == '02_课程库/知识内化训练营/11_证据索引.md'
    assert plan.target.replace('\\', '/').endswith('00_主页/12_TALOS_Daily_Missions/2026-07-02.md')


def test_render_contains_v8_sections_and_boundary(tmp_path):
    vault = make_vault(tmp_path)
    text = render(build_plan(vault, '知识内化训练营', mission_date='2026-07-02'))
    assert '## 1. Evidence / 证据' in text
    assert '## 2. Recall / 主动回忆' in text
    assert '## 3. Project / 项目动作' in text
    assert '不新增课程事实' in text
    assert text.count('```') % 2 == 0


def test_generate_dry_run_does_not_write(tmp_path):
    vault = make_vault(tmp_path)
    result = generate(vault, '知识内化训练营', mission_date='2026-07-02', apply=False)
    assert result['apply'] is False
    assert not (vault / '00_主页/12_TALOS_Daily_Missions/2026-07-02.md').exists()


def test_generate_apply_writes_and_protects_existing(tmp_path):
    vault = make_vault(tmp_path)
    generate(vault, '知识内化训练营', mission_date='2026-07-02', apply=True)
    target = vault / '00_主页/12_TALOS_Daily_Missions/2026-07-02.md'
    assert target.exists()
    assert 'TALOS Daily Mission' in target.read_text(encoding='utf-8')
    assert_raises(FileExistsError, generate, vault, '知识内化训练营', '2026-07-02', None, True)


def test_generate_overwrite_backs_up(tmp_path):
    vault = make_vault(tmp_path)
    target = vault / '00_主页/12_TALOS_Daily_Missions/2026-07-02.md'
    write(target, 'old')
    backup = tmp_path / 'backup'
    generate(vault, '知识内化训练营', mission_date='2026-07-02', apply=True, overwrite=True, backup_dir=backup)
    assert (backup / '2026-07-02.before.md').exists()
    assert 'old' in (backup / '2026-07-02.before.md').read_text(encoding='utf-8')


def test_missing_course_overview_raises(tmp_path):
    vault = tmp_path / 'vault'
    assert_raises(FileNotFoundError, build_plan, vault, '不存在课程')
