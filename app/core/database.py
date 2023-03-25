# stdlib
from contextvars import ContextVar

# thirdparty
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool

# project
import settings

bind = create_async_engine(
    settings.connection,
    poolclass=AsyncAdaptedQueuePool,
    pool_size=1,
    max_overflow=5,
    pool_timeout=1800,
    pool_pre_ping=True,
    connect_args={"server_settings": {"jit": "off", "application_name": "complaints-service"}},
)

session_maker = sessionmaker(bind, expire_on_commit=False, class_=AsyncSession)

base_model_session_ctx = ContextVar("session")
