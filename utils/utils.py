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