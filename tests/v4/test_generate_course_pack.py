from pathlib import Path
from scripts.v4.generate_course_pack import build_course_pack, write_to_output


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
