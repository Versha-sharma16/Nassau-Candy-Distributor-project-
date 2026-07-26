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

st.success("✅ Data Cleaning ")

# Cleaning Summary
summary = {
    "Original Rows": df.shape[0],
    "Rows After Cleaning": clean_df.shape[0],
    "Duplicates Removed": duplicates,
    "Missing Values Remaining": clean_df.isnull().sum().sum()
}

st.write(summary)

# ==========================================================
# STEP 4 : FEATURE ENGINEERING
# ==========================================================

st.header("⚙️ Feature Engineering")

# Gross Margin %
if "Sales" in clean_df.columns and "Gross Profit" in clean_df.columns:
    clean_df["Gross Margin %"] = (
        clean_df["Gross Profit"] / clean_df["Sales"]
    ) * 100

# Profit Per Unit
if "Units" in clean_df.columns and "Gross Profit" in clean_df.columns:
    clean_df["Profit Per Unit"] = (
        clean_df["Gross Profit"] / clean_df["Units"]
    )

# Total Profit Contribution
total_profit = clean_df["Gross Profit"].sum()

clean_df["Profit Contribution %"] = (
    clean_df["Gross Profit"] / total_profit
) * 100

st.success("✅ New Features Created")

st.dataframe(
    clean_df[
        [
            "Sales",
            "Gross Profit",
            "Gross Margin %",
            "Profit Per Unit",
            "Profit Contribution %"
        ]
    ].head()
)

# ==========================================================
# STEP 5 : KPI DASHBOARD
# ==========================================================

st.header("📊 KPI Dashboard")

total_sales = clean_df["Sales"].sum()
total_profit = clean_df["Gross Profit"].sum()
total_units = clean_df["Units"].sum()

gross_margin = (
    total_profit / total_sales
) * 100

products = clean_df["Product Name"].nunique()
divisions = clean_df["Division"].nunique()

c1, c2, c3 = st.columns(3)

c1.metric("💰 Revenue", f"${total_sales:,.2f}")
c2.metric("📈 Profit", f"${total_profit:,.2f}")
c3.metric("📦 Units", f"{int(total_units):,}")

c4, c5, c6 = st.columns(3)

c4.metric("📊 Margin", f"{gross_margin:.2f}%")
c5.metric("🛒 Products", products)
c6.metric("🏢 Divisions", divisions)
