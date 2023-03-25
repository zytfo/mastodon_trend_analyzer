# stdlib
from datetime import datetime, timedelta

import mastodon
# thirdparty
from mastodon import Mastodon

# project
import settings

mastodon_instance = Mastodon(
    access_token=settings.MASTODON_INSTANCE_ACCESS_TOKEN,
    api_base_url=settings.MASTODON_INSTANCE_ENDPOINT
)


class Listener(mastodon.StreamListener):
    def on_update(self, status):
        # check if only tags is more than 0
        if len(status["tags"]) != 0:
            # get post author
            account = status["account"]

            # get author register date
            created_at = account["created_at"].strftime("%Y-%m-%d %H:%M:%S")

            # get time difference to check
            difference = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")

            # check newly registered user
            if created_at >= difference:
                # print(status["tags"])
                print(status)

            # print(json.dumps(status["tags"], indent=1))


async def listen_mastodon_stream():
    mastodon_instance.stream_public(Listener(), run_async=True)
