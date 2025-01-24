import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import json
import io
from fpdf import FPDF

# 🌍 Set up the page layout
st.set_page_config(page_title="US Tariffs on Canada - Economic Impact", layout="wide")

# 🇨🇦 Title
st.markdown("<h1 style='text-align: center;'>US Tariffs Impact on Canada - Policy Simulation</h1>", unsafe_allow_html=True)

# 📊 **Fetch Trade Data from Statistics Canada API**
@st.cache_data
def fetch_trade_data():
    url = "https://www150.statcan.gc.ca/t1/wds/rest/getDataFromCube"
    payload = {
        "productId": "12100036",  # Example dataset (change if needed)
        "dimensionValues": [
            {"key": "GEO", "values": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]},  # Provinces
            {"key": "TRADE_FLOW", "values": ["1"]},  # Exports
            {"key": "PARTNER", "values": ["15"]}  # US
        ]
    }

    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        records = data.get("object", [])
        trade_data = []
        
        for record in records:
            trade_data.append({
                "Province": record.get("GEO"),
                "Total Exports (Million CAD)": record.get("VALUE")
            })
        
        df = pd.DataFrame(trade_data)
        
        # Convert to billions
        df["Total Exports (Billion CAD)"] = df["Total Exports (Million CAD)"] / 1e3  

        # Assume 75% of exports go to the US
        df["Exports to US (Billion CAD)"] = df["Total Exports (Billion CAD)"] * 0.75  

        # Handle missing or incorrect API data
        df.fillna(0, inplace=True)

        return df
    else:
        st.error("⚠️ Failed to fetch data from Statistics Canada.")
        return pd.DataFrame()

# 🔄 **Fetch the data**
trade_df = fetch_trade_data()

# **DEBUG:** Print column names to verify structure
st.write("📊 Debugging - Trade Data Columns:", trade_df.columns.tolist())
st.write(trade_df.head())

# 📊 **Compute Export Dependency & Vulnerability**
if not trade_df.empty:
    trade_df["Export Dependency (%)"] = (trade_df["Exports to US (Billion CAD)"] / trade_df["Total Exports (Billion CAD)"]) * 100

    # Define a vulnerability index based on export dependency
    def assign_vulnerability_index(export_dependency):
        if export_dependency >= 75:
            return "High"
        elif 50 <= export_dependency < 75:
            return "Moderate"
        else:
            return "Low"

    trade_df["Vulnerability Index"] = trade_df["Export Dependency (%)"].apply(assign_vulnerability_index)

    # 🗺 **Heatmap of Provincial Vulnerability**
    st.markdown("## 📊 Provincial Vulnerability Heatmap")
    fig = px.choropleth(
        trade_df,
        locations="Province",
        locationmode="country names",
        color="Export Dependency (%)",
        hover_name="Province",
        color_continuous_scale="Reds",
        scope="north america",
        title="Canadian Provinces' Export Dependency on the US"
    )
    st.plotly_chart(fig)

# 🏛 **Economic Simulation - Policy Response**
st.sidebar.header("📉 Simulation Controls")

# 🔹 **US Tariff on Canadian Goods**
us_tariff_rate = st.sidebar.slider("US Tariff Rate on Canadian Goods (%)", 0, 50, 25, 5)

# 🔹 **Canada’s Response: Tariffs on US**
canada_tariff_rate = st.sidebar.slider("Canada's Tariff on US Goods (%)", 0, 50, 10, 5)

# 🔹 **Inflation Impacts**
us_inflation = st.sidebar.slider("US Inflation Increase (%)", 0, 10, 3, 1)
canada_inflation = st.sidebar.slider("Canada Inflation Increase (%)", 0, 10, 2, 1)

# 📊 **Simulated Impact**
st.markdown("## 📊 Simulated Economic Impact")

# **GDP & Trade Impact Calculations**
if "Exports to US (Billion CAD)" in trade_df.columns:
    predicted_trade_loss = round(trade_df["Exports to US (Billion CAD)"].sum() * (us_tariff_rate / 100), 2)
    gdp_loss_canada = round(predicted_trade_loss * 0.5, 2)  # Assume 50% of trade loss affects GDP
    gdp_loss_us = round(predicted_trade_loss * 0.3, 2)  # Assume 30% of lost imports impact US GDP

    # **Canadian Inflation Impact**
    inflationary_pressure_canada = round(canada_inflation * gdp_loss_canada * 0.1, 2)
    inflationary_pressure_us = round(us_inflation * gdp_loss_us * 0.1, 2)

    # **Display Results**
    impact_data = pd.DataFrame({
        "Impact Factor": [
            "Total Canadian Trade Loss (Billion CAD)", 
            "Canadian GDP Loss (Billion CAD)",
            "US GDP Loss (Billion CAD)",
            "Canadian Inflationary Pressure Increase",
            "US Inflationary Pressure Increase"
        ],
        "Estimated Value": [
            predicted_trade_loss, 
            gdp_loss_canada, 
            gdp_loss_us, 
            inflationary_pressure_canada, 
            inflationary_pressure_us
        ]
    })
    st.table(impact_data)
else:
    st.error("⚠️ Data missing for 'Exports to US (Billion CAD)'. Check API response.")

# 📄 **Download Reports**
st.markdown("## 📑 Export Reports")

# 📥 Export to Excel
excel_buffer = io.BytesIO()
trade_df.to_excel(excel_buffer, index=False, engine='openpyxl')
st.download_button(
    label="📥 Download Economic Impact Report (Excel)",
    data=excel_buffer.getvalue(),
    file_name="economic_impact_analysis.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# 📥 Export to PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, "US-Canada Trade Impact Report", ln=True, align='C')
pdf.ln(10)

if "Exports to US (Billion CAD)" in trade_df.columns:
    for index, row in impact_data.iterrows():
        pdf.cell(200, 10, f"{row['Impact Factor']}: {row['Estimated Value']}", ln=True)
else:
    pdf.cell(200, 10, "⚠️ Data unavailable for economic impact analysis.", ln=True)

pdf_buffer = io.BytesIO()
pdf.output(pdf_buffer, 'F')

st.download_button(
    label="📥 Download Economic Impact Report (PDF)",
    data=pdf_buffer.getvalue(),
    file_name="economic_impact_analysis.pdf",
    mime="application/pdf"
)

# ✅ **Final Message**
st.markdown("<h4 style='text-align: center;'>📊 Built by VisiVault Analytics Ltd.</h4>", unsafe_allow_html=True)
