import pandas as pd


def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna()
    df.columns = [c.lower().strip() for c in df.columns]
    return df
