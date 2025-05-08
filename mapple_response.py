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
            df = df[df['value'].notnull()]
            df['date'] = df['date'].astype(int)
            return df.sort_values('date', ascending=True)
        return pd.DataFrame()
    except Exception:
        return pd.DataFrame()

@st.cache_data(show_spinner=False)
def fetch_latest_value(series_df):
    if not series_df.empty:
        return series_df.iloc[-1]['value']
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
    return f"{prefix}{value:,.2f}" if isinstance(value, (int, float)) else "Unavailable"

col1, col2 = st.columns(2)
col1.metric("🇨🇦 Canada GDP", format_metric(canada_gdp, "CAD "))
col2.metric("📈 Canada Inflation", f"{canada_inflation:.2f}%" if isinstance(canada_inflation, (int, float)) else "Unavailable")

col3, col4 = st.columns(2)
col3.metric("🇺🇸 US GDP", format_metric(us_gdp, "USD "))
col4.metric("📈 US Inflation", f"{us_inflation:.2f}%" if isinstance(us_inflation, (int, float)) else "Unavailable")

# ==================== 📊 GDP Trend ====================
if not canada_gdp_series.empty:
    st.markdown('<p class="sub-header">📈 Historical GDP Trend - Canada</p>', unsafe_allow_html=True)
    fig_gdp = px.line(canada_gdp_series, x="date", y="value", title="Canada GDP Over Time (US$)")
    st.plotly_chart(fig_gdp, use_container_width=True)

# ==================== 📂 Upload Feature ====================
st.sidebar.markdown("### 📂 Upload Your Dataset")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type="csv")

if uploaded_file is not None:
    user_df = pd.read_csv(uploaded_file)
    st.markdown("### 👁 Preview of Uploaded Data")
    st.dataframe(user_df)

    numeric_cols = user_df.select_dtypes(include=np.number).columns.tolist()
    if len(numeric_cols) >= 2:
        st.markdown("### 🔍 Try Predicting")
        feature = st.selectbox("Select feature to use for prediction:", numeric_cols)
        target = st.selectbox("Select target variable:", [col for col in numeric_cols if col != feature])
        value = st.slider(f"Select value for {feature}", float(user_df[feature].min()), float(user_df[feature].max()))

        model = LinearRegression()
        model.fit(user_df[[feature]], user_df[target])
        prediction = model.predict([[value]])
        st.success(f"📈 Predicted {target}: {prediction[0]:.2f}")

# ==================== 🏭 Select Economic Sector 🏭 ====================
st.sidebar.header("📌 Select Industry Sector")
sectors = ["Automotive", "Agriculture", "Manufacturing", "Energy", "Technology"]
selected_sector = st.sidebar.selectbox("Select Sector:", sectors)

# ==================== 🇺🇸 U.S. Tariff Impact 🇺🇸 ====================
st.markdown('<p class="sub-header">🇺🇸 U.S. Tariffs on Canada</p>', unsafe_allow_html=True)
us_tariff_rate = st.slider("U.S. Tariff Rate on Canadian Goods (%)", 5, 50, 20, 5)

canada_trade_loss = round(500 - (us_tariff_rate * 5), 2)
canada_gdp_loss = round(0.03 * us_tariff_rate, 2)
canada_job_loss = round(3000 * us_tariff_rate, 0)
canada_inflation_increase = round(0.02 * us_tariff_rate, 2)

us_impact_table = pd.DataFrame({
    "Indicator": ["Canada Trade Loss (Billion CAD)", "Canada GDP Loss (Billion CAD)", 
                  "Canada Job Loss Estimate", "Canada Inflation Increase (%)"],
    "Estimated Value": [canada_trade_loss, canada_gdp_loss, canada_job_loss, canada_inflation_increase]
})

st.table(us_impact_table)

# ==================== 🇨🇦 Canada’s Response 🇨🇦 ====================
st.markdown('<p class="sub-header">🇨🇦 Canada’s Countermeasures</p>', unsafe_allow_html=True)

canada_retaliation_tariff = st.slider("Canada’s Tariff on U.S. Goods (%)", 0, 50, 10, 5)
subsidy_amount = st.slider("Government Subsidy Support (Billion CAD)", 0, 50, 10, 1)
corporate_tax_change = st.slider("Corporate Tax Rate Change (%)", -5, 5, 0, 1)

us_trade_loss = round(canada_trade_loss * (canada_retaliation_tariff / 50), 2)
us_gdp_impact = round(canada_gdp_loss * (canada_retaliation_tariff / 50), 2)
us_job_loss = round(canada_job_loss * (canada_retaliation_tariff / 50), 0)
us_inflation_increase = round(canada_inflation_increase * (canada_retaliation_tariff / 50), 2)

canada_response_table = pd.DataFrame({
    "Indicator": ["U.S. Trade Loss (Billion USD)", "U.S. GDP Impact (Billion USD)", 
                  "U.S. Job Loss Estimate", "U.S. Inflation Increase (%)"],
    "Estimated Value": [us_trade_loss, us_gdp_impact, us_job_loss, us_inflation_increase]
})

st.table(canada_response_table)

# ==================== 🔥 Heatmap of Provincial Vulnerability 🔥 ====================
st.markdown('<p class="sub-header">🇨🇦 Provincial Vulnerability</p>', unsafe_allow_html=True)

provinces = ["Ontario", "Quebec", "British Columbia", "Alberta", "Manitoba", "Saskatchewan"]
vulnerability = [0.35, 0.25, 0.15, 0.1, 0.1, 0.05]
province_df = pd.DataFrame({"Province": provinces, "Vulnerability Index": vulnerability})

fig, ax = plt.subplots(figsize=(10, 4))
sns.heatmap(province_df.set_index("Province").T, cmap="Reds", annot=True, linewidths=0.5)
st.pyplot(fig)

# ==================== 📄 Export Reports 📄 ====================
st.markdown('<p class="sub-header">📑 Export Report</p>', unsafe_allow_html=True)

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, "US Tariff Impact Report", ln=True, align='C')
pdf.ln(10)

for index, row in us_impact_table.iterrows():
    pdf.cell(200, 10, f"{row['Indicator']}: {row['Estimated Value']}", ln=True)

for index, row in canada_response_table.iterrows():
    pdf.cell(200, 10, f"{row['Indicator']}: {row['Estimated Value']}", ln=True)

pdf_buffer = io.BytesIO()
pdf.output(pdf_buffer, dest='S')
pdf_data = pdf_buffer.getvalue()

st.download_button(
    label="📥 Download PDF Report",
    data=pdf_data,
    file_name="us_tariff_impact.pdf",
    mime="application/pdf"
)

st.markdown('<p class="info-text">📊 Developed by VisiVault Analytics Ltd.</p>', unsafe_allow_html=True)
