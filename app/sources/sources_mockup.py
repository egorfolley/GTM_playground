"""Mock market signals from HN, Reddit, TechCrunch, Crunchbase for Fintech GTM context.

These signals are calibrated for Fintech B2B SaaS founders at $1M-$10M ARR
and inform Market Intelligence, ICP, and Channel Strategy agent outputs.
"""

MARKET_SIGNALS = [
    # Founder-led sales & early hiring challenges
    ("🟠", "Hacker News", "2h ago", 
     "How I got my first 10 Fintech customers without a sales team"),
    ("🔴", "Reddit r/fintech", "3h ago", 
     "Cold outbound not converting in Payments — what changed?"),
    ("🟠", "Hacker News", "6h ago", 
     "Founder-led sales in Payments — what works at $1M ARR"),
    ("🟢", "TechCrunch", "4h ago", 
     "Fintech B2B sales cycles stretched 40% in 2025"),
    ("🔴", "Reddit r/startups", "8h ago", 
     "How do you find ICP signal before hiring your first AE?"),
    ("🔵", "Crunchbase", "today", 
     "Payments infrastructure — 14 Series A closes this month"),
    ("🔴", "Reddit r/SaaS", "yesterday", 
     "AE hired 3 months ago, zero closes — do I let them go?"),
    ("🟠", "Hacker News", "yesterday", 
     "Why most early Fintech outbound fails and how to fix it"),
    
    # Pipeline & sales motion challenges
    ("🔴", "Reddit r/fintech", "22h ago",
     "Pipeline density at $1M ARR — how many deals in flight?"),
    ("🟠", "Hacker News", "1d ago",
     "Payments founders: does your first $100K ARR come from outbound or inbound?"),
    ("🟢", "TechCrunch", "1d ago",
     "B2B SaaS sales velocity down 15% YoY — what's driving it?"),
    ("🔴", "Reddit r/SaaS", "2d ago",
     "Fired sales team, founder back in deals — still faster to $3M ARR"),
    
    # Buyer behavior & ICP discovery
    ("🟠", "Hacker News", "1d ago",
     "Payments compliance buyers move slow — how to accelerate decisions"),
    ("🔴", "Reddit r/fintech", "2d ago",
     "Who really makes the payment gateway decision at mid-market banks?"),
    ("🟢", "TechCrunch", "2d ago",
     "Fintech vendor consolidation: buyers want fewer, deeper relationships"),
    ("🔴", "Reddit r/startups", "2d ago",
     "Trying to sell to Stripe ecosystem companies — buyer profile changing?"),
    
    # Competitive & market shifts
    ("🟠", "Hacker News", "3d ago",
     "The payment infrastructure wars are heating up — where to win at $1M"),
    ("🟢", "TechCrunch", "3d ago",
     "Stripe + Fintech API consolidation — is there white space left?"),
    ("🔴", "Reddit r/fintech", "3d ago",
     "Everyone's building Payments. How do you differentiate in 2025?"),
    
    # Regulatory & compliance
    ("🟠", "Hacker News", "4d ago",
     "New Fintech licensing requirements — GTM impact for small vendors"),
    ("🟢", "TechCrunch", "4d ago",
     "Compliance delays shipping for 30% of Fintech sales teams this year"),
    
    # Channel & partnership signals
    ("🔴", "Reddit r/SaaS", "4d ago",
     "Partner go-to-market for Fintech — does it work before $3M?"),
    ("🟠", "Hacker News", "5d ago",
     "Event-driven GTM in Payments — still worth it post-2024?"),
    ("🟢", "Crunchbase", "5d ago",
     "Fintech API marketplace adoption up 60% — integration as GTM lever"),
    
    # Metrics & forecasting reality checks
    ("🔴", "Reddit r/startups", "6d ago",
     "Payments SaaS CAC payback — what's realistic at this stage?"),
    ("🟠", "Hacker News", "6d ago",
     "Magic number below 0.7? Here's what Payments founders are seeing"),
]
