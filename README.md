# Growth Goaled — $1M to $10M GTM Copilot

Fintech B2B SaaS · Payments vertical

A Streamlit app that takes a founder's plain-language GTM situation and runs a 5-agent pipeline to produce a focused execution plan for Fintech Payments.

---

## How It Works

1. **Founder input**
Single text area. The founder describes their situation in plain language and clicks **Build My GTM Plan**.

2. **Signal feed UI**
Hardcoded Fintech Payments signals are loaded from [app/signals.py](app/signals.py), shown as feed cards (with source/time/engagement), plus market context pills.

3. **5 specialist agents in parallel**
Executed with `concurrent.futures.ThreadPoolExecutor`:
- Market Intelligence
- ICP Profiler
- Channel Strategist
- Sales Playbook
- Metrics & Forecaster

4. **One synthesizer call**
After all 5 complete, a single Claude call (`claude-sonnet-4-20250514`, `temperature=0.2`) combines the founder text + agent outputs into one GTM plan.

5. **Output + trace**
The plan is shown as markdown, then code view, and can be downloaded as `gtm_plan.txt`. A step-by-step execution trace is shown below.

6. **Always-visible footer**
Three summary columns explain the system design: specialist agents, fintech signals, and free-text-first input.

---

## Project structure

```
app.py                  # Streamlit UI — single entry point
app/
  __init__.py
  market_intelligence.py
  icp_profiler.py
  channel_strategist.py
  sales_playbook.py
  metrics_forecaster.py
  synthesizer.py
  signals.py            # collect_signals() — cached mock signal feed data
requirements.txt
.env                    # ANTHROPIC_API_KEY
```

## Running

```bash
source .venv/bin/activate
streamlit run app.py
```

Requires `ANTHROPIC_API_KEY` in `.env`.

## Notes

- Signal data is mocked and deterministic (no scraping).
- The app uses one free-text input instead of dropdown-driven use cases.
