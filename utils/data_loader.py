import pandas as pd

def load_finances(path="data/state_finances.csv"):
    df = pd.read_csv(path)
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", ""), errors='coerce')
    return df