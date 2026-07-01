from pathlib import Path
from scripts.v4.generate_course_pack import build_course_pack, load_spec, write_to_output


def test_build_course_pack_contains_required_files():
    files = build_course_pack("Demo课程", "templates/v4")
    required = {"00_课程主页.md", "01_课程地图.canvas", "08_导入报告.md"}
    assert required <= set(files)


def test_generate_course_pack_dry_run_no_write(tmp_path):
    files = build_course_pack("Demo课程", "templates/v4")
    result = write_to_output(files, tmp_path / "demo", apply=False)
    assert result["dry_run"] is True
    assert not (tmp_path / "demo" / "00_课程主页.md").exists()


def test_generate_course_pack_apply_writes(tmp_path):
    files = build_course_pack("Demo课程", "templates/v4")
    result = write_to_output(files, tmp_path / "demo", apply=True)
    assert result["dry_run"] is False
    assert (tmp_path / "demo" / "00_课程主页.md").exists()


def test_load_course_spec_and_generate_spec_driven_files():
    spec = load_spec("examples/v4-course-spec.json")
    files = build_course_pack(spec["course"], "templates/v4", spec=spec)
    assert "02_逐节总结/第01节_输入箱与素材识别.md" in files
    assert "02_逐节总结/第02节_卡片化与复习.md" in files
    assert "03_知识卡片/概念_证据索引.md" in files
    assert "07_证据索引/spec-demo-001.md" in files
    assert "输入箱与素材识别" in files["02_逐节总结/第01节_输入箱与素材识别.md"]
    assert "V4 Spec Demo课程" in files["00_课程主页.md"]


def test_spec_driven_apply_writes_multiple_lessons(tmp_path):
    spec = load_spec("examples/v4-course-spec.json")
    files = build_course_pack(spec["course"], "templates/v4", spec=spec)
    result = write_to_output(files, tmp_path / "spec-demo", apply=True)
    assert result["dry_run"] is False
    assert (tmp_path / "spec-demo" / "02_逐节总结" / "第01节_输入箱与素材识别.md").exists()
    assert (tmp_path / "spec-demo" / "02_逐节总结" / "第02节_卡片化与复习.md").exists()
