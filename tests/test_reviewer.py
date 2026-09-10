from reviewer.config import load_config, DEFAULT_CONFIG
from reviewer.main import filter_diff


def test_load_config_defaults_when_missing():
    config = load_config("does-not-exist.yml")
    assert config["model"] == DEFAULT_CONFIG["model"]


def test_filter_diff_keeps_small_diff():
    diff = "\n".join([f"line {i}" for i in range(10)])
    result = filter_diff(diff, {"max_diff_lines": 100})
    assert "line 9" in result
    assert "truncated" not in result


def test_filter_diff_truncates_large_diff():
    diff = "\n".join([f"line {i}" for i in range(1000)])
    result = filter_diff(diff, {"max_diff_lines": 50})
    assert "truncated" in result