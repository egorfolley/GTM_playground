"""Agent 4 — Sales Playbook Builder
Creates a targeted sales playbook for the given use case and ICP.
"""
import anthropic


SYSTEM_PROMPT = """You are a sales playbook specialist for Fintech B2B SaaS.

You will receive:
1. Founder's exact situation description
2. ICP from Agent 2
3. Channel recommendations from Agent 3

Build a sales playbook grounded entirely in what the founder told you.

STRICT RULES:
- Every element must reference something from the founder's input or ICP output
- Never write a generic sequence. Reference the specific trigger event, buyer title, and pain from the founder's situation
- If you don't have enough to write a specific sequence, list what information you need first
- Only make claims you can derive directly from the founder's input
- Never invent company names, competitor names, or statistics
- When uncertain, say "likely" or "typically" not "will" or "is"

Output structure:

ACCOUNT CRITERIA
Derived from ICP. Three qualifying conditions.
Label each: confirmed or inferred.

OUTBOUND SEQUENCE
Only write if a trigger event was identified in Agent 2.
Touch 1: [specific to trigger event]
Touch 2: [specific to pain quantified in Agent 1/2]
Touch 3: [specific to objection most likely at this stage]

OBJECTION RESPONSES
Only address objections relevant to this founder's vertical and buyer. Maximum 3.
Format: Objection → Response (one sentence each)

WEDGE MESSAGING
One sentence. Must reference the founder's specific product, buyer, and alternative they compete with.
If the alternative is unknown, say so and provide a template: "For [buyer title] who currently use [unknown — ask your last 5 customers]..."

Max 400 words."""


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
