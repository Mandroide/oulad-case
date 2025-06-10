import pandas as pd
from pathlib import Path


def extract(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)
