import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import load_and_clean_data
from plotly.subplots import make_subplots
from utils.utils import download_cleaned_data, get_distinct_colors, create_stacked_bar_chart
from functools import lru_cache

# ========== CACHING & OPTIMIZATION ==========
@st.cache_data
def get_cached_colors(num_colors):
    """Cache color generation to avoid recalculation."""
    return get_distinct_colors(num_colors)

@st.cache_data
def prepare_component_colors(components):
    """Create and cache color mapping for components."""
    return dict(zip(sorted(components), get_cached_colors(len(components))))

# ========== HELPER FUNCTIONS ==========
def create_percentage_share(df, group_cols):
    """Calculate percentage share for grouped data."""
    return (
        df.groupby(group_cols)['value']
        .transform(lambda x: (x / x.sum() * 100) if x.sum() > 0 else 0)
    )

# ========== MAIN DASHBOARD FUNCTION ==========
def create_expenditure_dashboard(
    page_title,
    data_path,
    download_filename,
    tab1_title,
    tab2_title,
    tab3_title,
    tab4_title
):
    """
    Enhanced reusable function to create expenditure analysis dashboard.
    
    Improvements:
    - Caching for performance optimization
    - DRY principles applied
    - Better error handling
    - Responsive UI with metrics
    - Improved interactivity
    """
    
    st.set_page_config(page_title=page_title, layout="wide")
    st.title(page_title)
    
    # ===== DATA LOADING =====
    df_full = load_and_clean_data(data_path)
    
    if df_full.empty:
        st.error(f"⚠️ No data found in {data_path}. Please check the file path.")
        st.stop()
    
    # ===== DOWNLOAD SECTION =====
    with st.container(border=True):
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            csv_data = download_cleaned_data(df_full)
            st.download_button(
                label="📥 Download Cleaned Data",
                data=csv_data,
                file_name=download_filename,
                mime="text/csv",
                use_container_width=True
            )
        with col3:
            st.metric(
                label="Records",
                value=f"{len(df_full):,}",
                delta=f"{len(df_full['state'].unique())} states"
            )
    
    # ===== PREPARE DATA =====
    all_components = sorted(df_full['component'].unique())
    component_colors = prepare_component_colors(all_components)
    states_list = sorted(df_full['state'].unique())
    years_list = sorted(df_full['year'].unique())
    
    # ===== TABS =====
    tab1, tab2, tab3, tab4 = st.tabs([tab1_title, tab2_title, tab3_title, tab4_title])
    
    # ========== TAB 1: PERCENTAGE COMPOSITION ==========
    with tab1:
        st.subheader(tab1_title)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            selected_states = st.multiselect(
                "Select States",
                states_list,
                default=states_list[:2] if len(states_list) >= 2 else states_list,
                key="tab1_states"
            )
        with col2:
            st.caption(f"📊 {len(selected_states)} selected")
        
        if selected_states:
            df_tab1 = df_full[df_full['state'].isin(selected_states)].copy()
            df_tab1['share_%'] = create_percentage_share(df_tab1, ['state', 'year'])
            
            fig = make_subplots(
                rows=1, cols=len(selected_states),
                specs=[[{'type': 'bar'} for _ in selected_states]],
                subplot_titles=selected_states,
                horizontal_spacing=0.12
            )
            
            for idx, state in enumerate(selected_states, 1):
                df_state = df_tab1[df_tab1['state'] == state].sort_values(['year', 'component'])
                
                for component in all_components:
                    df_comp = df_state[df_state['component'] == component]
                    if df_comp.empty:
                        continue
                    
                    fig.add_trace(
                        go.Bar(
                            x=df_comp['year'],
                            y=df_comp['share_%'],
                            name=component,
                            showlegend=(idx == 1),
                            marker_color=component_colors[component],
                            hovertemplate=f"<b>{component}</b><br>Year: %{{x}}<br>Share: %{{y:.1f}}%<extra></extra>",
                            legendgroup=component,
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
                height=max(500, len(selected_states) * 80),
                hovermode='x unified',
                legend=dict(yanchor="top", y=0.99, xanchor="left", x=1.02),
                dragmode='zoom',
                margin=dict(b=50, l=50, r=50, t=50)
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # ========== TAB 2: RAW VALUE COMPOSITION ==========
    with tab2:
        st.subheader(tab2_title)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            selected_states = st.multiselect(
                "Select States",
                states_list,
                default=states_list[:2] if len(states_list) >= 2 else states_list,
                key="tab2_states"
            )
        with col2:
            st.caption(f"📊 {len(selected_states)} selected")
        
        if selected_states:
            df_tab2 = df_full[df_full['state'].isin(selected_states)].copy()
            
            fig = make_subplots(
                rows=1, cols=len(selected_states),
                specs=[[{'type': 'bar'} for _ in selected_states]],
                subplot_titles=selected_states,
                horizontal_spacing=0.12
            )
            
            for idx, state in enumerate(selected_states, 1):
                df_state = df_tab2[df_tab2['state'] == state].sort_values(['year', 'component'])
                
                for component in all_components:
                    df_comp = df_state[df_state['component'] == component]
                    if df_comp.empty:
                        continue
                    
                    fig.add_trace(
                        go.Bar(
                            x=df_comp['year'],
                            y=df_comp['value'],
                            name=component,
                            showlegend=(idx == 1),
                            marker_color=component_colors[component],
                            hovertemplate=f"<b>{component}</b><br>Year: %{{x}}<br>Value: ₹%{{y:,.0f}} Cr<extra></extra>",
                            legendgroup=component,
                        ),
                        row=1, col=idx
                    )
                
                fig.update_xaxes(title_text="Year", row=1, col=idx)
                if idx == 1:
                    fig.update_yaxes(title_text="Value (₹ Crores)", row=1, col=idx)
            
            fig.update_layout(
                barmode='stack',
                height=max(500, len(selected_states) * 80),
                hovermode='x unified',
                legend=dict(yanchor="top", y=0.99, xanchor="left", x=1.02),
                dragmode='zoom',
                margin=dict(b=50, l=50, r=50, t=50)
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # ========== TAB 3: PERCENTAGE COMPOSITION BY STATE ==========
    with tab3:
        st.subheader(tab3_title)
        
        col1, col2 = st.columns(2)
        with col1:
            selected_year = st.selectbox("Select Year", years_list, index=len(years_list)-1, key="tab3_year")
        with col2:
            sort_component = st.selectbox(
                "Sort by Component (%)",
                options=["None"] + all_components,
                key="tab3_sort_component"
            )
        
        df_tab3 = df_full[df_full['year'] == selected_year].copy()
        df_tab3['share_%'] = create_percentage_share(df_tab3, ['state'])
        
        # Sort logic
        if sort_component != "None":
            state_order = (
                df_tab3[df_tab3['component'] == sort_component]
                .sort_values('share_%', ascending=False)['state']
                .tolist()
            )
            df_tab3['state'] = pd.Categorical(df_tab3['state'], categories=state_order, ordered=True)
            df_tab3 = df_tab3.sort_values(['state', 'component'])
        else:
            df_tab3 = df_tab3.sort_values(['state', 'component'])
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("States", len(df_tab3['state'].unique()))
        with col2:
            st.metric("Components", len(df_tab3['component'].unique()))
        with col3:
            st.metric("Year", selected_year)
        with col4:
            total_value = df_tab3['value'].sum()
            st.metric("Total Value", f"₹{total_value:,.0f} Cr")
        
        # Chart
        fig = create_stacked_bar_chart(
            data=df_tab3,
            x_col='share_%',
            y_col='state',
            color_col='component',
            colors=component_colors,
            title=f"{tab3_title} - {selected_year}",
            height=max(400, len(df_tab3['state'].unique()) * 35),
            x_label="Percentage (%)",
            y_label="State",
            is_percentage=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # ========== TAB 4: RAW COMPOSITION BY STATE ==========
    with tab4:
        st.subheader(tab4_title)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            selected_year = st.selectbox("Select Year", years_list, index=len(years_list)-1, key="tab4_year")
        with col2:
            st.caption(f"📊 Showing data for {selected_year}")
        
        df_tab4 = df_full[df_full['year'] == selected_year].copy()
        df_tab4 = df_tab4.sort_values(['state', 'component'])
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("States", len(df_tab4['state'].unique()))
        with col2:
            st.metric("Components", len(df_tab4['component'].unique()))
        with col3:
            st.metric("Year", selected_year)
        with col4:
            total_value = df_tab4['value'].sum()
            st.metric("Total Value", f"₹{total_value:,.0f} Cr")
        
        # Chart
        fig = create_stacked_bar_chart(
            data=df_tab4,
            x_col='value',
            y_col='state',
            color_col='component',
            colors=component_colors,
            title=f"{tab4_title} - {selected_year}",
            height=max(400, len(df_tab4['state'].unique()) * 35),
            x_label="Value (₹ Crores)",
            y_label="State",
            is_percentage=False
        )
        
        st.plotly_chart(fig, use_container_width=True)