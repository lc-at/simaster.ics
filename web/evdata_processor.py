from textwrap import dedent

import arrow
from html2text import html2text
from ics import Calendar, Event


TIMEZONE = "Asia/Jakarta"
LOCALE = "id_ID"


def process_class_evdata(events: list) -> str:
    def preprocess_time(s: str):
        return arrow.get(s, "YYYY-M-D HH:mm:ss", tzinfo=TIMEZONE)

    calendar = Calendar()

    for event_data in events:
        e = Event()
        e.name = event_data["title"]
        e.description = html2text(event_data["description"])
        e.begin = preprocess_time(event_data["start"])
        e.end = preprocess_time(event_data["end"])
        calendar.events.add(e)

    return str(calendar)


def process_exam_evdata(exam_tables: list) -> str:
    def preprocess_str(s: str):
        if not isinstance(s, str) and not s:
            return None
        s = s.strip()
        if not s:
            return None
        return s

    calendar = Calendar()

    for exam_type, exam_table in zip(("UTS", "UAS"), exam_tables):
        for row in exam_table:
            e = Event()
            row = [preprocess_str(e) for e in row]

            if not row[5] or not row[6]:
                continue
            time_span = row[6].split('-')
            dt_format = "D MMMM YYYY HH:mm"
            e.begin = arrow.get(f"{row[5]} {time_span[0]}",
                                dt_format, locale=LOCALE, tzinfo=TIMEZONE)
            e.end = arrow.get(f"{row[5]} {time_span[1]}",
                              dt_format, locale=LOCALE, tzinfo=TIMEZONE)

            e.name = f"[{exam_type}] {row[2]} ({row[4]})"
            e.description = dedent(f"""\
                    Kode: {row[1]}
                    SKS: {row[3]}
                    Ruangan: {row[7]}
                    No. kursi: {row[8]}
            """)
            calendar.events.add(e)

    return str(calendar)
