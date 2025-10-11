import pandas as pd
import streamlit as st
import re

def load_state_finances(path="data/state_finances.csv"):
    df = pd.read_csv(path)
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", ""), errors='coerce')
    return df

def load_state_revenue_components(path="data/state_revenue_components.csv"):
    df = pd.read_csv(path)

    # Fill forward the state names (since only the "Total" row has the state name)
    df['State'] = df['Components'].where(df['Components'].str.contains('Total', na=False))
    df['State'] = df['State'].ffill()

    # Remove "(Total)" from state names
    df['State'] = df['State'].str.replace(r"\s*\(Total\)", "", regex=True)

    # Remove "Total" rows since we can compute totals ourselves later
    df = df[~df['Components'].str.contains('Total', na=False)]

    # Melt to long format
    df_long = df.melt(id_vars=['State', 'Components'], var_name='Year', value_name='Value')

    # Clean numeric values (remove commas, convert to int)
    df_long['Value'] = (
        df_long['Value']
        .astype(str)
        .str.replace(",", "")
        .astype(float)
    )

    # Check the result
    return df_long

# -------------------------------
# Data Loading and Cleaning
# -------------------------------
@st.cache_data
def load_and_clean_data(file_path: str):
    df_raw = pd.read_csv(file_path, index_col=0)
    
    all_data = []
    current_state = None
    state_pattern = re.compile(r'^([A-Za-z\s]+)\s*\(total\)$', re.IGNORECASE)
    
    for idx, row in df_raw.iterrows():
        # Check if this row is a state total row
        match = state_pattern.match(str(idx).strip())
        if match:
            current_state = match.group(1).strip()
        else:
            # This is a component row
            if current_state is not None:
                component = idx.strip()
                for year_col in df_raw.columns:
                    value = row[year_col]
                    
                    # Clean the value
                    value_str = str(value).strip()
                    value_str = value_str.replace(",", "").replace("₹", "")
                    value_str = value_str.replace("-", "").replace("nan", "").replace("None", "")
                    
                    if value_str:
                        try:
                            value_numeric = float(value_str)
                            all_data.append({
                                'state': current_state,
                                'component': component,
                                'year': int(re.search(r'\d{4}', year_col).group()),
                                'value': value_numeric
                            })
                        except (ValueError, AttributeError):
                            pass
    
    df_long = pd.DataFrame(all_data)
    
    if len(df_long) == 0:
        st.error("No data found. Please check the file format.")
        return pd.DataFrame()
    
    return df_long
