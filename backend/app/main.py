import os
import re
import time

import anthropic
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.agents import actions, benchmarking, distribution, icp, positioning, scraper, signals

load_dotenv()

PROFILE_MODEL = "claude-haiku-4-5-20251001"


class BuildGtmRequest(BaseModel):
    founderText: str


def _client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return anthropic.Anthropic(api_key=api_key)


def _display_int(value):
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        cleaned = value.replace(",", "").strip()
        if cleaned.isdigit():
            return int(cleaned)
    return None


def _build_snapshot(payload: dict) -> str:
    profile = payload.get("profile", {}) or {}
    bench = payload.get("benchmarking", {}) or {}
    icp_data = payload.get("icp", {}) or {}
    pos = payload.get("positioning", {}) or {}
    dist = payload.get("distribution", {}) or {}
    act = payload.get("actions", {}) or {}

    arr = _display_int(profile.get("arr")) or 0
    acv = _display_int(profile.get("acv")) or 0

    return f"""GROWTH GOALED - GTM SNAPSHOT
{profile.get('company_name', '')}
Generated: {time.strftime('%Y-%m-%d')}

COMPANY PROFILE
Overview: {profile.get('overview', '')}
Problem: {profile.get('problem', '')}
Solution: {profile.get('solution', '')}
Vertical: {profile.get('vertical', '')}
Founded: {profile.get('founding_year', '')}
ARR: ${arr:,}
ACV: ${acv:,}
Sales Cycle: {profile.get('sales_cycle_days', '')} days
Motion: {profile.get('sales_motion', '')}

BENCHMARKING
Overall Percentile: {bench.get('overall_percentile', '')}
Biggest Gap: {bench.get('biggest_gap', '')}
Highest Leverage: {bench.get('highest_leverage_lever', '')}

ICP
{icp_data.get('company_profile', '')}
Buyer: {icp_data.get('buyer_title', '')}
Champion: {icp_data.get('champion_title', '')}
Trigger: {icp_data.get('trigger_event', '')}
Avoid: {icp_data.get('negative_icp', '')}

POSITIONING
Wedge: {pos.get('wedge', '')}
ROI: {pos.get('roi', '')}
Objection: {pos.get('objection', '')}
Response: {pos.get('objection_response', '')}

DISTRIBUTION
Engine 1: {dist.get('engine_1', {}).get('channel', '')}
{dist.get('engine_1', {}).get('action', '')}
Engine 2: {dist.get('engine_2', {}).get('channel', '')}
{dist.get('engine_2', {}).get('action', '')}
Engine 3: {dist.get('engine_3', {}).get('channel', '')}
{dist.get('engine_3', {}).get('action', '')}

EXECUTION
This week:
1. {act.get('action_1', '')}
2. {act.get('action_2', '')}
3. {act.get('action_3', '')}
Day 30: {act.get('day_30', '')}
Day 60: {act.get('day_60', '')}
Day 90: {act.get('day_90', '')}
"""


app = FastAPI(title="Growth Goaled API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/build-gtm")
async def build_gtm(request: BuildGtmRequest):
    founder_text = request.founderText.strip()
    if not founder_text:
        raise HTTPException(status_code=400, detail="founderText is required")

    try:
        client = _client()
        url_match = re.search(r"https?://[^\s.,]+|[A-Za-z0-9.-]+\.[A-Za-z]{2,}", founder_text)
        url = url_match.group() if url_match else ""

        homepage = scraper.scrape_url(url)
        profile, error = scraper.extract_profile(
            founder_text,
            homepage,
            client,
            model=PROFILE_MODEL,
        )
        if error:
            raise HTTPException(status_code=502, detail=error)

        signal_list = signals.get_signals(
            profile.get("vertical", ""),
            profile.get("sub_vertical", ""),
        )

        payload = {
            "profile": profile,
            "signals": [
                {"tone": tone, "source": source, "time": signal_time, "title": title}
                for tone, source, signal_time, title in signal_list
            ],
            "benchmarking": benchmarking.run(profile, client),
            "icp": icp.run(profile, signal_list, client),
            "positioning": positioning.run(profile, signal_list, client),
            "distribution": distribution.run(profile, signal_list, client),
            "actions": actions.run(profile, signal_list, client),
        }
        payload["snapshot"] = _build_snapshot(payload)
        return payload
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/api/health")
async def health():
    return {"ok": True}
