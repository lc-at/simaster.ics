import sys
import json

import arrow
from html2text import html2text
from ics import Calendar, Event


TIMEZONE = "Asia/Jakarta"


def preprocess_time(s: str):
    return arrow.get(s, "YYYY-M-D HH:mm:ss", tzinfo=TIMEZONE)


def get_events_ics(events: list) -> str:
    calendar = Calendar()

    for event_data in events:
        e = Event()
        e.name = event_data["title"]
        e.description = html2text(event_data["description"])
        e.begin = preprocess_time(event_data["start"])
        e.end = preprocess_time(event_data["end"])
        calendar.events.add(e)

    return str(calendar)
