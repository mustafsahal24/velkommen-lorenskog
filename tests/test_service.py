"""Tester for forretningslogikken i welcome.service."""

import pytest

from scripts.init_db import init_db
from welcome.db import get_connection
from welcome.models import MoveInEvent
from welcome.service import AddressNotFoundError, handle_move_in


@pytest.fixture
def conn(tmp_path):
    """Gir hver test en egen, ny testdatabase."""
    db_path = tmp_path / "test.db"
    init_db(db_path)
    connection = get_connection(db_path)
    yield connection
    connection.close()


def make_event(**overrides) -> MoveInEvent:
    """Lager en gyldig hendelse. Enkeltfelt kan overstyres i hver test."""
    data = {
        "event_id": "evt-1",
        "full_name": "Kari Nordmann",
        "email": "kari@example.no",
        "street": "Testgata 10",
        "postal_code": "1472",
        "has_children": False,
    }
    data.update(overrides)
    return MoveInEvent.from_dict(data)


def test_message_without_children_has_no_school(conn):
    result = handle_move_in(conn, make_event())

    assert result.created is True
    assert "Hei Kari" in result.message
    assert "Fjellhamar skole" not in result.message
    assert "helsenorge.no/fastlegen" in result.message


def test_message_with_children_includes_school_and_kindergarten(conn):
    result = handle_move_in(conn, make_event(has_children=True))

    assert "Fjellhamar skole" in result.message
    assert "Barnehage" in result.message


def test_same_event_twice_creates_only_one_welcome(conn):
    first = handle_move_in(conn, make_event())
    second = handle_move_in(conn, make_event())

    assert second.created is False
    assert second.welcome_id == first.welcome_id
    count = conn.execute("SELECT COUNT(*) FROM welcome_messages").fetchone()[0]
    assert count == 1


def test_unknown_address_raises_error(conn):
    with pytest.raises(AddressNotFoundError):
        handle_move_in(conn, make_event(street="Finnesikkeveien 1"))