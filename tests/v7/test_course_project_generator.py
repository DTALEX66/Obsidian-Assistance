from pathlib import Path

from scripts.v7.course_project_generator import build_plan, generate, render


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def make_course(vault: Path, course: str):
    d = vault / '02_课程库' / course
    write(d / '00_课程总览.md', '# 总览')
    write(d / '07_实操工作流.md', '# 工作流')
    return d


def test_build_plan_uses_existing_notes_and_boundary(tmp_path):
    vault = tmp_path / 'vault'
    make_course(vault, '知识内化训练营')
    plan = build_plan(vault, '知识内化训练营')
    assert plan.course == '知识内化训练营'
    assert '00_课程总览.md' in plan.source_notes
    assert '不新增课程事实' in plan.boundary
    assert '个人学习系统' in plan.project_title


def test_render_contains_project_sections_and_no_fake_evidence(tmp_path):
    vault = tmp_path / 'vault'
    make_course(vault, '版式设计')
    text = render(build_plan(vault, '版式设计'))
    assert '## 3. 里程碑' in text
    assert '## 4. 交付物' in text
    assert '作品集' in text
    assert '不新增课程事实' in text
    assert text.count('```') % 2 == 0


def test_generate_dry_run_does_not_write(tmp_path):
    vault = tmp_path / 'vault'
    make_course(vault, '大模型应用开发介绍')
    result = generate(vault, '大模型应用开发介绍', apply=False)
    assert result['apply'] is False
    assert not (vault / '02_课程库/大模型应用开发介绍/13_项目转化.md').exists()


def test_generate_apply_writes_and_backs_up(tmp_path):
    vault = tmp_path / 'vault'
    course_dir = make_course(vault, 'UI系统全能班')
    target = course_dir / '13_项目转化.md'
    write(target, 'old')
    backup = tmp_path / 'backup'
    result = generate(vault, 'UI系统全能班', apply=True, backup_dir=backup)
    assert result['apply'] is True
    assert 'UI系统全能班' in target.read_text(encoding='utf-8')
    assert (backup / 'UI系统全能班_13_项目转化.md.before').exists()
