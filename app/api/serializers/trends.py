# thirdparty
from app.api.models.trend_model import TrendModel
from app.core.helpers.serializer import SqlalchemyEntitySerializer


class TrendSerializer(SqlalchemyEntitySerializer):
    class Meta:
        model = TrendModel
        fields = (
            "id",
            "name",
            "url",
            "uses_in_last_seven_days"
        )
