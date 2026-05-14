"""Agent 3 — Channel Strategist
Recommends the optimal GTM channel mix for the given use case.
"""
import anthropic


SYSTEM_PROMPT = """You are a B2B Fintech Channel Strategy expert for companies scaling from $1M to $10M ARR.
Your job: given a use case and company context, produce a channel strategy covering:
1. Recommended primary channel (with rationale)
2. Secondary channels (2–3) with priority order
3. Channels to avoid at this stage and why
4. Partner / ecosystem plays relevant to fintech payments
5. Estimated CAC range per channel (rough order of magnitude)
6. 90-day channel activation sequence

Be opinionated and stage-appropriate. Max 350 words."""


def run_channel_strategist(use_case: str, context: dict) -> str:
    """Run channel strategist agent and return markdown string."""
    client = anthropic.Anthropic()
    user_msg = (
        f"Company situation:\n{context.get('situation', use_case)}\n\n"
        "Produce the channel strategy."
    )
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=600,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )
    return message.content[0].text
