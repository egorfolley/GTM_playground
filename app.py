import streamlit as st
import anthropic
import os
import re
import json
import time
from dotenv import load_dotenv
from agents import scraper, signals, benchmarking, icp, positioning, distribution, actions

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def main():
    st.set_page_config(
        page_title="Growth Goaled",
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

    st.button("Build My GTM Snapshot →", type="primary")

if __name__ == "__main__":
    main()
