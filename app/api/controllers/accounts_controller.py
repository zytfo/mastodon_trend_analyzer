# stdlib
# thirdparty
import sanic_ext
from sanic import Blueprint, HTTPResponse, Request
from sanic_ext.extensions.openapi import openapi

from app.api.models.account_model import GetAccountsQuery
from app.api.serializers.accounts import AccountSerializer
from app.api.services.accounts_service import get_accounts
from app.core.helpers import rest_helper

# project

accounts_blueprint = Blueprint("accounts", url_prefix="/accounts")


@openapi.definition(
    parameter=GetAccountsQuery.get_query_definitions(),
    summary="Get Suspicious Accounts",
    tag="accounts"
)
@sanic_ext.validate(query=GetAccountsQuery)
@accounts_blueprint.route("/", methods=["GET"])
async def get_suspicious_accounts(request: Request) -> HTTPResponse:
    session = request.ctx.session
    limit = request.args.get("limit", default=100)
    offset = request.args.get("offset", default=0)
    instance = request.args.get("instance", default=None)

    async with session.begin():
        accounts, total_count, limit, offset = await get_accounts(
            session=session,
            limit=limit,
            offset=offset,
            instance=instance
        )

        return rest_helper.on_write_json(
            result=[AccountSerializer(account).marshal() for account in accounts],
            total_count=total_count,
            limit=limit,
            offset=offset
        )
