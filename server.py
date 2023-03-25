# stdlib
from asyncio import current_task

# thirdparty
from sanic import Sanic
from sqlalchemy.ext.asyncio import async_scoped_session

# project
import settings
from app.api.controllers import v1
from app.api.services.stream_service import listen_mastodon_stream
from app.core.database import base_model_session_ctx, session_maker

app = Sanic(__name__)
app.add_task(listen_mastodon_stream())

app.blueprint(v1)


@app.middleware("request")
async def inject_session(request):
    request.ctx.session = async_scoped_session(session_maker, scopefunc=current_task)
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
