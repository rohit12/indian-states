import streamlit as st
import pandas as pd
import plotly.express as px
from utils.constants import indian_states, state_to_initial, state_colors
from utils.data_loader import load_state_finances
import plotly.express as px

# -------------------------
# App Title
# -------------------------
st.set_page_config(layout="wide")
st.title("📊 Indian State Finances Over Time 💰")

# -------------------------
# Sidebar Filters
# -------------------------
st.sidebar.header("Filters")

# State selection
states_selected = st.sidebar.multiselect(
    "Select States",
    options=indian_states,
    default=indian_states,
    format_func=lambda x: f"{x} ({state_to_initial[x]})"
)

# Combine multiple qualitative color palettes to get enough distinct colors
extended_colors = px.colors.qualitative.Dark24 + px.colors.qualitative.Alphabet + px.colors.qualitative.Light24

# Year selection for bar chart
data = load_state_finances()
data_long = data.melt(id_vars='States', var_name='Year', value_name='Value')
data_long['Year'] = data_long['Year'].str[:4].astype(int)
data_long['Initial'] = data_long['States'].map(state_to_initial)

year_min = int(data_long['Year'].min())
year_max = int(data_long['Year'].max())
year_selected = st.sidebar.slider(
    "Select Year for Bar Chart",
    year_min,
    year_max,
    year_min
)

# Filter selected states
data_long_filtered = data_long[data_long['States'].isin(states_selected)]

# -------------------------
# Tabs
# -------------------------
tab1, tab2 = st.tabs(["Bar Chart", "Line Chart"])

# -------------------------
# Tab 1: Bar Chart
# -------------------------
with tab1:
    st.subheader(f"Revenue Bar Chart for {year_selected}")

    data_year = data_long_filtered[data_long_filtered['Year'] == year_selected].sort_values("Value", ascending=True)

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
        hover_data={"Value": ":,.0f", "Initial": True}
    )
    fig_bar.update_traces(textposition="outside", textfont_size=12)
    fig_bar.update_layout(
        yaxis=dict(autorange="reversed"),
        xaxis=dict(separatethousands=True, tickprefix="₹"),
        showlegend=False,
        height=700,
        margin=dict(l=150, r=50, t=50, b=50),
        font=dict(family="Arial", size=14),
        title_text=f"Revenue by State ({year_selected})",
        title_font=dict(size=20, family="Arial")
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# -------------------------
# Tab 2: Line Chart
# -------------------------
with tab2:
    st.subheader("Revenue Line Chart (All Years)")
    states = data_long_filtered['States'].unique()

    # Map colors to states
    color_map = {state: extended_colors[i % len(extended_colors)] for i, state in enumerate(states)}
    fig_line = px.line(
        data_long_filtered,
        x="Year",
        y="Value",
        color="States",
        markers=True,
        color_discrete_map=color_map,
        labels={"Value": "Revenue (₹ Crores)"},
        hover_data={"Initial": True, "Value": ":,.0f"},
        template="plotly_white"
    )
    fig_line.update_layout(
        legend_title_text="State",
        xaxis=dict(tickmode='linear', dtick=1),
        yaxis=dict(separatethousands=True, tickprefix="₹"),
        hovermode="x unified",
        height=700,
        margin=dict(l=80, r=50, t=50, b=50),
        font=dict(family="Arial", size=14),
        title_text="Revenue Trends Across States",
        title_font=dict(size=20, family="Arial")
    )
    st.plotly_chart(fig_line, use_container_width=True)

# -------------------------
# Optional: Data Table
# -------------------------
with st.expander("View Revenue Data Table"):
    st.dataframe(data_long_filtered.sort_values(["Year", "Value"], ascending=[False, False]).reset_index(drop=True))
