# -*- coding: utf-8 -*-
"""mapple_response.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1vBgokslmxSxhAJErbjI9nOLCyLhvCUwc
"""

import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
import plotly.express as px

# 🇨🇦 Improved Canadian Styling for Better Visibility 🇨🇦
st.markdown(
    """
    <style>
        .stApp {
            background-color: #ffffff;
        }
        .title-text {
            font-size: 36px;
            font-weight: bold;
            color: #b71c1c; /* Dark Red */
            text-align: center;
        }
        .sub-header {
            font-size: 24px;
            font-weight: bold;
            color: #0d47a1; /* Deep Blue */
            text-align: center;
        }
        .info-text {
            font-size: 18px;
            color: #333333; /* Dark Gray */
            text-align: center;
        }
        .table-text {
            font-size: 18px;
            color: #333333; /* Dark Gray */
        }
        .section-bg {
            background-color: #f9f9f9;
            padding: 10px;
            border-radius: 5px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# 🇨🇦 Display Canadian Flag and Title 🇨🇦
st.markdown('<p class="title-text">🍁 Trade Impact Analysis & Policy Simulation Tool 🍁</p>', unsafe_allow_html=True)
st.image("https://upload.wikimedia.org/wikipedia/commons/c/cf/Flag_of_Canada.svg", width=200)

# Sidebar Header with 🇨🇦 Flag
st.sidebar.header("🇨🇦 Simulation Settings 🇨🇦")

# User Inputs: Select Industry & Tariff Rate
sectors = ["Automotive", "Agriculture", "Manufacturing", "Energy", "Technology"]
selected_sector = st.sidebar.selectbox("Select Industry Sector:", sectors)
tariff_rate = st.sidebar.slider("Tariff Rate Increase (%)", 10, 50, 25, 5)

# 🇨🇦 Canadian Economic Data (Mock)
st.markdown('<p class="sub-header">📊 Canadian Trade Overview</p>', unsafe_allow_html=True)
st.markdown('<p class="info-text">🇨🇦 <strong>Canada GDP:</strong> CAD 2.2 Trillion</p>', unsafe_allow_html=True)
st.markdown('<p class="info-text">🌎 <strong>Top Trading Partners:</strong> USA, China, EU, Mexico</p>', unsafe_allow_html=True)
st.markdown('<p class="info-text">📈 <strong>Annual Exports to USA:</strong> CAD 500 Billion</p>', unsafe_allow_html=True)

# Gravity Model Data (Mock Data for Demonstration)
trade_data = pd.DataFrame({
    "Tariff Rate": [0, 5, 10, 15, 20, 25, 30],
    "GDP_Canada": [2200] * 7,  # Billion CAD
    "GDP_USA": [23000] * 7,  # Billion USD
    "Distance": [3000] * 7,  # km
    "Trade Volume (Billion CAD)": [500, 480, 450, 420, 390, 360, 330]  # Exports from Canada to USA
})

# Fit Gravity Model using OLS Regression
X = trade_data[['Tariff Rate', 'GDP_Canada', 'GDP_USA', 'Distance']]
X = sm.add_constant(X)
y = trade_data['Trade Volume (Billion CAD)']
model = sm.OLS(y, X).fit()

# Prepare input for prediction
new_data = pd.DataFrame([[tariff_rate, 2200, 23000, 3000]],
                        columns=['Tariff Rate', 'GDP_Canada', 'GDP_USA', 'Distance'])
new_data = sm.add_constant(new_data)

# Predict Trade Volume
predicted_trade_volume = model.predict(new_data)[0]

# 🇨🇦 Display Trade Impact Analysis 🇨🇦
st.markdown('<p class="sub-header">📉 Economic Impact Analysis</p>', unsafe_allow_html=True)
st.markdown('<p class="table-text">This section estimates how tariffs impact trade volume, GDP, and employment.</p>', unsafe_allow_html=True)

trade_impact_data = pd.DataFrame({
    "Indicator": ["Predicted Trade Volume (Billion CAD)", "GDP Loss Estimate (Billion CAD)", "Job Loss Estimate"],
    "Estimated Value": [round(predicted_trade_volume, 2), round(0.05 * tariff_rate, 2), round(3000 * tariff_rate, 0)]
})
st.table(trade_impact_data)

# 🇨🇦 Retaliatory Tariff Policy Simulation 🇨🇦
st.markdown('<p class="sub-header">⚖️ Policy Response Simulation</p>', unsafe_allow_html=True)
st.markdown('<p class="table-text">Explore potential government responses, including counter-tariffs and subsidies.</p>', unsafe_allow_html=True)

retaliatory_tariffs = {
    "U.S. Imports Affected (Billion CAD)": round(0.2 * tariff_rate, 2),
    "Potential Revenue from Tariffs (Billion CAD)": round(0.08 * tariff_rate, 2)
}
st.write("**Retaliatory Tariffs:**", retaliatory_tariffs)

# 🇨🇦 Alternative Trade Market Analysis 🇨🇦
st.markdown('<p class="sub-header">🌍 Trade Diversification Strategy</p>', unsafe_allow_html=True)
alternative_markets = pd.DataFrame({
    "Market": ["EU", "China", "Mexico", "India", "Japan"],
    "Potential Increase in Exports (Billion CAD)": np.random.uniform(5, 20, 5).round(2)
})
st.dataframe(alternative_markets)

# Visualization: 🇨🇦 Trade Exposure by Province 🇨🇦
st.markdown('<p class="sub-header">📍 Trade Exposure by Province</p>', unsafe_allow_html=True)
province_data = pd.DataFrame({
    "Province": ["Ontario", "Quebec", "British Columbia", "Alberta", "Manitoba"],
    "Trade Exposure (%)": np.random.randint(20, 60, 5)
})
fig = px.bar(province_data, x="Province", y="Trade Exposure (%)", color="Trade Exposure (%)",
             title="Provincial Trade Exposure to U.S. Tariffs", text="Trade Exposure (%)")
st.plotly_chart(fig)

st.markdown('<p class="info-text">🍁 <strong>Prototype Version 1.3 - Developed by VisiVault Analytics Ltd.</strong> 🍁</p>', unsafe_allow_html=True)