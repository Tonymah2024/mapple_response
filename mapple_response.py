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
import requests
import io
import joblib
import os
import plotly.express as px
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

# ==================== 🌍 Fetch Real Data 🌍 ====================
st.markdown('<p class="sub-header">🌍 Real-Time Economic Indicators</p>', unsafe_allow_html=True)

# Fetch GDP data for Canada & US
gdp_canada_data = requests.get("https://api.worldbank.org/v2/country/CA/indicator/NY.GDP.MKTP.CD?format=json").json()
gdp_us_data = requests.get("https://api.worldbank.org/v2/country/US/indicator/NY.GDP.MKTP.CD?format=json").json()

canada_gdp = gdp_canada_data[1][0]["value"] if gdp_canada_data and len(gdp_canada_data) > 1 else "Unavailable"
us_gdp = gdp_us_data[1][0]["value"] if gdp_us_data and len(gdp_us_data) > 1 else "Unavailable"

# Fetch Inflation (CPI) data for Canada & US
inflation_canada_data = requests.get("https://api.worldbank.org/v2/country/CA/indicator/FP.CPI.TOTL?format=json").json()
inflation_us_data = requests.get("https://api.worldbank.org/v2/country/US/indicator/FP.CPI.TOTL?format=json").json()

canada_inflation = inflation_canada_data[1][0]["value"] if inflation_canada_data and len(inflation_canada_data) > 1 else "Unavailable"
us_inflation = inflation_us_data[1][0]["value"] if inflation_us_data and len(inflation_us_data) > 1 else "Unavailable"

st.markdown(f"🇨🇦 **Canada GDP:** CAD {canada_gdp:,.2f}")
st.markdown(f"📈 **Canada Inflation Rate:** {canada_inflation:.2f}%")
st.markdown(f"🇺🇸 **US GDP:** USD {us_gdp:,.2f}")
st.markdown(f"📈 **US Inflation Rate:** {us_inflation:.2f}%")

# ==================== 🇺🇸 U.S. Tariff Impact 🇺🇸 ====================
st.markdown('<p class="sub-header">🇺🇸 U.S. Tariffs on Canada</p>', unsafe_allow_html=True)
us_tariff_rate = st.slider("U.S. Tariff Rate on Canadian Goods (%)", 5, 50, 20, 5)

# Estimate economic impact
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

# ==================== 🇨🇦 Canada's Response 🇨🇦 ====================
st.markdown('<p class="sub-header">🇨🇦 Canada’s Countermeasures</p>', unsafe_allow_html=True)

# Canada’s retaliation tariffs
canada_retaliation_tariff = st.slider("Canada’s Tariff on U.S. Goods (%)", 0, 50, 10, 5)
subsidy_amount = st.slider("Government Subsidy Support (Billion CAD)", 0, 50, 10, 1)
corporate_tax_change = st.slider("Corporate Tax Rate Change (%)", -5, 5, 0, 1)

# U.S. impact due to retaliation
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

# ==================== 🇨🇦 Provincial Vulnerability 🇨🇦 ====================
st.markdown('<p class="sub-header">🇨🇦 Provincial Vulnerability</p>', unsafe_allow_html=True)

provinces = ["Ontario", "Quebec", "British Columbia", "Alberta", "Manitoba", "Saskatchewan"]
vulnerability = [0.35, 0.25, 0.15, 0.1, 0.1, 0.05]

province_df = pd.DataFrame({"Province": provinces, "Vulnerability Index": vulnerability})
fig = px.bar(province_df, x="Province", y="Vulnerability Index", title="Trade Vulnerability by Province")
st.plotly_chart(fig)

# ==================== 📄 Export Reports 📄 ====================
st.markdown('<p class="sub-header">📑 Export Report</p>', unsafe_allow_html=True)

# Export to PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, "US Tariff Impact Report", ln=True, align='C')
pdf.ln(10)

for index, row in us_impact_table.iterrows():
    pdf.cell(200, 10, f"{row['Indicator']}: {row['Estimated Value']}", ln=True)

for index, row in canada_response_table.iterrows():
    pdf.cell(200, 10, f"{row['Indicator']}: {row['Estimated Value']}", ln=True)

pdf_file = "us_tariff_impact.pdf"
pdf.output(pdf_file)
st.download_button("📥 Download PDF Report", open(pdf_file, "rb"), pdf_file, "application/pdf")

st.markdown('<p class="info-text">📊 Developed by VisiVault Analytics Ltd.</p>', unsafe_allow_html=True)