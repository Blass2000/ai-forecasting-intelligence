from __future__ import annotations

from datetime import date
import pandas as pd

OPEN_STAGES = {"Strong Commit", "Upside", "Development"}

def load_pipeline(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    for col in ["close_date", "created_date", "last_activity_date"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    return df

def score_deal_risk(row: pd.Series, as_of: date | None = None) -> int:
    as_of_ts = pd.Timestamp(as_of or date.today())
    score = 0
    close_date = row.get("close_date")
    last_activity = row.get("last_activity_date")
    stage = row.get("stage", "")
    amount = float(row.get("amount", 0) or 0)

    if stage == "Development":
        score += 25
    elif stage == "Upside":
        score += 15

    if pd.notna(close_date):
        days_to_close = (close_date - as_of_ts).days
        if days_to_close < 0 and stage in OPEN_STAGES:
            score += 30
        elif days_to_close <= 14 and stage != "Strong Commit":
            score += 20

    if pd.notna(last_activity):
        days_stale = (as_of_ts - last_activity).days
        if days_stale > 30:
            score += 25
        elif days_stale > 14:
            score += 15

    if amount >= 250000:
        score += 10

    return min(score, 100)

def enrich_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    enriched = df.copy()
    enriched["risk_score"] = enriched.apply(score_deal_risk, axis=1)
    enriched["risk_band"] = pd.cut(
        enriched["risk_score"],
        bins=[-1, 29, 59, 100],
        labels=["Low", "Medium", "High"],
    )
    enriched["is_open"] = enriched["stage"].isin(OPEN_STAGES)
    return enriched

def summarize_pipeline(df: pd.DataFrame) -> dict:
    enriched = enrich_pipeline(df)
    open_df = enriched[enriched["is_open"]]
    summary = {
        "total_open_pipeline": float(open_df["amount"].sum()),
        "weighted_open_pipeline": float(open_df["weighted_amount"].sum()),
        "strong_commit": float(open_df.loc[open_df["stage"] == "Strong Commit", "amount"].sum()),
        "upside": float(open_df.loc[open_df["stage"] == "Upside", "amount"].sum()),
        "development": float(open_df.loc[open_df["stage"] == "Development", "amount"].sum()),
        "high_risk_value": float(open_df.loc[open_df["risk_band"] == "High", "amount"].sum()),
        "open_deal_count": int(len(open_df)),
        "high_risk_count": int((open_df["risk_band"] == "High").sum()),
    }
    region = (
        open_df.groupby("region")
        .agg(
            open_pipeline=("amount", "sum"),
            weighted_pipeline=("weighted_amount", "sum"),
            deal_count=("opportunity_id", "count"),
            avg_risk=("risk_score", "mean"),
        )
        .reset_index()
        .sort_values("weighted_pipeline", ascending=False)
    )
    return {"summary": summary, "region_summary": region.to_dict(orient="records")}

def top_risky_deals(df: pd.DataFrame, limit: int = 10) -> pd.DataFrame:
    enriched = enrich_pipeline(df)
    return enriched[enriched["is_open"]].sort_values(
        ["risk_score", "amount"], ascending=[False, False]
    ).head(limit)
