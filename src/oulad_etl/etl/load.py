from sqlalchemy import create_engine
from oulad_etl.settings import settings
import pandas as pd

def load(df: pd.DataFrame, table: str = "oulad_raw") -> None:
    engine = create_engine(settings.db_url, future=True)
    with engine.begin() as conn:
        df.to_sql(table, conn, if_exists="replace", index=False)