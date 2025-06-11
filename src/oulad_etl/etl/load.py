from sqlalchemy import create_engine
import pandas as pd

from ..settings import Settings


def load(df: pd.DataFrame, table: str = "oulad_raw") -> None:
    settings = Settings()
    db_url = f"mysql+pymysql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
    engine = create_engine(db_url, future=True)
    with engine.begin() as conn:
        df.to_sql(table, conn, if_exists="replace", index=False)
