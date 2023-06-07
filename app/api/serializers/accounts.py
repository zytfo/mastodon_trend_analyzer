# thirdparty
from app.api.models.account_model import AccountModel
from app.core.helpers.serializer import SqlalchemyEntitySerializer


class AccountSerializer(SqlalchemyEntitySerializer):
    class Meta:
        model = AccountModel
        fields = (
            "id",
            "username",
            "acct",
            "display_name",
            "locked",
            "bot",
            "discoverable",
            "group",
            "created_at",
            "note",
            "url",
            "avatar",
            "avatar_static",
            "header",
            "header_static",
            "followers_count",
            "following_count",
            "statuses_count",
            "last_status_at",
            "instance_url"
        )
