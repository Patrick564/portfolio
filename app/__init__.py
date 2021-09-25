import os

from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SENDGRID_KEY=os.environ.get('SENDGRID_KEY'),
        MY_EMAIL=os.environ.get('MY_EMAIL')
    )

    from . import portfolio

    app.register_blueprint(portfolio.bp)

    return app
