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
    return dict or None of ID Value can not be found
    """
    id = request.args.get('login_as', None)
    if id is not None and int(id) in users.keys():
        return users.get(int(id))
    return None


@app.before_request
def before_request():
    """
    To add users to flask if user is found
    """
    user = get_user()
    g.user = user


@babel.localeselector
def get_locale():
    """
    Select and do return to determine the best match
    with our supported languages.
    """
    local = request.args.get('locale')
    if local in app.config['LANGUAGES']:
        return local

    return request.accept_languages.supported_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def index() -> str:
    """
    Handle the app routing
    """
    return render_template('5-index.html')


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", debug=True)
