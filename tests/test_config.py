from reviewer.config import load_config, DEFAULT_CONFIG


def test_load_config_defaults_when_missing():
    config = load_config("does-not-exist.yml")
    assert config["model"] == DEFAULT_CONFIG["model"]


def test_load_config_accepts_valid_custom_config(tmp_path):
    config_file = tmp_path / ".ai-reviewer.yml"
    config_file.write_text(
        """
model: custom-model
max_diff_lines: 900
ignore_files:
  - "*.tmp"
ignore_patterns:
  - "vendor/"
""",
        encoding="utf-8",
    )

    config = load_config(config_file)

    assert config["model"] == "custom-model"
    assert config["max_diff_lines"] == 900
    assert config["ignore_files"] == ["*.tmp"]
    assert config["ignore_patterns"] == ["vendor/"]


def test_load_config_rejects_invalid_max_diff_lines(tmp_path, capsys):
    config_file = tmp_path / ".ai-reviewer.yml"
    config_file.write_text(
        "max_diff_lines: banana\n",
        encoding="utf-8",
    )

    config = load_config(config_file)

    assert config == DEFAULT_CONFIG
    assert "[WARN]" in capsys.readouterr().out


def test_load_config_rejects_invalid_ignore_files(tmp_path):
    config_file = tmp_path / ".ai-reviewer.yml"
    config_file.write_text(
        "ignore_files: not-a-list\n",
        encoding="utf-8",
    )

    config = load_config(config_file)

    assert config == DEFAULT_CONFIG


def test_load_config_rejects_invalid_model(tmp_path):
    config_file = tmp_path / ".ai-reviewer.yml"
    config_file.write_text(
        "model: ''\n",
        encoding="utf-8",
    )

    config = load_config(config_file)

    assert config == DEFAULT_CONFIG
