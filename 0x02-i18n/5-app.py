#!/usr/bin/env python3
""" Setup a basic Flask app """

import locale
from flask import Flask, render_template, request, g
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
    Return user dict or None if the ID cannot be found.
    """
    user_id = request.args.get('login_as', None)
    if user_id is not None and int(user_id) in users:
        return users.get(int(user_id))
    return None


@app.before_request
def before_request():
    """
    Set global user (g.user) before handling the request.
    """
    user = get_user()
    g.user = user


@babel.localeselector
def get_locale():
    """
    Determine the best match for locale.
    """
    locale_param = request.args.get('locale')
    if locale_param in app.config['LANGUAGES']:
        return locale_param
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def index() -> str:
    """
    Render the homepage.
    """
    return render_template('5-index.html')


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", debug=True)
