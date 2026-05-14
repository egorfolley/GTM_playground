"""
Growth Goaled — $1M to $10M GTM Copilot
Fintech B2B SaaS · Payments vertical
"""
import time
import concurrent.futures

from dotenv import load_dotenv
load_dotenv()

import streamlit as st

from app.market_intelligence import run_market_intelligence
from app.icp_profiler import run_icp_profiler
from app.channel_strategist import run_channel_strategist
from app.sales_playbook import run_sales_playbook
from app.metrics_forecaster import run_metrics_forecaster
from app.synthesizer import run_synthesizer
from app.signals import collect_signals

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Growth Goaled — GTM Copilot",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Session state defaults ────────────────────────────────────────────────────
if "selected_use_case" not in st.session_state:
    st.session_state.selected_use_case = None
if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False
if "agent_outputs" not in st.session_state:
    st.session_state.agent_outputs = {}
if "final_plan" not in st.session_state:
    st.session_state.final_plan = ""
if "context" not in st.session_state:
    st.session_state.context = {}
if "trace_log" not in st.session_state:
    st.session_state.trace_log = []

# ── Constants ─────────────────────────────────────────────────────────────────
AGENT_DEFINITIONS = [
    ("Market Intelligence", run_market_intelligence),
    ("ICP Profiler", run_icp_profiler),
    ("Channel Strategist", run_channel_strategist),
    ("Sales Playbook", run_sales_playbook),
    ("Metrics & Forecaster", run_metrics_forecaster),
]

def _add_trace(msg: str):
    ts = time.strftime("%H:%M:%S")
    st.session_state.trace_log.append(f"[{ts}] {msg}")


def _run_agents_parallel(use_case: str, context: dict) -> dict:
    """Run all 5 agents concurrently and return name → output dict."""
    results = {}
    _add_trace("Pipeline started")
    _add_trace(f"Situation: {str(context.get('situation', ''))[:120]}…")

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(fn, use_case, context): name
            for name, fn in AGENT_DEFINITIONS
        }
        for future in concurrent.futures.as_completed(futures):
            name = futures[future]
            try:
                result = future.result()
                results[name] = result
                _add_trace(f"Agent '{name}' completed — {len(result.split())} words")
            except Exception as exc:
                results[name] = f"⚠️ Agent error: {exc}"
                _add_trace(f"Agent '{name}' FAILED: {exc}")

    return results


def _run_synthesizer(use_case: str, context: dict, agent_outputs: dict) -> str:
    _add_trace("Synthesizer started — aggregating all agent outputs")
    plan = run_synthesizer(use_case, context, agent_outputs)
    _add_trace(f"Synthesizer completed — {len(plan.split())} words in final plan")
    return plan


# ── UI ────────────────────────────────────────────────────────────────────────

st.title("🚀 Growth Goaled — $1M to $10M GTM Copilot")
st.caption("**Fintech B2B SaaS · Payments vertical** — multi-agent strategy engine")
st.divider()

# ════════════════════════════════════════════════════════════════════════════
# MODULE 1 — Situation input
# ════════════════════════════════════════════════════════════════════════════
st.subheader("① Describe Your Situation")

situation = st.text_area(
    "Describe your situation",
    placeholder=(
        "We're a Fintech B2B SaaS at $1M ARR selling to payments companies. "
        "Founder still closing all deals. ACV $18K. 3 SDRs hired but pipeline "
        "not converting. Trying to hire first AE but not sure if ready."
    ),
    height=120,
)

submitted = st.button("Build My GTM Plan", type="primary", use_container_width=True)

if submitted:
    if not situation.strip():
        st.warning("Please describe your situation before running the pipeline.")
        st.stop()
    st.session_state.selected_use_case = situation.strip()
    st.session_state.form_submitted = True
    st.session_state.agent_outputs = {}
    st.session_state.final_plan = ""
    st.session_state.trace_log = []
    st.session_state.context = {"situation": situation.strip()}

st.divider()

# ════════════════════════════════════════════════════════════════════════════
# MODULE 2 — Signal collection (mock)
# ════════════════════════════════════════════════════════════════════════════
# Signal feed display
st.markdown("#### 📡 Market Signal Feed")
st.caption("Live intelligence collected from across the web")

signals = collect_signals()

# Animate discovery feel with a short spinner
with st.spinner("Scanning Fintech GTM signals..."):
    import time
    time.sleep(1.2)

# Render each signal as a card
for item in signals["sources"]:
    meta = f"{item['icon']} **{item['source']}** · {item['time']}"
    if item["points"]:
        meta += f" · ⬆ {item['points']} points · 💬 {item['comments']} comments"
    st.markdown(
        f"""
        <div style="
            border: 1px solid #1e293b;
            border-radius: 8px;
            padding: 10px 14px;
            margin-bottom: 8px;
            background: #0d1117;
        ">
            <div style="font-size:12px; color:#64748b; margin-bottom:4px;">{meta}</div>
            <div style="font-size:14px; color:#f1f5f9;">{item['title']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Market context pills
st.markdown("**Market context:**")
cols = st.columns(len(signals["market_context"]))
for col, ctx in zip(cols, signals["market_context"]):
    col.info(ctx)

st.divider()

# ════════════════════════════════════════════════════════════════════════════
# MODULE 3 — Agent pipeline
# ════════════════════════════════════════════════════════════════════════════
st.subheader("③ Agent Pipeline")

agent_names = [name for name, _ in AGENT_DEFINITIONS]
agent_cols = st.columns(len(agent_names))

STATUS_IDLE = "⬜ Idle"
STATUS_RUNNING = "🔄 Running"
STATUS_DONE = "✅ Done"
STATUS_ERROR = "❌ Error"

def _agent_status(name: str) -> str:
    if not st.session_state.form_submitted:
        return STATUS_IDLE
    output = st.session_state.agent_outputs.get(name)
    if output is None:
        return STATUS_RUNNING
    if output.startswith("⚠️"):
        return STATUS_ERROR
    return STATUS_DONE

for col, name in zip(agent_cols, agent_names):
    with col:
        st.markdown(f"**{name}**")
        st.caption(_agent_status(name))

# Run agents if form was just submitted and we have no outputs yet
if st.session_state.form_submitted and not st.session_state.agent_outputs:
    with st.spinner("Running 5 agents in parallel via concurrent.futures…"):
        st.session_state.agent_outputs = _run_agents_parallel(
            st.session_state.selected_use_case,
            st.session_state.context,
        )
    # Re-render status badges after completion
    for col, name in zip(agent_cols, agent_names):
        with col:
            st.caption(_agent_status(name))

# Show individual agent output cards
if st.session_state.agent_outputs:
    st.markdown("---")
    tabs = st.tabs(agent_names)
    for tab, name in zip(tabs, agent_names):
        with tab:
            output = st.session_state.agent_outputs.get(name, "")
            st.markdown(output)

st.divider()

# ════════════════════════════════════════════════════════════════════════════
# MODULE 4 — Synthesizer output
# ════════════════════════════════════════════════════════════════════════════
st.subheader("📋 Your GTM Plan")

if st.session_state.agent_outputs and not st.session_state.final_plan:
    with st.spinner("Synthesizer combining all agent outputs…"):
        st.session_state.final_plan = _run_synthesizer(
            st.session_state.selected_use_case,
            st.session_state.context,
            st.session_state.agent_outputs,
        )

if st.session_state.final_plan:
    st.markdown(st.session_state.final_plan)
    st.divider()
    st.code(st.session_state.final_plan)
    st.download_button(
        label="Download Plan",
        data=st.session_state.final_plan,
        file_name="gtm_plan.txt",
        use_container_width=True,
    )
elif not st.session_state.form_submitted:
    st.info("Describe your situation above and click **Build My GTM Plan** to generate your plan.")

st.divider()

# ════════════════════════════════════════════════════════════════════════════
# MODULE 5 — Step-by-step trace
# ════════════════════════════════════════════════════════════════════════════
st.subheader("⑤ Execution Trace")

if st.session_state.trace_log:
    with st.expander("View full trace log", expanded=False):
        for line in st.session_state.trace_log:
            st.text(line)
else:
    st.caption("Trace log will appear here after the pipeline runs.")

# ════════════════════════════════════════════════════════════════════════════
# FOOTER — always visible
# ════════════════════════════════════════════════════════════════════════════
st.divider()
st.caption("How this plan was built")

fc1, fc2, fc3 = st.columns(3)
with fc1:
    st.markdown("**5 specialist agents**")
    st.caption("ICP · Signals · Pain · Positioning · Distribution\nEach reads your words, not a dropdown")
with fc2:
    st.markdown("**Fintech Payments signals**")
    st.caption("Mock market data calibrated for 2025\nPayments buyer behavior and sales cycle norms")
with fc3:
    st.markdown("**One free-text input**")
    st.caption("No forms. No use case selection.\nAgents extract what matters from your description")
