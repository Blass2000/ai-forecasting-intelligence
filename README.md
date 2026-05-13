
# WS Sample AI Forecast Intelligence Engine

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## Overview
The **AI Forecast Intelligence Engine** (cathcy name huh?) is an enterprise-style analytics solution designed to evaluate sales pipeline data, identify forecast risk, and generate executive-ready insights using a combination of data analysis and AI-driven reasoning.
This project simulates a real-world **Revenue Operations (RevOps)** workflow by transforming Salesforce or HubSpot-style pipeline data into actionable intelligence for sales leadership.
It bridges the gap between **raw data → business insight → executive decision-making**
---
## Demo
> Dashboard showing pipeline health, risk exposure, and AI-generated executive insights.
<img width="1883" height="753" alt="image" src="https://github.com/user-attachments/assets/af97f1fa-b6d4-4c77-8c80-d26f78908ff5" />
and details

<img width="1813" height="789" alt="image" src="https://github.com/user-attachments/assets/4a67366c-72a8-43a0-be67-ded9b49be65c" />
---

## Problem Statement

I have often seen that Sales organizations oface: - Inaccurate or inconsistent forecasts ,  Limited visibility into deal risk , - Manual and time-consuming reporting  and lacke of clear executive narritives.

---

## Solution

This sample solution provides:

- Automated pipeline analysis  
- Forecast risk scoring  
- Regional performance insights  
- AI-generated executive summaries  
- Interactive dashboard + API access  
---

## Core Features

### Forecast Risk Scoring
Each opportunity is evaluated using a scoring model based on:
- Stage maturity  
- Days to close  
- Recency of activity  
- Deal size  
**Output:**
- Low Risk  
- Medium Risk  
- High Risk  
---
### Pipeline Intelligence
- Total open pipeline  
- Weighted pipeline  
- Stage distribution (Commit / Upside / Development)  
- High-risk deal exposure  
- Regional performance  
---

### AI Executive Insights
Automatically generates leadership-ready summaries such as:

> “Pipeline strength is concentrated in the West region, while Central shows elevated slippage risk due to stale late-stage opportunities.”
---

### Interactive Dashboard
Built with Streamlit, allowing users to:
- Upload pipeline data  
- View KPIs instantly  
- Analyze high-risk deals  
- Review AI-generated insights  
---

### API Integration (FastAPI)
- Analyze pipeline via REST endpoints  
- Integrate with other systems  
- Enable automation workflows  

---

## Architecture
In the control folder, I have plaed the Python, Streamlit and shell code - have fun. 
## Architecture

### System Components

#### 1. **Data Pipeline**
- **Input Layer**: Accepts CSV/JSON data from Salesforce or HubSpot exports
- **Data Validation**: Schema validation and data quality checks
- **Transformation Layer**: Normalizes deal stages, probability scoring, and date handling
- **Storage**: In-memory processing with optional Parquet caching

#### 2. **Risk Scoring Engine**
- **Algorithm**: Multi-factor scoring model combining:
  - `stage_maturity`: Probability adjustment based on pipeline stage
  - `days_to_close`: Temporal urgency metric (lower is riskier near deadline)
  - `activity_recency`: Days since last customer interaction (staleness factor)
  - `deal_size`: Amount weighting for revenue impact
- **Output Classes**: Low Risk (0.0-0.5), Medium Risk (0.5-0.8), High Risk (0.8-1.0)

#### 3. **Frontend - Streamlit Dashboard**
- **Pages**:
  - **Overview**: KPI cards (Total Pipeline, Weighted Pipeline, Risk Distribution)
  - **Deal Analysis**: Filterable table with risk flags, stage distribution
  - **Regional Insights**: Heatmaps and performance metrics by region
  - **AI Insights**: LLM-generated executive summaries
- **Interactivity**: Real-time filtering by region, rep, deal status

#### 4. **Backend - FastAPI Server**
- **Endpoints**:
  - `POST /analyze`: Accept pipeline data and return risk scores
  - `GET /pipeline/summary`: Aggregate KPI metrics
  - `GET /deals/{id}`: Individual deal risk assessment
  - `GET /forecast`: Executive summary generation
- **Performance**: Async request handling for large datasets

#### 5. **AI/LLM Integration**
- **Model**: OpenAI/Claude API for narrative generation
- **Prompts**: Dynamic context construction from pipeline analytics
- **Output**: Executive-ready summaries with regional analysis

### Tech Stack
- **Backend**: Python 3.11, FastAPI, Pandas, NumPy
- **Frontend**: Streamlit
- **Data Processing**: CSV/JSON parsing, Polars/Pandas DataFrames
- **AI/LLM**: LangChain, OpenAI API
- **Deployment**: Docker (optional), Python virtual environment


