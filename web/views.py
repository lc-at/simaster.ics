from flask import Blueprint, request, render_template

from .simaster import get_simaster_session
from .calendar import get_events_ics

bp = Blueprint("views", __name__)


@bp.route("/")
def homepage():
    return render_template("index.html")


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

    return get_events_ics(events), {"content-type": "text/calendar"}
