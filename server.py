# thirdparty
from sanic import Sanic, text
from sanic_routing.exceptions import NotFound

# project
import settings
import nltk
from app.api.controllers import v1
from app.api.controllers.favicon_controller import favicon_blueprint
from app.api.services.instance_service import update_instances
from app.api.services.stream_service import listen_mastodon_stream
from app.api.services.trends_service import update_mastodon_trends
from app.core.cors import add_cors_headers
from app.core.database import base_model_session_ctx, async_session
from app.core.options import setup_options

app = Sanic(__name__)

# add application secret to run on nginx
app.config.FORWARDED_SECRET = settings.APP_SECRET

# update the list of available mastodon instances
app.add_task(update_instances(session=async_session,
                              url=settings.MASTODON_UPDATE_INSTANCE_ENDPOINT))

# get the list of current trends and write them in database
app.add_task(update_mastodon_trends(session=async_session,
                                    url=settings.MASTODON_SOCIAL_TRENDS_ENDPOINT))

# start listening mastodon network
app.add_task(listen_mastodon_stream())

# Add OPTIONS handlers to any route that is missing it
app.register_listener(setup_options, "before_server_start")

# Fill in CORS headers
app.register_middleware(add_cors_headers, "response")

app.blueprint(v1)

# handle favicon request
app.blueprint(favicon_blueprint)


@app.exception(NotFound)
async def handle_404(request, exception):
    return text("Route not found", status=404)


@app.middleware("request")
async def inject_session(request):
    request.ctx.session = async_session
    request.ctx.session_ctx_token = base_model_session_ctx.set(request.ctx.session)


@app.middleware("response")
async def close_session(request, response):
    if hasattr(request.ctx, "session_ctx_token"):
        base_model_session_ctx.reset(request.ctx.session_ctx_token)
        await request.ctx.session.close()


def create_app(run=True, fast=settings.SANIC_FAST):
    nltk.download('punkt')
    if run:
        app.run(
            settings.HOST_IP,
            int(settings.HOST_PORT),
            debug=bool(settings.DEBUG),
            auto_reload=bool(settings.DEBUG),
            fast=fast,
        )
    return app


if __name__ == "__main__":
    create_app()
