from __future__ import annotations

from typing import Any

from growth_goaled.logging_utils import log_step
from growth_goaled.models import CompanyProfile


PRELOADED_COMPANIES = {
    "UC1: Wrong AE hire risk": {
        "label": "$3M ARR Fintech, founder closing all deals, about to hire 2 AEs, no SDR, pipeline coverage 1.8x",
        "company": CompanyProfile(
            company_summary="$3M ARR Fintech, founder closing all deals, about to hire 2 AEs, no SDR, pipeline coverage 1.8x",
            stage="Series A",
            vertical="Fintech SaaS",
            arr_m=3.0,
            growth_rate_yoy=0.44,
            quarterly_growth_rate=0.06,
            pipeline_volume_m=5.4,
            qualified_pipeline_m=2.1,
            win_rate=0.18,
            sales_cycle_days=92,
            acv_k=34.0,
            gross_margin=0.78,
            cac_payback_months=17,
            net_revenue_retention=1.03,
            new_logo_arr_m=0.82,
            expansion_arr_m=0.18,
            churn_rate=0.10,
            aes=1,
            sdrs=0,
            founder_sourced_pipeline_pct=0.62,
            founder_in_late_stage_deals_pct=0.82,
            outbound_reply_rate=0.052,
            demo_to_sql_rate=0.32,
            sql_to_opportunity_rate=0.39,
            opportunity_to_close_rate=0.18,
            hiring_plan_next_90_days={"AEs": 2, "SDRs": 0, "RevOps": 0},
            detected_signals=[
                "LinkedIn hiring spike: 2 AE roles opened before SDR or RevOps foundation exists",
                "Founder posts highlight personally closing strategic accounts",
                "Pipeline coverage is 1.8x, thin for a scaling sales hiring motion",
            ],
        ),
    },
    "UC2: Growth stall diagnosis": {
        "label": "$6M ARR Healthtech, growth stalling, strong top-of-funnel, CAC payback 19 months, pipeline source mix 70% outbound",
        "company": CompanyProfile(
            company_summary="$6M ARR Healthtech, growth stalling, strong top-of-funnel, CAC payback 19 months, pipeline source mix 70% outbound",
            stage="Series A",
            vertical="Healthtech SaaS",
            arr_m=6.0,
            growth_rate_yoy=0.33,
            quarterly_growth_rate=0.03,
            pipeline_volume_m=10.8,
            qualified_pipeline_m=4.0,
            win_rate=0.20,
            sales_cycle_days=104,
            acv_k=39.0,
            gross_margin=0.76,
            cac_payback_months=19,
            net_revenue_retention=1.04,
            new_logo_arr_m=1.1,
            expansion_arr_m=0.34,
            churn_rate=0.11,
            aes=6,
            sdrs=5,
            founder_sourced_pipeline_pct=0.22,
            founder_in_late_stage_deals_pct=0.29,
            outbound_reply_rate=0.044,
            demo_to_sql_rate=0.31,
            sql_to_opportunity_rate=0.37,
            opportunity_to_close_rate=0.20,
            hiring_plan_next_90_days={"AEs": 1, "SDRs": 2, "RevOps": 1},
            detected_signals=[
                "High top-of-funnel volume is not converting into enough qualified pipeline",
                "Pipeline source mix is 70% outbound, creating CAC pressure",
                "Growth has stalled while CAC payback remains elevated at 19 months",
            ],
        ),
    },
    "UC3: Series B defensibility": {
        "label": "$9M ARR Fintech, preparing for Series B in 9 months, metrics okay but narrative weak, board pressure on burn multiple",
        "company": CompanyProfile(
            company_summary="$9M ARR Fintech, preparing for Series B in 9 months, metrics okay but narrative weak, board pressure on burn multiple",
            stage="Series A, preparing for Series B",
            vertical="Fintech SaaS",
            arr_m=9.0,
            growth_rate_yoy=0.58,
            quarterly_growth_rate=0.11,
            pipeline_volume_m=16.5,
            qualified_pipeline_m=8.1,
            win_rate=0.26,
            sales_cycle_days=74,
            acv_k=58.0,
            gross_margin=0.82,
            cac_payback_months=15,
            net_revenue_retention=1.12,
            new_logo_arr_m=2.4,
            expansion_arr_m=1.0,
            churn_rate=0.07,
            aes=8,
            sdrs=5,
            founder_sourced_pipeline_pct=0.18,
            founder_in_late_stage_deals_pct=0.24,
            outbound_reply_rate=0.068,
            demo_to_sql_rate=0.42,
            sql_to_opportunity_rate=0.49,
            opportunity_to_close_rate=0.26,
            hiring_plan_next_90_days={"AEs": 2, "SDRs": 2, "RevOps": 1},
            detected_signals=[
                "Board materials mention Series B readiness within 9 months",
                "Metrics are acceptable, but burn multiple narrative needs sharpening",
                "Hiring plan suggests the company must prove efficient scaling before fundraising",
            ],
        ),
    },
}


COMPANY_OPTIONS = list(PRELOADED_COMPANIES.keys()) + ["Enter your own data"]


def get_mock_company(option: str = "UC2: Growth stall diagnosis") -> CompanyProfile:
    """Return one of the preloaded demo companies."""
    company = PRELOADED_COMPANIES[option]["company"]
    log_step("STEP 1 | Mock data loaded", {"option": option, "company": company})
    return company


def build_custom_company(
    arr_m: float,
    acv_k: float,
    aes: int,
    sdrs: int,
    pipeline_volume_m: float,
    qualified_pipeline_m: float,
    win_rate: float,
    outbound_source_pct: float,
    founder_dependency_pct: float,
    planned_aes: int,
    planned_sdrs: int,
) -> CompanyProfile:
    company = CompanyProfile(
        company_summary=(
            f"${arr_m:.1f}M ARR founder-entered company with ${acv_k:.0f}K ACV, "
            f"{win_rate:.0%} win rate, {outbound_source_pct:.0%} outbound source mix, "
            f"and {founder_dependency_pct:.0%} founder dependency."
        ),
        stage="Series A",
        vertical="Founder-entered SaaS",
        arr_m=arr_m,
        growth_rate_yoy=0.42,
        quarterly_growth_rate=0.07,
        pipeline_volume_m=pipeline_volume_m,
        qualified_pipeline_m=qualified_pipeline_m,
        win_rate=win_rate,
        sales_cycle_days=82,
        acv_k=acv_k,
        gross_margin=0.78,
        cac_payback_months=18,
        net_revenue_retention=1.06,
        new_logo_arr_m=max(arr_m * 0.22, 0.1),
        expansion_arr_m=max(arr_m * 0.07, 0.05),
        churn_rate=0.09,
        aes=aes,
        sdrs=sdrs,
        founder_sourced_pipeline_pct=founder_dependency_pct,
        founder_in_late_stage_deals_pct=founder_dependency_pct,
        outbound_reply_rate=max(0.03, min(0.10, 0.12 - outbound_source_pct * 0.08)),
        demo_to_sql_rate=0.36,
        sql_to_opportunity_rate=0.42,
        opportunity_to_close_rate=win_rate,
        hiring_plan_next_90_days={"AEs": planned_aes, "SDRs": planned_sdrs, "RevOps": 0},
        detected_signals=[
            "Founder-entered intake data provided through the sidebar",
            f"Pipeline source mix: {outbound_source_pct:.0%} outbound",
            f"Hiring plan: {planned_aes} AEs and {planned_sdrs} SDRs in the next 90 days",
        ],
    )
    log_step("STEP 1C | Custom company data loaded", company)
    return company


def get_mock_market_data() -> dict[str, Any]:
    """Hardcoded category context for the demo."""
    market_data = {
        "category": "Fintech SaaS",
        "category_avg_cac_payback_months": 16,
        "category_avg_win_rate": 0.21,
        "category_avg_acv_k": 38,
        "top_quartile_cac_payback_months": 10,
        "top_quartile_win_rate": 0.31,
        "top_quartile_acv_k": 62,
        "competitor_hiring_signals": [
            "Competitors are hiring enterprise AEs with fintech compliance experience.",
            "Competitors are adding partner managers for bank and payments channel motions.",
            "Competitors are recruiting RevOps leaders to improve pipeline quality and forecasting.",
        ],
        "vc_sentiment": "VC appetite remains selective but constructive for fintech SaaS companies with efficient growth and clear enterprise demand.",
        "category_growth_rate_yoy": 0.34,
        "median_series_a_arr_m": 5.2,
    }
    log_step("STEP 1B | Mock market data loaded", market_data)
    return market_data
