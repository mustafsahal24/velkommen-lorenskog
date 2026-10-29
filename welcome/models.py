"""Dataformer og validering for flyttehendelser."""

import re
from dataclasses import dataclass
from enum import Enum

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
REQUIRED_FIELDS = ("event_id", "full_name", "email", "street", "postal_code")


class Audience(str, Enum):
    """Hvem en tjeneste gjelder for. Samme verdier som CHECK-regelen i databasen."""

    ALL = "all"
    FAMILIES = "families"


class ValidationError(ValueError):
    """Kastes når data i en forespørsel er ugyldige."""


def _text(value: object) -> str:
    """Gjør en verdi om til tekst uten mellomrom i endene. None blir tom tekst."""
    return "" if value is None else str(value).strip()


@dataclass(frozen=True)
class MoveInEvent:
    """En flyttehendelse: en ny innbygger har flyttet til kommunen."""

    event_id: str
    full_name: str
    email: str
    street: str
    postal_code: str
    has_children: bool = False

    @classmethod
    def from_dict(cls, data: object) -> "MoveInEvent":
        """Lager en MoveInEvent fra JSON-data, eller kaster ValidationError."""
        if not isinstance(data, dict):
            raise ValidationError("Forespørselen må være et JSON-objekt.")

        missing = [name for name in REQUIRED_FIELDS if not _text(data.get(name))]
        if missing:
            raise ValidationError(f"Mangler felt: {', '.join(missing)}.")

        email = _text(data["email"])
        if not EMAIL_PATTERN.match(email):
            raise ValidationError("Ugyldig e-postadresse.")

        has_children = data.get("has_children", False)
        if not isinstance(has_children, bool):
            raise ValidationError("has_children må være true eller false.")

        return cls(
            event_id=_text(data["event_id"]),
            full_name=_text(data["full_name"]),
            email=email.lower(),
            street=_text(data["street"]),
            postal_code=_text(data["postal_code"]),
            has_children=has_children,
        )