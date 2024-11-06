#!/usr/bin/env python3
""" Setup a basic Flask app """

import locale
from flask import (
    Flask,
    render_template,
    request,
    g
)
from flask_babel import Babel
from datetime import timezone as tmzn
from datetime import datetime
from pytz import timezone
import pytz.exceptions
from typing import (
    Dict,
    Union
)


class Config(object):
    """
    Babel configuration
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """
    return dict or None if ID value cannot be found
    """
    user_id = request.args.get('login_as', None)
    if user_id is not None and int(user_id) in users.keys():
        return users.get(int(user_id))
    return None


@app.before_request
def before_request():
    """
    Add user to Flask if the user is found
    """
    user = get_user()
    g.user = user
    time_now = pytz.utc.localize(datetime.utcnow())
    time = time_now.astimezone(timezone(get_timezone()))
    locale.setlocale(locale.LC_TIME, (get_locale(), 'UTF-8'))
    format = "%b %d, %Y %I:%M:%S %p"
    g.time = time.strftime(format)


@babel.localeselector
def get_locale():
    """
    Select and return the best match with our supported languages
    """
    local = request.args.get('locale')
    if local in app.config['LANGUAGES']:
        return local
    if g.user:
        local = g.user.get('locale')
        if local and local in app.config['LANGUAGES']:
            return local
        local = request.headers.get('locale', None)
        if local in app.config['LANGUAGES']:
            return local
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    """
    Check and return the right timezone
    """
    tzn = request.args.get('timezone', None)
    if tzn:
        try:
            return timezone(tzn).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    if g.user:
        try:
            tzn = g.user.get('timezone')
            return timezone(tzn).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    default = app.config['BABEL_DEFAULT_TIMEZONE']
    return default


@app.route('/', strict_slashes=False)
def index() -> str:
    """
    Handle the app routing
    """
    return render_template('7-index.html')


if __name__ == "__main__":
    app.run(port="5000", host="0.0.0.0", debug=True)