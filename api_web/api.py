from flask import Blueprint, abort, request

from .simaster import get_simaster_session
from .calendar import get_events_ics

bp = Blueprint("api", __name__)


@bp.errorhandler(500)
def internal_server_error(e):
    return {"error": "Internal server error"}, 500


@bp.route("/ics")
def get_icalendar():
    username = request.args.get("username")
    password = request.args.get("password")
    period = request.args.get("period")

    if not (username and password and period):
        return {"error": "Missing fields"}, 400

    ses = get_simaster_session(username, password)
    if not ses:
        return {"error": "Invalid username or password"}, 401

    events = ses.get(
        "https://simaster.ugm.ac.id/akademik/mhs_jadwal_kuliah/content_harian",
        params={"sesi": period},
    ).json()["events"]

    return get_events_ics(events)
