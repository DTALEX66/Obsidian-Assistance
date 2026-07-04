from scripts.v4.validate_yaml_schema import validate_root


def test_demo_yaml_schema_ok():
    issues = validate_root("examples/v4-demo-course")
    assert issues == {}


def test_template_yaml_schema_ok():
    issues = validate_root("templates/v4")
    assert issues == {}
