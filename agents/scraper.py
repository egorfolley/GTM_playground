import json
import re

import requests
from bs4 import BeautifulSoup


def scrape_url(url: str) -> str:
    try:
        response = requests.get(
            url,
            timeout=8,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        text = soup.get_text(" ", strip=True)
        text = re.sub(r"\s+", " ", text).strip()
        return text[:3000]
    except Exception:
        return ""


def extract_profile(
    founder_text: str,
    homepage_text: str,
    client,
) -> dict:
    try:
        system_prompt = (
            "You are a company intelligence analyst.\n"
            "Extract from homepage text and founder input.\n"
            "Return valid JSON only. No markdown. No explanation.\n"
            "{\n"
            "  'company_name': 'string or null',\n"
            "  'overview': '2 sentences what company does or null',\n"
            "  'problem': '1 sentence problem they solve or null',\n"
            "  'solution': '1 sentence their solution or null',\n"
            "  'vertical': 'top-level industry or null',\n"
            "  'sub_vertical': 'specific niche or null',\n"
            "  'founding_year': integer or null,\n"
            "  'acv': integer in dollars or null,\n"
            "  'sales_cycle_days': integer or null,\n"
            "  'arr': integer in dollars or null,\n"
            "  'sales_motion':\n"
            "    'Founder-led|Outbound|Inbound|PLG|Mixed|null'\n"
            "}\n"
            "Never invent numbers not in the input.\n"
            "Return null for anything missing or unclear."
        )

        user_message = (
            f"Founder input: {founder_text}\n"
            f"Homepage text: {homepage_text[:2000]}"
        )

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=600,
            temperature=0.1,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )

        text = ""
        for block in getattr(response, "content", []):
            if hasattr(block, "text"):
                text += block.text

        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            return {}
        return json.loads(match.group(0))
    except Exception:
        return {}
