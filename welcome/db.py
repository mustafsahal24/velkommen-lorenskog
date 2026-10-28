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

    Radene kan leses med kolonnenavn, for eksempel row["street"].
    """
    conn = sqlite3.connect(db_path or get_db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn