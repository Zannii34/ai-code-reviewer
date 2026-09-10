import os
import yaml
from pathlib import Path

DEFAULT_CONFIG = {
    "model": "claude-3-5-sonnet-20241022",
    "max_diff_lines": 500,
    "ignore_files": ["*.lock", "package-lock.json", "*.min.js"],
    "ignore_patterns": ["node_modules/", "venv/", "dist/", "build/"],
}


def load_config(path=".ai-reviewer.yml"):
    config = DEFAULT_CONFIG.copy()
    config_path = Path(path)
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                user_config = yaml.safe_load(f) or {}
            config.update(user_config)
        except Exception as e:
            print(f"[WARN] Could not load {path}: {e}")
    return config


def get_env(key, required=True):
    value = os.environ.get(key)
    if required and not value:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return value