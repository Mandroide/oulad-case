"""Smoke-test that bulk_insert can run end-to-end without FK errors."""
import pathlib
import pandas as pd
import pytest

from oulad_etl.etl import ddl_loader, load
from oulad_etl.etl.models import TablesSchema

# --- tiny golden dataset ----------------------------------------------------
BASE = pathlib.Path(__file__).with_suffix("")  # same dir
RAW = {
    TablesSchema.assessments: pd.DataFrame(
        [{"id_assessment": 1, "code_module": "AAA", "code_presentation": "2013J"}]
    ),
    TablesSchema.studentAssessment: pd.DataFrame(
        [{"id_student": 42, "id_assessment": 1, "date_submitted": 1, "is_banked": 0, "score": 90.0}]
    ),
}
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session", autouse=True)
def ddl_applied():
    """Apply DDL once per test session."""
    ddl_loader.apply_ddl()


def test_bulk_insert_roundtrip(tmp_path):
    # Use tmp_path so the test DB is clean
    load.bulk_insert(RAW)

    # quick row-count sanity check
    engine = load._schema_engine()
    with engine.begin() as conn:
        rows = conn.execute("SELECT COUNT(*) FROM studentAssessment").scalar_one()
        assert rows == 1
