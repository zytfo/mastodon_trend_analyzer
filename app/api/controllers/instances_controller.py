# stdlib
# thirdparty
from sanic import Blueprint, HTTPResponse
from sanic_ext.extensions.openapi import openapi

import settings
from app.api.services.instance_service import update_instances

# project

instances_blueprint = Blueprint("instances", url_prefix="/instances")


@openapi.definition()
@instances_blueprint.route("/", methods=["GET"])
async def update_available_instances(request) -> HTTPResponse:
    session = request.ctx.session

    return await update_instances(session=session, url=settings.MASTODON_UPDATE_INSTANCE_ENDPOINT)
