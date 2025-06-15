import logging
import pathlib

import mysql.connector

from ..settings import settings

log = logging.getLogger(__name__)


def apply_ddl() -> None:
    """Apply every *.sql file in config/ddl in lexical order."""
    try:
        cnx = mysql.connector.connect(
            host=settings.db_host,
            port=settings.db_port,
            user=settings.db_user,
            password=settings.db_password,
            autocommit=True,
        )
        cur = cnx.cursor()
        ddl_dir = pathlib.Path(__file__).resolve().parents[3] / "config" / "ddl"
        for sql_file in sorted(ddl_dir.glob("*.sql")):
            sql_text = pathlib.Path(sql_file).read_text()
            for stmt in filter(None, (s.strip() for s in sql_text.split(";"))):
                cur.execute(stmt)
            log.info("Applied %s", sql_file.name)
        cur.close()
        cnx.close()
    except (mysql.connector.Error, IOError) as exc:
        log.error("Failed to apply DDL: %s", exc)
        raise
