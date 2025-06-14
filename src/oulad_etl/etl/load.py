import pathlib
import sys

import pandas as pd
import sqlalchemy as sa
import logging
from ..settings import settings

engine = sa.create_engine(
    f"mysql+mysqlconnector://{settings.db_user}:{settings.db_password}"
    f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
)
log = logging.getLogger(__name__)


def load_raw(target: pathlib.Path) -> dict[str, pd.DataFrame]:
    """
    Load raw data from CSV file.
    :param target: Directory with csv files
    :return: Dictionary of dataframes
    """
    dataset = {}
    csv_tablas = {
        "assessments.csv": "assessments",
        "courses.csv": "courses",
        "studentAssessment.csv": "studentAssessment",
        "studentInfo.csv": "studentInfo",
        "studentRegistration.csv": "studentRegistration",
        "studentVle.csv": "studentVle",
        "vle.csv": "vle",
    }
    for file_name in csv_tablas:
        file_path = target / file_name
        try:
            df_name = file_name.replace(
                ".csv", ""
            )  # Nombre del DataFrame sin la extensión .csv
            dataset[df_name] = pd.read_csv(file_path)
            print(f"  - '{file_name}' cargado como '{df_name}'")
        except FileNotFoundError:
            logging.error("Expected %s not found", file_path)
            sys.exit(1)
    return dataset


def bulk_insert(dataset: dict[str, pd.DataFrame]) -> None:
    for relation, df in dataset.items():
        try:
            df.to_sql(
                name=relation,
                con=engine,
                if_exists="append",
                index=False,
                method="multi",
                chunksize=1000,
            )
            log.info(f" Datos insertados en la tabla '{relation}' desde '{relation}'")
        except Exception as e:
            log.error(f" Error al insertar '{relation}' en la tabla '{relation}': {e}")
