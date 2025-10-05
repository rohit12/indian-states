import pandas as pd

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