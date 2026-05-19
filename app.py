"""
Growth Goaled — $1M to $10M GTM Copilot
Fintech B2B SaaS · Payments vertical
"""
import time
import concurrent.futures
import os
import re

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


def _keyword_set(text: str) -> set:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def _compute_source_importance(founder_text: str, signals: dict) -> list:
    """Score each news source using baseline credibility + query relevance."""
    base_weight = {
        "Hacker News": 1.0,
        "Reddit r/fintech": 0.9,
        "Reddit r/startups": 0.8,
        "Reddit r/SaaS": 0.8,
        "TechCrunch": 1.1,
        "Crunchbase News": 1.05,
    }

    founder_tokens = _keyword_set(founder_text)
    by_source = {}

    for item in signals.get("sources", []):
        source = item.get("source", "Unknown")
        title_tokens = _keyword_set(item.get("title", ""))
        overlap = len(founder_tokens & title_tokens)
        score = base_weight.get(source, 0.85) + (0.15 * overlap)

        if source not in by_source:
            by_source[source] = {
                "source": source,
                "score": 0.0,
                "signal_count": 0,
                "max_overlap": 0,
            }
        by_source[source]["score"] += score
        by_source[source]["signal_count"] += 1
        by_source[source]["max_overlap"] = max(by_source[source]["max_overlap"], overlap)

    total_score = sum(v["score"] for v in by_source.values()) or 1.0
    ranked = sorted(by_source.values(), key=lambda x: x["score"], reverse=True)

    for item in ranked:
        item["importance_pct"] = round((item["score"] / total_score) * 100, 1)
        if item["max_overlap"] >= 3:
            rationale = "high keyword match to founder request"
        elif item["max_overlap"] >= 1:
            rationale = "some keyword overlap with founder request"
        else:
            rationale = "baseline market context coverage"
        item["rationale"] = rationale

    return ranked


# ── UI ────────────────────────────────────────────────────────────────────────

st.title("AI GTM for Founders")
st.caption("demo version")
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
if st.session_state.form_submitted:
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

st.caption("Hints: include stage/revenue, product, target buyer, current GTM bottleneck, and your goal timeline.")
st.caption("Example: We are a B2B SaaS at $1M ARR selling to payment ops leaders; outbound is not converting and we need to reach $2M ARR in 12 months.")

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
    signals = collect_signals()
    source_importance = _compute_source_importance(candidate_text, signals)

    st.session_state.context = {
        "situation": candidate_text,
        "signals": signals,
        "source_importance": source_importance,
    }
    st.session_state.input_evaluation = None

    # Step 1 — Signal feed appears first, simulates live search
    st.markdown("#### 📡 Step 1: Scanning market signals...")

    signal_placeholder = st.empty()

    import time
    rendered = []

    for item in st.session_state.context["signals"].get("sources", []):
        rendered.append(item)
        lines = []
        for s in rendered:
            lines.append(f"{s.get('icon', '•')} **{s.get('source', 'Unknown')}** · {s.get('time', '')}")
            lines.append(f"- {s.get('title', '')}")
        signal_placeholder.markdown("\n".join(lines))
        time.sleep(0.3)

    signal_count = len(st.session_state.context["signals"].get("sources", []))
    st.success(f"✅ {signal_count} signals collected from Hacker News, Reddit, Crunchbase, TechCrunch")

    st.markdown("#### 📊 Source importance for this request")
    importance_lines = []
    for row in st.session_state.context.get("source_importance", []):
        importance_lines.append(
            f"- **{row['source']}**: {row['importance_pct']}% importance ({row['signal_count']} signals, {row['rationale']})"
        )
    st.markdown("\n".join(importance_lines))
    time.sleep(0.5)

if st.session_state.form_submitted:
    st.divider()
    st.subheader("② Logical Step-by-Step Actions")

    step_3_status = "✅ Done" if st.session_state.agent_outputs else "🔄 Running"
    step_4_status = "✅ Done" if st.session_state.final_plan else "🔄 Running"
    st.markdown(
        "\n".join(
            [
                "1. ✅ Input quality evaluated",
                "2. ✅ Market signals scanned",
                f"3. {step_3_status} Specialist agents executed",
                f"4. {step_4_status} Final GTM plan synthesized",
            ]
        )
    )

    st.markdown("#### 📊 Source importance used in processing")
    importance_lines = []
    for row in st.session_state.context.get("source_importance", []):
        importance_lines.append(
            f"- **{row['source']}**: {row['importance_pct']}% importance ({row['signal_count']} signals, {row['rationale']})"
        )
    if importance_lines:
        st.markdown("\n".join(importance_lines))

    st.divider()

    # ════════════════════════════════════════════════════════════════════════
    # MODULE 3 — Agent pipeline
    # ════════════════════════════════════════════════════════════════════════
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
    if not st.session_state.agent_outputs:
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

    # ════════════════════════════════════════════════════════════════════════
    # MODULE 4 — Synthesizer output
    # ════════════════════════════════════════════════════════════════════════
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

    st.divider()

    # ════════════════════════════════════════════════════════════════════════
    # MODULE 5 — Step-by-step trace
    # ════════════════════════════════════════════════════════════════════════
    st.subheader("⑤ Execution Trace")

    if st.session_state.trace_log:
        with st.expander("View full trace log", expanded=False):
            for line in st.session_state.trace_log:
                st.text(line)
    else:
        st.caption("Trace log will appear here after the pipeline runs.")

    # ════════════════════════════════════════════════════════════════════════
    # FOOTER — visible after processing
    # ════════════════════════════════════════════════════════════════════════
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
