# stdlib

# thirdparty
from sanic import Sanic

# project
import settings
from app.api.controllers import v1
from app.api.services.instance_service import update_instances
from app.api.services.stream_service import listen_mastodon_stream
from app.core.database import base_model_session_ctx, async_session

app = Sanic(__name__)

# update the list of available mastodon instances
app.add_task(update_instances(session=async_session,
                              url=settings.MASTODON_UPDATE_INSTANCE_ENDPOINT))

# start listening mastodon network
app.add_task(listen_mastodon_stream())

app.blueprint(v1)


@app.middleware("request")
async def inject_session(request):
    request.ctx.session = async_session
    request.ctx.session_ctx_token = base_model_session_ctx.set(request.ctx.session)


@app.middleware("response")
async def close_session(request, response):
    if hasattr(request.ctx, "session_ctx_token"):
        base_model_session_ctx.reset(request.ctx.session_ctx_token)
        await request.ctx.session.close()


def create_app(run=True, fast=False):
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
