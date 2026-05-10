from __future__ import annotations

from typing import Any

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from growth_goaled.export import build_export_pdf
from growth_goaled.logging_utils import log_step
from growth_goaled.models import CompanyProfile, DiagnosticOutput, PillarScores
from growth_goaled.mock_data import COMPANY_OPTIONS, build_custom_company, get_mock_company
from growth_goaled.scoring import calculate_pillar_scores, score_color


def peer_benchmark_df(scores: PillarScores) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Pillar": ["Sales Efficiency", "Funnel Efficiency", "Founder Dependency"],
            "Company": [
                scores.sales_efficiency,
                scores.funnel_efficiency,
                scores.founder_dependency,
            ],
            "Series A Peer Benchmark": [72, 68, 74],
        }
    )


def render_company_selector() -> tuple[CompanyProfile, str, bool]:
    with st.sidebar:
        st.markdown("#### Company")
        selected_option = st.selectbox(
            "Choose a demo company",
            COMPANY_OPTIONS,
            index=1,
            key="company_selector",
        )
        if st.session_state.get("last_company_selector") != selected_option:
            st.session_state.last_company_selector = selected_option
            st.session_state.snapshot_has_run = selected_option != "Enter your own data"

        if selected_option != "Enter your own data":
            company = get_mock_company(selected_option)
            st.session_state.snapshot_has_run = True
            return company, selected_option, True

        st.caption("Enter founder data and run the diagnostic.")
        with st.form("custom_company_form"):
            arr_m = st.number_input("ARR ($M)", min_value=0.1, value=5.0, step=0.5)
            acv_k = st.number_input("ACV ($K)", min_value=1.0, value=45.0, step=5.0)
            aes = st.number_input("AEs", min_value=0, value=4, step=1)
            sdrs = st.number_input("SDRs", min_value=0, value=2, step=1)
            pipeline_volume_m = st.number_input("Pipeline ($M)", min_value=0.1, value=8.0, step=0.5)
            qualified_pipeline_m = st.number_input(
                "Qualified pipeline ($M)",
                min_value=0.1,
                value=3.6,
                step=0.5,
            )
            win_rate = st.slider("Win rate", min_value=0.01, max_value=0.60, value=0.22, step=0.01)
            outbound_source_pct = st.slider(
                "Outbound source mix",
                min_value=0.0,
                max_value=1.0,
                value=0.60,
                step=0.05,
            )
            founder_dependency_pct = st.slider(
                "Founder dependency",
                min_value=0.0,
                max_value=1.0,
                value=0.45,
                step=0.05,
            )
            planned_aes = st.number_input("Planned AE hires", min_value=0, value=1, step=1)
            planned_sdrs = st.number_input("Planned SDR hires", min_value=0, value=1, step=1)
            submitted = st.form_submit_button("Run diagnostic", use_container_width=True)

        if submitted:
            st.session_state.custom_company = build_custom_company(
                arr_m=arr_m,
                acv_k=acv_k,
                aes=aes,
                sdrs=sdrs,
                pipeline_volume_m=pipeline_volume_m,
                qualified_pipeline_m=min(qualified_pipeline_m, pipeline_volume_m),
                win_rate=win_rate,
                outbound_source_pct=outbound_source_pct,
                founder_dependency_pct=founder_dependency_pct,
                planned_aes=planned_aes,
                planned_sdrs=planned_sdrs,
            )
            st.session_state.snapshot_has_run = True
            st.session_state.page = "Analysis"

        company = st.session_state.get(
            "custom_company",
            build_custom_company(
                arr_m=arr_m,
                acv_k=acv_k,
                aes=aes,
                sdrs=sdrs,
                pipeline_volume_m=pipeline_volume_m,
                qualified_pipeline_m=min(qualified_pipeline_m, pipeline_volume_m),
                win_rate=win_rate,
                outbound_source_pct=outbound_source_pct,
                founder_dependency_pct=founder_dependency_pct,
                planned_aes=planned_aes,
                planned_sdrs=planned_sdrs,
            ),
        )
        return company, selected_option, bool(st.session_state.get("snapshot_has_run"))


def render_sidebar(company: CompanyProfile, market_data: dict[str, Any]) -> None:
    log_step("STEP 7A | Rendering sidebar")
    with st.sidebar:
        st.markdown("### Growth Goaled")
        st.caption("Series A GTM diagnostic")
        st.markdown(
            """
            This demo shows how a founder can move from external growth signals
            to a focused GTM action plan in minutes.
            """
        )
        st.divider()

        if st.button("Home", use_container_width=True):
            st.session_state.page = "Home"
        if st.button("Analysis", use_container_width=True):
            st.session_state.page = "Analysis"
        if st.button("90-Day Roadmap", use_container_width=True):
            st.session_state.page = "90-Day Execution Roadmap"
        if st.button("How It Works", use_container_width=True):
            st.session_state.page = "How It Works"

        st.divider()
        st.markdown("#### Mock Signal Feed")
        st.caption("How we detected this company")
        for signal in company.detected_signals:
            st.markdown(f"<div class='signal'>{signal}</div>", unsafe_allow_html=True)

        st.divider()
        st.markdown("#### Market Context")
        st.caption(f"Category benchmarks: {market_data['category']}")
        st.metric(
            "CAC Payback",
            f"{company.cac_payback_months} mo",
            f"Category avg: {market_data['category_avg_cac_payback_months']} mo",
        )
        st.metric(
            "Win Rate",
            f"{company.win_rate:.0%}",
            f"Category avg: {market_data['category_avg_win_rate']:.0%}",
        )
        st.metric(
            "ACV",
            f"${company.acv_k:.0f}K",
            f"Category avg: ${market_data['category_avg_acv_k']:.0f}K",
        )


def render_home(company: CompanyProfile) -> None:
    log_step("STEP 7B | Rendering Home page")
    st.markdown(
        """
        <section class="hero">
          <h1>Find the GTM bottleneck before the next board meeting.</h1>
          <p>
            Growth Goaled Snapshot turns buying signals and operating metrics into a CRO-level
            diagnosis for Series A founders: what is slowing growth, what to fix first, and what
            to tell the board.
          </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-title'>Demo workflow</div>", unsafe_allow_html=True)
    st.markdown(
        """
        - Detects when a funded company looks ready to scale but may have hidden GTM friction.
        - Scores sales efficiency, funnel quality, and founder dependency from realistic operating metrics.
        - Turns the diagnosis into a ranked fix order and 90-day execution plan.
        """
    )

    # col_a, col_b, col_c, col_d = st.columns(4)
    # col_a.metric("ARR", "$6.0M")
    # col_b.metric("CAC Payback", "19 mo")
    # col_c.metric("Win Rate", "24%")
    # col_d.metric("Sales Cycle", "78 days")

    st.markdown("<div class='section-title'>Detected Company</div>", unsafe_allow_html=True)
    st.markdown(company.company_summary)

    if st.button("Run Growth Goaled Snapshot Demo", type="primary", use_container_width=True):
        st.session_state.snapshot_has_run = True
        st.session_state.page = "Analysis"
        st.rerun()


def render_score_cards(scores: PillarScores) -> None:
    log_step("STEP 7D | Rendering score cards", scores)
    cards = [
        (
            "Sales Efficiency",
            scores.sales_efficiency,
            "CAC payback, rep load, ACV, margin, and growth quality.",
        ),
        (
            "Funnel Efficiency",
            scores.funnel_efficiency,
            "Qualification rate, conversion quality, and sales cycle health.",
        ),
        (
            "Founder Dependency",
            scores.founder_dependency,
            "Repeatability of the sales motion without founder intervention.",
        ),
    ]
    cols = st.columns(3)
    for col, (label, score, note) in zip(cols, cards):
        col.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value" style="color:{score_color(score)}">{score}</div>
                <div class="metric-note">{note}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_benchmark_chart(scores: PillarScores) -> None:
    log_step("STEP 7E | Rendering peer benchmark chart", peer_benchmark_df(scores).to_dict("records"))
    df = peer_benchmark_df(scores)
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["Pillar"],
            y=df["Company"],
            name="Company",
            marker_color="#42D9FF",
            text=df["Company"],
            textposition="outside",
            textfont=dict(color="#F8FAFC", size=14),
        )
    )

    fig.add_trace(
        go.Bar(
            x=df["Pillar"],
            y=df["Series A Peer Benchmark"],
            name="Series A Peer Benchmark",
            marker_color="#1677FF",
            text=df["Series A Peer Benchmark"],
            textposition="outside",
            textfont=dict(color="#F8FAFC", size=14),
        )
    )

    fig.update_layout(
        barmode="group",
        height=410,
        margin=dict(l=16, r=16, t=50, b=20),
        paper_bgcolor="#000000",
        plot_bgcolor="#000000",
        yaxis=dict(
            range=[0, 105],
            title=dict(text="Score", font=dict(color="#F8FAFC")),
            gridcolor="#1D4ED8",
            zerolinecolor="#1D4ED8",
            tickfont=dict(color="#A9C7FF"),
        ),
        xaxis=dict(
            tickfont=dict(color="#F8FAFC", size=13),
            linecolor="#1D4ED8",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#F8FAFC"),
        ),
        font=dict(family="Inter, Arial, sans-serif", color="#F8FAFC"),
    )
    st.plotly_chart(fig, use_container_width=True)


def render_snapshot(company: CompanyProfile, diagnostic: DiagnosticOutput) -> None:
    log_step(
        "STEP 7C | Rendering Analysis page",
        {
            "diagnostic_source": diagnostic.source,
            "warnings": diagnostic.warnings,
            "ranked_fix_order": diagnostic.ranked_fix_order,
        },
    )
    scores = diagnostic.raw_scores or calculate_pillar_scores(company)
    st.title("Analysis")
    st.caption(diagnostic.source)
    st.markdown(
        """
        <div class="context-panel">
            <p>
                This page shows where growth is getting stuck and what the founder should
                fix before adding more sales and marketing headcount.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for warning in diagnostic.warnings:
        st.warning(warning)

    st.markdown("<div class='section-title'>Executive Diagnosis</div>", unsafe_allow_html=True)
    st.markdown(diagnostic.executive_summary)
    st.caption(f"Situation detected: {diagnostic.detected_situation}")
    st.markdown(
        """
        <div class="explainer-grid">
            <div class="explainer-card">
                <strong>Sales Efficiency</strong>
                <p>Answers whether the company is creating ARR with a healthy cost structure, payback period, and rep capacity model.</p>
            </div>
            <div class="explainer-card">
                <strong>Funnel Efficiency</strong>
                <p>Answers whether the top-of-funnel volume is turning into qualified pipeline and closed revenue at the right rate.</p>
            </div>
            <div class="explainer-card">
                <strong>Founder Dependency</strong>
                <p>Answers whether revenue is repeatable through the team or still relies too heavily on founder involvement.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_score_cards(scores)

    st.markdown("<div class='section-title'>Peer Benchmark Comparison</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="context-panel">
            <h3>Why the benchmark matters</h3>
            <p>
                A single metric can look acceptable in isolation. Comparing each pillar to a
                Series A peer benchmark shows whether the company is truly ready to scale the
                current GTM motion or needs to fix quality first.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_benchmark_chart(scores)

    left, right = st.columns([1.2, 0.8])
    with left:
        st.markdown("<div class='section-title'>Key Insights</div>", unsafe_allow_html=True)
        for insight in diagnostic.key_insights:
            st.markdown(f"<div class='insight'>{insight}</div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='section-title'>Ranked Fix Order</div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="context-panel">
                <h3>Why order matters</h3>
                <p>
                    Fixing pipeline quality first prevents the team from optimizing around
                    bad-fit demand. ICP and ACV discipline come next. Hiring waits until the
                    motion is efficient enough to scale.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        for idx, fix in enumerate(diagnostic.ranked_fix_order, start=1):
            st.markdown(
                f"<div class='fix'><strong>{idx}. {fix}</strong></div>",
                unsafe_allow_html=True,
            )

        export_pdf = build_export_pdf(company, diagnostic)
        st.download_button(
            "Export PDF",
            data=export_pdf,
            file_name="growth_goaled_snapshot.pdf",
            mime="application/pdf",
            use_container_width=True,
            help="Download a simple board-ready PDF generated by the app.",
        )


def render_roadmap(company: CompanyProfile, diagnostic: DiagnosticOutput) -> None:
    log_step(
        "STEP 7F | Rendering 90-Day Execution Roadmap page",
        {
            "roadmap_windows": [item["window"] for item in diagnostic.roadmap],
            "weekly_rhythm_items": len(diagnostic.weekly_rhythm),
        },
    )
    st.title("90-Day Execution Roadmap")
    st.caption("A practical operating plan for the next three board cycles.")
    st.markdown(
        """
        <div class="context-panel">
            <h3>Why this page exists</h3>
            <p>
                A useful GTM diagnostic should not stop at insight. This roadmap turns the
                Snapshot into a 90-day operating cadence: what to change first, how to measure
                progress, and what the founder can say to the board.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-title'>Three Operating Windows</div>", unsafe_allow_html=True)
    cols = st.columns(3)
    for col, item in zip(cols, diagnostic.roadmap):
        col.markdown(
            f"""
            <div class="roadmap">
                <div class="roadmap-window">{item['window']}</div>
                <h3>{item['focus']}</h3>
                <p>{item['actions']}</p>
                <p class="small-muted"><strong>Success metric:</strong> {item['success_metric']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    left, right = st.columns([0.95, 1.05])
    with left:
        st.markdown("<div class='section-title'>Weekly Rhythm Checklist</div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="context-panel">
                <h3>How to use it</h3>
                <p>
                    These meetings keep the team focused on quality, ACV, and founder
                    dependency instead of simply celebrating more activity.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        for item in diagnostic.weekly_rhythm:
            st.markdown(
                f"<div class='check-row'><span class='check-mark'>&check;</span><span>{item}</span></div>",
                unsafe_allow_html=True,
            )

    with right:
        st.markdown("<div class='section-title'>Copyable Board Narrative</div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="context-panel">
                <h3>What the board needs to hear</h3>
                <p>
                    The narrative frames the decision clearly: the business has demand, but
                    the next phase should improve conversion economics before expanding GTM capacity.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.code(diagnostic.board_narrative, language="markdown")

        export_pdf = build_export_pdf(company, diagnostic)
        st.download_button(
            "Export PDF",
            data=export_pdf,
            file_name="growth_goaled_90_day_roadmap.pdf",
            mime="application/pdf",
            use_container_width=True,
            help="Download a simple board-ready PDF generated by the app.",
        )


def render_logic_page(
    company: CompanyProfile,
    market_data: dict[str, Any],
    scores: PillarScores,
    diagnostic: DiagnosticOutput,
) -> None:
    log_step(
        "STEP 7G | Rendering How It Works page",
        {
            "company": company.company_summary,
            "scores": scores,
            "diagnostic_source": diagnostic.source,
        },
    )
    st.title("How It Works")
    st.caption("A plain-English walkthrough of what the agent used and why it reached this outcome.")

    st.markdown("<div class='section-title'>1. The Company Snapshot We Gave It</div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="context-panel">
            <p>{company.company_summary}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    metric_cols = st.columns(4)
    metric_cols[0].metric("ARR", f"${company.arr_m:.1f}M")
    metric_cols[1].metric("CAC Payback", f"{company.cac_payback_months} mo")
    metric_cols[2].metric("Win Rate", f"{company.win_rate:.0%}")
    metric_cols[3].metric("Sales Cycle", f"{company.sales_cycle_days} days")

    st.markdown(
        """
        <div class="context-panel">
            <p>
                These inputs describe a company that has real demand, but may be spending too
                much time and money to turn that demand into efficient revenue.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-title'>2. The Market Context We Compared Against</div>", unsafe_allow_html=True)
    market_cols = st.columns(3)
    market_cols[0].metric(
        "CAC Payback",
        f"{company.cac_payback_months} mo",
        f"Category avg: {market_data['category_avg_cac_payback_months']} mo",
    )
    market_cols[1].metric(
        "Win Rate",
        f"{company.win_rate:.0%}",
        f"Category avg: {market_data['category_avg_win_rate']:.0%}",
    )
    market_cols[2].metric(
        "ACV",
        f"${company.acv_k:.0f}K",
        f"Category avg: ${market_data['category_avg_acv_k']:.0f}K",
    )
    st.markdown(
        f"""
        <div class="context-panel">
            <p>
                The category is {market_data['category']}. The company is above the category
                average on win rate and ACV, but CAC payback is worse than the category average.
                That suggests the core issue is not whether customers buy, but whether the
                company is creating revenue efficiently enough.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-title'>3. The Three Health Checks</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="explainer-grid">
            <div class="explainer-card">
                <strong>Sales Efficiency</strong>
                <p>Checks whether growth is worth the cost. Long payback and too much hiring pressure lower the score.</p>
            </div>
            <div class="explainer-card">
                <strong>Funnel Efficiency</strong>
                <p>Checks whether pipeline is high quality. Lots of leads are not enough if too few become qualified opportunities.</p>
            </div>
            <div class="explainer-card">
                <strong>Founder Dependency</strong>
                <p>Checks whether the sales motion can work without the founder personally helping too many deals close.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_score_cards(scores)

    st.markdown("<div class='section-title'>4. Why This Outcome Happened</div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="context-panel">
            <p>
                The agent saw a company with strong demand signals, but weak efficiency signals:
                CAC payback is {company.cac_payback_months} months, only
                {company.qualified_pipeline_m / company.pipeline_volume_m:.0%} of pipeline is
                qualified, and the founder is involved in {company.founder_in_late_stage_deals_pct:.0%}
                of late-stage deals. That combination points to a quality and repeatability
                problem, not simply a need for more salespeople.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-title'>5. Final Recommendation Logic</div>", unsafe_allow_html=True)
    for idx, fix in enumerate(diagnostic.ranked_fix_order, start=1):
        st.markdown(
            f"<div class='fix'><strong>{idx}. {fix}</strong></div>",
            unsafe_allow_html=True,
        )
    st.markdown(
        """
        <div class="context-panel">
            <p>
                Pipeline quality comes first because better targeting improves everything after it.
                ICP and ACV come second because the company needs bigger, better-fit deals to
                improve payback. Hiring comes last because adding people before fixing quality
                would likely make the expensive growth problem worse.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-title'>6. AI Processing</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="context-panel">
            <p>
                The formulas create the scores. AI turns the scores, company facts, and
                market context into a founder-friendly explanation, key insights, ranked fix
                order, 90-day roadmap, weekly rhythm, and board narrative.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
