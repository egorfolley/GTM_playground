import json
import re


def run(profile: dict, signals: list, client) -> dict:
    try:
        system_prompt = (
            "You are a positioning strategist for B2B SaaS.\n"
            "Reference the vertical and ACV in your answer.\n"
            "Return JSON only. No markdown. No explanation.\n"
            "{\n"
            "  'wedge': 'what for whom vs what alternative',\n"
            "  'roi': 'efficiency cost or revenue in 1 sentence',\n"
            "  'objection': 'most likely objection',\n"
            "  'objection_response': '1 sentence response'\n"
            "}\n"
            "Never invent competitor names."
        )

        signal_titles = [s[3] for s in signals]
        user_message = (
            f"Profile: {json.dumps(profile, indent=2)}\n"
            f"Signals: {signal_titles}"
        )

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            temperature=0.2,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
        text = response.content[0].text

        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            return {}
        return json.loads(match.group(0))
    except Exception:
        return {}
