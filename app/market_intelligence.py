"""Agent 1 — Market Intelligence
Analyzes market signals and competitive landscape for the given use case.
"""
import anthropic


SYSTEM_PROMPT = """You are a B2B Fintech Market Intelligence analyst specializing in the $1M–$10M ARR growth stage.
Your job: given a use case and company context, produce a concise market intelligence briefing covering:
1. Market size & TAM snapshot (payments vertical focus)
2. Top 3–5 competitive threats with differentiation angle
3. Key regulatory / macro signals relevant right now
4. Whitespace opportunity in 1–2 sentences

Be direct, specific, and data-grounded. Use bullet points. Max 350 words."""


def run_market_intelligence(use_case: str, context: dict) -> str:
    """Run market intelligence agent and return markdown string."""
    client = anthropic.Anthropic()
    user_msg = (
        f"Company situation:\n{context.get('situation', use_case)}\n\n"
        "Produce the market intelligence briefing."
    )
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=600,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )
    return message.content[0].text
