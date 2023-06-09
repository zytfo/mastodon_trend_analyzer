# thirdparty
import sanic
from sanic import Blueprint, HTTPResponse, Request
from sanic_ext.extensions.openapi import openapi

# project

favicon_blueprint = Blueprint("favicon", url_prefix="/favicon.ico")


@openapi.definition()
@favicon_blueprint.route("/", methods=["GET"])
async def get_available_instances(request: Request) -> HTTPResponse:
    return sanic.response.empty(status=404)
