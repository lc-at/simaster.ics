import re
import random
import string

import cachelib
import requests
from lxml.html.soupparser import fromstring

BASE_URL = "https://simaster.ugm.ac.id"
HOME_URL = f"{BASE_URL}/beranda"
LOGIN_URL = f"{BASE_URL}/services/simaster/service_login"
HEADERS = {"UGMFWSERVICE": "1", "User-Agent": "SimasterICS/1.0.0"}

cache = cachelib.SimpleCache()


def get_simaster_session(username, password, reuse_session=False):
    # get session from cache, then return it if valid
    ses = cache.get(username)
    if ses and reuse_session:
        req = ses.get(HOME_URL)
        if 'simasterUGM_token' in req.text:
            return ses

    # create new session
    ses = requests.Session()
    req = ses.post(
        LOGIN_URL,
        data={
            "aId": "",
            "username": username,
            "password": password,
        },
        headers=HEADERS,
    )
    if req.status_code != 200:
        return None

    # update cache
    cache.set(username, ses)
    return ses


def get_class_evdata(ses, period):
    evdata = ses.get(f"{BASE_URL}/akademik/mhs_jadwal_kuliah/content_harian",
                     params={"sesi": period}).json()["events"]
    return evdata


def get_exam_evdata(ses, period):
    if len(period) != 5 or not period.isdigit():
        raise ValueError("invalid period")

    odd = period[4] == "1"
    year = int(period[:4])

    period_key = "Gasal" if odd else "Genap"
    period_key += f" {year}/{year + 1}"

    resp = ses.get(f"{BASE_URL}/akademik/mhs_jadwal_ujian/view")

    cal_sesid = re.findall(r"value='(.+?)'.*?" + period_key, resp.text)
    if not cal_sesid:
        return []
    cal_sesid = cal_sesid[0]
    resp = ses.get(f"{BASE_URL}/akademik/mhs_jadwal_ujian/content/{cal_sesid}")

    evdata = []
    tree = fromstring(resp.text)

    for table in tree.xpath("//table"):
        new_table = []
        for row in table.xpath(".//tr")[1:]:  # skip header
            new_row = []
            for field in row.iterchildren():
                new_row.append(field.text)
            new_table.append(new_row)
        evdata.append(new_table)

    return evdata
