"""Databasetilkobling for applikasjonen.

Bruker Azure SQL når AZURE_SQL_CONNECTIONSTRING er satt, ellers lokal SQLite.
"""

import os
import sqlite3
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = ROOT_DIR / "data" / "welcome.db"


def get_db_path() -> Path:
    """Returnerer stien til den lokale SQLite-databasen."""
    return Path(os.environ.get("DB_PATH", DEFAULT_DB_PATH))


def get_connection(db_path: Path | None = None):
    """Åpner en tilkobling til Azure SQL eller lokal SQLite."""
    connection_string = os.environ.get("AZURE_SQL_CONNECTIONSTRING")
    if connection_string and db_path is None:
        from mssql_python import connect

        return connect(connection_string)

    path = Path(db_path or get_db_path())
    if not path.exists():
        # Lager den lokale databasen hvis den mangler
        from scripts.init_db import init_db

        init_db(path)

    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn