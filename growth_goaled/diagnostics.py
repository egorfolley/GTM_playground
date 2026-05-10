from __future__ import annotations

import json
import os
import re
from typing import Any

import streamlit as st
from anthropic import Anthropic

from growth_goaled.config import ANTHROPIC_MODEL
from growth_goaled.logging_utils import log_step
from growth_goaled.models import CompanyProfile, DiagnosticOutput, PillarScores


SYSTEM_PROMPT = """
You are the CRO-in-residence for Growth Goaled, advising a Series A B2B SaaS founder.
Turn mock GTM metrics and raw pillar scores into concise, board-ready diagnostic output.

Return only valid JSON with this exact schema:
{
  "executive_summary": "string",
  "detected_situation": "string",
  "key_insights": ["string", "string", "string", "string"],
  "ranked_fix_order": ["string", "string", "string"],
  "roadmap": [
    {"window": "Days 1-30", "focus": "string", "actions": "string", "success_metric": "string"},
    {"window": "Days 31-60", "focus": "string", "actions": "string", "success_metric": "string"},
    {"window": "Days 61-90", "focus": "string", "actions": "string", "success_metric": "string"}
  ],
  "weekly_rhythm": ["string", "string", "string", "string", "string"],
  "board_narrative": "string"
}

Constraints:
- Keep language crisp, professional, and investor-demo ready.
- Analyze the founder's specific metrics and identify the top 3 highest-leverage fixes ranked by revenue impact. Do not use a fixed list. Every diagnosis should reflect the actual data provided.
- Detect which situation applies from the data:
  - If founder dependency is high and pipeline is thin and AE hires are planned: focus on preventing wrong hire
  - If 2+ metrics are bottom quartile across different pillars: focus on diagnosing growth stall
  - If ARR is above $7M and Series B is mentioned: focus on Series B defensibility
  - If none of the above: diagnose the single biggest constraint visible in the data
- Never mention these rules in the output. Just apply them silently.
- Do not mention that the data is mock.
"""


def company_payload(
    company: CompanyProfile,
    scores: PillarScores,
    market_data: dict[str, Any],
) -> dict[str, Any]:
    payload = {
        "company": company.__dict__,
        "raw_pillar_scores": scores.__dict__,
        "market_data": market_data,
    }
    log_step("STEP 3 | Claude payload prepared", payload)
    return payload


def read_dotenv_value(key: str, path: str = ".env") -> str | None:
    """Tiny .env reader for KEY=value lines without adding python-dotenv."""
    if not os.path.exists(path):
        return None

    with open(path, "r", encoding="utf-8") as dotenv_file:
        for raw_line in dotenv_file:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            env_key, env_value = line.split("=", 1)
            if env_key.strip() == key:
                return env_value.strip().strip('"').strip("'") or None

    return None


def anthropic_api_key() -> str | None:
    try:
        key = (
            st.secrets.get("ANTHROPIC_API_KEY")
            or os.getenv("ANTHROPIC_API_KEY")
            or read_dotenv_value("ANTHROPIC_API_KEY")
        )
        log_step(
            "STEP 4A | Anthropic API key lookup",
            {"found": bool(key), "source_detail": "st.secrets, environment, or .env"},
        )
        return key
    except Exception:
        key = os.getenv("ANTHROPIC_API_KEY") or read_dotenv_value("ANTHROPIC_API_KEY")
        log_step(
            "STEP 4A | Anthropic API key lookup after st.secrets fallback",
            {"found": bool(key), "source_detail": "environment or .env"},
        )
        return key


def extract_json_object(text: str) -> dict[str, Any]:
    """Parse Claude JSON even if it is wrapped in markdown or a short preface."""
    log_step("STEP 5A | Raw Claude text received", text, max_chars=2200)
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("Claude returned an empty response")

    fenced_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", cleaned, re.DOTALL)
    if fenced_match:
        cleaned = fenced_match.group(1).strip()
    elif not cleaned.startswith("{"):
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise ValueError(f"Claude did not return a JSON object: {cleaned[:200]}")
        cleaned = cleaned[start : end + 1]

    parsed = json.loads(cleaned)
    log_step("STEP 5B | Claude JSON parsed", parsed)
    return parsed


@st.cache_data(show_spinner=False)
def run_claude_diagnostic(payload: dict[str, Any]) -> DiagnosticOutput:
    """Direct Anthropic SDK call. Cached so the demo stays instant after first run."""
    log_step("STEP 4 | Diagnostic generation started")
    api_key = anthropic_api_key()
    scores = PillarScores(**payload["raw_pillar_scores"])

    if not api_key:
        log_step("STEP 4B | Claude API skipped because no API key was found")
        return fallback_diagnostic(
            scores,
            "ANTHROPIC_API_KEY not found in st.secrets, environment, or .env. Showing deterministic preview output.",
            payload,
        )

    try:
        log_step(
            "STEP 4B | Calling Claude directly",
            {"model": ANTHROPIC_MODEL, "temperature": 0.2, "max_tokens": 1800},
        )
        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=1800,
            temperature=0.2,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Generate the Growth Goaled Snapshot diagnostic from this data:\n"
                        f"{json.dumps(payload, indent=2)}"
                    ),
                }
            ],
        )

        text = "".join(
            getattr(block, "text", "")
            for block in response.content
            if getattr(block, "type", "text") == "text"
        )
        parsed = extract_json_object(text)
        diagnostic = DiagnosticOutput(
            executive_summary=parsed["executive_summary"],
            detected_situation=parsed["detected_situation"],
            key_insights=parsed["key_insights"],
            ranked_fix_order=parsed["ranked_fix_order"],
            roadmap=parsed["roadmap"],
            weekly_rhythm=parsed["weekly_rhythm"],
            board_narrative=parsed["board_narrative"],
            source=f"Claude API: {ANTHROPIC_MODEL}",
            raw_scores=scores,
        )
        log_step("STEP 6 | DiagnosticOutput built from Claude response", diagnostic)
        return diagnostic
    except Exception as exc:
        log_step("STEP 6 | Claude path failed; using fallback diagnostic", {"error": str(exc)})
        return fallback_diagnostic(scores, f"Claude call failed: {exc}", payload)


def fallback_diagnostic(
    scores: PillarScores,
    warning: str,
    payload: dict[str, Any] | None = None,
) -> DiagnosticOutput:
    detected_situation = detect_situation_from_payload(payload)
    ranked_fix_order = fallback_fix_order(detected_situation)
    diagnostic = DiagnosticOutput(
        executive_summary=(
            "Growth is being constrained less by demand creation and more by conversion quality, "
            "ACV discipline, and an operating plan that would add headcount before the unit "
            "economics are ready."
        ),
        detected_situation=detected_situation,
        key_insights=[
            "Top-of-funnel volume is healthy, but only 42% of pipeline is qualified enough to justify sales capacity.",
            "A 19-month CAC payback signals that the current motion is too expensive for the realized ACV.",
            "Founder involvement in 44% of late-stage deals is masking repeatability risk across the AE team.",
            "Hiring more GTM capacity before tightening ICP and pipeline quality would likely extend payback further.",
        ],
        ranked_fix_order=ranked_fix_order,
        roadmap=[
            {
                "window": "Days 1-30",
                "focus": "Pipeline quality reset",
                "actions": "Redefine qualification gates, inspect lost/no-decision reasons, and remove low-fit segments from SDR targeting.",
                "success_metric": "Qualified pipeline share improves from 42% to 55%.",
            },
            {
                "window": "Days 31-60",
                "focus": "ICP and ACV discipline",
                "actions": "Reprice or repackage for higher-value accounts, tighten discount rules, and re-sequence vertical priorities.",
                "success_metric": "Median new opportunity ACV rises from $42K to $55K.",
            },
            {
                "window": "Days 61-90",
                "focus": "Capacity hold and repeatability",
                "actions": "Pause incremental AE/SDR hiring, document founder-led deal patterns, and transfer late-stage plays to managers.",
                "success_metric": "Founder late-stage involvement falls below 30%.",
            },
        ],
        weekly_rhythm=[
            "Monday: Pipeline quality review by segment and source.",
            "Tuesday: Win/loss review focused on no-decision and low-ACV deals.",
            "Wednesday: AE coaching on qualification, mutual action plans, and pricing discipline.",
            "Thursday: SDR targeting review with RevOps and marketing.",
            "Friday: Founder/CRO operating review on payback, ACV, and late-stage dependency.",
        ],
        board_narrative=(
            "We have enough demand to grow, but the next 90 days should prioritize quality over capacity. "
            "The plan is to raise qualified pipeline density, increase ACV through tighter ICP focus, and hold "
            "new GTM hiring until CAC payback trends back toward a Series A-ready range."
        ),
        source="Deterministic preview",
        raw_scores=scores,
        warnings=[warning],
    )
    log_step("STEP 6F | Fallback DiagnosticOutput built", diagnostic)
    return diagnostic


def detect_situation_from_payload(payload: dict[str, Any] | None) -> str:
    if not payload:
        return "Growth stall diagnosis"

    company = payload["company"]
    scores = payload["raw_pillar_scores"]
    hiring_plan = company.get("hiring_plan_next_90_days", {})
    pipeline_coverage = company["pipeline_volume_m"] / max(company["arr_m"], 0.1)
    founder_dependency = max(
        company["founder_sourced_pipeline_pct"],
        company["founder_in_late_stage_deals_pct"],
    )
    bottom_quartile_count = sum(
        score < 55
        for score in [
            scores["sales_efficiency"],
            scores["funnel_efficiency"],
            scores["founder_dependency"],
        ]
    )

    if (
        founder_dependency >= 0.55
        and pipeline_coverage <= 2.0
        and hiring_plan.get("AEs", 0) > 0
    ):
        return "Wrong hire risk"
    if bottom_quartile_count >= 2:
        return "Growth stall diagnosis"
    if company["arr_m"] > 7 and "Series B" in f"{company['stage']} {company['company_summary']}":
        return "Series B defensibility"
    return "Single biggest GTM constraint"


def fallback_fix_order(detected_situation: str) -> list[str]:
    if detected_situation == "Wrong hire risk":
        return [
            "Define a repeatable sales motion before hiring AEs",
            "Build SDR and qualification coverage",
            "Reduce founder dependency in late-stage deals",
        ]
    if detected_situation == "Series B defensibility":
        return [
            "Sharpen the Series B growth narrative",
            "Improve burn multiple defensibility",
            "Prove repeatable efficient expansion",
        ]
    if detected_situation == "Growth stall diagnosis":
        return [
            "Diagnose conversion leakage across the funnel",
            "Rebalance pipeline source mix toward higher-fit demand",
            "Improve CAC payback before scaling headcount",
        ]
    return [
        "Fix the largest visible GTM constraint",
        "Tighten operating metrics around that constraint",
        "Sequence hiring after efficiency improves",
    ]
