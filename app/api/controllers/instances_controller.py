# stdlib
import aiohttp
# thirdparty
from sanic import Blueprint, HTTPResponse
from sanic_ext.extensions.openapi import openapi

import settings
from app.api.serializers.instances import InstanceSerializer
from app.api.services.instance_service import delete_all_instances, update_and_retrieve_instances
from app.core.helpers import rest_helper

# project

instances_blueprint = Blueprint("instances", url_prefix="/instances")


@openapi.definition()
@instances_blueprint.route("/", methods=["GET"])
async def update_available_instances(request) -> HTTPResponse:
    # retrieve alive, open to register and with min number of active users mastodon instances
    url = settings.INSTANCES_SOCIAL_ENDPOINT + "/instances/list?include_closed=false&count=0&min_active_users=500&include_down=false"
    session = request.ctx.session
    async with aiohttp.ClientSession(headers=settings.INSTANCES_SOCIAL_HEADERS) as aio_session:
        async with aio_session.get(url) as response:
            data = await response.json()
            instances = data["instances"]

            async with session.begin():
                # delete all existing instances in the database
                await delete_all_instances(session=session)

                # update the list of instances in the database and retrieve them
                retrieved_instances = await update_and_retrieve_instances(session=session, instances=instances)

                if retrieved_instances and len(retrieved_instances) > 0:
                    return rest_helper.on_write_data(
                        result=[InstanceSerializer(instance).marshal() for instance in retrieved_instances])
                else:
                    rest_helper.on_write_error(errors={"error": "Something went wrong"})
