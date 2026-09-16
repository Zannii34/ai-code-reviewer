import os
from pathlib import Path

import yaml


DEFAULT_CONFIG = {
    "model": "claude-sonnet-4-6",
    "max_diff_lines": 500,
    "ignore_files": ["*.lock", "package-lock.json", "*.min.js"],
    "ignore_patterns": ["node_modules/", "venv/", "dist/", "build/"],
}


def _validate_config(config):
    """Validate and normalize reviewer configuration."""
    if not isinstance(config, dict):
        raise ValueError("Configuration must be a YAML mapping/object.")

    validated = DEFAULT_CONFIG.copy()

    if "model" in config:
        model = config["model"]
        if not isinstance(model, str) or not model.strip():
            raise ValueError("'model' must be a non-empty string.")
        validated["model"] = model.strip()

    if "max_diff_lines" in config:
        max_diff_lines = config["max_diff_lines"]

        if isinstance(max_diff_lines, bool) or not isinstance(max_diff_lines, int):
            raise ValueError("'max_diff_lines' must be an integer.")

        if max_diff_lines <= 0:
            raise ValueError("'max_diff_lines' must be greater than 0.")

        validated["max_diff_lines"] = max_diff_lines

    for key in ("ignore_files", "ignore_patterns"):
        if key in config:
            value = config[key]

            if value is None:
                validated[key] = []
                continue

            if not isinstance(value, list):
                raise ValueError(f"'{key}' must be a list.")

            if not all(isinstance(item, str) and item.strip() for item in value):
                raise ValueError(f"Every item in '{key}' must be a non-empty string.")

            validated[key] = [item.strip() for item in value]

    return validated


def load_config(path=".ai-reviewer.yml"):
    """Load, validate, and return reviewer configuration."""
    config_path = Path(path)

    if not config_path.exists():
        return DEFAULT_CONFIG.copy()

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}

        return _validate_config(user_config)

    except yaml.YAMLError as e:
        print(f"[WARN] Could not parse {path}: {e}")
    except (OSError, ValueError) as e:
        print(f"[WARN] Could not load {path}: {e}")

    return DEFAULT_CONFIG.copy()


def get_env(key, required=True):
    """Read an environment variable and optionally require it."""
    value = os.environ.get(key)

    if required and not value:
        raise RuntimeError(f"Missing required environment variable: {key}")

    return value
