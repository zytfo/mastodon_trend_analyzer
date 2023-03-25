# thirdparty
from app.api.models.instance_model import InstanceModel
from app.core.helpers.serializer import SqlalchemyEntitySerializer


class InstanceSerializer(SqlalchemyEntitySerializer):
    class Meta:
        model = InstanceModel
        fields = (
            "id",
            "name",
            "added_at",
            "updated_at",
            "uptime",
            "up",
            "dead",
            "version",
            "ipv6",
            "https_score",
            "https_rank",
            "obs_score",
            "obs_rank",
            "users",
            "statuses",
            "connections",
            "open_registrations",
            "info",
            "thumbnail",
            "thumbnail_proxy",
            "active_users",
            "email",
            "admin"
        )
