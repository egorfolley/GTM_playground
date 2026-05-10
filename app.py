from __future__ import annotations

import streamlit as st

from growth_goaled.diagnostics import company_payload, run_claude_diagnostic
from growth_goaled.logging_utils import log_step
from growth_goaled.mock_data import get_mock_company, get_mock_market_data
from growth_goaled.scoring import calculate_pillar_scores
from growth_goaled.styles import inject_css
from growth_goaled.ui import (
    render_home,
    render_logic_page,
    render_roadmap,
    render_sidebar,
    render_snapshot,
)


def main() -> None:
    log_step("APP | Streamlit rerun started")
    st.set_page_config(
        page_title="Growth Goaled Snapshot",
        page_icon="GG",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_css()

    company = get_mock_company()
    market_data = get_mock_market_data()
    scores = calculate_pillar_scores(company)
    payload = company_payload(company, scores, market_data)

    if "page" not in st.session_state:
        st.session_state.page = "Home"
    if "snapshot_has_run" not in st.session_state:
        st.session_state.snapshot_has_run = False

    log_step(
        "APP | Session state",
        {
            "page": st.session_state.page,
            "snapshot_has_run": st.session_state.snapshot_has_run,
        },
    )
    render_sidebar(company, market_data)

    diagnostic = None
    if st.session_state.snapshot_has_run:
        log_step("APP | Requesting diagnostic output; may return cached result")
        diagnostic = run_claude_diagnostic(payload)

    if st.session_state.page == "Home":
        render_home(company)
    elif st.session_state.page == "Analysis":
        if diagnostic is None:
            st.session_state.snapshot_has_run = True
            log_step("APP | Analysis requested before demo run; generating diagnostic")
            diagnostic = run_claude_diagnostic(payload)
        render_snapshot(company, diagnostic)
    elif st.session_state.page == "90-Day Execution Roadmap":
        if diagnostic is None:
            st.session_state.snapshot_has_run = True
            log_step("APP | Roadmap requested before demo run; generating diagnostic")
            diagnostic = run_claude_diagnostic(payload)
        render_roadmap(company, diagnostic)
    else:
        if diagnostic is None:
            st.session_state.snapshot_has_run = True
            log_step("APP | How It Works requested before demo run; generating diagnostic")
            diagnostic = run_claude_diagnostic(payload)
        render_logic_page(company, market_data, scores, diagnostic)

    log_step("APP | Streamlit rerun finished")


if __name__ == "__main__":
    main()
