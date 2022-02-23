# `simaster.ics`
Simple Python-based web API to generate an iCalendar file from SIMASTER courses schedule. 

## Usage
Once you have deployed simaster.ics (or, just use the [demo](https://simaster-ics.herokuapp.com), you can directly utilize its API to make an iCalendar file.
- Method: `GET`
- URI: `/ics`
- Parameters:
  - `username`: your SIMASTER account username
  - `password`: your SIMASTER account password
  - `period`: calendar period (e.g. `20212`, `20211`)
  
URL Example: https://simaster-ics.herokuapp.com/ics?username=john.doe1999&password=myPassword&period=20212

Then, you can use the URL in some calendar services like Google Calendar (by subscribing to a URL).

## Deployment
Before deploying, make sure that you have already installed the requirements (e.g. by using `pip install -r requirements.txt`).

- Gunicorn: `gunicorn wsgi:app`
- Flask Development Server: `python wsgi.py`
- Heroku: use the provided (or your own) Procfile

## License
This small project is licensed under the MIT License.

## Contribution
Any form of contribution is highly appreciated. Feel free to contribute (or maybe even [buying me a cofffee](https://github.com/p4kl0nc4t)).
