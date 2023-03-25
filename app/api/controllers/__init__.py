# thirdparty
from sanic import Blueprint

from app.api.controllers.instances_controller import instances_blueprint
from app.api.controllers.trends_controller import trends_blueprint

# project

v1 = Blueprint.group(
    trends_blueprint,
    instances_blueprint,
    url_prefix="/api/v1/"
)
