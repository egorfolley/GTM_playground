import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import anthropic
import os
import re
import json
import time
from html import escape
from dotenv import load_dotenv
from agents import scraper, signals, benchmarking, icp, positioning, distribution, actions

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

    model_choice = st.radio(
        "AI model",
        options=["Gemini Flash (Free)", "Claude Haiku 4.5"],
        horizontal=True,
        label_visibility="collapsed",
    )

    if model_choice == "Gemini Flash (Free)":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            st.error("GEMINI_API_KEY not set. Add it to your .env file and restart.")
            st.stop()
        genai.configure(api_key=api_key)
        client = genai.GenerativeModel("gemini-2.0-flash")
        model_id = "gemini-2.0-flash"
    else:
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


if __name__ == "__main__":
    main()

# https://www.getauctor.com/ · 2023 · ACV $24K · 45-day cycle · $1.2M ARR · Outbound