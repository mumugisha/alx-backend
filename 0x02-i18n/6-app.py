#!/usr/bin/env python3
"""Setup a basic Flask app"""

from flask import (
    Flask,
    render_template,
    request,
    g
)
from flask_babel import Babel

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


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


def get_user():
    """
    Return dict or None if ID value cannot be found.
    """
    user_id = request.args.get('login_as', None)
    if user_id is not None and int(user_id) in users.keys():
        return users.get(int(user_id))
    return None


@app.before_request
def before_request():
    """
    Add user to Flask's global context if the user is found.
    """
    user = get_user()
    g.user = user


@babel.localeselector
def get_locale():
    """
    Select and return the best match with our supported languages.
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


@app.route('/',  strict_slashes=True)
def index() -> str:
    """
    Handle the app routing.
    """
    return render_template('6-index.html')


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", debug=True)
