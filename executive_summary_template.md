from __future__ import annotations

import pandas as pd
import streamlit as st

from forecast_model import load_pipeline, summarize_pipeline, top_risky_deals
from ai_insights import generate_ai_summary

st.set_page_config(page_title="AI Forecast Intelligence", page_icon="📊", layout="wide")
st.title("📊 AI Forecast Intelligence Engine")
st.caption("Enterprise-style sales forecast analysis with risk scoring and executive commentary.")

uploaded = st.file_uploader("Upload Salesforce / HubSpot pipeline CSV", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)
    for col in ["close_date", "created_date", "last_activity_date"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")
else:
    df = load_pipeline("data/sample_sales_pipeline.csv")

metrics = summarize_pipeline(df)
s = metrics["summary"]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Open Pipeline", f"${s['total_open_pipeline']:,.0f}")
c2.metric("Weighted Pipeline", f"${s['weighted_open_pipeline']:,.0f}")
c3.metric("High-Risk Value", f"${s['high_risk_value']:,.0f}")
c4.metric("Open Deals", f"{s['open_deal_count']}")

st.subheader("Executive Forecast Narrative")
st.info(generate_ai_summary(metrics))

st.subheader("Regional Summary")
st.dataframe(pd.DataFrame(metrics["region_summary"]), use_container_width=True)

st.subheader("Top Risky Deals")
st.dataframe(
    top_risky_deals(df)[
        ["opportunity_id", "customer", "region", "rep", "stage", "amount", "close_date", "last_activity_date", "risk_score", "risk_band", "next_step"]
    ],
    use_container_width=True,
)
