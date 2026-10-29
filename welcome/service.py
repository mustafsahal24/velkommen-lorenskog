"""Forretningslogikk: lager og lagrer velkomstmeldinger for nye innbyggere."""

import sqlite3
import uuid
from dataclasses import dataclass

from welcome import repository
from welcome.models import MoveInEvent


class AddressNotFoundError(Exception):
    """Adressen finnes ikke i adresseregisteret."""


@dataclass(frozen=True)
class WelcomeResult:
    """Resultatet av å behandle en flyttehendelse."""

    welcome_id: str
    message: str
    created: bool  # False betyr at hendelsen var behandlet fra før (duplikat)


def build_message(
    full_name: str,
    address: sqlite3.Row,
    services: list[sqlite3.Row],
    has_children: bool,
) -> str:
    """Lager teksten i velkomstmeldingen. Rører ikke databasen, så den er lett å teste."""
    first_name = full_name.split()[0]
    lines = [f"Hei {first_name}, og velkommen til Lørenskog!", ""]

    if has_children:
        lines.append(
            f"Skolen for adressen din er {address['school_name']}: {address['school_url']}"
        )
        lines.append("")

    lines.append("Her er noen nyttige steg de første ukene:")
    for service in services:
        lines.append(f"- {service['title']}: {service['description']} {service['url']}")

    lines.extend(["", "Vi er glade for å ha deg her!"])
    return "\n".join(lines)


def handle_move_in(conn: sqlite3.Connection, event: MoveInEvent) -> WelcomeResult:
    """Behandler en flyttehendelse. Samme hendelse to ganger gir samme velkomst."""
    existing = repository.find_welcome_by_event_id(conn, event.event_id)
    if existing is not None:
        return WelcomeResult(existing["id"], existing["message"], created=False)

    address = repository.find_address(conn, event.street, event.postal_code)
    if address is None:
        raise AddressNotFoundError("Fant ikke adressen i adresseregisteret.")

    services = repository.list_services(conn, event.has_children)
    message = build_message(event.full_name, address, services, event.has_children)
    welcome_id = str(uuid.uuid4())

    repository.save_welcome(conn, welcome_id, event, address["id"], message)
    return WelcomeResult(welcome_id, message, created=True)