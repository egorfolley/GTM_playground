from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class CompanyProfile:
    company_summary: str
    stage: str
    vertical: str
    arr_m: float
    growth_rate_yoy: float
    quarterly_growth_rate: float
    pipeline_volume_m: float
    qualified_pipeline_m: float
    win_rate: float
    sales_cycle_days: int
    acv_k: float
    gross_margin: float
    cac_payback_months: int
    net_revenue_retention: float
    new_logo_arr_m: float
    expansion_arr_m: float
    churn_rate: float
    aes: int
    sdrs: int
    founder_sourced_pipeline_pct: float
    founder_in_late_stage_deals_pct: float
    outbound_reply_rate: float
    demo_to_sql_rate: float
    sql_to_opportunity_rate: float
    opportunity_to_close_rate: float
    hiring_plan_next_90_days: dict[str, int]
    detected_signals: list[str]


@dataclass(frozen=True)
class PillarScores:
    sales_efficiency: int
    funnel_efficiency: int
    founder_dependency: int


@dataclass
class DiagnosticOutput:
    executive_summary: str
    key_insights: list[str]
    ranked_fix_order: list[str]
    roadmap: list[dict[str, str]]
    weekly_rhythm: list[str]
    board_narrative: str
    source: str = "Claude"
    raw_scores: PillarScores | None = None
    warnings: list[str] = field(default_factory=list)

