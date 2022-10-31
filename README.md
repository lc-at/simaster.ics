# `simaster.ics`

Simple Python-based web app to generate an iCalendar file from SIMASTER courses
schedule.

## Quick Usage

1.  Open the [demo](https://simaster-ics.onrender.com) or your server URL if
    you self-hosted it.
2.  Fill in all the fields
3.  Copy the iCalendar URL
4.  Subscribe to it using your preferred calendar app (e.g. Google Calendar)

## API

Once you have deployed simaster.ics (or, just use the
[demo](https://simaster-ics.onrender.com), you can directly utilize its API to
make an iCalendar file.

-   Method: `GET`
-   URI: `/ics`
-   Parameters:
    -   `username`: your SIMASTER account username
    -   `password`: your SIMASTER account password
    -   `period`: calendar period (e.g. `20212`, `20211`)
    -   `type`: optional, calendar event type (possible values: `exam`, `class`)
    -   `reuse_session`: optional, cache and reuse session (possible values:
        `0`, `1`)

## Deployment

Before deploying, make sure that you have already installed the requirements
(e.g. by using `pip install -r requirements.txt`).

-   Gunicorn: `gunicorn wsgi:app`
-   Flask Development Server: `python wsgi.py`
-   Heroku: use the provided (or your own) `Procfile`
-   Docker: use the `Dockerfile`
    -   `docker build . -t simasterics`
    -   `docker run -p 8000:8000 simasterics`

## License

Distributed under the MIT License.

## Contribution

Any form of contribution is highly appreciated. Feel free to contribute (or
maybe even [buying me a cofffee](https://github.com/ttycelery)).
