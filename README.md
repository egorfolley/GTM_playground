# 🚀 Growth Goaled — $1M to $10M GTM Copilot

**Fintech B2B SaaS · Payments vertical**

A Streamlit app that takes a founder's plain-language GTM situation and runs a **5-agent AI pipeline** to produce a grounded, actionable execution plan.

---

## ✨ Value Proposition

### Problem
- Founders waste hours in generic GTM templates or conversations with advisors who invent details not based on the founder's reality
- GTM plans hallucinate: invented company names, competitor profiles, CAC numbers, and stage-inappropriate recommendations

### Solution
- **Grounded GTM planning**: Each agent only makes claims derived from the founder's input or validated market context
- **Explicit confidence signals**: Red/yellow/green flags showing where data gaps exist
- **5 specialist agents**: Market trends, ICP, channels, sales playbook, metrics — built in parallel for speed
- **One free-text input**: No forms, dropdowns, or templates. Just describe your situation.

### Output
A customized GTM plan with:
- Market signals relevant to this founder's specific stage/vertical
- ICP derived from their described customer profile (not invented)
- 2-3 channel recommendations with realistic effort/CAC estimates
- Sales playbook grounded in their buyer and trigger events
- 90-day metrics model (if data exists) or list of required inputs

---

## 🏗️ Architecture

### Data Flow

```
Founder Input (free text)
    ↓
+ Market Signals (25 calibrated Fintech signals)
    ↓
5 Agents run in parallel:
  • Market Intelligence   → market trends relevant to founder's ARR/buyer
  • ICP Profiler         → ideal customer profile (derived, not invented)
  • Channel Strategist   → 2-3 channels with fit rationale + CAC estimates
  • Sales Playbook       → outbound sequences grounded in founder's trigger events
  • Metrics & Forecaster → 90-day projections (if data exists)
    ↓
Synthesizer aggregates all agent outputs into one GTM Plan
    ↓
UI displays plan + Confidence Indicators (🟢 🟡 🔴)
```

### Core Anti-Hallucination Principle

Every agent follows **STRICT RULES**:
- Only reference founder's input or provided signals
- Mark all observations with source: `[HN]`, `[Reddit]`, `[TC]`
- Use "signals suggest" not "data shows"
- Label claims as "confirmed", "inferred", or "likely"
- If uncertain, ask for data explicitly rather than inventing

---

## 📁 Project Structure

```
Growth_playground/
├── app.py                          # Streamlit UI entry point
├── requirements.txt                # Python dependencies
├── .env                            # ANTHROPIC_API_KEY
└── app/
    ├── __init__.py
    ├── market_intelligence.py      # Agent 1: Market analyst
    ├── icp_profiler.py             # Agent 2: ICP specialist
    ├── channel_strategist.py       # Agent 3: Channel strategy
    ├── sales_playbook.py           # Agent 4: Sales playbook
    ├── metrics_forecaster.py       # Agent 5: GTM metrics
    ├── synthesizer.py              # Aggregates all 5 outputs into final plan
    ├── signals.py                  # collect_signals() helper
    └── sources/
        ├── __init__.py
        └── sources_mockup.py       # 25 calibrated Fintech market signals
```

### Key Files Explained

| File | Purpose |
|------|---------|
| `app.py` | Streamlit UI, session management, concurrent agent execution, confidence labels |
| `market_intelligence.py` | Analyzes signals in context of founder's specific situation |
| `icp_profiler.py` | Builds ICP only from founder input; marks unknown details as "not specified" |
| `channel_strategist.py` | Recommends 2-3 channels; estimates CAC only if derivable |
| `sales_playbook.py` | Creates sequences grounded in trigger events + buyer pain |
| `metrics_forecaster.py` | Builds 90-day model only if ACV + pipeline + win rate provided |
| `synthesizer.py` | Combines all 5 outputs into one cohesive GTM plan |
| `app/sources/sources_mockup.py` | 25 market signals (HN, Reddit, TechCrunch, Crunchbase) |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Anthropic API key (free tier available at https://console.anthropic.com)

### Installation

```bash
# Clone the repository
git clone https://github.com/egorfolley/GTM_playground.git
cd GTM_playground

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
```

### Run

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 💡 How to Use

1. **Describe Your Situation** (required)
   - Be specific: ARR, ACV, buyer title, current sales approach, team size
   - Example: *"We're at $1.2M ARR, ACV $18K, selling to payments companies. Founder closing, 3 SDRs hired but low conversion. First AE hire next month."*

2. **Click "Build My GTM Plan"**
   - Signals feed streams 25 market signals
   - 5 agents run in parallel (~15-20 sec)
   - Each outputs grounded analysis

3. **Review Agent Outputs**
   - Check each agent's tab
   - **Confidence indicator** shows data gaps:
     - 🟢 High confidence (grounded in your input)
     - 🟡 Medium confidence (some gaps)
     - 🔴 Low confidence (need more detail)

4. **Read Final GTM Plan**
   - Synthesized playbook combining all 5 agents
   - Download as `.txt` for offline use

---

## 🎯 What Each Agent Delivers

### 1️⃣ Market Intelligence
- Market signals relevant to your ARR/vertical
- Competitive threats (if applicable)
- Regulatory/macro signals
- All tagged with source: `[HN]`, `[Reddit]`, `[TC]`

**Confidence gap**: "not specified" = signals exist but not relevant to your situation

### 2️⃣ ICP Profiler
- Firmographics derived from your input
- Buyer map (economic buyer, champion, gatekeeper)
- Trigger events (confirmed vs. likely)
- Negative signals (who to avoid)

**Confidence gap**: "not specified — recommend asking your best 3 customers" = validation needed

### 3️⃣ Channel Strategist
- 2-3 recommended channels (max)
- Fit rationale (must cite your input)
- Effort level + first experiment
- CAC estimate (only if derivable from your ACV)

**Confidence gap**: "insufficient data to estimate" = not enough info to calculate

### 4️⃣ Sales Playbook
- Account criteria (3 conditions)
- Outbound sequence (if trigger events found)
- Objection handling
- Wedge messaging grounded in your product

**Confidence gap**: "unknown — ask your last 5 customers" = info needed

### 5️⃣ Metrics & Forecaster
- North Star metric
- Leading indicators
- 90-day model (conservative / base / optimistic)
- Week 1 metrics to start tracking

**Confidence gap**: "only build if you have: ACV, current pipeline, win rate" = lists what's missing

---

## 🔧 Customization

### Add More Market Signals
Edit `app/sources/sources_mockup.py`:
```python
MARKET_SIGNALS = [
    ("🟠", "Hacker News", "2h ago", "Your signal title here"),
    # ... add more
]
```

### Change Agent Models
Each agent uses `claude-opus-4-5` (stable, instruction-following). To use a different model:
```python
# In any agent file (e.g., market_intelligence.py)
message = client.messages.create(
    model="claude-sonnet-4-20250514",  # ← Change here
    max_tokens=600,
    system=SYSTEM_PROMPT,
    messages=[{"role": "user", "content": user_msg}],
)
```

### Adjust Confidence Thresholds
In `app.py`, update `confidence_label()`:
```python
def confidence_label(agent_output: str) -> str:
    uncertain_phrases = [
        "not specified", "insufficient data", 
        "recommend asking", "unknown"
    ]
    count = sum(1 for p in uncertain_phrases 
                if p in agent_output.lower())
    # Adjust the counts to change confidence bands
    if count == 0:
        return "🟢 High confidence — grounded in your input"
    # ...
```

---

## 📊 Example Input & Output

### Input
```
We're a Fintech B2B SaaS at $1M ARR selling to payments companies. 
Founder still closing all deals. ACV $18K. 3 SDRs hired but pipeline 
not converting. Trying to hire first AE but not sure if ready.
```

### Output (Example)
**Market Intelligence**: 
- `[HN]` Founders at $1M ARR report outbound reply rates under 5%...
- `[Reddit]` Compliance buyers in Payments move slow...

**ICP Profiler**:
- Company size: inferred $10-50M based on $18K ACV
- Champion: VP of payments operations (not specified — ask your best 3 customers)
- Trigger events: 2 confirmed, 1 likely

**Channel Strategist**:
- Primary: Outbound to payments company VP titles
- CAC estimate: $3-5K (based on $18K ACV × typical 15-20% close rate)
- Secondary: Niche fintech communities

**Sales Playbook**:
- Outbound sequence grounded in compliance trigger event
- Objections addressed: budget, integration timeline, vendor risk

**Metrics & Forecaster**:
- North Star: Pipeline value (your bottleneck at 3 SDRs)
- 90-day model: Only build if you provide: current pipeline value, current win rate
- Week 1 tracking: 1) SDR reply rate, 2) Discovery-to-demo rate, 3) Win rate

**Confidence**: 🟡 Medium — some gaps in buyer titles and competitor names

---

## 🛠️ Troubleshooting

### "Missing ANTHROPIC_API_KEY"
- Check `.env` file exists in root directory
- Verify format: `ANTHROPIC_API_KEY=sk-ant-...`
- Restart Streamlit: `streamlit run app.py`

### Agent runs very slowly
- Check internet connection
- Verify API key is valid
- See token usage in trace log at bottom

### Agent output is generic
- Provide more specific details in your situation input
- Mention: ARR, ACV, buyer title, current sales motion, team structure
- Less detail = more "not specified" gaps (🔴 Low confidence)

---

## 📚 Learn More

- **Anthropic Claude API**: https://docs.anthropic.com/
- **Streamlit Docs**: https://docs.streamlit.io/
- **Fintech B2B GTM**: https://www.reforge.com/courses/gtm

---

## 📝 License

Open source. Use freely.
