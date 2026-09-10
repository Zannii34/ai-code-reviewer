from anthropic import Anthropic
from reviewer.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from reviewer.config import get_env


def review_diff(diff, pr_title="", pr_body="", model="claude-3-5-sonnet-20241022"):
    client = Anthropic(api_key=get_env("ANTHROPIC_API_KEY"))
    user_prompt = USER_PROMPT_TEMPLATE.format(
        title=pr_title or "(no title)",
        body=pr_body or "(no description)",
        diff=diff,
    )
    message = client.messages.create(
        model=model,
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return message.content[0].text