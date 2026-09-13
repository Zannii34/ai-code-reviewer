# AI Code Reviewer

![Python](https://img.shields.io/badge/python-3.11-blue) ![Claude](https://img.shields.io/badge/claude-AI-purple)


A GitHub Action that reviews pull requests using Claude AI and posts the review as a comment.

## How It Works

When you open a PR, the action:
1. Fetches the diff via GitHub API
2. Sends it to Claude with a code-review prompt
3. Posts the review back as a PR comment

## Features

- Runs automatically on every PR
- Configurable via `.ai-reviewer.yml`
- Trims large diffs to control cost
- Ignores lockfiles / build artifacts
- Posts a formatted review comment

## Setup

1. Copy `.github/workflows/review.yml` to your repo
2. Add your Anthropic API key as a GitHub secret
3. Copy `examples/.ai-reviewer.yml` to `.ai-reviewer.yml` (optional)
4. Open a PR - the bot reviews it

## Tech Stack

- Python 3.11
- Anthropic Claude API
- GitHub Actions
- PyGithub

## Local Testing

```bash
python -m venv venv
pip install -r requirements.txt
pytest
```

## What I Learned

- GitHub Actions environment (secrets, tokens, permissions)
- Working with GitHub REST API to fetch diffs and post comments
- Prompt engineering for code review
- Handling large diffs responsibly (cost control)

## What is Next

- Language-specific prompts
- Inline suggestions (line-level comments)
- Cost tracking per review
- Support for OpenAI as an alternative backend

## License

MIT
