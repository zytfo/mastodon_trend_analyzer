# stdlib
from http import HTTPStatus

# thirdparty
from sanic import Blueprint, json

# project
from app.core.helpers import jsonapi

blueprint = Blueprint("bp")
DEFAULT_TYPE = "application/json"


@blueprint.middleware("response")
def jsonapi_standard_response_header(request, response):
    response.headers["Content-Type"] = DEFAULT_TYPE


@blueprint.middleware("request")
def check_content_negotiation(request):
    accept = request.headers.get("accept")
    content_type = request.headers.get("content-type", None)
    method = request.method

    if accept != DEFAULT_TYPE:
        error = jsonapi.format_error(
            title="Not Acceptable", detail="Cannot continue process for your requested media type."
        )
        return json(jsonapi.return_an_error(error), status=HTTPStatus.NOT_ACCEPTABLE)

    if method != "GET":
        if content_type != DEFAULT_TYPE:
            error = jsonapi.format_error(
                title="Unsupported Media Type", detail="Cannot continue process for your requested media type."
            )
            return json(jsonapi.return_an_error(error), status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
