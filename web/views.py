from flask import Blueprint, request, render_template, current_app

from .simaster import get_simaster_session, get_class_evdata, get_exam_evdata
from .evdata_processor import process_class_evdata, process_exam_evdata
from .cryptutils import decrypt_b64_password

bp = Blueprint("views", __name__)


@bp.route("/")
def homepage():
    return render_template("index.html")


@bp.route("/pub.pem")
def get_public_key():
    """Serves the public key if password encryption is enabled"""
    if not current_app.config["ENABLE_PWD_ENC"]:
        return {"error": "Password encryption is disabled"}, 404
    return current_app.config["PUBLIC_KEY_PEM"], {"Content-Type": "text/plain"}


@bp.route("/ics")
def get_icalendar():
    """Generates the iCalendar string as a response"""

    # mandatory
    username = request.args.get("username")
    password = request.args.get("password")
    period = request.args.get("period")

    # optional
    type_ = request.args.get("type")
    reuse_session = request.args.get("reuse_session")
    encrypt_password = request.args.get("encrypt_password")

    if not (username and password and period):
        return {"error": "Mandatory fields missing"}, 400
    elif not type_:
        type_ = "class"

    reuse_session = reuse_session == "1"
    encrypt_password = encrypt_password == "1"

    if encrypt_password:
        if not current_app.config["ENABLE_PWD_ENC"]:
            return {"error": "Password encryption is disabled"}, 400
        try:
            password = decrypt_b64_password(current_app.config["PRIVATE_KEY"], password)
        except Exception as e:
            return {"error": "Failed to decrypt password"}, 400

    ses = get_simaster_session(username, password, reuse_session)
    if not ses:
        return {"error": "Invalid username or password"}, 401

    title_suffix = f"({username} / {period})"

    try:
        if type_ == "class":
            evdata = get_class_evdata(ses, period)
            ics_str = process_class_evdata(evdata, f"SIMASTER Classes {title_suffix}")
        elif type_ == "exam":
            evdata = get_exam_evdata(ses, period)
            ics_str = process_exam_evdata(evdata, f"SIMASTER Exams {title_suffix}")
        else:
            return {"error": "Invalid type"}, 400
    except Exception as e:
        return {
            "error": "Failed to collect calendar events from SIMASTER, please file an issue"
        }, 500

    return ics_str, {"content-type": "text/calendar"}
