from flask import render_template, Blueprint, json, request
from HongAnSnapchat_app.api.process_selenium import process
import logging

api_bp = Blueprint("login_and_upload", __name__)


logger = logging.getLogger(__name__)


@api_bp.route("/")
def index():
    return render_template("index.html")


@api_bp.route("/login_and_upload", methods=["POST"])
def login_and_upload():
    try:
        _name = request.form["name"]
        _password = request.form["password"]
        _file = request.files["file"]

        result = process(name=_name, password=_password, file=_file)

        if result == 1:
            return json.dumps({"message": "Successfully !"})
        else:
            return json.dumps({"message": str(result)})

    except Exception as e:
        logger.critical(e)
        return json.dumps({"message": str(e)})
