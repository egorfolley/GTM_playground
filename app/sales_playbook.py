"""Agent 4 — Sales Playbook Builder
Creates a targeted sales playbook for the given use case and ICP.
"""
import anthropic


SYSTEM_PROMPT = """You are a B2B Fintech Sales Playbook architect who builds motion-specific playbooks for payments SaaS.
Your job: given a use case and company context, produce a sales playbook covering:
1. Opening hook / value prop statement (1 sentence)
2. Discovery question framework (5 questions)
3. Objection handling: top 3 objections + responses
4. Proof points / social proof angles to lead with
5. Proposed deal stages with exit criteria (4–5 stages)
6. Recommended close motion and champion enablement tactic

Tone: direct, practitioner-level. Max 400 words."""


def run_sales_playbook(use_case: str, context: dict) -> str:
    """Run sales playbook agent and return markdown string."""
    client = anthropic.Anthropic()
    user_msg = (
        f"Company situation:\n{context.get('situation', use_case)}\n\n"
        "Produce the sales playbook."
    )
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=700,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )
    return message.content[0].text
