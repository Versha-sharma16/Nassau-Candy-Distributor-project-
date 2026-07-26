import streamlit as st
import pandas as pd

st.title("🍬 Nassau Candy Dashboard")

df = pd.read_csv("Nassau Candy Distributor.csv")

st.write(df.head())

import plotly.express as px
import streamlit as st
import pandas as pd
import plotly.express as px

# Page title
st.title("Nassau Candy Distributor Analysis")

# Load dataset
df = pd.read_csv("Nassau Candy Distributor.csv")

# -----------------------------
# Data Cleaning
# -----------------------------
st.header("1. Data Cleaning")
# cleaning code...
st.write(df.head())

# -----------------------------
# EDA
# -----------------------------
st.header("2. Exploratory Data Analysis")
# summary statistics
st.write(df.describe())

# -----------------------------
# Visualizations
# -----------------------------
st.header("3. Sales by Division")
# create chart
st.plotly_chart(fig)

# -----------------------------
# Profitability Analysis
# -----------------------------
st.header("4. Profitability Analysis")
# show tables and charts

# -----------------------------
# Division Analysis
# -----------------------------
st.header("5. Division Analysis")

# -----------------------------
# Pareto Analysis
# -----------------------------
st.header("6. Pareto Analysis")

# -----------------------------
# Cost Structure Diagnostics
# -----------------------------
st.header("7. Cost Structure Diagnostics")

# -----------------------------
# Business Insights
# -----------------------------
st.header("8. Key Business Insights")
st.markdown("""
- Insight 1
- Insight 2
- Insight 3
""")
