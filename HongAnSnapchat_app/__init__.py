from flask import Flask
from HongAnSnapchat_app.api import rest_api


def create_app(flask_env=None, db_uri=None):
    app = Flask(__name__)

    app.register_blueprint(rest_api.api_bp, url_prefix="/")

    return app
