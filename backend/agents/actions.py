import json
import re


def run(profile: dict, signals: list, client) -> dict:
    try:
        system_prompt = (
            "You are a GTM execution advisor for B2B SaaS.\n"
            "Return JSON only. No markdown. No explanation.\n"
            "{\n"
            "  'action_1': 'specific executable action today',\n"
            "  'action_2': 'specific executable action this week',\n"
            "  'action_3': 'specific executable action this week',\n"
            "  'day_30': 'one measurable outcome',\n"
            "  'day_60': 'one measurable outcome',\n"
            "  'day_90': 'one measurable outcome'\n"
            "}\n"
            "Actions must reference this company vertical and ACV.\n"
            "No generic advice."
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
