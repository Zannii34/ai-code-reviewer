import os

import requests
from github import Github


GITHUB_API_TIMEOUT = 30


def get_pr_client():
    token = os.environ.get("GITHUB_TOKEN")
    repo_name = os.environ.get("GITHUB_REPOSITORY")
    pr_number = os.environ.get("PR_NUMBER")

    if not token:
        raise RuntimeError("Missing required environment variable: GITHUB_TOKEN")

    if not repo_name:
        raise RuntimeError("Missing required environment variable: GITHUB_REPOSITORY")

    if not pr_number:
        raise RuntimeError("Missing required environment variable: PR_NUMBER")

    try:
        pr_number_int = int(pr_number)
    except ValueError as exc:
        raise RuntimeError("PR_NUMBER must be a valid integer") from exc

    if pr_number_int <= 0:
        raise RuntimeError("PR_NUMBER must be greater than 0")

    gh = Github(token)
    repo = gh.get_repo(repo_name)
    pr = repo.get_pull(pr_number_int)

    return repo, pr


def get_pr_diff(pr):
    token = os.environ.get("GITHUB_TOKEN")

    if not token:
        raise RuntimeError("Missing required environment variable: GITHUB_TOKEN")

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3.diff",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    try:
        response = requests.get(
            pr.url,
            headers=headers,
            timeout=GITHUB_API_TIMEOUT,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"Failed to fetch PR diff from GitHub: {exc}") from exc

    return response.text


def post_review_comment(pr, body):
    if not body or not body.strip():
        raise ValueError("Review comment body cannot be empty")

    try:
        return pr.create_issue_comment(body)
    except Exception as exc:
        raise RuntimeError(f"Failed to post review comment to GitHub: {exc}") from exc
