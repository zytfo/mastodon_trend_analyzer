# stdlib
from datetime import datetime, timedelta

import mastodon
# thirdparty
from mastodon import Mastodon
from sqlalchemy import insert

# project
import settings
from app.api.models.status_model import StatusModel
from app.api.services.trends import check_if_trend_exist
from app.core.database import ScopedSession

mastodon_instance = Mastodon(
    access_token=settings.MASTODON_INSTANCE_ACCESS_TOKEN,
    api_base_url=settings.MASTODON_INSTANCE_ENDPOINT
)


def save_status(session: ScopedSession, status: dict):
    status = dict(**status)
    query = insert(StatusModel).values(status)
    session.execute(query)
    session.commit()


class Listener(mastodon.StreamListener):

    def on_update(self, status):
        # print(status)
        status.pop("reblog", None)
        # status.pop("account", None)
        status.pop("media_attachments", None)
        status.pop("mentions", None)
        status.pop("emojis", None)
        status.pop("card", None)
        status.pop("poll", None)
        status.pop("filtered", None)
        status.pop("application", None)

        # check if only tags is more than 0
        if len(status["tags"]) != 0:
            with ScopedSession() as session:
                for tag in status["tags"]:
                    trend = check_if_trend_exist(session=session, name=tag["name"])

                    # if no trend there is no such trend in the database and this is a new one
                    if not trend:
                        # get post author
                        account = status["account"]

                        # get author register date
                        created_at = account["created_at"].strftime("%Y-%m-%d %H:%M:%S")

                        # get time difference to check
                        difference = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")

                        # check newly registered user
                        if created_at >= difference:
                            print("POSSIBLE ARTIFICIAL TREND AND THIS USER IS BOT!")
                            print("Account: " + account["username"])
                            print("Trend: " + tag["name"])

                status.pop("tags", None)
                status.pop("account", None)
                save_status(session=session, status=status)

            # print(json.dumps(status["tags"], indent=1))


async def listen_mastodon_stream():
    mastodon_instance.stream_public(Listener(), run_async=True)
