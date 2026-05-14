"""Agent 5 — Metrics & Forecaster
Projects key GTM metrics and milestones for the growth path.
"""
import anthropic


SYSTEM_PROMPT = """You are a B2B Fintech GTM Metrics & Forecasting expert for companies growing from $1M to $10M ARR.
Your job: given a use case and company context, produce a metrics framework covering:
1. North Star metric recommendation with rationale
2. Leading indicators to instrument immediately (4–5)
3. Funnel benchmarks for payments SaaS at this stage (conversion rates, cycle times)
4. 12-month ARR progression model (3 scenarios: base / bull / bear)
5. GTM efficiency targets: CAC payback, LTV:CAC, magic number
6. Top 2 metrics that, if missed, indicate the GTM motion needs to pivot

Be quantitative where possible. Use tables or structured bullets. Max 400 words."""


def run_metrics_forecaster(use_case: str, context: dict) -> str:
    """Run metrics forecaster agent and return markdown string."""
    client = anthropic.Anthropic()
    user_msg = (
        f"Company situation:\n{context.get('situation', use_case)}\n\n"
        "Produce the metrics framework and forecast."
    )
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=700,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )
    return message.content[0].text
