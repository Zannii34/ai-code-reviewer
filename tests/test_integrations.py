import pytest

from reviewer.github import get_pr_client, get_pr_diff, post_review_comment
from reviewer.ai import review_diff


def test_get_pr_client_requires_github_token(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo")
    monkeypatch.setenv("PR_NUMBER", "1")

    with pytest.raises(RuntimeError, match="GITHUB_TOKEN"):
        get_pr_client()


def test_get_pr_client_requires_repository(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "test-token")
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
    monkeypatch.setenv("PR_NUMBER", "1")

    with pytest.raises(RuntimeError, match="GITHUB_REPOSITORY"):
        get_pr_client()


def test_get_pr_client_requires_valid_pr_number(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "test-token")
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo")
    monkeypatch.setenv("PR_NUMBER", "abc")

    with pytest.raises(RuntimeError, match="PR_NUMBER must be a valid integer"):
        get_pr_client()


def test_get_pr_diff_requires_token(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)

    with pytest.raises(RuntimeError, match="GITHUB_TOKEN"):
        get_pr_diff(object())


def test_post_review_comment_rejects_empty_body():
    with pytest.raises(ValueError, match="cannot be empty"):
        post_review_comment(object(), "")


def test_review_diff_rejects_empty_diff():
    with pytest.raises(ValueError, match="empty diff"):
        review_diff("")


def test_review_diff_requires_api_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY"):
        review_diff("diff --git a/app.py b/app.py")


def test_review_diff_rejects_empty_model(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

    with pytest.raises(ValueError, match="valid Claude model"):
        review_diff(
            "diff --git a/app.py b/app.py",
            model="",
        )
