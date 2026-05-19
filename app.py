"""
Growth Goaled — $1M to $10M GTM Copilot
Fintech B2B SaaS · Payments vertical
"""
import time
import concurrent.futures
import os

from dotenv import load_dotenv
load_dotenv()

import streamlit as st

from app.market_intelligence import run_market_intelligence
from app.icp_profiler import run_icp_profiler
from app.channel_strategist import run_channel_strategist
from app.sales_playbook import run_sales_playbook
from app.metrics_forecaster import run_metrics_forecaster
from app.input_evaluator import run_input_evaluator
from app.synthesizer import run_synthesizer
from app.signals import collect_signals
from app.sources import MARKET_SIGNALS


def _resolve_anthropic_api_key() -> str:
    """Resolve Anthropic API key from env first, then Streamlit secrets."""
    api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if api_key:
        return api_key

    try:
        if "ANTHROPIC_API_KEY" in st.secrets:
            api_key = str(st.secrets["ANTHROPIC_API_KEY"]).strip()
        elif "anthropic_api_key" in st.secrets:
            api_key = str(st.secrets["anthropic_api_key"]).strip()
    except Exception:
        api_key = ""

    if api_key:
        os.environ["ANTHROPIC_API_KEY"] = api_key
    return api_key


ANTHROPIC_API_KEY = _resolve_anthropic_api_key()

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
if "input_evaluation" not in st.session_state:
    st.session_state.input_evaluation = None

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


def confidence_label(agent_output: str) -> str:
    """Calculate confidence indicator based on grounding language in agent output."""
    uncertain_phrases = [
        "not specified", "insufficient data", 
        "recommend asking", "unknown"
    ]
    count = sum(1 for p in uncertain_phrases 
                if p in agent_output.lower())
    if count == 0:
        return "🟢 High confidence — grounded in your input"
    elif count <= 2:
        return "🟡 Medium confidence — some gaps in input data"
    else:
        return "🔴 Low confidence — describe your situation in more detail"


# ── UI ────────────────────────────────────────────────────────────────────────

st.title("AI GTM for Founders")
st.caption("demo version")
st.caption("**Fintech B2B SaaS · Payments vertical** — multi-agent strategy engine")
st.divider()

if not ANTHROPIC_API_KEY:
    st.error(
        "Missing ANTHROPIC_API_KEY. On Streamlit Cloud, add it in App Settings → Secrets "
        "as ANTHROPIC_API_KEY = \"...\" and redeploy."
    )
    st.stop()

# ════════════════════════════════════════════════════════════════════════════
# MODULE 1 — Situation input
# ════════════════════════════════════════════════════════════════════════════
st.subheader("① Describe Your Situation")

founder_text = st.text_area(
    "Describe your situation",
    placeholder=(
        "We're a Fintech B2B SaaS at $1M ARR selling to payments companies. "
        "Founder still closing all deals. ACV $18K. 3 SDRs hired but pipeline "
        "not converting. Trying to hire first AE but not sure if ready."
    ),
    height=120,
)

if st.session_state.input_evaluation and not st.session_state.form_submitted:
    evaluation = st.session_state.input_evaluation
    st.warning("Not enough detail to build a reliable GTM plan yet.")
    if evaluation.get("missing"):
        st.caption("Please add:")
        for item in evaluation.get("missing", []):
            st.markdown(f"- {item}")
    st.markdown("**Response format to use**")
    st.code(evaluation.get("response_format", ""), language="text")
    st.markdown("**Quick input template**")
    st.text(evaluation.get("template", ""))

if st.button("Build My GTM Plan"):

    # Input validation
    if len(founder_text.strip()) < 20:
        st.warning("Please describe your situation in at least one sentence.")
        st.stop()

    candidate_text = founder_text.strip()
    evaluation = run_input_evaluator(candidate_text, {"situation": candidate_text})
    st.session_state.input_evaluation = evaluation

    if not evaluation.get("is_sufficient", False):
        st.session_state.form_submitted = False
        st.session_state.agent_outputs = {}
        st.session_state.final_plan = ""
        st.session_state.selected_use_case = None
        st.session_state.context = {}
        st.session_state.trace_log = []
        st.warning("Input is not detailed enough yet. Use the template below and try again.")
        if evaluation.get("reason"):
            st.caption(evaluation.get("reason"))
        st.markdown("**Response format to use**")
        st.code(evaluation.get("response_format", ""), language="text")
        st.markdown("**Quick input template**")
        st.text(evaluation.get("template", ""))
        st.stop()

    st.session_state.selected_use_case = candidate_text
    st.session_state.form_submitted = True
    st.session_state.agent_outputs = {}
    st.session_state.final_plan = ""
    st.session_state.trace_log = []
    st.session_state.context = {"situation": candidate_text}
    st.session_state.input_evaluation = None

    # Step 1 — Signal feed appears first, simulates live search
    st.markdown("#### 📡 Scanning market signals...")

    signal_placeholder = st.empty()

    sources = MARKET_SIGNALS

    import time
    rendered = []

    for icon, source, time_ago, title in sources:
        rendered.append((icon, source, time_ago, title))
        lines = []
        for s in rendered:
            lines.append(f"{s[0]} **{s[1]}** · {s[2]}")
            lines.append(f"- {s[3]}")
        signal_placeholder.markdown("\n".join(lines))
        time.sleep(0.3)

    st.success(f"✅ {len(MARKET_SIGNALS)} signals collected from Hacker News, Reddit, Crunchbase, TechCrunch")
    time.sleep(0.5)

    # Step 2 — Agents run after signals displayed
    signals = collect_signals()

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
            st.caption(confidence_label(output))

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
