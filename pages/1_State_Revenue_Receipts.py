import streamlit as st
import pandas as pd
import plotly.express as px
from utils.constants import indian_states, state_to_initial, state_colors
from utils.data_loader import load_finances

st.title("📊 State Finances Over Time 💰")

# Sidebar filters
states = st.multiselect("Select States", indian_states, default=indian_states)

# Load data
data = load_finances()
data_filtered = data[data['States'].isin(states)]

# Melt into long form
data_long = data_filtered.melt(id_vars='States', var_name='Year', value_name='Value')
data_long['Year'] = data_long['Year'].str[:4].astype(int)
data_long['Initial'] = data_long['States'].map(state_to_initial)

# Tabs
tab1, tab2 = st.tabs(["Bar Chart", "Line Chart"])

with tab1:
    st.subheader("Revenue Bar Chart (Single Year)")
    year_selected = st.slider(
        "Select Year",
        int(data_long['Year'].min()),
        int(data_long['Year'].max()),
        int(data_long['Year'].min())
    )
    data_year = data_long[data_long['Year'] == year_selected]

    fig_bar = px.bar(
        data_year,
        x="Value",
        y="States",
        orientation='h',
        text="Initial",
        color="States",
        color_discrete_map=state_colors,
        labels={"Value": "Revenue (₹ Crores)", "States": "State"},
        template="plotly_white",
    )
    fig_bar.update_layout(
        yaxis=dict(autorange="reversed"),
        xaxis=dict(separatethousands=True),
        showlegend=False,
        width=1200,
        height=800,
        font=dict(family="Arial", size=14),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with tab2:
    st.subheader("Revenue Line Chart (All Years)")
    fig_line = px.line(
        data_long,
        x="Year",
        y="Value",
        color="States",
        markers=True,
        color_discrete_map=state_colors,
        labels={"Value": "Revenue (₹ Crores)"},
        template="plotly_white",
    )
    fig_line.update_layout(
        legend_title_text="State",
        xaxis=dict(tickmode='linear', dtick=1),
        yaxis=dict(separatethousands=True),
        hovermode="x unified",
        width=1200,
        height=800,
        font=dict(family="Arial", size=14),
    )
    st.plotly_chart(fig_line, use_container_width=True)