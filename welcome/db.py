"""Databasetilkobling for applikasjonen."""

import os
import sqlite3
from pathlib import Path

# Standardsti brukes lokalt hvis miljøvariabelen DB_PATH ikke er satt
ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = ROOT_DIR / "data" / "welcome.db"


def get_db_path() -> Path:
    """Returnerer stien til databasen fra DB_PATH, eller standardstien."""
    return Path(os.environ.get("DB_PATH", DEFAULT_DB_PATH))

def get_connection(db_path: Path | None = None) -> sqlite3.Connection:
    """Åpner en tilkobling med fremmednøkler slått på.

    Finnes ikke databasen, lages den fra schema.sql og seed.sql.
    Radene kan leses med kolonnenavn, for eksempel row["street"].
    """
    path = Path(db_path or get_db_path())
    if not path.exists():
        # Midlertidig løsning for SQLite i skyen, erstattes av Azure SQL
        from scripts.init_db import init_db

        init_db(path)

    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn