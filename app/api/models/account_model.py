# thirdparty
from typing import Optional

from pydantic import Field
from sqlalchemy import Column, Integer, String, BigInteger, Boolean, DateTime

from app.core.helpers import base_models
from app.core.helpers.base_entities import BaseModel


class GetAccountsQuery(base_models.BaseRequestQuery):
    limit: Optional[int] = Field(default=100)
    offset: Optional[int] = Field(default=0)


class AccountModel(BaseModel):
    __table_args__ = {"schema": "mastodon_service"}
    __tablename__ = "accounts"

    id = Column(BigInteger(), nullable=False, primary_key=True)
    username = Column(String(), nullable=True)
    acct = Column(String(), nullable=True)
    display_name = Column(String(), nullable=True)
    locked = Column(Boolean(), nullable=True)
    bot = Column(Boolean(), nullable=True)
    discoverable = Column(Boolean(), nullable=True)
    group = Column(Boolean(), nullable=True)
    created_at = Column(DateTime(), nullable=True)
    note = Column(String(), nullable=True)
    url = Column(String(), nullable=True)
    avatar = Column(String(), nullable=True)
    avatar_static = Column(String(), nullable=True)
    header = Column(String(), nullable=True)
    header_static = Column(String(), nullable=True)
    followers_count = Column(Integer(), nullable=True)
    following_count = Column(Integer(), nullable=True)
    statuses_count = Column(Integer(), nullable=True)
    last_status_at = Column(DateTime(), nullable=True)
    instance_url = Column(String(), nullable=True)
