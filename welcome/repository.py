"""All databasetilgang for velkomsttjenesten.

Virker mot både SQLite og Azure SQL. Alle spørringer bruker parametere (?)
for å hindre SQL-injeksjon.
"""

from welcome.models import MoveInEvent


def _fetch_one(conn, sql: str, params: tuple = ()) -> dict | None:
    """Kjører en spørring og returnerer første rad som dictionary, eller None."""
    cursor = conn.cursor()
    cursor.execute(sql, params)
    row = cursor.fetchone()
    if row is None:
        return None
    columns = [column[0] for column in cursor.description]
    return dict(zip(columns, row))


def _fetch_all(conn, sql: str, params: tuple = ()) -> list[dict]:
    """Kjører en spørring og returnerer alle rader som dictionaries."""
    cursor = conn.cursor()
    cursor.execute(sql, params)
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def find_address(conn, street: str, postal_code: str) -> dict | None:
    """Finner en adresse og skolen den hører til."""
    return _fetch_one(
        conn,
        """
        SELECT a.id, a.street, a.postal_code,
               s.school_name, s.url AS school_url
        FROM addresses a
        JOIN school_districts s ON s.id = a.school_district_id
        WHERE LOWER(a.street) = LOWER(?)
          AND a.postal_code = ?
        """,
        (street, postal_code),
    )


def list_services(conn, has_children: bool) -> list[dict]:
    """Henter tjenestene som skal med. Familietjenester bare når man har barn."""
    return _fetch_all(
        conn,
        """
        SELECT category, title, description, url, audience
        FROM services
        WHERE audience = 'all'
           OR (audience = 'families' AND ? = 1)
        ORDER BY sort_order
        """,
        (int(has_children),),
    )


def find_welcome_by_event_id(conn, event_id: str) -> dict | None:
    """Finner en velkomst som allerede er laget for denne hendelsen."""
    return _fetch_one(
        conn,
        "SELECT id, message, created_at FROM welcome_messages WHERE event_id = ?",
        (event_id,),
    )


def get_welcome(conn, welcome_id: str) -> dict | None:
    """Henter en velkomst med sin id."""
    return _fetch_one(
        conn,
        "SELECT id, full_name, message, created_at FROM welcome_messages WHERE id = ?",
        (welcome_id,),
    )


def save_welcome(
    conn, welcome_id: str, event: MoveInEvent, address_id: int, message: str
) -> None:
    """Lagrer en ny velkomst. Databasen stopper duplikater via UNIQUE på event_id."""
    cursor = conn.cursor()
    cursor.execute(
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