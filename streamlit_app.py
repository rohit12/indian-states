import streamlit as st
from utils.constants import indian_states, state_colors1
import plotly.express as px
st.set_page_config(page_title="Indian States Dashboard", layout="wide")

st.title("🏛️ Indian States Dashboard")
st.markdown("""
Welcome to the dashboard!  

Use the sidebar to explore different statistics:

- 📊 State Revenue Receipts
""")

color_map = {state: state_colors1[i % len(state_colors1)] for i, state in enumerate(indian_states)}
px.defaults.color_discrete_map = color_map
