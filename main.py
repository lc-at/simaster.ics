import sys
import json

from html2text import html2text
from ics import Calendar, Event


def main(events_fpath):
    try:
        events = json.load(open(events_fpath))['events']
    except Exception as e:  # noqa
        print(f'error: {e}', file=sys.stderr)
        sys.exit(-1)
    
    calendar = Calendar()

    for event_data in events:
        e = Event()
        e.name = event_data['title']
        e.description = html2text(event_data['description'])
        e.begin = event_data['start']
        e.end = event_data['end']
        calendar.events.add(e)

    print(calendar)


if __name__ == '__main__':
    if (len(sys.argv) != 2):
        print(f'usage: {sys.argv[0]} <events.json>', file=sys.stderr)
        sys.exit(-1)
    main(sys.argv[1])

