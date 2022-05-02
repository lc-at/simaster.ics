import random
import string

import requests

LOGIN_URL = "https://simaster.ugm.ac.id/services/simaster/service_login"
HEADERS = {"UGMFWSERVICE": "1", "User-Agent": "SimasterICS/1.0.0"}


def get_simaster_session(username, password):
    ses = requests.Session()
    req = ses.post(
        LOGIN_URL,
        data={
            "aId": "".join(random.choice(string.hexdigits) for _ in range(16)).lower(),
            "username": username,
            "password": password,
        },
        headers=HEADERS,
    )
    if req.status_code != 200:
        return None
    return ses
