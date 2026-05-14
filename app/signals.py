import streamlit as st


@st.cache_data
def collect_signals() -> dict:
    return {
        "sources": [
            {
                "source": "Hacker News",
                "icon": "🟠",
                "time": "2 hours ago",
                "title": "How I got my first 10 Fintech customers without a sales team",
                "points": 312,
                "comments": 47,
            },
            {
                "source": "Hacker News",
                "icon": "🟠",
                "time": "6 hours ago",
                "title": "Founder-led sales in Payments — what actually works at $1M ARR",
                "points": 218,
                "comments": 33,
            },
            {
                "source": "Hacker News",
                "icon": "🟠",
                "time": "yesterday",
                "title": "Why most early Fintech outbound fails and how to fix it",
                "points": 176,
                "comments": 28,
            },
            {
                "source": "Reddit r/fintech",
                "icon": "🔴",
                "time": "3 hours ago",
                "title": "Cold outbound not converting in Payments vertical — what changed?",
                "points": 94,
                "comments": 61,
            },
            {
                "source": "Reddit r/startups",
                "icon": "🔴",
                "time": "8 hours ago",
                "title": "How do you find ICP signal before hiring your first AE?",
                "points": 187,
                "comments": 43,
            },
            {
                "source": "Reddit r/SaaS",
                "icon": "🔴",
                "time": "yesterday",
                "title": "AE hired 3 months ago, zero closes — do I let them go?",
                "points": 203,
                "comments": 89,
            },
            {
                "source": "TechCrunch",
                "icon": "🟢",
                "time": "4 hours ago",
                "title": "Fintech B2B sales cycles stretched 40% in 2025 — compliance now gate",
                "points": None,
                "comments": None,
            },
            {
                "source": "Crunchbase News",
                "icon": "🔵",
                "time": "today",
                "title": "Payments infrastructure funding up 28% — 14 Series A closes this month",
                "points": None,
                "comments": None,
            },
        ],
        "market_context": [
            "Payments fintechs seeing 40% longer sales cycles in 2025",
            "Compliance buyers now require 2+ vendor references before signing",
            "Top trigger: companies switching core banking infrastructure",
            "Series A Fintech AE ramp averages 4.2 months in Payments",
            "Partner channel converting 3x vs cold outbound at $3M+ ARR",
        ],
    }
