from http import HTTPStatus

from sanic import Blueprint
from sanic.exceptions import NotFound
from sanic.response import json

from app.core.helpers import jsonapi

blueprint = Blueprint("exceptions")


@blueprint.exception(NotFound)
def handle_404(request, exception):
    error = jsonapi.format_error(title="Resource not found", detail=str(exception))
    return json(jsonapi.return_an_error(error), status=HTTPStatus.NOT_FOUND)
