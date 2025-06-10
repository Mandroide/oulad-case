import pandas as pd

def describe(df: pd.DataFrame) -> pd.DataFrame:
    """Return basic summary stats."""
    return df.describe(include="all")