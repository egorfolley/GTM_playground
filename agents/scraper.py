import json
import re

import requests
from bs4 import BeautifulSoup


def scrape_url(url: str) -> str:
    if not url:
        return ""

    normalized_url = url.strip()
    if not normalized_url.startswith(("http://", "https://")):
        normalized_url = f"https://{normalized_url}"

    candidate_urls = [normalized_url]
    if normalized_url.startswith("https://"):
        candidate_urls.append("http://" + normalized_url[len("https://"):])

    try:
        for candidate_url in candidate_urls:
            try:
                response = requests.get(
                    candidate_url,
                    timeout=8,
                    headers={"User-Agent": "Mozilla/5.0"},
                )
                soup = BeautifulSoup(response.text, "html.parser")

                for tag in soup(["script", "style", "nav", "footer"]):
                    tag.decompose()

                text = soup.get_text(" ", strip=True)
                text = re.sub(r"\s+", " ", text).strip()
                if text:
                    return text[:3000]
            except Exception:
                continue
        return ""
    except Exception:
        return ""


def extract_profile(
    founder_text: str,
    homepage_text: str,
    client,
    model: str = "claude-haiku-4-5-20251001",
) -> tuple:
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

        full_prompt = f"{system_prompt}\n\n{user_message}"

        # Dispatch based on client type
        if hasattr(client, "generate_content"):
            # Google Gemini
            response = client.generate_content(full_prompt)
            text = response.text
        else:
            # Anthropic
            response = client.messages.create(
                model=model,
                max_tokens=1024,
                messages=[{"role": "user", "content": full_prompt}],
            )
            text = response.content[0].text

        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            return {}, f"AI responded but returned no JSON. Raw response: {text[:300]}"
        try:
            return json.loads(match.group(0)), None
        except json.JSONDecodeError as e:
            return {}, f"JSON parse error: {e}. Raw: {match.group(0)[:200]}"
    except Exception as e:
        return {}, str(e)
