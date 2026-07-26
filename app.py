import streamlit as st
import pandas as pd

st.title("🍬 Nassau Candy Dashboard")

df = pd.read_csv("Nassau Candy Distributor.csv")

st.write(df.head())
