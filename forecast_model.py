from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, UploadFile, File

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "app"))

from forecast_model import load_pipeline, summarize_pipeline, top_risky_deals
from ai_insights import generate_ai_summary

app = FastAPI(title="AI Forecast Intelligence API")

@app.get("/")
def health_check():
    return {"status": "ok", "service": "ai-forecast-intelligence"}

@app.get("/analyze-sample")
def analyze_sample():
    df = load_pipeline(str(ROOT / "data" / "sample_sales_pipeline.csv"))
    metrics = summarize_pipeline(df)
    return {
        "metrics": metrics,
        "executive_summary": generate_ai_summary(metrics),
        "top_risky_deals": top_risky_deals(df).to_dict(orient="records"),
    }

@app.post("/analyze-csv")
async def analyze_csv(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    for col in ["close_date", "created_date", "last_activity_date"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    metrics = summarize_pipeline(df)
    return {
        "metrics": metrics,
        "executive_summary": generate_ai_summary(metrics),
        "top_risky_deals": top_risky_deals(df).to_dict(orient="records"),
    }
