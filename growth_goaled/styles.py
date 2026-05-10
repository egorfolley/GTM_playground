from __future__ import annotations

import streamlit as st


def inject_css() -> None:
    st.markdown(
        """
        <style>
        :root {
            --gg-bg: #000000;
            --gg-panel: #06132E;
            --gg-panel-2: #0A1F4D;
            --gg-cyan: #42D9FF;
            --gg-blue: #1677FF;
            --gg-green: #66B3FF;
            --gg-pink: #8A7DFF;
            --gg-yellow: #B8D8FF;
            --gg-ink: #F8FAFC;
            --gg-muted: #A9C7FF;
            --gg-border: #1D4ED8;
        }
        .stApp {
            background:
                linear-gradient(180deg, rgba(22,119,255,0.16), transparent 320px),
                var(--gg-bg);
            color: var(--gg-ink);
        }
        [data-testid="stSidebar"] {
            background: #020817;
            border-right: 1px solid var(--gg-border);
        }
        [data-testid="stSidebar"] * {
            color: var(--gg-ink);
        }
        h1, h2, h3, h4, h5, h6, p, label, span, div {
            color: var(--gg-ink);
        }
        [data-testid="stCaptionContainer"],
        [data-testid="stCaptionContainer"] * {
            color: var(--gg-muted);
        }
        [data-testid="stMetric"] {
            background: var(--gg-panel);
            border: 1px solid var(--gg-border);
            border-radius: 8px;
            padding: 1rem;
            box-shadow: 0 0 30px rgba(22, 119, 255, 0.22);
        }
        [data-testid="stMetricLabel"],
        [data-testid="stMetricLabel"] * {
            color: var(--gg-muted);
        }
        [data-testid="stMetricValue"],
        [data-testid="stMetricValue"] * {
            color: var(--gg-cyan);
        }
        .stAlert {
            background: rgba(22, 119, 255, 0.16);
            border: 1px solid rgba(66, 217, 255, 0.42);
            color: var(--gg-ink);
        }
        .hero {
            padding: 4.5rem 3.5rem;
            background:
                linear-gradient(135deg, rgba(22,119,255,0.95), rgba(66,217,255,0.32) 48%, rgba(10,31,77,0.88)),
                #020817;
            color: white;
            border: 1px solid rgba(66,217,255,0.55);
            border-radius: 8px;
            margin-bottom: 1.25rem;
            min-height: 430px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            box-shadow: 0 0 70px rgba(22, 119, 255, 0.35);
        }
        .hero h1 {
            font-size: clamp(2rem, 3.8vw, 3.7rem);
            line-height: 1.02;
            letter-spacing: 0;
            margin: 0 0 1rem 0;
            max-width: 860px;
        }
        .hero p {
            font-size: 1.25rem;
            line-height: 1.55;
            max-width: 780px;
            margin-bottom: 0;
            color: rgba(248,250,252,0.90);
        }
        .section-title {
            color: var(--gg-ink);
            font-size: 1.15rem;
            font-weight: 750;
            margin: 1.2rem 0 0.75rem 0;
        }
        .explainer-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 1rem;
            margin: 1rem 0 1.25rem 0;
        }
        .explainer-card {
            background: linear-gradient(180deg, rgba(10,31,77,0.98), rgba(6,19,46,0.98));
            border: 1px solid var(--gg-border);
            border-radius: 8px;
            padding: 1rem 1.1rem;
            box-shadow: 0 0 28px rgba(22, 119, 255, 0.18);
            min-height: 150px;
        }
        .explainer-card strong {
            color: var(--gg-cyan);
            display: block;
            font-size: 1rem;
            margin-bottom: 0.45rem;
        }
        .explainer-card p {
            color: var(--gg-muted);
            line-height: 1.45;
            margin: 0;
            font-size: 0.95rem;
        }
        .context-panel {
            background: rgba(22, 119, 255, 0.14);
            border: 1px solid rgba(66, 217, 255, 0.36);
            border-radius: 8px;
            padding: 1rem 1.15rem;
            margin: 0.8rem 0 1.1rem 0;
        }
        .context-panel h3 {
            color: var(--gg-cyan);
            font-size: 1.05rem;
            margin: 0 0 0.45rem 0;
        }
        .context-panel p {
            color: var(--gg-ink);
            margin: 0;
            line-height: 1.5;
        }
        .metric-card {
            background: linear-gradient(180deg, rgba(10,31,77,0.98), rgba(6,19,46,0.98));
            border: 1px solid var(--gg-border);
            border-radius: 8px;
            padding: 1.1rem 1.15rem;
            min-height: 145px;
            box-shadow: 0 0 34px rgba(22, 119, 255, 0.22);
        }
        .metric-label {
            color: var(--gg-muted);
            font-size: 0.86rem;
            font-weight: 650;
            text-transform: uppercase;
            letter-spacing: 0;
        }
        .metric-value {
            font-size: 2.5rem;
            line-height: 1;
            font-weight: 850;
            margin: 0.55rem 0 0.5rem 0;
        }
        .metric-note {
            color: var(--gg-muted);
            font-size: 0.93rem;
            line-height: 1.35;
        }
        .insight {
            background: var(--gg-panel);
            border-left: 4px solid var(--gg-cyan);
            border-radius: 8px;
            padding: 0.9rem 1rem;
            margin-bottom: 0.7rem;
            box-shadow: 0 0 26px rgba(66, 217, 255, 0.18);
        }
        .fix {
            background: var(--gg-panel);
            border: 1px solid var(--gg-border);
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 0.75rem;
        }
        .fix strong {
            color: var(--gg-cyan);
        }
        .signal {
            background: rgba(22, 119, 255, 0.18);
            border: 1px solid rgba(66, 217, 255, 0.45);
            border-radius: 8px;
            padding: 0.8rem;
            margin-bottom: 0.6rem;
            color: var(--gg-ink);
            font-size: 0.94rem;
        }
        .roadmap {
            background: var(--gg-panel);
            border: 1px solid var(--gg-border);
            border-radius: 8px;
            padding: 1rem 1.15rem;
            min-height: 220px;
            box-shadow: 0 0 34px rgba(22, 119, 255, 0.20);
        }
        .roadmap-window {
            color: var(--gg-green);
            font-weight: 800;
            font-size: 0.92rem;
            text-transform: uppercase;
            letter-spacing: 0;
        }
        .roadmap h3 {
            margin: 0.35rem 0 0.6rem 0;
            font-size: 1.25rem;
            color: var(--gg-ink);
        }
        .small-muted {
            color: var(--gg-muted);
            font-size: 0.9rem;
        }
        .check-row {
            display: flex;
            gap: 0.65rem;
            align-items: flex-start;
            background: var(--gg-panel);
            border: 1px solid var(--gg-border);
            border-radius: 8px;
            padding: 0.8rem 0.9rem;
            margin-bottom: 0.65rem;
            line-height: 1.35;
        }
        .check-mark {
            color: var(--gg-cyan);
            font-weight: 900;
        }
        div.stButton > button,
        div.stDownloadButton > button {
            background: linear-gradient(135deg, var(--gg-cyan), var(--gg-blue));
            color: #020617;
            border: 1px solid rgba(66, 217, 255, 0.85);
            border-radius: 8px;
            min-height: 3rem;
            font-weight: 750;
        }
        div.stButton > button:hover,
        div.stDownloadButton > button:hover {
            background: linear-gradient(135deg, #8BE8FF, #4B9DFF);
            color: #020617;
            border-color: var(--gg-cyan);
        }
        .stCodeBlock,
        .stCodeBlock pre {
            background: #020817;
            border: 1px solid var(--gg-border);
            color: var(--gg-cyan);
        }
        @media (max-width: 900px) {
            .explainer-grid {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
