"""Agent 2 — ICP Profiler
Builds an Ideal Customer Profile for the given use case and context.
"""
import anthropic


SYSTEM_PROMPT = """You are a B2B Fintech ICP (Ideal Customer Profile) specialist focused on payments SaaS.
Your job: given a use case and company context, produce a crisp ICP definition covering:
1. Firmographics: company size, industry sub-verticals, revenue range
2. Technographics: existing stack signals, integration needs
3. Trigger events that indicate buying intent (3–5 bullets)
4. Champion persona (title, pain, what they care about)
5. Economic buyer profile
6. Negative ICP signals (who to avoid)

Be precise. Use bullets. Max 350 words."""


def run_icp_profiler(use_case: str, context: dict) -> str:
    """Run ICP profiler agent and return markdown string."""
    client = anthropic.Anthropic()
    user_msg = (
        f"Company situation:\n{context.get('situation', use_case)}\n\n"
        "Produce the ICP profile."
    )
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=600,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )
    return message.content[0].text
