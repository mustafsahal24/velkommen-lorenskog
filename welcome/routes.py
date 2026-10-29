"""HTTP-endepunktene for velkomsttjenesten."""

import hmac
import json
import logging
import os

import azure.functions as func

from welcome import repository, service
from welcome.db import get_connection
from welcome.models import MoveInEvent, ValidationError

bp = func.Blueprint()


def _json_response(
    body: dict, status_code: int, headers: dict | None = None
) -> func.HttpResponse:
    """Lager et JSON-svar. ensure_ascii=False beholder æ, ø og å som de er."""
    return func.HttpResponse(
        json.dumps(body, ensure_ascii=False),
        status_code=status_code,
        mimetype="application/json",
        headers=headers,
    )


def _is_authorized(req: func.HttpRequest) -> bool:
    """Sjekker at avsenderen kjenner den delte hemmeligheten."""
    expected = os.environ.get("WEBHOOK_SECRET", "")
    received = req.headers.get("X-Webhook-Secret", "")
    return bool(expected) and hmac.compare_digest(received, expected)


@bp.route(route="health", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def health(req: func.HttpRequest) -> func.HttpResponse:
    """Enkel helsesjekk som viser at tjenesten kjører."""
    return _json_response({"status": "ok"}, 200)


@bp.route(route="events/move-in", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def move_in(req: func.HttpRequest) -> func.HttpResponse:
    """Tar imot en flyttehendelse (webhook) og lager en velkomst."""
    if not _is_authorized(req):
        return _json_response({"error": "Ikke autorisert."}, 401)

    try:
        data = req.get_json()
    except ValueError:
        return _json_response({"error": "Ugyldig JSON."}, 400)

    try:
        event = MoveInEvent.from_dict(data)
    except ValidationError as exc:
        return _json_response({"error": str(exc)}, 400)

    conn = get_connection()
    try:
        result = service.handle_move_in(conn, event)
    except service.AddressNotFoundError as exc:
        return _json_response({"error": str(exc)}, 422)
    finally:
        conn.close()

    # Logger bare hendelses-id, aldri navn eller e-post
    logging.info(
        "Flyttehendelse behandlet: event_id=%s created=%s",
        event.event_id,
        result.created,
    )

    body = {"id": result.welcome_id, "created": result.created}
    if result.created:
        return _json_response(
            body, 201, headers={"Location": f"/api/welcome/{result.welcome_id}"}
        )
    return _json_response(body, 200)


@bp.route(route="welcome/{welcome_id}", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def get_welcome(req: func.HttpRequest) -> func.HttpResponse:
    """Henter en velkomst med sin id."""
    welcome_id = req.route_params.get("welcome_id", "")

    conn = get_connection()
    try:
        row = repository.get_welcome(conn, welcome_id)
    finally:
        conn.close()

    if row is None:
        return _json_response({"error": "Fant ikke velkomsten."}, 404)

    return _json_response(
        {"id": row["id"], "message": row["message"], "created_at": row["created_at"]},
        200,
    )