from io import BytesIO
import pandas as pd
import plotly.express as px

def download_cleaned_data(df):
    """Generate downloadable CSV of cleaned data."""
    output = BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return output.getvalue()

def get_distinct_colors(n):
    """Generate n visually distinct colors."""
    # Use a combination of plotly color sequences
    colors = (
        px.colors.qualitative.Plotly +
        px.colors.qualitative.Set1 +
        px.colors.qualitative.Dark2 +
        px.colors.qualitative.Set2 +
        px.colors.qualitative.Pastel1 +
        px.colors.qualitative.Bold
    )
    # Remove duplicates while preserving order
    seen = set()
    distinct = []
    for color in colors:
        if color not in seen:
            seen.add(color)
            distinct.append(color)
    
    # Cycle through if we need more colors than available
    return [distinct[i % len(distinct)] for i in range(n)]

def create_stacked_bar_chart(
    data,
    x_col,
    y_col,
    color_col,
    colors,
    title,
    height,
    x_label="",
    y_label="",
    value_format=None,
    is_percentage=False
):
    """Create a reusable stacked bar chart with consistent styling."""
    fig = px.bar(
        data,
        x=x_col,
        y=y_col,
        color=color_col,
        orientation='h' if y_col != 'year' else 'v',
        barmode='stack',
        title=title,
        color_discrete_map=colors,
        height=height,
        labels={x_col: x_label, y_col: y_label, color_col: 'Component'}
    )
    
    if is_percentage:
        x_range = [0, 100]
        hover_template = '<b>%{customdata}</b><br>%{y}<br>Share: %{x:.1f}%<extra></extra>'
        x_axis_config = dict(range=x_range, title_text=x_label)
    else:
        hover_template = '<b>%{customdata}</b><br>%{y}<br>Value: ₹%{x:,.0f} Cr<extra></extra>'
        x_axis_config = dict(title_text=x_label)
    
    fig.update_xaxes(**x_axis_config)
    fig.update_traces(
        hovertemplate=hover_template,
        customdata=data[color_col]
    )
    fig.update_layout(
        hovermode='closest',
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=1.02),
        dragmode='zoom'
    )
    
    return fig