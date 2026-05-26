import json
import re


def run(profile: dict, signals: list, client) -> dict:
    try:
        system_prompt = (
            "You are a distribution designer for B2B SaaS.\n"
            "Design 3 channels for this ARR and motion.\n"
            "Return JSON only. No markdown. No explanation.\n"
            "{\n"
            "  'engine_1': {\n"
            "    'channel': 'channel name',\n"
            "    'rationale': '1 sentence why this fits',\n"
            "    'action': 'specific first step this week'\n"
            "  },\n"
            "  'engine_2': {\n"
            "    'channel': 'channel name',\n"
            "    'rationale': '1 sentence why this fits',\n"
            "    'action': 'specific first step this week'\n"
            "  },\n"
            "  'engine_3': {\n"
            "    'channel': 'channel name',\n"
            "    'rationale': '1 sentence why this fits',\n"
            "    'action': 'specific first step this week'\n"
            "  }\n"
            "}\n"
            "No enterprise channels below $3M ARR."
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
