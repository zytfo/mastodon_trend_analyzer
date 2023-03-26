# stdlib
from asyncio import current_task
from contextvars import ContextVar

from sqlalchemy import create_engine
# thirdparty
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import AsyncAdaptedQueuePool, NullPool

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

async_session = async_scoped_session(session_maker, scopefunc=current_task)

engine = create_engine(
    settings.psycopg2_connection,
    poolclass=NullPool,
)

Session = sessionmaker(bind=engine)
ScopedSession = scoped_session(Session)
