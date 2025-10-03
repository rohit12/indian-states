import streamlit as st
import pandas as pd
import plotly.express as px
from utils.constants import indian_states, indian_state_initials

state_to_initial = dict(zip(indian_states, indian_state_initials))

st.title("Indian States Finances Over Time 💰")

# Sidebar controls
states = st.multiselect("Select States", indian_states, default=indian_states)
rolling_average = st.checkbox("3-Year Rolling Average")

# Load data
data = pd.read_csv("State Finances CAG.csv")

# Convert to numeric
for col in data.columns[1:]:
    data[col] = pd.to_numeric(data[col].str.replace(",", ""), errors='coerce')

# Filter states
data_filtered = data[data['States'].isin(states)]

# Apply rolling average if selected
if rolling_average:
    data_filtered.iloc[:, 1:] = data_filtered.iloc[:, 1:].rolling(3, axis=1).mean()

# Melt to long form
data_long = data_filtered.melt(id_vars='States', var_name='Year', value_name='Value')
data_long['Year'] = data_long['Year'].str[:4].astype(int)  # convert to int
data_long['Initial'] = data_long['States'].map(state_to_initial)

# Tabs
tab1, tab2 = st.tabs(["Bar Chart", "Line Chart"])

with tab1:
    st.subheader("Revenue Bar Chart (Single Year)")
    year_selected = st.slider("Select Year", int(data_long['Year'].min()), int(data_long['Year'].max()), int(data_long['Year'].min()))

    # Filter by year
    data_year = data_long[data_long['Year'] == year_selected]
    data_year['Initial'] = data_year['States'].map(state_to_initial)

    fig_bar = px.bar(
        data_year,
        x="Value",
        y="States",
        orientation='h',
        text="Initial",
        color="States",
        labels={"Value": "Revenue (₹ Crores)", "States": "State"},
        template="plotly_white",
    )
    fig_bar.update_layout(
        yaxis=dict(autorange="reversed"),  # highest value on top
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
        labels={"Value": "Revenue (₹ Crores)"},
        template="plotly_white",
    )

    # Add initials at last year
    for state in states:
        df_state = data_long[data_long['States'] == state]
        last_point = df_state[df_state['Year'] == df_state['Year'].max()]
        fig_line.add_scatter(
            x=last_point['Year'],
            y=last_point['Value'],
            text=last_point['Initial'],
            mode='text',
            showlegend=False,
            textposition="middle right",
            textfont=dict(size=12, color="black")
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
