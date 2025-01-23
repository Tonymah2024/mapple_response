# Trade Impact Analysis & Policy Simulation Tool

An interactive web application designed to analyze the economic impact of U.S. tariffs on Canadian exports and simulate various policy responses. Built with **Streamlit**, this tool provides real-time insights for policymakers and trade analysts.

---

## **Features**

- **Economic Impact Analysis**: 
  - Predicts GDP loss, job losses, and inflation effects based on tariff rate adjustments.
  - Uses a **Gravity Model of Trade** to forecast trade volume changes.

- **Policy Response Simulation**: 
  - Analyzes the effects of retaliatory tariffs on U.S. imports.
  - Estimates subsidy support required to offset trade disruptions.

- **Trade Diversification**: 
  - Identifies potential alternative export markets (e.g., EU, China, India).
  - Visualizes trade exposure by Canadian provinces.

- **Interactive Visualizations**: 
  - Displays trade exposure heatmaps and bar charts for better decision-making.

---

## **Technology Stack**

- **Frontend & Backend**: [Streamlit](https://streamlit.io)
- **Data Analysis**: [Pandas](https://pandas.pydata.org), [NumPy](https://numpy.org)
- **Econometrics**: [Statsmodels](https://www.statsmodels.org)
- **Visualizations**: [Plotly](https://plotly.com)

---

## **Installation**

### **Prerequisites**
1. Python 3.8 or higher installed on your system.
2. Required Python libraries:
   - `streamlit`
   - `pandas`
   - `numpy`
   - `statsmodels`
   - `plotly`

### **Steps to Install and Run**
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/YourUsername/trade-impact-analysis.git
   cd trade-impact-analysis
