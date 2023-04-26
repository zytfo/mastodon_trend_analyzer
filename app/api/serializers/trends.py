# thirdparty
from app.api.models.trend_model import TrendModel, SuspiciousTrendModel
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


class SuspiciousTrendSerializer(SqlalchemyEntitySerializer):
    class Meta:
        model = SuspiciousTrendModel
        fields = (
            "id",
            "name",
            "url",
            "uses_in_last_seven_days",
            "number_of_accounts",
            "instance_url",
            "number_of_similar_statuses"
        )
