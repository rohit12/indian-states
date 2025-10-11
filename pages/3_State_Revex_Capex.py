import streamlit as st
import pandas as pd
import plotly.express as px

st.title("State-wise Revenue and Capital Expenditure")

# --- Load and clean data ---
df = pd.read_csv("data/state_revex_capex.csv")

# Drop rows without states
df = df.dropna(subset=['States'])

df = df[~df['States'].str.strip().str.lower().isin(['total', 'all states', 'india total', 'grand total'])]

# Extract header info (REx/CEx alternating columns)
header_row = df.iloc[0]
df = df[1:].reset_index(drop=True)

# Build proper column names (e.g., 2022-23_REx, 2022-23_CEx)
new_cols = ['States']
for i in range(1, len(df.columns), 2):
    year = df.columns[i]
    new_cols.extend([f"{year}_REx", f"{year}_CEx"])
df.columns = new_cols

# --- Clean and convert to numeric safely ---
for col in new_cols[1:]:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.strip()
        .replace({"-": None, "–": None, "": None})
    )
    df[col] = pd.to_numeric(df[col], errors="coerce")

# --- Reshape to long format ---
df_long = df.melt(id_vars="States", var_name="Year_Type", value_name="Value")
df_long["Year"] = df_long["Year_Type"].str.extract(r"(\d{4}-\d{2})")
df_long["Type"] = df_long["Year_Type"].str.extract(r"(REx|CEx)")
df_long = df_long.drop(columns=["Year_Type"])

# Extract numeric year for sorting
df_long['Year_Start'] = df_long['Year'].str[:4].astype(int)

# Sort df_long by Year_Start ascending
df_long = df_long.sort_values(['Year_Start', 'States']).reset_index(drop=True)

# --- Year Slider ---
years = sorted(df_long["Year"].dropna().unique(), reverse=True)
selected_year = st.selectbox("Select Year", options=years, index=0)

# Filter for the selected year
df_year = df_long[df_long["Year"] == selected_year]
df_rex = df_year[df_year["Type"] == "REx"]
df_cex = df_year[df_year["Type"] == "CEx"]

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs([
    "💰 Revenue Expenditure (Bar)",
    "🏗️ Capital Expenditure (Bar)",
    "📈 Revenue Expenditure Trend (Line)",
    "📉 Capital Expenditure Trend (Line)"
])

# --- Tab 1: Revenue Expenditure Bar ---
with tab1:
    st.subheader(f"Revenue Expenditure by State ({selected_year})")
    fig_rex = px.bar(
        df_rex.sort_values("Value", ascending=False),
        x="States",
        y="Value",
        color="States",
        title=f"Revenue Expenditure by State ({selected_year})"
    )
    st.plotly_chart(fig_rex, use_container_width=True)

# --- Tab 2: Capital Expenditure Bar ---
with tab2:
    st.subheader(f"Capital Expenditure by State ({selected_year})")
    fig_cex = px.bar(
        df_cex.sort_values("Value", ascending=False),
        x="States",
        y="Value",
        color="States",
        title=f"Capital Expenditure by State ({selected_year})"
    )
    st.plotly_chart(fig_cex, use_container_width=True)

# --- Tab 3: Revenue Expenditure Trend ---
with tab3:
    st.subheader("Revenue Expenditure Trend (All Years)")
    df_rex_trend = df_long[df_long["Type"] == "REx"]
    fig_rex_line = px.line(
        df_long[df_long["Type"] == "REx"],
        x="Year",
        y="Value",
        color="States",
        title="Revenue Expenditure Trend by State (2012–2023)"
    )
    st.plotly_chart(fig_rex_line, use_container_width=True)

# --- Tab 4: Capital Expenditure Trend ---
with tab4:
    st.subheader("Capital Expenditure Trend (All Years)")
    df_cex_trend = df_long[df_long["Type"] == "CEx"]
    fig_cex_line = px.line(
        df_long[df_long["Type"] == "REx"],
        x="Year",
        y="Value",
        color="States",
        title="Capital Expenditure Trend by State (2012–2023)"
    )  
    st.plotly_chart(fig_cex_line, use_container_width=True)
