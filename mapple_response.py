# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import requests
import io
import joblib
import os
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from fpdf import FPDF
from sklearn.linear_model import LinearRegression

# ==================== 🇨🇦 Page Configuration ====================
st.set_page_config(page_title="US Tariffs Impact on Canada", layout="wide")

st.markdown(
    """
    <style>
        .title-text {
            font-size: 36px;
            font-weight: bold;
            color: #4a4a4a;
            text-align: center;
        }
        .sub-header {
            font-size: 24px;
            font-weight: bold;
            color: #333333;
            text-align: center;
        }
        .info-text {
            font-size: 18px;
            color: #4a4a4a;
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==================== 🇨🇦 Title ====================
st.markdown('<p class="title-text">📊 US Tariffs Impact on Canada - Policy Simulation</p>', unsafe_allow_html=True)

# ==================== ℹ️ Interpretation Help ====================
st.info("""
**How to Interpret the Results**

- **GDP and Inflation Metrics** reflect real-time economic indicators pulled from the World Bank API.
- **Tariff Impact Tables** estimate the economic effects of tariffs, such as trade loss and job loss.
- **Vulnerability Index** represents how sensitive each province is to U.S. tariffs. Values closer to 1 indicate higher vulnerability, meaning that province's economy is more affected by tariffs.
- **User Upload & Prediction** lets users try a basic prediction using their own CSV dataset with numerical columns.
- **GDP Trend Chart** (below) shows a historical trajectory of Canada's GDP to support time-based analysis.
""")

st.sidebar.markdown("""
**📄 CSV Upload Requirements:**
- Upload a CSV file containing only numeric columns (e.g., GDP, employment, output).
- At least 2 columns are needed.
- Example structure:

| GDP | Employment |
|-----|------------|
| 500 | 12000      |
| 700 | 15000      |
""")

# ==================== 🌍 Fetch Real Data 🌍 ====================
st.markdown('<p class="sub-header">🌍 Real-Time Economic Indicators</p>', unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def fetch_economic_data_series(country_code, indicator):
    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}?format=json&per_page=100"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data and isinstance(data, list) and len(data) > 1 and isinstance(data[1], list):
            df = pd.DataFrame(data[1])
            df = df[df['value'].notnull()].copy()
            df['value'] = pd.to_numeric(df['value'], errors='coerce')
            df['date'] = df['date'].astype(int)
            return df.sort_values('date', ascending=True)
        return pd.DataFrame()
    except Exception as e:
        st.warning(f"Failed to fetch data: {e}")
        return pd.DataFrame()

@st.cache_data(show_spinner=False)
def fetch_latest_value(series_df):
    if not series_df.empty:
        return series_df.dropna(subset=['value']).iloc[-1]['value']
    return None

canada_gdp_series = fetch_economic_data_series("CA", "NY.GDP.MKTP.CD")
us_gdp_series = fetch_economic_data_series("US", "NY.GDP.MKTP.CD")
canada_inflation_series = fetch_economic_data_series("CA", "FP.CPI.TOTL")
us_inflation_series = fetch_economic_data_series("US", "FP.CPI.TOTL")

canada_gdp = fetch_latest_value(canada_gdp_series)
us_gdp = fetch_latest_value(us_gdp_series)
canada_inflation = fetch_latest_value(canada_inflation_series)
us_inflation = fetch_latest_value(us_inflation_series)

def format_metric(value, prefix=""):
    return f"{prefix}{value:,.2f}" if isinstance(value, (int, float, np.float64)) else "Unavailable"

col1, col2 = st.columns(2)
col1.metric("🇨🇦 Canada GDP", format_metric(canada_gdp, "CAD "))
col2.metric("📈 Canada Inflation", f"{canada_inflation:.2f}%" if isinstance(canada_inflation, (int, float, np.float64)) else "Unavailable")

col3, col4 = st.columns(2)
col3.metric("🇺🇸 US GDP", format_metric(us_gdp, "USD "))
col4.metric("📈 US Inflation", f"{us_inflation:.2f}%" if isinstance(us_inflation, (int, float, np.float64)) else "Unavailable")

# ==================== 📊 GDP Trend ====================
if not canada_gdp_series.empty:
    st.markdown('<p class="sub-header">📈 Historical GDP Trend - Canada</p>', unsafe_allow_html=True)
    fig_gdp = px.line(canada_gdp_series, x="date", y="value", title="Canada GDP Over Time (US$)")
    st.plotly_chart(fig_gdp, use_container_width=True)

# [The rest of the code remains unchanged]
