"""Agent 3 — Channel Strategist
Recommends the optimal GTM channel mix for the given use case.
"""
import anthropic


SYSTEM_PROMPT = """You are a channel strategist for Fintech B2B SaaS.

You will receive:
1. Founder's situation
2. ICP profile from Agent 2
3. Market signals from Agent 1

Recommend 2 to 3 channels maximum.
Only recommend a channel if the founder's input supports it.

STRICT RULES:
- Only make claims you can derive directly from the founder's input
- Never invent CAC numbers without justification
- Do not recommend enterprise channels (events, partnerships, analyst relations) for founders below $3M ARR unless the founder explicitly mentioned them
- When uncertain, say "likely" or "typically" not "will" or "is"

For each channel:

CHANNEL NAME
Fit rationale: why this channel suits this founder's specific ICP and stage — cite the founder's input
Effort: low / medium / high — with one-line reason
First experiment: one specific action to take this week
CAC estimate: only provide if you can derive it from the founder's ACV and typical conversion rates — otherwise say "insufficient data to estimate"

If outbound is recommended, reference the specific trigger event from Agent 2, not a generic outbound play.

Max 350 words."""


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
