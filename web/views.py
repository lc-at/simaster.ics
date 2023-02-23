from flask import Blueprint, request, render_template

from .simaster import get_simaster_session, get_class_evdata, get_exam_evdata
from .evdata_processor import process_class_evdata, process_exam_evdata

bp = Blueprint("views", __name__)


@bp.route("/")
def homepage():
    return render_template("index.html")


@bp.route("/ics")
def get_icalendar():
    username = request.args.get("username")
    password = request.args.get("password")
    period = request.args.get("period")
    type_ = request.args.get("type")
    reuse_session = request.args.get("reuse_session")

    if not (username and password and period):
        return {"error": "Missing fields"}, 400
    elif not type_:
        type_ = "class"

    if reuse_session and reuse_session.isdigit():
        reuse_session = bool(int(reuse_session))
    else:
        reuse_session = False

    ses = get_simaster_session(username, password, reuse_session)
    if not ses:
        return {"error": "Invalid username or password"}, 401

    title_suffix = f"({username} / {period})"

    if type_ == "class":
        evdata = get_class_evdata(ses, period)
        ics_str = process_class_evdata(
            evdata, f"SIMASTER Classes {title_suffix}")
    elif type_ == "exam":
        evdata = get_exam_evdata(ses, period)
        ics_str = process_exam_evdata(
            evdata, f"SIMASTER Exams {title_suffix}")
    else:
        return {"error": "Invalid type"}, 401

    return ics_str, {"content-type": "text/calendar"}
