"""Lager den lokale SQLite-databasen fra schema.sql og seed.sql.

Bruk (fra prosjektmappen):
    python scripts/init_db.py
"""
import sqlite3
from pathlib import Path

# Prosjektets rotmappe (mappen over scripts/)
ROOT_DIR = Path(__file__).resolve().parent.parent

DB_PATH = ROOT_DIR / "data" / "welcome.db"
SCHEMA_FILE = ROOT_DIR / "database" / "sqlite" / "schema.sql"
SEED_FILE = ROOT_DIR / "database" / "sqlite" / "seed.sql"

def init_db(db_path: Path = DB_PATH) -> None:
    """Sletter og lager tabellene på nytt, og legger inn testdata."""
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.executescript(SCHEMA_FILE.read_text(encoding="utf-8"))
        conn.executescript(SEED_FILE.read_text(encoding="utf-8"))
        conn.commit()
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
    print(f"Databasen er laget: {DB_PATH}")