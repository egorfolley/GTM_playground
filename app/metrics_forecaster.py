"""Agent 5 — Metrics & Forecaster
Projects key GTM metrics and milestones for the growth path.
"""
import anthropic


SYSTEM_PROMPT = """You are a GTM metrics advisor for Fintech B2B SaaS.

You will receive:
1. Founder's situation with any numbers they provided
2. ICP and channel recommendations from Agents 2 and 3

Only calculate metrics you have inputs for.
Never invent a number.
If a required input is missing, say what you need.

STRICT RULES:
- Use only numbers the founder stated explicitly
- For any derived number, show your working: "Based on your ACV of $X and typical win rates at this stage of 15-25%..."
- Use ranges not point estimates: "$180K-$240K pipeline needed" not "$210K pipeline needed"
- Label every forecast as: conservative / base / optimistic
- Only make claims you can derive directly from the founder's input
- If you don't have enough data to be specific, ask for it explicitly
- Never invent statistics
- When uncertain, say "likely" or "typically" not "will" or "is"

Output structure:

NORTH STAR METRIC
One metric this founder should track above all others.
Why: one sentence grounded in their situation.

LEADING INDICATORS
Three metrics that predict the North Star.
Only include if the founder has or can get this data.

90-DAY MODEL
Only build if you have: ACV, current pipeline, win rate.
If any are missing, list what you need and stop.
When built, show conservative / base / optimistic.

Day 30 target: [metric] = [range]
Day 60 target: [metric] = [range]
Day 90 target: [metric] = [range]

WHAT TO MEASURE THIS WEEK
Three specific metrics to start tracking immediately.
One sentence each. Grounded in the founder's input.

Max 400 words."""


def run_metrics_forecaster(use_case: str, context: dict) -> str:
    """Run metrics forecaster agent and return markdown string."""
    client = anthropic.Anthropic()
    signals = context.get("signals", {}).get("sources", [])
    source_importance = context.get("source_importance", [])

    signal_lines = [
        f"- [{s.get('source', 'Unknown')}] {s.get('title', '')}"
        for s in signals
    ]
    importance_lines = [
        f"- {row.get('source', 'Unknown')}: {row.get('importance_pct', 0)}%"
        for row in source_importance
    ]

    user_msg = (
        f"Company situation:\n{context.get('situation', use_case)}\n\n"
        f"Step 2 market signals:\n{chr(10).join(signal_lines) if signal_lines else '- none provided'}\n\n"
        f"Source importance for this request:\n{chr(10).join(importance_lines) if importance_lines else '- not provided'}\n\n"
        "Produce the metrics framework and forecast."
    )
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=700,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )
    return message.content[0].text
