import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import load_and_clean_data
from utils.utils import download_cleaned_data, get_distinct_colors

def format_crore(value):
    """Format value in Crores with INR symbol."""
    if pd.isna(value):
        return "₹0 Cr"
    crore_value = value / 10_000_000
    if crore_value >= 1000:
        return f"₹{crore_value/1000:.1f}K Cr"
    return f"₹{crore_value:.1f} Cr"

st.set_page_config(page_title="Capital Expenditure Components", layout="wide")
st.title("Capital Expenditure Components")

# Download button at top
with st.container():
    col1, col2 = st.columns([1, 4])
    with col1:
        data_path = "data/states_capex_components.csv"
        df_full = load_and_clean_data(data_path)
        
        if not df_full.empty:
            csv_data = download_cleaned_data(df_full)
            st.download_button(
                label="📥 Download Cleaned Data",
                data=csv_data,
                file_name="cleaned_capex_component_data.csv",
                mime="text/csv"
            )

if df_full.empty:
    st.stop()

# Get distinct colors for all components
all_components = sorted(df_full['component'].unique())
component_colors = dict(zip(all_components, get_distinct_colors(len(all_components))))
color_sequence = [component_colors[comp] for comp in all_components]

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Capital Expenditure Composition (%)",
    "💰 Capital Expenditure Composition (Raw)",
    "📈 Component Share by State (%)",
    "📈 Component Share by State (Raw)"
])

# ==========================================
# Tab 1: Capital Expenditure Composition (%) Over Time
# ==========================================
with tab1:
    st.subheader("Capital Expenditure Composition Over Time (% of Total)")
    
    states = sorted(df_full['state'].unique())
    selected_states = st.multiselect(
        "Select States",
        states,
        default=states[:2] if len(states) >= 2 else states,
        key="tab1_states"
    )
    
    if selected_states:
        df_tab1 = df_full[df_full['state'].isin(selected_states)].copy()
        
        # Calculate percentages
        df_tab1['share_%'] = (
            df_tab1.groupby(['state', 'year'])['value']
            .transform(lambda x: (x / x.sum() * 100) if x.sum() > 0 else 0)
        )
        
        # Create subplots for each state
        from plotly.subplots import make_subplots
        
        fig = make_subplots(
            rows=1, cols=len(selected_states),
            specs=[[{'type': 'bar'} for _ in selected_states]],
            subplot_titles=selected_states,
            horizontal_spacing=0.12
        )
        
        for idx, state in enumerate(selected_states, 1):
            df_state = df_tab1[df_tab1['state'] == state].sort_values(['year', 'component'])
            
            for component in df_state['component'].unique():
                df_comp = df_state[df_state['component'] == component]
                
                fig.add_trace(
                    go.Bar(
                        x=df_comp['year'],
                        y=df_comp['share_%'],
                        name=component,
                        showlegend=(idx == 1),
                        marker_color=component_colors[component],
                        hovertemplate=f"<b>{component}</b><br>Year: %{{x}}<br>Share: %{{y:.1f}}%<extra></extra>",
                        legendgroup=component,
                        hoverinfo='skip'
                    ),
                    row=1, col=idx
                )
            
            fig.update_xaxes(title_text="Year", row=1, col=idx)
            if idx == 1:
                fig.update_yaxes(title_text="Percentage (%)", range=[0, 100], row=1, col=idx)
            else:
                fig.update_yaxes(range=[0, 100], row=1, col=idx)
        
        fig.update_layout(
            barmode='stack', 
            height=500, 
            hovermode='closest',
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=1.02),
            dragmode='zoom'
        )
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Tab 2: Capital Expenditure Composition (Raw) Over Time
# ==========================================
with tab2:
    st.subheader("Capital Expenditure Composition Over Time (Raw Values)")
    
    states = sorted(df_full['state'].unique())
    selected_states = st.multiselect(
        "Select States",
        states,
        default=states[:2] if len(states) >= 2 else states,
        key="tab2_states"
    )
    
    if selected_states:
        df_tab2 = df_full[df_full['state'].isin(selected_states)].copy()
        
        from plotly.subplots import make_subplots
        
        fig = make_subplots(
            rows=1, cols=len(selected_states),
            specs=[[{'type': 'bar'} for _ in selected_states]],
            subplot_titles=selected_states,
            horizontal_spacing=0.12
        )
        
        for idx, state in enumerate(selected_states, 1):
            df_state = df_tab2[df_tab2['state'] == state].sort_values(['year', 'component'])
            
            for component in df_state['component'].unique():
                df_comp = df_state[df_state['component'] == component]
                
                fig.add_trace(
                    go.Bar(
                        x=df_comp['year'],
                        y=df_comp['value'],
                        name=component,
                        showlegend=(idx == 1),
                        marker_color=component_colors[component],
                        hovertemplate=f"<b>{component}</b><br>Year: %{{x}}<br>Value: ₹%{{y:,.0f}} Cr<extra></extra>",
                        legendgroup=component,
                        hoverinfo='skip'
                    ),
                    row=1, col=idx
                )
            
            fig.update_xaxes(title_text="Year", row=1, col=idx)
            if idx == 1:
                fig.update_yaxes(title_text="Value (₹)", row=1, col=idx)
        
        fig.update_layout(
            barmode='stack', 
            height=500, 
            hovermode='closest',
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=1.02),
            dragmode='zoom'
        )
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Tab 3: Component Share by State (%) - Single Year
# ==========================================
with tab3:
    st.subheader("Component Share by State (% of Total)")
    
    col1, col2 = st.columns(2)
    with col1:
        years = sorted(df_full['year'].unique())
        selected_year = st.selectbox("Select Year", years, index=len(years)-1, key="tab3_year")
    
    df_tab3 = df_full[df_full['year'] == selected_year].copy()
    
    # Calculate percentages by state
    df_tab3['share_%'] = (
        df_tab3.groupby('state')['value']
        .transform(lambda x: (x / x.sum() * 100) if x.sum() > 0 else 0)
    )
    
    # Add dropdown to sort by component
    with col2:
        sort_component = st.selectbox(
            "Sort by Component (%)",
            options=["None"] + sorted(df_tab3['component'].unique()),
            key="tab3_sort_component"
        )
    
    # Sort by component percentage or state
    if sort_component != "None":
        # Create a pivot to sort by the selected component
        state_component_pct = df_tab3[df_tab3['component'] == sort_component].set_index('state')['share_%']
        state_order = state_component_pct.sort_values(ascending=False).index.tolist()
        df_tab3['state'] = pd.Categorical(df_tab3['state'], categories=state_order, ordered=True)
        df_tab3 = df_tab3.sort_values(['state', 'component'])
    else:
        df_tab3 = df_tab3.sort_values(['state', 'component'])
    
    # Add info about the data
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("States", len(df_tab3['state'].unique()))
    with col2:
        st.metric("Components", len(df_tab3['component'].unique()))
    with col3:
        st.metric("Year", selected_year)
    
    fig = px.bar(
        df_tab3,
        x='share_%',
        y='state',
        color='component',
        orientation='h',
        barmode='stack',
        title=f"Component Share by State - {selected_year} (%)",
        labels={'share_%': 'Percentage (%)', 'state': 'State', 'component': 'Component'},
        color_discrete_map=component_colors,
        height=max(400, len(df_tab3['state'].unique()) * 40),
        hover_data={'component': True, 'state': False, 'share_%': False}
    )
    
    fig.update_xaxes(range=[0, 100], title_text="Percentage (%)")
    fig.update_traces(
        hovertemplate='<b>%{customdata}</b><br>State: %{y}<br>Share: %{x:.1f}%<extra></extra>',
        legendgroup='component'
    )
    fig.update_layout(hovermode='closest', legend=dict(yanchor="top", y=0.99, xanchor="left", x=1.02))
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Tab 4: Component Share by State (Raw) - Single Year
# ==========================================
with tab4:
    st.subheader("Component Share by State (Raw Values)")
    
    years = sorted(df_full['year'].unique())
    selected_year = st.selectbox("Select Year", years, index=len(years)-1, key="tab4_year")
    
    df_tab4 = df_full[df_full['year'] == selected_year].copy()
    
    # Sort by state
    df_tab4 = df_tab4.sort_values(['state', 'component'])
    
    # Add info about the data
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("States", len(df_tab4['state'].unique()))
    with col2:
        st.metric("Components", len(df_tab4['component'].unique()))
    with col3:
        st.metric("Year", selected_year)
    
    fig = px.bar(
        df_tab4,
        x='value',
        y='state',
        color='component',
        orientation='h',
        barmode='stack',
        title=f"Component Share by State - {selected_year} (Raw Values)",
        labels={'value': 'Value (₹ Crores)', 'state': 'State', 'component': 'Component'},
        color_discrete_map=component_colors,
        height=max(400, len(df_tab4['state'].unique()) * 40),
        hover_data={'component': True, 'state': False, 'value': False}
    )
    
    fig.update_xaxes(title_text="Value (₹ Crores)")
    fig.update_traces(
        hovertemplate='<b>%{customdata}</b><br>State: %{y}<br>Value: ₹%{x:,.0f} Cr<extra></extra>',
        legendgroup='component'
    )
    fig.update_layout(hovermode='closest', legend=dict(yanchor="top", y=0.99, xanchor="left", x=1.02))
    st.plotly_chart(fig, use_container_width=True)