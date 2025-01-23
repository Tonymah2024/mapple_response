# -*- coding: utf-8 -*-
"""Untitled108.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1BWvPLs9O5-RKRQE00R9Ds9-4-8voAkux
"""

# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
import plotly.express as px
import requests
import io
import os  # Fix: Import os
import joblib  # AI Model
from fpdf import FPDF
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# ==================== 🌍 Fetch Real Economic Data 🌍 ====================

st.markdown('<p class="title-text">🍁 Trade Impact Analysis & Policy Simulation Tool 🍁</p>', unsafe_allow_html=True)
st.image("https://upload.wikimedia.org/wikipedia/commons/c/cf/Flag_of_Canada.svg", width=200)

# World Bank API - Fetch Trade Volume as % of GDP
wb_url = "https://api.worldbank.org/v2/country/CA/indicator/NE.TRD.GNFS.ZS?format=json"
response = requests.get(wb_url)

if response.status_code == 200:
    data = response.json()
    trade_percent_gdp = [entry["value"] for entry in data[1] if entry["value"] is not None]
else:
    st.warning("⚠️ Unable to fetch real trade data. Using default projections.")
    trade_percent_gdp = list(np.random.randint(60, 90, size=30))

# ==================== 📊 Sidebar Inputs 📊 ====================
st.sidebar.header("🇨🇦 Simulation Settings 🇨🇦")

sectors = ["Automotive", "Agriculture", "Manufacturing", "Energy", "Technology"]
selected_sector = st.sidebar.selectbox("Select Industry Sector:", sectors)
tariff_rate = st.sidebar.slider("Tariff Rate Increase (%)", 10, 50, 25, 5)

# ==================== 📉 Economic Impact Analysis 📉 ====================
predicted_trade_volume = round(500 - (tariff_rate * 5), 2)
gdp_loss = round(0.05 * tariff_rate, 2)
job_loss = round(3000 * tariff_rate, 0)

economic_table = pd.DataFrame({
    "Indicator": ["Predicted Trade Volume (Billion CAD)", "GDP Loss Estimate (Billion CAD)", "Job Loss Estimate"],
    "Estimated Value": [predicted_trade_volume, gdp_loss, job_loss]
})

st.table(economic_table)

# ==================== ⚖️ Custom Policy Adjustments ⚖️ ====================
st.markdown('<p class="sub-header">⚖️ Custom Policy Adjustments</p>', unsafe_allow_html=True)

subsidy_amount = st.slider("Government Subsidy Support (Billion CAD)", 0, 50, 10, 1)
alternative_trade_agreements = st.selectbox("Expand Trade with:", ["EU", "China", "India", "Mexico", "Japan"])
corporate_tax_change = st.slider("Adjust Corporate Tax Rate (%)", -5, 5, 0, 1)

policy_results = {
    "Subsidy Amount (Billion CAD)": subsidy_amount,
    "New Trade Partner": alternative_trade_agreements,
    "Corporate Tax Adjustment (%)": corporate_tax_change
}
st.json(policy_results)

# ==================== 🔍 Train AI Model (if not exists) 🔍 ====================
model_file = "ai_trade_model.pkl"

if not os.path.exists(model_file):
    df = pd.DataFrame({
        "Year": np.arange(1990, 2020),
        "Tariff Rate (%)": np.random.randint(10, 50, size=30),
        "Government Subsidy (Billion CAD)": np.random.randint(0, 50, size=30),
        "Corporate Tax Change (%)": np.random.randint(-5, 5, size=30),
        "Future Trade Volume (% GDP)": trade_percent_gdp
    })

    X = df[["Tariff Rate (%)", "Government Subsidy (Billion CAD)", "Corporate Tax Change (%)"]]
    y = df["Future Trade Volume (% GDP)"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    joblib.dump(model, model_file)

# ==================== 🤖 AI-Powered Trade Predictions 🤖 ====================
st.markdown('<p class="sub-header">📊 Predictive Economic Simulation</p>', unsafe_allow_html=True)

try:
    model = joblib.load(model_file)
    future_trade_volume = model.predict([[tariff_rate, subsidy_amount, corporate_tax_change]])[0]
    st.markdown(f'<p class="info-text">📈 **Predicted Trade Volume in 5 Years:** {future_trade_volume:,.2f}% of GDP</p>', unsafe_allow_html=True)
except Exception as e:
    st.warning("⚠️ AI model not found. Using default projections.")
    print(e)

# ==================== 📄 Export Reports 📄 ====================
st.markdown('<p class="sub-header">📑 Export Report</p>', unsafe_allow_html=True)

# 📥 Export to Excel
excel_buffer = io.BytesIO()
with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
    economic_table.to_excel(writer, index=False)
    writer.close()

st.download_button(
    label="📥 Download Excel Report",
    data=excel_buffer.getvalue(),
    file_name="trade_impact_analysis.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# 📥 Export to PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, "Trade Impact Analysis Report", ln=True, align='C')
pdf.ln(10)

pdf.cell(200, 10, f"Predicted Trade Volume: {predicted_trade_volume} Billion CAD", ln=True)
pdf.cell(200, 10, f"GDP Loss Estimate: {gdp_loss} Billion CAD", ln=True)
pdf.cell(200, 10, f"Job Loss Estimate: {job_loss}", ln=True)
pdf.ln(10)

pdf.cell(200, 10, f"Subsidy Support: {subsidy_amount} Billion CAD", ln=True)
pdf.cell(200, 10, f"New Trade Partner: {alternative_trade_agreements}", ln=True)
pdf.cell(200, 10, f"Corporate Tax Change: {corporate_tax_change}%", ln=True)

pdf_buffer = io.BytesIO()
pdf.output(pdf_buffer, 'S')  # Fix TypeError

st.download_button(
    label="📥 Download PDF Report",
    data=pdf_buffer.getvalue(),
    file_name="trade_impact_analysis.pdf",
    mime="application/pdf"
)

# ==================== ✅ Final Message ✅ ====================
st.markdown('<p class="info-text">🍁 <strong>Prototype Version 2.0 - Developed by VisiVault Analytics Ltd.</strong> 🍁</p>', unsafe_allow_html=True)
