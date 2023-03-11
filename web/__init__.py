import os

import dotenv
from flask import Flask

from .cryptutils import read_private_bytes_from_b64, derive_serialized_public_key


def create_app():
    dotenv.load_dotenv()
    app = Flask(__name__)

    private_key_b64 = os.getenv("SICS_PRIVATE_KEY")
    if os.getenv("SICS_ENABLE_PWD_ENC") == "1" and private_key_b64 is not None:
        private_key = read_private_bytes_from_b64(private_key_b64)
        app.config["ENABLE_PWD_ENC"] = True
        app.config["PRIVATE_KEY"] = private_key
        app.config["PUBLIC_KEY_PEM"] = derive_serialized_public_key(private_key)
    else:
        app.config["ENABLE_PWD_ENC"] = False
        app.config["PRIVATE_KEY"] = None
        app.config["PUBLIC_KEY_PEM"] = None

    from . import views

    app.register_blueprint(views.bp)

    return app
