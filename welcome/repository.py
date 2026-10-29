"""All databasetilgang for velkomsttjenesten.

Resten av koden kaller funksjonene her og trenger ikke kjenne til SQL.
Alle spørringer bruker parametere (?) for å hindre SQL-injeksjon.
"""

import sqlite3

from welcome.models import MoveInEvent


def find_address(
    conn: sqlite3.Connection, street: str, postal_code: str
) -> sqlite3.Row | None:
    """Finner en adresse og skolen den hører til. Returnerer None hvis den ikke finnes."""
    return conn.execute(
        """
        SELECT a.id, a.street, a.postal_code,
               s.school_name, s.url AS school_url
        FROM addresses a
        JOIN school_districts s ON s.id = a.school_district_id
        WHERE a.street = ? COLLATE NOCASE
          AND a.postal_code = ?
        """,
        (street, postal_code),
    ).fetchone()


def list_services(conn: sqlite3.Connection, has_children: bool) -> list[sqlite3.Row]:
    """Henter tjenestene som skal med i velkomsten, i riktig rekkefølge.

    Tjenester for familier tas bare med når innbyggeren har barn.
    """
    return conn.execute(
        """
        SELECT category, title, description, url
        FROM services
        WHERE audience = 'all'
           OR (audience = 'families' AND ?)
        ORDER BY sort_order
        """,
        (int(has_children),),
    ).fetchall()


def find_welcome_by_event_id(
    conn: sqlite3.Connection, event_id: str
) -> sqlite3.Row | None:
    """Finner en velkomst som allerede er laget for denne hendelsen."""
    return conn.execute(
        "SELECT id, message, created_at FROM welcome_messages WHERE event_id = ?",
        (event_id,),
    ).fetchone()


def get_welcome(conn: sqlite3.Connection, welcome_id: str) -> sqlite3.Row | None:
    """Henter en velkomst med sin tilfeldige id."""
    return conn.execute(
        "SELECT id, full_name, message, created_at FROM welcome_messages WHERE id = ?",
        (welcome_id,),
    ).fetchone()


def save_welcome(
    conn: sqlite3.Connection,
    welcome_id: str,
    event: MoveInEvent,
    address_id: int,
    message: str,
) -> None:
    """Lagrer en ny velkomst. Databasen stopper duplikater via UNIQUE på event_id."""
    conn.execute(
        """
        INSERT INTO welcome_messages
            (id, event_id, full_name, email, address_id, has_children, message)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            welcome_id,
            event.event_id,
            event.full_name,
            event.email,
            address_id,
            int(event.has_children),
            message,
        ),
    )
    conn.commit()