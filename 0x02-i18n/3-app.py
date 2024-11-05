#!/usr/bin/env python3
""" Setup a basic Flask app"""

from flask import (
        Flask,
        render_template,
        request
)
from flask_babel import Babel


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


@babel.localeselector
def get_locale():
    """
    Select and return the best match with our supported languages.
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def index() -> str:
    """
    Handle the app routing
    """
    return render_template('3-index.html')


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", debug=True)
