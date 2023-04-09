# thirdparty
from sanic import Blueprint, HTTPResponse, Request
from sanic_ext.extensions.openapi import openapi

from app.api.serializers.trends import TrendSerializer, SuspiciousTrendSerializer
from app.api.services.trends_service import get_global_trends, get_suspicious_trends_internal
from app.core.helpers import rest_helper

trends_blueprint = Blueprint("trends", url_prefix="/trends")
suspicious_trends_blueprint = Blueprint("suspicious_trends", url_prefix="/suspicious_trends")


@openapi.definition()
@trends_blueprint.route("/", methods=["GET"])
async def get_trends(request: Request) -> HTTPResponse:
    session = request.ctx.session
    limit = request.args.get("limit", default=20)
    offset = request.args.get("offset", default=0)

    async with session.begin():
        trends, total_count, limit, offset = await get_global_trends(
            session=session,
            limit=limit,
            offset=offset
        )

        return rest_helper.on_write_json(
            result=[TrendSerializer(trend).marshal() for trend in trends],
            total_count=total_count,
            limit=limit,
            offset=offset
        )


@openapi.definition()
@suspicious_trends_blueprint.route("/", methods=["GET"])
async def get_suspicious_trends(request: Request) -> HTTPResponse:
    session = request.ctx.session
    limit = request.args.get("limit", default=20)
    offset = request.args.get("offset", default=0)

    async with session.begin():
        trends, total_count, limit, offset = await get_suspicious_trends_internal(
            session=session,
            limit=limit,
            offset=offset
        )

        return rest_helper.on_write_json(
            result=[SuspiciousTrendSerializer(suspicious_trend).marshal() for suspicious_trend in trends],
            total_count=total_count,
            limit=limit,
            offset=offset
        )
