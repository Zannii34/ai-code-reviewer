# AI Code Reviewer

An automated GitHub Pull Request reviewer built with Python, GitHub Actions, and Anthropic Claude.

The reviewer fetches a pull request diff, filters files that should not be reviewed, sends the relevant changes to Claude for analysis, and publishes the resulting review as a GitHub pull-request comment.

## Features

- Automated pull-request reviews through GitHub Actions
- Claude-powered code analysis
- Configurable review model
- Configurable maximum diff size
- Ignore rules for lockfiles, dependencies, build output, and minified files
- GitHub API integration for fetching PR diffs
- Automated PR comment publishing
- Input validation for configuration and environment variables
- Error handling around GitHub and Claude API requests
- Unit and integration-style tests with mocked external services
- Separate runtime and development dependencies

## How It Works

```text
GitHub Pull Request
        |
        v
GitHub Actions
        |
        v
Load configuration
        |
        v
Fetch PR diff
        |
        v
Filter ignored files
        |
        v
Limit diff size
        |
        v
Send review request to Claude
        |
        v
Generate structured review
        |
        v
Post review as PR comment
```

## Project Structure

```text
ai-code-reviewer/
|
├── .github/
│   └── workflows/
│       └── review.yml
|
├── examples/
│   └── .ai-reviewer.yml
|
├── reviewer/
│   ├── ai.py
│   ├── config.py
│   ├── github.py
│   ├── main.py
│   ├── prompts.py
│   └── __init__.py
|
├── tests/
│   ├── test_reviewer.py
│   ├── test_config.py
│   ├── test_integrations.py
│   └── test_mocked_integrations.py
|
├── .env.example
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Configuration

Create a `.ai-reviewer.yml` file in the repository being reviewed.

Example:

```yaml
model: claude-sonnet-4-6
max_diff_lines: 800

ignore_files:
  - '*.lock'
  - 'package-lock.json'
  - '*.min.js'

ignore_patterns:
  - 'node_modules/'
  - 'venv/'
  - 'dist/'
  - 'build/'
```

### Configuration options

| Option | Description |
|---|---|
| `model` | Claude model used for reviews |
| `max_diff_lines` | Maximum number of diff lines sent for review |
| `ignore_files` | File-name patterns that should be skipped |
| `ignore_patterns` | Path patterns that should be skipped |

If no configuration file exists, the application uses its built-in defaults.

## GitHub Actions Setup

The workflow is located at `.github/workflows/review.yml`.

Add the Anthropic API key as a GitHub Actions repository secret:

```text
ANTHROPIC_API_KEY
```

The workflow provides the GitHub Actions token and pull-request information automatically.

## Pull Requests From Forks

GitHub restricts repository secrets for workflows triggered by pull requests from forks.

This project intentionally uses the normal `pull_request` workflow rather than exposing secrets through a `pull_request_target` workflow.

## Local Development

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install runtime dependencies:

```bash
python -m pip install -r requirements.txt
```

Install development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

## Running Tests

```bash
python -m pytest -q
```

On Windows, if the pytest cache causes a filesystem warning:

```bash
python -m pytest -q -p no:cacheprovider
```

## Current Test Status

```text
26 passed
```

External GitHub and Claude API calls are mocked in the integration-style tests, so the test suite does not require live credentials.

## Security Considerations

- API credentials are supplied through environment variables or GitHub Actions secrets.
- `.env` is excluded from Git.
- Repository contents are not given write permissions by the workflow.
- Pull-request write permission is limited to publishing review comments.
- External API failures are handled explicitly.
- Pull-request diffs are filtered before being sent for review.
- Large diffs are truncated to control processing and API usage.

## Tech Stack

- Python
- Anthropic Claude API
- GitHub Actions
- GitHub REST API
- PyGithub
- Requests
- PyYAML
- pytest

## What This Project Demonstrates

- Python application structure
- API integration
- GitHub automation
- CI/CD workflows
- Environment variables and secrets
- Configuration files
- Input validation
- Error handling
- Automated testing
- Mocking external services
- Prompt engineering
- Diff processing
- Cost-aware AI workflows
- Secure CI credential handling

## Future Improvements

- Inline line-level GitHub review comments
- Language-specific review prompts
- Review severity configuration
- Cost and token tracking
- Review result caching
- Additional CI checks
- Multiple AI provider backends
- Web-based configuration
- Review history and analytics

## License

MIT
