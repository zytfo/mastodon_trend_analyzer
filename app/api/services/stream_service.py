# stdlib
import re
from datetime import datetime, timedelta

import mastodon
# thirdparty
from mastodon import Mastodon
from sqlalchemy import insert

# project
import settings
from app.api.models.status_model import StatusModel
from app.api.services.trends_service import check_if_trend_exist, create_or_update_account, \
    create_or_update_suspicious_trend, check_if_suspicious_trend_exist, get_statuses_by_tag, \
    increment_suspicious_trend_number_of_similar_posts
from app.api.utils.similarity_checker import calculate_cosine_similarity_between_two_statuses
from app.core.database import ScopedSession
from app.core.helpers.mastodon_social_client import HTTPXMastodonInstanceServiceClient

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
        status.pop("reblog", None)
        status.pop("media_attachments", None)
        status.pop("mentions", None)
        status.pop("emojis", None)
        status.pop("card", None)
        status.pop("poll", None)
        status.pop("filtered", None)
        status.pop("application", None)

        # check if only tags is more than 0
        if len(status["tags"]) != 0:
            tags = []
            with ScopedSession() as session:
                for tag in status["tags"]:
                    # get post author
                    account = status["account"]

                    # add tag to tags array to save status then
                    tags.append(tag["name"])

                    # get author register date
                    created_at = account["created_at"].strftime("%Y-%m-%d %H:%M:%S")

                    # get time difference to check
                    difference = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")

                    # check if a user was registered less than a month ago, has less than 1000 followers and has less than 100 statuses
                    if created_at >= difference \
                            and account["followers_count"] <= 1000 \
                            and account["statuses_count"] <= 100:
                        # check if this is an existing trend
                        trend = check_if_trend_exist(session=session, name=tag["name"])

                        # if no trend, this is probably a new one
                        if not trend:
                            # try to find this trend in the database, if not - retrieve information from API
                            suspicious_trend = check_if_suspicious_trend_exist(session=session, name=tag["name"])

                            # get mastodon instance url
                            instance_url = account["url"]

                            # if mastodon.social in url, get it
                            if "mastodon.social" in instance_url:
                                instance_url = "https://mastodon.social"
                            # get the first element of the array if it contains https
                            else:
                                instance_url = re.findall(r'^(https?:\/\/[\w.-]+)', instance_url)
                                instance_url = instance_url[0]

                            # retrieve info if trend does not exist
                            if not suspicious_trend:
                                # get info about this trend
                                with HTTPXMastodonInstanceServiceClient as client:  # type: HTTPXMastodonInstanceServiceClient
                                    # get aggregated info about tag in last seven days
                                    url, accounts, uses, errors = client.get_tag_info(tag=tag["name"])

                                    # if an error happened, just continue
                                    if errors:
                                        continue

                                    # check trend info: if less than 100 account and less than 100 uses, it might a suspicious trend, so write in the database
                                    if accounts <= 100 and uses <= 100:
                                        # get rid of unnecessary fields for account model
                                        account.pop("emojis", None)
                                        account.pop("fields", None)
                                        account.pop("noindex", None)
                                        account.pop("roles", None)

                                        # create a new account entity or update in case of existence
                                        create_or_update_account(
                                            session=session,
                                            account=account,
                                            instance_url=instance_url
                                        )

                                        # create a new suspicious trend entity or update in case of existence
                                        suspicious_trend = create_or_update_suspicious_trend(
                                            session=session,
                                            name=tag["name"],
                                            url=url,
                                            uses_in_last_seven_days=uses,
                                            number_of_accounts=accounts,
                                            instance_url=instance_url
                                        )

                                        print("\nPROBABLY AN ARTIFICIAL TREND AND THIS USER MIGHT BE A BOT!")
                                        print("ACCOUNT ACCT: " + account["acct"])
                                        print("ACCOUNT URL: " + account["url"])
                                        print("ACCOUNT CREATED_AT: " + str(account["created_at"]))
                                        print("ACCOUNT FOLLOWERS_COUNT: " + str(account["followers_count"]))
                                        print("ACCOUNT FOLLOWING_COUNT: " + str(account["following_count"]))
                                        print("ACCOUNT STATUSES_COUNT: " + str(account["statuses_count"]))
                                        print("TREND NAME: " + tag["name"])
                                        print("TREND URL: " + tag["url"])

                                        # get statuses with this tag to check for a similar status text
                                        statuses = get_statuses_by_tag(session=session, tag=tag["name"])

                                        # iterate over all stored statuses by tag
                                        for stored_status in statuses:
                                            # get cosine similarity between stored status and a new one
                                            similarity = calculate_cosine_similarity_between_two_statuses(
                                                status_content_1=stored_status.content,
                                                status_content_2=status["content"]
                                            )

                                            # if similarity >= 0.5, update suspicious trend model with an incremented number_of_similar_posts value
                                            if similarity >= 0.5:
                                                increment_suspicious_trend_number_of_similar_posts(
                                                    session=session,
                                                    suspicious_trend_id=suspicious_trend.id,
                                                    number_of_similar_statuses=suspicious_trend.number_of_similar_statuses + 1
                                                )

                # remove unnecessary, non-parsable elements
                status.pop("tags", None)
                status.pop("account", None)

                # add parsed tags to status model to store it in the database
                status["tags"] = tags

                save_status(session=session, status=status)


async def listen_mastodon_stream():
    mastodon_instance.stream_public(Listener(), run_async=True)
