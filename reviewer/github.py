import os
import requests
from github import Github


def get_pr_client():
    token = os.environ.get("GITHUB_TOKEN")
    repo_name = os.environ.get("GITHUB_REPOSITORY")
    pr_number = os.environ.get("PR_NUMBER")
    if not all([token, repo_name, pr_number]):
        raise RuntimeError("Missing GITHUB_TOKEN, GITHUB_REPOSITORY, or PR_NUMBER")
    gh = Github(token)
    repo = gh.get_repo(repo_name)
    pr = repo.get_pull(int(pr_number))
    return repo, pr


def get_pr_diff(pr):
    token = os.environ.get("GITHUB_TOKEN")
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3.diff",
    }
    response = requests.get(pr.url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.text


def post_review_comment(pr, body):
    pr.create_issue_comment(body)