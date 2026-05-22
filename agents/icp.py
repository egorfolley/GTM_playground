import json
import re


def run(profile: dict, signals: list, client) -> dict:
    try:
        system_prompt = (
            "You are an ICP specialist for B2B SaaS.\n"
            "Derive ICP only from the company profile.\n"
            "Return JSON only. No markdown. No explanation.\n"
            "{\n"
            "  'company_profile': '2 sentences on ideal customer',\n"
            "  'buyer_title': 'economic buyer title',\n"
            "  'champion_title': 'internal champion title',\n"
            "  'trigger_event': 'top buying trigger 1 sentence',\n"
            "  'negative_icp': 'who to avoid 1 sentence'\n"
            "}\n"
            "Never invent company names.\n"
            "Label inferred claims as likely."
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
