from __future__ import annotations

from typing import Any

from growth_goaled.logging_utils import log_step
from growth_goaled.models import CompanyProfile


def get_mock_company() -> CompanyProfile:
    """Hardcoded mock data only. No user input, upload, or form state."""
    company = CompanyProfile(
        company_summary=(
            "$6M ARR Fintech SaaS with strong top-of-funnel, decent win rates, "
            "but flattening growth and CAC payback at 18+ months."
        ),
        stage="Series A",
        vertical="Fintech SaaS",
        arr_m=6.0,
        growth_rate_yoy=0.52,
        quarterly_growth_rate=0.07,
        pipeline_volume_m=9.8,
        qualified_pipeline_m=4.1,
        win_rate=0.24,
        sales_cycle_days=78,
        acv_k=42.0,
        gross_margin=0.81,
        cac_payback_months=19,
        net_revenue_retention=1.08,
        new_logo_arr_m=1.55,
        expansion_arr_m=0.52,
        churn_rate=0.09,
        aes=7,
        sdrs=5,
        founder_sourced_pipeline_pct=0.31,
        founder_in_late_stage_deals_pct=0.44,
        outbound_reply_rate=0.075,
        demo_to_sql_rate=0.38,
        sql_to_opportunity_rate=0.46,
        opportunity_to_close_rate=0.24,
        hiring_plan_next_90_days={"AEs": 2, "SDRs": 3, "RevOps": 1},
        detected_signals=[
            "LinkedIn hiring spike: 5 open GTM roles added in the last 21 days",
            "Crunchbase recent funding: Series A announced 8 weeks ago",
            "Job posts emphasize new-logo acquisition and outbound motion",
            "Founder posts mention enterprise pipeline momentum but longer cycles",
        ],
    )
    log_step("STEP 1 | Mock data loaded", company)
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

