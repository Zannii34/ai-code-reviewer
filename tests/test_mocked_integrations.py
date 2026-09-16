from types import SimpleNamespace

import pytest

import reviewer.ai as ai_module
import reviewer.github as github_module


def test_get_pr_diff_success(monkeypatch):
    class FakeResponse:
        text = "diff --git a/app.py b/app.py\n+print('hello')"

        def raise_for_status(self):
            pass

    def fake_get(url, headers, timeout):
        assert url == "https://api.github.com/repos/owner/repo/pulls/1"
        assert headers["Authorization"] == "Bearer test-token"
        assert headers["Accept"] == "application/vnd.github.v3.diff"
        assert timeout == 30
        return FakeResponse()

    monkeypatch.setenv("GITHUB_TOKEN", "test-token")
    monkeypatch.setattr(github_module.requests, "get", fake_get)

    pr = SimpleNamespace(
        url="https://api.github.com/repos/owner/repo/pulls/1"
    )

    result = github_module.get_pr_diff(pr)

    assert "print('hello')" in result


def test_get_pr_diff_http_failure(monkeypatch):
    class FakeResponse:
        text = ""

        def raise_for_status(self):
            raise github_module.requests.HTTPError("403 Forbidden")

    def fake_get(url, headers, timeout):
        return FakeResponse()

    monkeypatch.setenv("GITHUB_TOKEN", "test-token")
    monkeypatch.setattr(github_module.requests, "get", fake_get)

    pr = SimpleNamespace(url="https://example.com/pr")

    with pytest.raises(RuntimeError, match="Failed to fetch PR diff"):
        github_module.get_pr_diff(pr)


def test_post_review_comment_success():
    class FakePR:
        def __init__(self):
            self.body = None

        def create_issue_comment(self, body):
            self.body = body
            return "comment-created"

    pr = FakePR()

    result = github_module.post_review_comment(
        pr,
        "## AI Code Review\nLooks good.",
    )

    assert result == "comment-created"
    assert pr.body == "## AI Code Review\nLooks good."


def test_post_review_comment_failure():
    class FakePR:
        def create_issue_comment(self, body):
            raise RuntimeError("GitHub unavailable")

    with pytest.raises(RuntimeError, match="Failed to post review comment"):
        github_module.post_review_comment(
            FakePR(),
            "Review",
        )


def test_review_diff_success(monkeypatch):
    class FakeMessage:
        content = [
            SimpleNamespace(
                text="## Summary\nThe code looks good."
            )
        ]

    class FakeMessages:
        def create(self, **kwargs):
            assert kwargs["model"] == "test-model"
            assert kwargs["max_tokens"] == 2000
            assert "diff --git" in kwargs["messages"][0]["content"]
            return FakeMessage()

    class FakeClient:
        def __init__(self):
            self.messages = FakeMessages()

    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setattr(
        ai_module,
        "Anthropic",
        lambda api_key: FakeClient(),
    )

    result = ai_module.review_diff(
        "diff --git a/app.py b/app.py\n+print('hello')",
        pr_title="Test PR",
        pr_body="Testing the reviewer",
        model="test-model",
    )

    assert result == "## Summary\nThe code looks good."


def test_review_diff_api_failure(monkeypatch):
    class FakeMessages:
        def create(self, **kwargs):
            raise RuntimeError("API unavailable")

    class FakeClient:
        def __init__(self):
            self.messages = FakeMessages()

    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setattr(
        ai_module,
        "Anthropic",
        lambda api_key: FakeClient(),
    )

    with pytest.raises(RuntimeError, match="Claude API request failed"):
        ai_module.review_diff(
            "diff --git a/app.py b/app.py\n+print('hello')",
            model="test-model",
        )


def test_review_diff_empty_response(monkeypatch):
    class FakeMessage:
        content = []

    class FakeMessages:
        def create(self, **kwargs):
            return FakeMessage()

    class FakeClient:
        def __init__(self):
            self.messages = FakeMessages()

    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setattr(
        ai_module,
        "Anthropic",
        lambda api_key: FakeClient(),
    )

    with pytest.raises(RuntimeError, match="empty response"):
        ai_module.review_diff(
            "diff --git a/app.py b/app.py\n+print('hello')",
            model="test-model",
        )