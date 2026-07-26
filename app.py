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


# ==========================================================
# STEP 6 : EDA DASHBOARD
# ==========================================================

st.header("📈 Exploratory Data Analysis")

st.subheader("Dataset Information")

col1, col2 = st.columns(2)

with col1:
    st.write("Shape")
    st.write(clean_df.shape)

with col2:
    st.write("Missing Values")
    st.dataframe(clean_df.isnull().sum().reset_index().rename(
        columns={"index":"Column",0:"Missing Values"}
    ))

st.subheader("Statistical Summary")
st.dataframe(clean_df.describe())

st.subheader("Data Types")
dtype_df = pd.DataFrame({
    "Column": clean_df.columns,
    "Datatype": clean_df.dtypes.astype(str)
})

st.dataframe(dtype_df)

# ==========================================================
# STEP 7 : INTERACTIVE VISUALIZATIONS
# ==========================================================

st.header("📊 Interactive Visualizations")

# Revenue vs Cost vs Profit
financial_summary = pd.DataFrame({
    "Metric":["Revenue","Cost","Profit"],
    "Amount":[
        clean_df["Sales"].sum(),
        clean_df["Cost"].sum(),
        clean_df["Gross Profit"].sum()
    ]
})

fig = px.bar(
    financial_summary,
    x="Metric",
    y="Amount",
    text="Amount",
    title="Revenue vs Cost vs Profit"
)

st.plotly_chart(fig, use_container_width=True)

# Revenue by Division
division_sales = (
    clean_df.groupby("Division")["Sales"]
    .sum()
    .reset_index()
)

fig = px.bar(
    division_sales,
    x="Division",
    y="Sales",
    color="Division",
    title="Revenue by Division"
)

st.plotly_chart(fig, use_container_width=True)

# Profit by Division
division_profit = (
    clean_df.groupby("Division")["Gross Profit"]
    .sum()
    .reset_index()
)

fig = px.bar(
    division_profit,
    x="Division",
    y="Gross Profit",
    color="Division",
    title="Profit by Division"
)

st.plotly_chart(fig, use_container_width=True)


# ==========================================================
# STEP 8 : PRODUCT PROFITABILITY ANALYSIS
# ==========================================================

st.header("💰 Product Profitability Analysis")

product_profitability = clean_df.groupby("Product Name").agg({
    "Sales":"sum",
    "Cost":"sum",
    "Units":"sum",
    "Gross Profit":"sum"
}).reset_index()

product_profitability["Gross Margin %"] = (
    product_profitability["Gross Profit"]
    /
    product_profitability["Sales"]
) * 100

st.subheader("Top 10 Products by Gross Profit")

top_profit = product_profitability.nlargest(
    10,
    "Gross Profit"
)

fig = px.bar(
    top_profit,
    x="Gross Profit",
    y="Product Name",
    orientation="h",
    color="Gross Profit"
)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(top_profit)

# ==========================================================
# STEP 9 : DIVISION PERFORMANCE ANALYSIS
# ==========================================================

st.header("🏢 Division Performance")

division_summary = clean_df.groupby("Division").agg({
    "Sales":"sum",
    "Cost":"sum",
    "Gross Profit":"sum",
    "Units":"sum"
}).reset_index()

division_summary["Gross Margin %"] = (
    division_summary["Gross Profit"]
    /
    division_summary["Sales"]
) * 100

st.dataframe(division_summary)

fig = px.bar(
    division_summary,
    x="Division",
    y="Gross Margin %",
    color="Division",
    title="Average Margin by Division"
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# STEP 10 : PARETO ANALYSIS
# ==========================================================

st.header("📈 Pareto Analysis")

pareto = product_profitability.sort_values(
    "Sales",
    ascending=False
)

pareto["Cumulative Revenue"] = pareto["Sales"].cumsum()

pareto["Cumulative %"] = (
    pareto["Cumulative Revenue"]
    /
    pareto["Sales"].sum()
) * 100

fig = px.line(
    pareto,
    x="Product Name",
    y="Cumulative %",
    title="80-20 Revenue Pareto Analysis"
)

st.plotly_chart(fig, use_container_width=True)


# ==========================================================
# STEP 11 : COST STRUCTURE DIAGNOSTICS
# ==========================================================

st.header("💸 Cost Structure Diagnostics")

fig = px.scatter(
    clean_df,
    x="Cost",
    y="Sales",
    color="Gross Profit",
    title="Cost vs Sales"
)

st.plotly_chart(fig, use_container_width=True)

cost_heavy = clean_df[
    clean_df["Cost"] >
    clean_df["Cost"].mean()
]

st.subheader("Cost Heavy Products")

st.dataframe(
    cost_heavy[
        [
            "Product Name",
            "Cost",
            "Sales",
            "Gross Profit"
        ]
    ]
)

# ==========================================================
# STEP 11 : COST STRUCTURE DIAGNOSTICS
# ==========================================================

st.header("💸 Cost Structure Diagnostics")

fig = px.scatter(
    clean_df,
    x="Cost",
    y="Sales",
    color="Gross Profit",
    title="Cost vs Sales"
)

st.plotly_chart(fig, use_container_width=True)

cost_heavy = clean_df[
    clean_df["Cost"] >
    clean_df["Cost"].mean()
]

st.subheader("Cost Heavy Products")

st.dataframe(
    cost_heavy[
        [
            "Product Name",
            "Cost",
            "Sales",
            "Gross Profit"
        ]
    ]
)

# ==========================================================
# STEP 12 : BUSINESS INSIGHTS
# ==========================================================

st.header("📌 Business Insights")

st.success("""
✔ Revenue is concentrated in a limited number of products.

✔ High-margin products should receive additional marketing support.

✔ Low-margin, high-sales products should be reviewed for pricing improvements.

✔ Cost-heavy products require supplier cost negotiation.

✔ Divisions with lower gross margins need operational improvements.

✔ Pareto analysis shows that a small percentage of products contribute the majority of revenue and profit.

✔ Focus on profitable products while reviewing consistently underperforming items.
""")

st.balloons()
