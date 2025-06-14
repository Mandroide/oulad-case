import mysql.connector
import pathlib
import logging

from ..settings import settings

log = logging.getLogger(__name__)


def apply_ddl():
    try:
        cnx = mysql.connector.connect(
            host=settings.db_host,
            port=settings.db_port,
            user=settings.db_user,
            password=settings.db_password,
        )
        cur = cnx.cursor()
        ddl_dir = pathlib.Path(__file__).parent.parent.parent.parent / "config/ddl"
        for sql_file in sorted(ddl_dir.glob("*.sql")):
            log.info("Applying %s", sql_file.name)
            cur.execute(open(sql_file).read())
        cur.close()
        cnx.close()
    except (mysql.connector.Error, IOError) as e:
        log.error("Failed to apply DDL: %s", e)
