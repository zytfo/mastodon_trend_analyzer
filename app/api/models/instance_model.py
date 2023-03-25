# stdlib

# thirdparty
from sqlalchemy import JSON, Boolean, Column, DateTime, Integer, String

from app.core.helpers.base_entities import BaseModel


# project


# thirdparty

class InstanceModel(BaseModel):
    __table_args__ = {"schema": "mastodon_service"}
    __tablename__ = "instances"

    id = Column(String, nullable=False, primary_key=True)
    name = Column(String, nullable=True)
    added_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    uptime = Column(Integer, nullable=True)
    up = Column(Boolean, nullable=True)
    dead = Column(Boolean, nullable=True)
    version = Column(String, nullable=True)
    ipv6 = Column(Boolean, nullable=True)
    https_score = Column(Integer, nullable=True)
    https_rank = Column(String, nullable=True)
    obs_score = Column(Integer, nullable=True)
    obs_rank = Column(String, nullable=True)
    users = Column(String, nullable=True)
    statuses = Column(String, nullable=True)
    connections = Column(String, nullable=True)
    open_registrations = Column(Boolean, nullable=True)
    info = Column(JSON, nullable=True)
    thumbnail = Column(String, nullable=True)
    thumbnail_proxy = Column(String, nullable=True)
    active_users = Column(Integer, nullable=True)
    email = Column(String, nullable=True)
    admin = Column(String, nullable=True)
