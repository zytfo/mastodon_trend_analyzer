# thirdparty
from sqlalchemy import Column, Integer, String

from app.core.helpers.base_entities import BaseModel


class TrendModel(BaseModel):
    __table_args__ = {"schema": "mastodon_service"}
    __tablename__ = "trends"

    id = Column(Integer(), nullable=False, primary_key=True)
    name = Column(String(), nullable=True)
    url = Column(String(), nullable=True)
    uses_in_last_seven_days = Column(Integer(), nullable=True)
