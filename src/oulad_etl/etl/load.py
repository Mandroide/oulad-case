from __future__ import annotations

import logging
import pathlib
import sys
from typing import Dict

import pandas as pd
import sqlalchemy as sa
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from ..settings import settings
from .models import TablesSchema

log = logging.getLogger(__name__)

_BASE_URL = (
    f"mysql+mysqlconnector://{settings.db_user}:{settings.db_password}"
    f"@{settings.db_host}:{settings.db_port}"
)


def _base_engine() -> sa.Engine:  # no specific schema
    return sa.create_engine(_BASE_URL, pool_pre_ping=True, pool_recycle=3600)


def _schema_engine() -> sa.Engine:  # connects straight to oulad.<table>
    return sa.create_engine(f"{_BASE_URL}/{settings.db_name}", pool_recycle=3600)


def _ensure_schema_exists() -> None:
    with _base_engine().begin() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS `{settings.db_name}`"))


def load_raw(target: pathlib.Path) -> dict[str, pd.DataFrame]:
    """
    Load raw data from CSV file.
    :param target: Directory with csv files
    :return: Dictionary of dataframes
    """
    dataset = {}
    csv_tablas = {
        f"{TablesSchema.courses}.csv": TablesSchema.courses,
        f"{TablesSchema.studentInfo}.csv": TablesSchema.studentInfo,
        f"{TablesSchema.assessments}.csv": TablesSchema.assessments,
        f"{TablesSchema.vle}.csv": TablesSchema.vle,
        f"{TablesSchema.studentAssessment}.csv": TablesSchema.studentAssessment,
        f"{TablesSchema.studentRegistration}.csv": TablesSchema.studentRegistration,
        f"{TablesSchema.studentVle}.csv": TablesSchema.studentVle,
    }
    for file_name in csv_tablas:
        file_path = target / file_name
        try:
            df_name = file_name.replace(
                ".csv", ""
            )  # DataFrame name without csv extension
            dataset[df_name] = pd.read_csv(file_path)
            log.debug(f"  - '{file_name}' loaded as '{df_name}'")
        except FileNotFoundError:
            log.error("Expected %s not found", file_path)
            sys.exit(1)
    return dataset


def bulk_insert(dataset: Dict[str, pd.DataFrame]) -> None:
    """
    Idempotently load *dataset* into MySQL.

    1. FK-aware **topological sort** so parents load before children.
    2. Bulk load wrapped in `FOREIGN_KEY_CHECKS = 0/1` for speed *and*
       final validation.
    3. **TRUNCATE TABLE** before each insert so the pipeline is repeatable.
    4. **Single transaction** for the whole load block (one connection).
    5. Separate handling of `IntegrityError` with offending key values logged.
    """
    if not dataset:
        log.warning("bulk_insert() called with an empty dataset – nothing to do.")
        return

    _ensure_schema_exists()

    engine = _schema_engine()

    with engine.begin() as conn:  # one transaction / one connection
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))

        for table in dataset.keys():
            df = dataset[table]  # guaranteed present
            try:
                table = table.lower()
                # idempotency – remove old data first
                conn.execute(text(f"TRUNCATE TABLE `{table}`"))

                log.info("Loading %s rows into %s …", len(df), table)
                df.to_sql(
                    name=table,
                    schema=settings.db_name,
                    con=conn,  # reuse same conn/txn
                    if_exists="append",
                    index=False,
                    chunksize=5_000,
                )
            except IntegrityError as exc:
                bad_values = getattr(exc.orig, "params", None)
                log.error(
                    "IntegrityError while inserting into %s – offending values: %s",
                    table,
                    bad_values,
                )
                raise
            except sa.exc.ProgrammingError as exc:
                bad_values = getattr(exc.orig, "params", None)
                log.error(
                    "IntegrityError while inserting into %s – offending values: %s",
                    table,
                    bad_values,
                )
                raise
            except Exception as exc:
                log.error("Unexpected failure while inserting into %s", exc)
                raise

        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))  # forces re-validation
        log.info("Bulk load finished with FK checks re-enabled ✅")


def save_to_csv(df: pd.DataFrame, target_file_path: pathlib.Path) -> None:
    # Guardar resultado
    df.to_csv(target_file_path, index=False)
    log.info(f"ETL file save correctly in: {target_file_path}")
