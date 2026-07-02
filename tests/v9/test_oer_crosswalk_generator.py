from pathlib import Path

from scripts.v9.oer_crosswalk_generator import analyze_course, generate


def assert_raises(exc_type, fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except exc_type:
        return
    except Exception as exc:  # pragma: no cover - tiny helper
        raise AssertionError(f'expected {exc_type.__name__}, got {type(exc).__name__}: {exc}')
    raise AssertionError(f'expected {exc_type.__name__}')


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def make_course(vault: Path, course='大模型应用开发介绍', evidence=False):
    root = vault / '02_课程库' / course
    write(root / '00_课程总览.md', '# 课程总览\n\n## RAG 实践\n大模型、RAG、Prompt、Agent。')
    write(root / '07_RAG实操工作流.md', '# RAG 实操工作流\n1. 文本切分\n2. Embedding\n3. TopK召回')
    write(root / '08_术语索引.md', '- [[RAG]]：检索增强生成\n- [[Embedding模型]]：向量化模型\n- [[AI Agent]]：工具调用智能体\n')
    write(root / '13_项目转化.md', '# 项目转化\n')
    write(root / '05_复习与检索练习.md', '# 复习\n')
    if evidence:
        write(root / '11_证据索引.md', '# 证据\nstatus: verified\n')
    return root


def test_analyze_course_classifies_techdocs_and_boundary(tmp_path):
    vault = tmp_path / 'vault'
    make_course(vault)
    data = analyze_course(vault, '大模型应用开发介绍')
    assert data.profile == 'techdocs'
    assert data.has_v6_verified is False
    assert '不得伪造' in data.boundary
    assert 'RAG' in data.terms
    assert data.workflow.endswith('07_RAG实操工作流.md')


def test_generate_dry_run_does_not_write(tmp_path):
    vault = tmp_path / 'vault'
    root = make_course(vault)
    result = generate(vault, '大模型应用开发介绍', apply=False, sample=True)
    assert result['plan']['apply'] is False
    assert '14_开放知识交叉对比.md' in result['plan']['crosswalk_path']
    assert not (root / '14_开放知识交叉对比.md').exists()
    assert 'contents' in result
    assert 'MDN Web Docs' in next(iter(result['contents'].values()))


def test_generate_apply_writes_pages_and_sample(tmp_path):
    vault = tmp_path / 'vault'
    root = make_course(vault, evidence=True)
    result = generate(vault, '大模型应用开发介绍', apply=True, sample=True)
    assert Path(result['plan']['crosswalk_path']).exists()
    assert Path(result['plan']['faq_path']).exists()
    assert Path(result['plan']['sample_path']).exists()
    text = (root / '14_开放知识交叉对比.md').read_text(encoding='utf-8')
    assert '已有 V6 verified 证据' in text
    assert 'Stack Exchange' in text
    assert text.count('```') % 2 == 0


def test_generate_refuses_overwrite_without_flag_and_backs_up(tmp_path):
    vault = tmp_path / 'vault'
    root = make_course(vault)
    target = root / '14_开放知识交叉对比.md'
    write(target, 'old')
    assert_raises(FileExistsError, generate, vault, '大模型应用开发介绍', apply=True)
    backup = tmp_path / 'backup'
    generate(vault, '大模型应用开发介绍', apply=True, overwrite=True, backup_dir=backup)
    backed = backup / '02_课程库' / '大模型应用开发介绍' / '14_开放知识交叉对比.md'
    assert backed.exists()
    assert backed.read_text(encoding='utf-8') == 'old'
    assert '开放知识交叉对比' in target.read_text(encoding='utf-8')


def test_course_path_traversal_is_blocked(tmp_path):
    vault = tmp_path / 'vault'
    make_course(vault, course='正常课程')
    assert_raises(ValueError, generate, vault, '../outside', apply=False)
