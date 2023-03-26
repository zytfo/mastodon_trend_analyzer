# stdlib

# thirdparty
from sqlalchemy import Boolean, Column, DateTime, Integer, String, BigInteger

from app.core.helpers.base_entities import BaseModel


class StatusModel(BaseModel):
    __table_args__ = {"schema": "mastodon_service"}
    __tablename__ = "statuses"

    id = Column(BigInteger(), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=True)
    in_reply_to_id = Column(BigInteger, nullable=True)
    in_reply_to_account_id = Column(BigInteger, nullable=True)
    sensitive = Column(Boolean, nullable=True)
    spoiler_text = Column(String, nullable=True)
    visibility = Column(String, nullable=True)
    language = Column(String, nullable=True)
    uri = Column(String, nullable=True)
    url = Column(String, nullable=True)
    replies_count = Column(Integer, nullable=True)
    reblogs_count = Column(Integer, nullable=True)
    favourites_count = Column(Integer, nullable=True)
    edited_at = Column(DateTime, nullable=True)
    content = Column(String, nullable=True)
    tags = Column(String, nullable=True)
