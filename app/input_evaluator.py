"""Agent 0 — Input Evaluator
Checks if founder input has enough detail to run the GTM pipeline.
"""
import json

import anthropic


SYSTEM_PROMPT = """You are an input quality gate for a GTM planning app.

Decide whether the founder input has enough detail to generate a useful GTM plan.

Minimum useful detail typically includes:
- Company stage or revenue context (for example ARR range)
- Product and customer type (who they sell to)
- Main GTM bottleneck or goal

Return ONLY valid JSON with this exact schema:
{
  "is_sufficient": true or false,
  "missing": ["short bullet", "short bullet"],
  "reason": "one short sentence",
    "template": "short fill-in template founders can copy",
    "response_format": "labeled format founders should follow"
}

Rules:
- If details are vague, set is_sufficient to false.
- Keep missing items concise.
- Keep template under 6 lines.
- No markdown code fences.
"""


def _fallback_evaluation(founder_text: str) -> dict:
    text = founder_text.lower()
    has_stage = any(token in text for token in ["arr", "mrr", "$", "revenue", "stage", "seed", "series"])
    has_customer = any(token in text for token in ["sell", "customer", "buyer", "b2b", "b2c", "fintech", "saas"])
    has_problem = any(token in text for token in ["problem", "stuck", "not", "goal", "pipeline", "convert", "hire", "growth"])

    is_sufficient = has_stage and has_customer and has_problem and len(founder_text.strip()) >= 40
    missing = []
    if not has_stage:
        missing.append("Company stage/revenue context")
    if not has_customer:
        missing.append("Who your product is for")
    if not has_problem:
        missing.append("Main GTM bottleneck or goal")

    return {
        "is_sufficient": is_sufficient,
        "missing": missing,
        "reason": "Input is too vague for a reliable GTM plan." if not is_sufficient else "Input is detailed enough to proceed.",
        "template": (
            "We are a [company type] at [stage/ARR].\n"
            "We sell [product] to [customer/buyer].\n"
            "Our current GTM problem is [specific bottleneck].\n"
            "Today we have [team/channel baseline].\n"
            "In the next [timeframe], we need [goal/metric]."
        ),
        "response_format": (
            "Stage/Revenue: [e.g., $1M ARR]\n"
            "Product: [what you sell]\n"
            "Target Customer: [who buys]\n"
            "Main GTM Problem: [what is not working]\n"
            "Current Setup: [team/channels today]\n"
            "Goal: [target and timeframe]"
        ),
    }


def run_input_evaluator(use_case: str, context: dict) -> dict:
    """Evaluate whether input is sufficient for downstream GTM agents."""
    founder_text = context.get("situation", use_case)

    try:
        client = anthropic.Anthropic()
        user_msg = (
            f"Founder input:\n{founder_text}\n\n"
            "Evaluate if this is sufficient to run GTM planning agents."
        )
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            temperature=0,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_msg}],
        )
        parsed = json.loads(message.content[0].text)

        if not isinstance(parsed, dict) or "is_sufficient" not in parsed:
            return _fallback_evaluation(founder_text)

        parsed.setdefault("missing", [])
        parsed.setdefault("reason", "")
        parsed.setdefault(
            "template",
            (
                "We are a [company type] at [stage/ARR].\n"
                "We sell [product] to [customer/buyer].\n"
                "Our current GTM problem is [specific bottleneck].\n"
                "Today we have [team/channel baseline].\n"
                "In the next [timeframe], we need [goal/metric]."
            ),
        )
        parsed.setdefault(
            "response_format",
            (
                "Stage/Revenue: [e.g., $1M ARR]\n"
                "Product: [what you sell]\n"
                "Target Customer: [who buys]\n"
                "Main GTM Problem: [what is not working]\n"
                "Current Setup: [team/channels today]\n"
                "Goal: [target and timeframe]"
            ),
        )
        return parsed
    except Exception:
        return _fallback_evaluation(founder_text)