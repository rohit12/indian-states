import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_state_revenue_components

# =====================================================
# 🧠 CONFIG & SETUP
# =====================================================
st.set_page_config(
    page_title="State Finances Dashboard",
    layout="wide",
    page_icon="💰"
)

# =====================================================
# ⚡ DATA LOADING (CACHED)
# =====================================================
@st.cache_data
def load_data():
    df_long = load_state_revenue_components()

    # Ensure year order oldest → newest
    df_long['Year'] = pd.Categorical(
        df_long['Year'],
        ordered=True,
        categories=sorted(df_long['Year'].unique(), key=lambda x: int(x.split('-')[0]))
    )

    # Keep only valid components
    valid_components = [
        "States' Own Tax",
        "Share in Union Taxes",
        "Grants in Aid - CSS",
        "Grants in Aid - Others",
        "Non Tax Rev - Int, Div, Profit",
        "Non Tax Rev - Others"
    ]
    df_long = df_long[df_long['Components'].isin(valid_components)]
    df_long['Components'] = pd.Categorical(df_long['Components'], categories=valid_components, ordered=True)

    # Compute percentage of total per state-year
    df_long['Percent'] = df_long['Value'] / df_long.groupby(['State','Year'])['Value'].transform('sum') * 100

    return df_long

df_long = load_data()

# =====================================================
# 🎨 COLOR MAP
# =====================================================
color_map = {
    "States' Own Tax": "#1f77b4",
    "Share in Union Taxes": "#2ca02c",
    "Grants in Aid - CSS": "#ff7f0e",
    "Grants in Aid - Others": "#d62728",
    "Non Tax Rev - Int, Div, Profit": "#9467bd",
    "Non Tax Rev - Others": "#8c564b"
}

# =====================================================
# 📖 ABOUT SECTION
# =====================================================
with st.expander("ℹ️ About this dashboard"):
    st.markdown("""
    This dashboard visualizes **Indian state revenues** from **2012–13 to 2022–23**,  
    using data compiled from CAG and RBI.  
    - Tabs 1–2: Revenue trends over time for selected states  
    - Tabs 3–4: Yearly comparison across all states  
    - You can view data as raw ₹ crore values or % of total revenue
    """)

# =====================================================
# 📊 SUMMARY METRICS
# =====================================================
latest_year = df_long['Year'].cat.categories[-1]
latest_total = int(df_long[df_long['Year']==latest_year]['Value'].sum())
own_tax_share = df_long[(df_long['Year']==latest_year) & (df_long['Components']=="States' Own Tax")]['Percent'].mean()

cols = st.columns(3)
cols[0].metric("📅 Latest Year", latest_year)
cols[1].metric("💰 Total State Revenue", f"₹{latest_total:,} crore")
cols[2].metric("🏦 Avg Own Tax Share", f"{own_tax_share:.1f}%")

# =====================================================
# 📂 DOWNLOAD BUTTON
# =====================================================
st.download_button(
    label="⬇️ Download Cleaned Data",
    data=df_long.to_csv(index=False),
    file_name="state_revenue_data.csv",
    mime="text/csv"
)

# =====================================================
# 🧭 TABS
# =====================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Revenue Composition (%)",
    "💵 Revenue Composition (Raw)",
    "🏛️ Component Share by State (%)",
    "🏛️ Component Share by State (Raw)"
])

# =====================================================
# TAB 1 — % Composition Trend (Vertical)
# =====================================================
with tab1:
    st.subheader("Revenue Composition Over Time (% of Total)")
    states = st.multiselect(
        "Select States",
        sorted(df_long['State'].unique()),
        default=["Maharashtra", "Tamil Nadu"]
    )

    df_view = df_long[df_long['State'].isin(states)].copy()
    fig = px.bar(
        df_view,
        x="Year",
        y="Percent",
        color="Components",
        facet_col="State",
        barmode="stack",
        category_orders={"Year": list(df_long['Year'].cat.categories)},
        color_discrete_map=color_map,
        height=600
    )
    fig.update_layout(margin=dict(l=60,r=60,t=60,b=60))
    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# TAB 2 — Raw Trend (Vertical)
# =====================================================
with tab2:
    st.subheader("Revenue Composition Over Time (₹ crore)")
    states = st.multiselect(
        "Select States",
        sorted(df_long['State'].unique()),
        default=["Maharashtra", "Tamil Nadu"],
        key="raw_states"
    )

    df_view = df_long[df_long['State'].isin(states)].copy()
    fig = px.bar(
        df_view,
        x="Year",
        y="Value",
        color="Components",
        facet_col="State",
        barmode="stack",
        category_orders={"Year": list(df_long['Year'].cat.categories)},
        color_discrete_map=color_map,
        height=600
    )
    fig.update_layout(margin=dict(l=60,r=60,t=60,b=60))
    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# TAB 3 — Yearly State Comparison (%) (Horizontal)
# =====================================================
with tab3:
    st.subheader("Revenue Components by State (% of Total)")
    year = st.selectbox("Select Year", list(df_long['Year'].cat.categories), index=len(df_long['Year'].cat.categories)-1)
    df_year = df_long[df_long['Year']==year].copy()

    # Optional: add "All States" if needed, or skip "Total"
    # df_year['State'] = df_year['State'].replace("Total", "All States")

    fig = px.bar(
        df_year,
        x="Percent",
        y="State",
        color="Components",
        orientation='h',
        barmode='stack',
        color_discrete_map=color_map,
        height=700
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(l=100,r=40,t=60,b=60))
    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# TAB 4 — Yearly State Comparison (Raw) (Horizontal)
# =====================================================
with tab4:
    st.subheader("Revenue Components by State (₹ crore)")
    year = st.selectbox("Select Year", list(df_long['Year'].cat.categories), index=len(df_long['Year'].cat.categories)-1, key="raw_year")
    df_year = df_long[df_long['Year']==year].copy()

    # Remove any "Total" rows
    df_year = df_year[~df_year['Components'].str.contains("Total", case=False, na=False)]
    df_year = df_year[~df_year['State'].str.contains("Total", case=False, na=False)]

    fig = px.bar(
        df_year,
        x="Value",
        y="State",
        color="Components",
        orientation='h',
        barmode='stack',
        color_discrete_map=color_map,
        height=700
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(l=100,r=40,t=60,b=60))
    st.plotly_chart(fig, use_container_width=True)