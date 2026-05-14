"""Synthesizer — combines all agent outputs into a unified GTM plan."""
import anthropic


SYSTEM_PROMPT = """You are a senior GTM advisor for Fintech B2B SaaS.
A founder described their situation in plain language.
Five specialist agents have analyzed it across ICP,
signals, pain, positioning, and distribution.

Combine everything into one GTM execution plan.
Structure exactly as:

WHO TO TARGET
One paragraph. Specific ICP + top trigger event.

WHAT PAIN YOU SOLVE
One paragraph. Quantified. Plain English.

HOW TO POSITION
Wedge sentence. ROI sentence. Top objection response.

HOW TO REACH THEM
Three engines. Two sentences each.

WHAT TO DO THIS WEEK
Three specific actions. One sentence each.

90-DAY MILESTONES
Day 30: one sentence
Day 60: one sentence
Day 90: one sentence

Write like a CRO in a 1:1 with this specific founder.
Direct. Specific. No generic advice. Under 450 words."""


def run_synthesizer(use_case: str, context: dict, agent_outputs: dict) -> str:
    """Synthesize all agent outputs into a final GTM plan."""
    client = anthropic.Anthropic()

    combined = "\n\n".join(
        f"### {name}\n{output}"
        for name, output in agent_outputs.items()
    )

    founder_text = context.get("situation", use_case)
    user_msg = (
        f"Founder situation (raw):\n{founder_text}\n\n"
        f"Agent outputs:\n\n{combined}\n\n"
        "Produce the GTM execution plan."
    )
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=800,
        temperature=0.2,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )
    return message.content[0].text

