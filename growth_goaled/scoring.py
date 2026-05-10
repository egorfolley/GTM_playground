from __future__ import annotations

from growth_goaled.logging_utils import log_step
from growth_goaled.models import CompanyProfile, PillarScores


def clamp_score(value: float) -> int:
    return int(max(0, min(100, round(value))))


def calculate_sales_efficiency(company: CompanyProfile) -> int:
    """Higher is better: efficient growth, healthy CAC payback, productive GTM capacity."""
    payback_component = max(0, 100 - (company.cac_payback_months - 10) * 6)
    growth_component = min(100, company.growth_rate_yoy * 120)
    acv_component = min(100, company.acv_k / 60 * 100)
    rep_load_penalty = max(0, (company.aes + company.sdrs - 9) * 4)
    score = clamp_score(
        payback_component * 0.45
        + growth_component * 0.25
        + acv_component * 0.20
        + company.gross_margin * 100 * 0.10
        - rep_load_penalty
    )
    log_step(
        "STEP 2A | Sales Efficiency score calculated",
        {
            "payback_component": round(payback_component, 2),
            "growth_component": round(growth_component, 2),
            "acv_component": round(acv_component, 2),
            "rep_load_penalty": round(rep_load_penalty, 2),
            "score": score,
        },
    )
    return score


def calculate_funnel_efficiency(company: CompanyProfile) -> int:
    """Higher is better: quality conversion through the funnel, not just raw volume."""
    qualification_component = company.qualified_pipeline_m / company.pipeline_volume_m * 100
    cycle_component = max(0, 100 - (company.sales_cycle_days - 45) * 1.1)
    conversion_component = (
        company.demo_to_sql_rate * 100 * 0.25
        + company.sql_to_opportunity_rate * 100 * 0.30
        + company.opportunity_to_close_rate * 100 * 0.45
    )
    score = clamp_score(
        qualification_component * 0.35
        + cycle_component * 0.25
        + conversion_component * 0.40
    )
    log_step(
        "STEP 2B | Funnel Efficiency score calculated",
        {
            "qualification_component": round(qualification_component, 2),
            "cycle_component": round(cycle_component, 2),
            "conversion_component": round(conversion_component, 2),
            "score": score,
        },
    )
    return score


def calculate_founder_dependency(company: CompanyProfile) -> int:
    """Higher is better: repeatable team-led GTM motion with low founder bottleneck."""
    founder_pipeline_penalty = company.founder_sourced_pipeline_pct * 100 * 0.55
    late_stage_penalty = company.founder_in_late_stage_deals_pct * 100 * 0.45
    dependency_risk = founder_pipeline_penalty + late_stage_penalty
    score = clamp_score(100 - dependency_risk)
    log_step(
        "STEP 2C | Founder Dependency score calculated",
        {
            "founder_pipeline_penalty": round(founder_pipeline_penalty, 2),
            "late_stage_penalty": round(late_stage_penalty, 2),
            "dependency_risk": round(dependency_risk, 2),
            "score": score,
        },
    )
    return score


def calculate_pillar_scores(company: CompanyProfile) -> PillarScores:
    scores = PillarScores(
        sales_efficiency=calculate_sales_efficiency(company),
        funnel_efficiency=calculate_funnel_efficiency(company),
        founder_dependency=calculate_founder_dependency(company),
    )
    log_step("STEP 2 | Raw pillar scores complete", scores)
    return scores


def score_color(score: int) -> str:
    if score >= 75:
        return "#42D9FF"
    if score >= 55:
        return "#66B3FF"
    return "#8A7DFF"
