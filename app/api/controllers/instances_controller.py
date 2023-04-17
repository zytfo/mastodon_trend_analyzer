# stdlib
# thirdparty
from sanic import Blueprint, HTTPResponse, Request
from sanic_ext.extensions.openapi import openapi

from app.api.services.instance_service import get_instances
from app.core.helpers import rest_helper

# project

instances_blueprint = Blueprint("instances", url_prefix="/instances")


@openapi.definition()
@instances_blueprint.route("/", methods=["GET"])
async def get_available_instances(request: Request) -> HTTPResponse:
    session = request.ctx.session

    limit = request.args.get("limit", default=20)
    offset = request.args.get("offset", default=0)

    async with session.begin():
        instances, total_count, limit, offset = await get_instances(
            session=session,
            limit=limit,
            offset=offset
        )

        return rest_helper.on_write_json(
            result=[instance for instance in instances],
            total_count=total_count,
            limit=limit,
            offset=offset
        )
