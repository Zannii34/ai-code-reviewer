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


def test_filter_diff_ignores_configured_files():
    diff = """diff --git a/app.py b/app.py
index 111..222 100644
--- a/app.py
+++ b/app.py
@@ -1 +1 @@
-old
+new
diff --git a/package-lock.json b/package-lock.json
index 333..444 100644
--- a/package-lock.json
+++ b/package-lock.json
@@ -1 +1 @@
-old lock
+new lock
"""
    config = {
        "max_diff_lines": 500,
        "ignore_files": ["*.lock", "package-lock.json"],
        "ignore_patterns": [],
    }

    result = filter_diff(diff, config)

    assert "app.py" in result
    assert "package-lock.json" not in result
    assert "new lock" not in result


def test_filter_diff_ignores_configured_directories():
    diff = """diff --git a/src/app.py b/src/app.py
index 111..222 100644
--- a/src/app.py
+++ b/src/app.py
@@ -1 +1 @@
-old
+new
diff --git a/node_modules/test.js b/node_modules/test.js
index 333..444 100644
--- a/node_modules/test.js
+++ b/node_modules/test.js
@@ -1 +1 @@
-old dependency
+new dependency
"""
    config = {
        "max_diff_lines": 500,
        "ignore_files": [],
        "ignore_patterns": ["node_modules/"],
    }

    result = filter_diff(diff, config)

    assert "src/app.py" in result
    assert "node_modules/test.js" not in result
    assert "new dependency" not in result


def test_filter_diff_empty_input():
    assert filter_diff("", DEFAULT_CONFIG) == ""
