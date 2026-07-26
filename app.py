import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
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
### Data Analyst Project
**Business Objective:** Analyze product profitability, division performance,
gross margins, Pareto contribution and cost structure.
""")

# -----------------------------
# LOAD DATA
# -----------------------------

import streamlit as st
import pandas as pd

# Load dataset
df = pd.read_csv("Nassau Candy Distributor.csv")

@st.cache_data
def load_data():
    return pd.read_csv("Nassau Candy Distributor.csv")

df = load_data()

st.header("📂 Dataset Preview")

col1, col2 = st.columns(2)

with col1:
    st.metric("Rows", df.shape[0])

with col2:
    st.metric("Columns", df.shape[1])

st.dataframe(df.head())


# ==========================================================
# STEP 3 : DATA CLEANING
# ==========================================================

st.header("🧹 Data Cleaning")

# Create a copy of original data
clean_df = df.copy()

# -----------------------------
# Remove duplicate rows
# -----------------------------
duplicates = clean_df.duplicated().sum()
clean_df.drop_duplicates(inplace=True)

# -----------------------------
# Fill missing Units with median
# -----------------------------
if "Units" in clean_df.columns:
    clean_df["Units"] = clean_df["Units"].fillna(clean_df["Units"].median())

# -----------------------------
# Remove rows where Sales <= 0
# -----------------------------
if "Sales" in clean_df.columns:
    clean_df = clean_df[clean_df["Sales"] > 0]

# -----------------------------
# Remove rows where Gross Profit is missing
# -----------------------------
if "Gross Profit" in clean_df.columns:
    clean_df = clean_df.dropna(subset=["Gross Profit"])

# -----------------------------
# Standardize Product Name
# -----------------------------
if "Product Name" in clean_df.columns:
    clean_df["Product Name"] = (
        clean_df["Product Name"]
        .astype(str)
        .str.strip()
        .str.title()
    )

# -----------------------------
# Standardize Division
# -----------------------------
if "Division" in clean_df.columns:
    clean_df["Division"] = (
        clean_df["Division"]
        .astype(str)
        .str.strip()
        .str.title()
    )

st.success("✅ Data Cleaning Completed Successfully")

# Cleaning Summary
summary = {
    "Original Rows": df.shape[0],
    "Rows After Cleaning": clean_df.shape[0],
    "Duplicates Removed": duplicates,
    "Missing Values Remaining": clean_df.isnull().sum().sum()
}

st.write(summary)

