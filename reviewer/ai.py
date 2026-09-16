from anthropic import Anthropic

from reviewer.config import get_env
from reviewer.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE


DEFAULT_MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 2000


def review_diff(
    diff,
    pr_title="",
    pr_body="",
    model=DEFAULT_MODEL,
):
    if not diff or not diff.strip():
        raise ValueError("Cannot review an empty diff")

    api_key = get_env("ANTHROPIC_API_KEY")

    if not model or not str(model).strip():
        raise ValueError("A valid Claude model must be provided")

    client = Anthropic(api_key=api_key)

    user_prompt = USER_PROMPT_TEMPLATE.format(
        title=pr_title or "(no title)",
        body=pr_body or "(no description)",
        diff=diff,
    )

    try:
        message = client.messages.create(
            model=model,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}],
        )
    except Exception as exc:
        raise RuntimeError(f"Claude API request failed: {exc}") from exc

    content = getattr(message, "content", None)

    if not content:
        raise RuntimeError("Claude returned an empty response")

    first_block = content[0]
    text = getattr(first_block, "text", None)

    if not text or not text.strip():
        raise RuntimeError("Claude returned an empty text response")

    return text.strip()
