from flask import Blueprint
from flask_restful import Api

from application import app
from src.api.resources.summ import SUMM


def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "content-type"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


def init_api():
    blueprint = Blueprint("api", __name__)
    api = Api(blueprint)

    api.add_resource(SUMM, "/api/v1/summarization", methods=["POST"])

    blueprint.after_request(add_cors_headers)
    app.register_blueprint(blueprint)
