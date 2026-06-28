import streamlit as st
import streamlit.components.v1 as components
import anthropic
import os
import re
import json
import time
from html import escape
from dotenv import load_dotenv
from backend.agents import scraper, signals, benchmarking, icp, positioning, distribution, actions

load_dotenv()

def main():
    st.set_page_config(
        page_title="AI GTM | Growth Goaled",
        page_icon="🎯",
        layout="wide"
    )

    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp { background-color: #0B0F1A; color: #F9FAFB; }

[data-testid="stSidebar"] {
    background-color: #0D1117;
    border-right: 1px solid #1E2D40;
}

.stTextInput > div > div > input {
    background-color: #111827;
    color: #F9FAFB;
    border: 1px solid #1E2D40;
    border-radius: 8px;
    font-size: 16px;
    padding: 14px;
}

.stTextInput > div > div > input::placeholder {
    color: #64748B;
}

.stTextInput > div > div > input:focus {
    border-color: #D4A843;
    box-shadow: 0 0 0 1px #D4A843;
}

.stButton > button {
    background-color: #D4A843;
    color: #0B0F1A;
    border: none;
    border-radius: 8px;
    padding: 12px 28px;
    font-size: 15px;
    font-weight: 700;
    width: 100%;
}

.stButton > button:hover {
    background-color: #B8922E;
    color: #0B0F1A;
}

.stExpander {
    background-color: #111827;
    border: 1px solid #1E2D40;
    border-radius: 10px;
}

hr { border-color: #1E2D40; }

[data-testid="stMarkdownContainer"] p {
    color: #94A3B8;
    line-height: 1.7;
}

.stAlert {
    background-color: #111827;
    border: 1px solid #1E2D40;
}

.stSuccess {
    background-color: rgba(212,168,67,0.08);
    border: 1px solid rgba(212,168,67,0.2);
    color: #D4A843;
}

div[data-testid="stCode"] {
    background-color: #0D1117;
    border: 1px solid #1E2D40;
}
</style>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div style="text-align:center; padding:48px 0 32px 0;">
    <p style="color:#D4A843; font-size:12px;
       font-weight:700; letter-spacing:0.12em;
       text-transform:uppercase; margin-bottom:12px;">
        GPS for GTM
    </p>
    <h1 style="font-size:40px; font-weight:700;
       color:#F9FAFB; line-height:1.2;
       margin-bottom:16px;">
        You have PMF.<br>Now build the motion.
    </h1>
    <p style="color:#94A3B8; font-size:17px;
       max-width:540px; margin:0 auto 32px auto;">
        Describe your company. Get a GTM plan
        grounded in your numbers — in 60 seconds.
    </p>
</div>
""",
        unsafe_allow_html=True,
    )

    founder_text = st.text_input(
        "",
        placeholder="https://acme.com · 2022 · ACV $18K · "
                    "60-day cycle · $1.2M ARR · Founder-led",
        label_visibility="collapsed"
    )

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("ANTHROPIC_API_KEY not set. Add it to your .env file and restart.")
        st.stop()
    client = anthropic.Anthropic(api_key=api_key)
    model_id = "claude-haiku-4-5-20251001"

    button_clicked = st.button("Build GTM", type="primary")

    if button_clicked and founder_text:
        # Step 1: extract URL from input
        url_match = re.search(r'https?://[^\s·,]+', founder_text)
        url = url_match.group() if url_match else ""

        # Step 2: scrape the URL
        with st.spinner("Reading your website..."):
            homepage = scraper.scrape_url(url)

        # Step 3: run AI on founder text + homepage
        with st.spinner("Analyzing with AI..."):
            profile, error = scraper.extract_profile(founder_text, homepage, client, model=model_id)

        if error:
            st.error(f"AI error: {error}")
        else:
            st.session_state['profile'] = profile

    if 'profile' in st.session_state:
        profile = st.session_state.get('profile', {}) or {}

        def display_text(value):
            if value is None:
                return "—"
            text = str(value).strip()
            return text if text else "—"

        def display_int(value):
            if isinstance(value, int):
                return value
            if isinstance(value, str):
                cleaned = value.replace(",", "").strip()
                if cleaned.isdigit():
                    return int(cleaned)
            return None

        vertical = display_text(profile.get('vertical'))
        sub_vertical = display_text(profile.get('sub_vertical'))
        company_name = display_text(profile.get('company_name'))
        overview = display_text(profile.get('overview'))
        problem = display_text(profile.get('problem'))
        solution = display_text(profile.get('solution'))

        vertical_safe = escape(vertical)
        sub_vertical_safe = escape(sub_vertical)
        company_name_safe = escape(company_name)
        overview_safe = escape(overview)
        problem_safe = escape(problem)
        solution_safe = escape(solution)

        founding_year = display_int(profile.get('founding_year'))
        acv = display_int(profile.get('acv'))
        sales_cycle_days = display_int(profile.get('sales_cycle_days'))
        arr = display_int(profile.get('arr'))
        sales_motion = display_text(profile.get('sales_motion'))

        metrics = [
            ("Founded", str(founding_year) if founding_year is not None else "—"),
            (
                "Average Deal Size (ACV)",
                f"${acv:,}" if acv is not None else "—",
            ),
            (
                "Sales Cycle Length",
                f"{sales_cycle_days} days" if sales_cycle_days is not None else "—",
            ),
            (
                "Annual Recurring Revenue (ARR)",
                f"${arr:,}" if arr is not None else "—",
            ),
            ("Sales Approach", sales_motion),
            ("Industry", vertical),
        ]

        metric_blocks = ""
        for label, value in metrics:
            safe_label = escape(label)
            safe_value = escape(value)
            metric_blocks += f"""
    <div style=\"margin-bottom:14px;\">
        <div style=\"color:#64748B; font-size:10px;
             font-weight:700; text-transform:uppercase;
             letter-spacing:0.08em;\">
            {safe_label}
        </div>
        <div style=\"color:#F9FAFB; font-size:15px;
             font-weight:600; margin-top:3px;\">
            {safe_value}
        </div>
    </div>
"""

        st.markdown("---")
        st.markdown("#### Company Profile")

        left_col, right_col = st.columns([2, 1])

        with left_col:
            components.html(
                f"""
<div style="background:#111827; border:1px solid #1E2D40;
     border-radius:10px; padding:24px; height:100%;">

    <div style="color:#D4A843; font-size:11px;
         font-weight:700; letter-spacing:0.1em;
         text-transform:uppercase; margin-bottom:8px;">
        {vertical_safe} · {sub_vertical_safe}
    </div>

    <div style="font-size:22px; font-weight:700;
         color:#F9FAFB; margin-bottom:12px;">
        {company_name_safe}
    </div>

    <div style="color:#64748B; font-size:10px;
         font-weight:700; text-transform:uppercase;
         letter-spacing:0.1em; margin-bottom:6px;">
        What this company does
    </div>

    <div style="color:#94A3B8; font-size:14px;
         line-height:1.7; margin-bottom:20px;">
        {overview_safe}
    </div>

    <div style="display:grid;
         grid-template-columns:1fr 1fr; gap:16px;">
        <div>
            <div style="color:#64748B; font-size:10px;
                 font-weight:700; text-transform:uppercase;
                 letter-spacing:0.1em; margin-bottom:6px;">
                Main customer problem
            </div>
            <div style="color:#F9FAFB; font-size:13px;
                 line-height:1.6;">
                {problem_safe}
            </div>
        </div>
        <div>
            <div style="color:#64748B; font-size:10px;
                 font-weight:700; text-transform:uppercase;
                 letter-spacing:0.1em; margin-bottom:6px;">
                How they solve it
            </div>
            <div style="color:#F9FAFB; font-size:13px;
                 line-height:1.6;">
                {solution_safe}
            </div>
        </div>
    </div>
</div>
""",
                height=420,
                scrolling=False,
            )

        with right_col:
            components.html(
                f"""
<div style="background:#111827; border:1px solid #1E2D40;
     border-radius:10px; padding:24px; height:100%;">

    <div style="color:#D4A843; font-size:11px;
         font-weight:700; letter-spacing:0.1em;
         text-transform:uppercase; margin-bottom:16px;">
        Business Snapshot
    </div>

    {metric_blocks}
</div>
""",
                height=420,
                scrolling=False,
            )

        # --- Market Signals ---
        signal_list = signals.get_signals(
            profile.get("vertical", ""),
            profile.get("sub_vertical", ""),
        )

        st.markdown("---")
        st.markdown("#### 📡 Market Signals")
        st.caption(
            f"Live intelligence — "
            f"{profile.get('vertical', 'B2B SaaS')} vertical"
        )

        placeholder = st.empty()
        rendered_html = ""

        for s in signal_list:
            rendered_html += f"""
        <div style="background:#111827;
             border:1px solid #1E2D40;
             border-radius:8px;
             padding:10px 14px;
             margin-bottom:8px;">
            <div style="font-size:11px;
                 color:#64748B; margin-bottom:3px;">
                {s[0]} <b>{s[1]}</b> · {s[2]}
            </div>
            <div style="font-size:13px;
                 color:#F9FAFB; line-height:1.5;">
                {s[3]}
            </div>
        </div>"""
            placeholder.markdown(rendered_html, unsafe_allow_html=True)
            time.sleep(0.3)

        st.success(
            f"✅ {len(signal_list)} signals collected"
            f" · {profile.get('vertical', 'B2B SaaS')} vertical detected"
        )

        st.session_state['signals'] = signal_list

        # --- Benchmarking ---
        st.markdown("---")
        with st.status(
            "📊 Benchmarking your metrics...",
            expanded=False
        ) as status:
            bench = benchmarking.run(profile, client)
            st.session_state['benchmarking'] = bench
            status.update(
                label="✅ Benchmarking complete",
                state="complete"
            )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
<div style="background:#3D3B8E;
     border-radius:10px; overflow:hidden;">
    <div style="padding:14px 16px;
         font-weight:700; color:#fff;
         font-size:14px;">
        Vertical + Stage peers
    </div>
    <div style="background:#EEEEF8;
         padding:16px; color:#1a1a2e;
         font-size:13px; line-height:1.8;
         min-height:220px;">
        Compares against companies in the same
        vertical and revenue band.<br><br>
        · ACV vs. vertical median<br>
        · Sales cycle vs. stage peers<br>
        · Revenue growth rate vs. cohort<br>
        · Deal volume efficiency
    </div>
</div>""", unsafe_allow_html=True)

        with col2:
            overall = bench.get('overall_percentile', 0)
            biggest = bench.get('biggest_gap', 'N/A')
            st.markdown(f"""
<div style="background:#1E7A5E;
     border-radius:10px; overflow:hidden;">
    <div style="padding:14px 16px;
         font-weight:700; color:#fff;
         font-size:14px;">
        Percentile ranking
    </div>
    <div style="background:#E8F5F0;
         padding:16px; color:#1a1a2e;
         font-size:13px; line-height:1.8;
         min-height:220px;">
        Overall GTM health score:
        <b>{overall}th percentile</b><br><br>
        · You are in the {overall}th percentile<br>
        · Per-metric breakdown below<br>
        · Biggest gap: {biggest}<br>
        · See scorecard for next tier targets
    </div>
</div>""", unsafe_allow_html=True)

        with col3:
            acv_tq = bench.get('acv_top_quartile', 0)
            cycle_tq = bench.get('cycle_top_quartile_days', 0)
            lever = bench.get('highest_leverage_lever', '')
            acv_val = profile.get('acv', 0) or 0
            st.markdown(f"""
<div style="background:#8B2500;
     border-radius:10px; overflow:hidden;">
    <div style="padding:14px 16px;
         font-weight:700; color:#fff;
         font-size:14px;">
        Top quartile gap analysis
    </div>
    <div style="background:#F9EDE8;
         padding:16px; color:#1a1a2e;
         font-size:13px; line-height:1.8;
         min-height:220px;">
        · Top quartile ACV:
          ${acv_tq:,} vs your ${acv_val:,}<br>
        · Cycle target: {cycle_tq} days<br>
        · Highest leverage: {lever}<br>
        · See full gap map below
    </div>
</div>""", unsafe_allow_html=True)

        # Scorecard pills
        st.markdown("<br>", unsafe_allow_html=True)
        st.caption(
            "SCORECARD LAYER — overlaid across all three lenses"
        )

        metrics = [
            ("ACV",          bench.get('acv_percentile', 0)),
            ("Sales Cycle",  bench.get('cycle_percentile', 0)),
            ("Revenue Eff.", bench.get('revenue_efficiency_percentile', 0)),
            ("GTM Motion",   bench.get('gtm_motion_percentile', 0)),
            ("Deal Velocity",bench.get('deal_velocity_percentile', 0)),
            ("Overall",      bench.get('overall_percentile', 0)),
        ]

        def pill_style(p: int) -> tuple:
            if p >= 67:
                return "#E8F5F0", "#1E7A5E", f"Top {100 - p}%"
            elif p >= 34:
                return "#FFF8E8", "#B8920E", f"{p}th %ile"
            else:
                return "#FDECEA", "#C0392B", f"Bottom {p}%"

        pill_cols = st.columns(6)
        for col, (label, pct) in zip(pill_cols, metrics):
            bg, color, display = pill_style(pct)
            col.markdown(f"""
<div style="background:{bg};
     border-radius:8px; padding:12px 14px;">
    <div style="font-size:12px;
         font-weight:700; color:#1a1a2e;">
        {label}
    </div>
    <div style="font-size:13px;
         font-weight:600; color:{color};
         margin-top:4px;">
        {display}
    </div>
</div>""", unsafe_allow_html=True)

        # --- ICP ---
        st.markdown("---")
        with st.status(
            "🎯 Profiling your ICP...",
            expanded=False
        ) as status:
            icp_data = icp.run(profile, signal_list, client)
            st.session_state['icp'] = icp_data
            status.update(
                label="✅ ICP complete",
                state="complete"
            )

        st.markdown("#### 🎯 Your ICP")

        icp_fields = [
            ("Company Profile",  icp_data.get('company_profile', '—')),
            ("Economic Buyer",   icp_data.get('buyer_title',     '—')),
            ("Champion",         icp_data.get('champion_title',  '—')),
            ("Trigger Event",    icp_data.get('trigger_event',   '—')),
            ("Who to Avoid",     icp_data.get('negative_icp',    '—')),
        ]

        for icp_label, icp_value in icp_fields:
            st.markdown(f"""
<div style="background:#111827;
     border:1px solid #1E2D40;
     border-radius:10px; padding:20px;
     margin-bottom:12px;">
    <div style="color:#D4A843; font-size:10px;
         font-weight:700; text-transform:uppercase;
         letter-spacing:0.1em; margin-bottom:6px;">
        {escape(icp_label)}
    </div>
    <div style="color:#F9FAFB; font-size:14px;
         line-height:1.6;">
        {escape(str(icp_value))}
    </div>
</div>""", unsafe_allow_html=True)

        # --- Positioning ---
        st.markdown("---")
        with st.status(
            "⚡ Building positioning...",
            expanded=False
        ) as status:
            pos = positioning.run(profile, signal_list, client)
            st.session_state['positioning'] = pos
            status.update(
                label="✅ Positioning complete",
                state="complete"
            )

        st.markdown("#### ⚡ Positioning")

        components.html(f"""
<div style="background:#111827;
     border:1px solid #1E2D40;
     border-radius:10px; padding:24px;
     font-family:'Inter',sans-serif;">

    <div style="color:#D4A843; font-size:10px;
         font-weight:700; text-transform:uppercase;
         letter-spacing:0.1em; margin-bottom:8px;">
        Wedge
    </div>
    <div style="color:#F9FAFB; font-size:17px;
         font-weight:600; line-height:1.5;
         margin-bottom:20px;">
        {escape(str(pos.get('wedge', '—')))}
    </div>

    <div style="color:#D4A843; font-size:10px;
         font-weight:700; text-transform:uppercase;
         letter-spacing:0.1em; margin-bottom:8px;">
        ROI
    </div>
    <div style="color:#94A3B8; font-size:14px;
         line-height:1.6; margin-bottom:20px;">
        {escape(str(pos.get('roi', '—')))}
    </div>

    <div style="height:1px; background:#1E2D40;
         margin-bottom:20px;"></div>

    <div style="color:#C0392B; font-size:10px;
         font-weight:700; text-transform:uppercase;
         letter-spacing:0.1em; margin-bottom:6px;">
        Top Objection
    </div>
    <div style="color:#F9FAFB; font-size:14px;
         margin-bottom:12px;">
        {escape(str(pos.get('objection', '—')))}
    </div>

    <div style="color:#1E7A5E; font-size:10px;
         font-weight:700; text-transform:uppercase;
         letter-spacing:0.1em; margin-bottom:6px;">
        Response
    </div>
    <div style="color:#94A3B8; font-size:14px;">
        {escape(str(pos.get('objection_response', '—')))}
    </div>

</div>""", height=320, scrolling=False)

        # --- Distribution ---
        st.markdown("---")
        with st.status(
            "🚀 Designing distribution engines...",
            expanded=False
        ) as status:
            dist = distribution.run(profile, signal_list, client)
            st.session_state['distribution'] = dist
            status.update(
                label="✅ Distribution complete",
                state="complete"
            )

        st.markdown("#### 🚀 Distribution Engines")

        dist_col1, dist_col2, dist_col3 = st.columns(3)
        engines = [
            dist.get('engine_1', {}),
            dist.get('engine_2', {}),
            dist.get('engine_3', {}),
        ]

        for col, engine in zip([dist_col1, dist_col2, dist_col3], engines):
            col.markdown(f"""
<div style="background:#111827;
     border:1px solid #1E2D40;
     border-radius:10px; padding:20px;
     height:100%;">
    <div style="color:#D4A843; font-size:14px;
         font-weight:700; margin-bottom:10px;">
        {escape(str(engine.get('channel', '—')))}
    </div>
    <div style="color:#94A3B8; font-size:13px;
         line-height:1.6; margin-bottom:14px;">
        {escape(str(engine.get('rationale', '—')))}
    </div>
    <div style="color:#F9FAFB; font-size:13px;
         line-height:1.6;">
        → {escape(str(engine.get('action', '—')))}
    </div>
</div>""", unsafe_allow_html=True)

        # --- Actions ---
        st.markdown("---")
        with st.status(
            "📅 Building execution plan...",
            expanded=False
        ) as status:
            act = actions.run(profile, signal_list, client)
            st.session_state['actions'] = act
            status.update(
                label="✅ Execution plan complete",
                state="complete"
            )

        st.markdown("#### 📅 Execution Plan")

        act_col1, act_col2 = st.columns(2)

        with act_col1:
            st.markdown("**✅ This Week**")
            for key in ['action_1', 'action_2', 'action_3']:
                val = escape(str(act.get(key, '—')))
                st.markdown(f"""
<div style="background:#111827;
     border:1px solid #1E2D40;
     border-radius:8px;
     padding:14px 16px;
     margin-bottom:10px;
     display:flex; gap:12px;
     align-items:flex-start;">
    <span style="color:#D4A843;
          font-weight:700;
          font-size:16px;">✓</span>
    <span style="color:#F9FAFB;
          font-size:14px;
          line-height:1.6;">
        {val}
    </span>
</div>""", unsafe_allow_html=True)

        with act_col2:
            st.markdown("**📅 90-Day Milestones**")
            milestones = [
                ("Day 30", act.get('day_30', '—')),
                ("Day 60", act.get('day_60', '—')),
                ("Day 90", act.get('day_90', '—')),
            ]
            for day, milestone in milestones:
                st.markdown(f"""
<div style="display:flex; gap:16px;
     align-items:flex-start;
     margin-bottom:16px;">
    <div style="display:flex;
         flex-direction:column;
         align-items:center;">
        <div style="background:#D4A843;
             color:#0B0F1A;
             font-size:11px;
             font-weight:700;
             padding:4px 8px;
             border-radius:4px;
             white-space:nowrap;">
            {escape(day)}
        </div>
        <div style="width:2px;
             background:#1E2D40;
             flex:1; margin-top:6px;
             min-height:30px;">
        </div>
    </div>
    <div style="color:#F9FAFB;
         font-size:14px;
         line-height:1.6;
         padding-top:4px;">
        {escape(str(milestone))}
    </div>
</div>""", unsafe_allow_html=True)

        # --- Download ---
        profile_data = st.session_state.get('profile', {})
        bench_data   = st.session_state.get('benchmarking', {})
        icp_d        = st.session_state.get('icp', {})
        pos_data     = st.session_state.get('positioning', {})
        dist_data    = st.session_state.get('distribution', {})
        act_data     = st.session_state.get('actions', {})

        arr_val = profile_data.get('arr', 0) or 0
        acv_dl  = profile_data.get('acv', 0) or 0

        full_output = f"""GROWTH GOALED — GTM SNAPSHOT
{profile_data.get('company_name', '')}
Generated: {time.strftime('%Y-%m-%d')}

COMPANY PROFILE
Overview: {profile_data.get('overview', '')}
Problem: {profile_data.get('problem', '')}
Solution: {profile_data.get('solution', '')}
Vertical: {profile_data.get('vertical', '')}
Founded: {profile_data.get('founding_year', '')}
ARR: ${arr_val:,}
ACV: ${acv_dl:,}
Sales Cycle: {profile_data.get('sales_cycle_days', '')} days
Motion: {profile_data.get('sales_motion', '')}

BENCHMARKING
Overall Percentile: {bench_data.get('overall_percentile', '')}
Biggest Gap: {bench_data.get('biggest_gap', '')}
Highest Leverage: {bench_data.get('highest_leverage_lever', '')}

ICP
{icp_d.get('company_profile', '')}
Buyer: {icp_d.get('buyer_title', '')}
Champion: {icp_d.get('champion_title', '')}
Trigger: {icp_d.get('trigger_event', '')}
Avoid: {icp_d.get('negative_icp', '')}

POSITIONING
Wedge: {pos_data.get('wedge', '')}
ROI: {pos_data.get('roi', '')}
Objection: {pos_data.get('objection', '')}
Response: {pos_data.get('objection_response', '')}

DISTRIBUTION
Engine 1: {dist_data.get('engine_1', {}).get('channel', '')}
{dist_data.get('engine_1', {}).get('action', '')}
Engine 2: {dist_data.get('engine_2', {}).get('channel', '')}
{dist_data.get('engine_2', {}).get('action', '')}
Engine 3: {dist_data.get('engine_3', {}).get('channel', '')}
{dist_data.get('engine_3', {}).get('action', '')}

EXECUTION
This week:
1. {act_data.get('action_1', '')}
2. {act_data.get('action_2', '')}
3. {act_data.get('action_3', '')}
Day 30: {act_data.get('day_30', '')}
Day 60: {act_data.get('day_60', '')}
Day 90: {act_data.get('day_90', '')}
"""

        st.markdown("---")
        company_slug = (
            profile_data.get('company_name', 'company')
            .lower()
            .replace(' ', '_')
        )
        st.download_button(
            label="⬇ Download GTM Snapshot",
            data=full_output,
            file_name=f"gtm_snapshot_{company_slug}.txt",
            mime="text/plain",
            use_container_width=True,
        )


if __name__ == "__main__":
    main()

# https://www.getauctor.com/ · 2023 · ACV $24K · 45-day cycle · $1.2M ARR · Outbound
