import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="Nassau Candy Distributor Analysis",
    page_icon="🍬",
    layout="wide"
)

# -----------------------------
# TITLE
# -----------------------------
st.title("🍬 Nassau Candy Distributor Analysis Dashboard")
st.markdown("""
### Internship Project
**Business Objective:** Analyze product profitability, division performance,
gross margins, Pareto contribution and cost structure.
""")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Nassau Candy Distributor.csv")
    return df



st.header("📂 Dataset Preview")

col1, col2 = st.columns(2)

with col1:
    st.metric("Rows", df.shape[0])

with col2:
    st.metric("Columns", df.shape[1])

st.dataframe(df.head())





df = load_data()
