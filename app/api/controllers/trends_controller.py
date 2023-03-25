# stdlib

# thirdparty
from sanic import Blueprint, HTTPResponse
from sanic_ext.extensions.openapi import openapi

# project

trends_blueprint = Blueprint("trends", url_prefix="/trends")


@openapi.definition()
@trends_blueprint.route("/", methods=["GET"])
async def get_trends(request) -> HTTPResponse:
    pass
