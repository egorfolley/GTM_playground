import json
import re


def run(profile: dict, client) -> dict:
    try:
        system_prompt = (
            "You are a GTM benchmarking specialist for B2B SaaS.\n"
            "Calculate percentile rankings vs peers in the same\n"
            "vertical and ARR band.\n"
            "Return JSON only. No markdown. No explanation.\n"
            "{\n"
            "  'acv_percentile': integer 1-99,\n"
            "  'cycle_percentile': integer 1-99,\n"
            "  'revenue_efficiency_percentile': integer 1-99,\n"
            "  'gtm_motion_percentile': integer 1-99,\n"
            "  'deal_velocity_percentile': integer 1-99,\n"
            "  'overall_percentile': integer 1-99,\n"
            "  'acv_top_quartile': integer in dollars,\n"
            "  'cycle_top_quartile_days': integer,\n"
            "  'biggest_gap': 'metric name',\n"
            "  'highest_leverage_lever': 'one sentence fix'\n"
            "}\n"
            "Use realistic B2B SaaS benchmarks.\n"
            "If value is null assume ACV $20K ARR $1M cycle 60 days."
        )

        user_message = f"Company profile: {json.dumps(profile, indent=2)}"

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
