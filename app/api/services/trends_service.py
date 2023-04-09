# stdlib

import aiohttp
from sqlalchemy import delete, select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

import settings
from app.api.models.account_model import AccountModel
from app.api.models.trend_model import TrendModel, SuspiciousTrendModel
from app.api.serializers.trends import TrendSerializer
from app.core.database import ScopedSession
from app.core.helpers import rest_helper


async def delete_all_trends(session: AsyncSession):
    query = delete(TrendModel)
    await session.execute(query)


async def update_and_retrieve_trends(session: AsyncSession, trends: list):
    session.add_all(trends)

    query = select(TrendModel)
    result = await session.execute(query)
    return result.scalars().all()


async def update_mastodon_trends(session: AsyncSession, url: str):
    async with aiohttp.ClientSession(headers=settings.INSTANCES_SOCIAL_HEADERS) as aio_session:
        async with aio_session.get(url) as response:
            trends = await response.json()

            async with session.begin():
                # delete all existing trends in the database
                await delete_all_trends(session=session)

                retrieved_trends = []

                for trend in trends:
                    counter = 0
                    for day in trend["history"]:
                        counter += int(day["uses"])
                    retrieved_trends.append(TrendModel(
                        name=trend["name"],
                        url=trend["url"],
                        uses_in_last_seven_days=counter
                    ))

                # update the list of trends in the database and retrieve them
                retrieved_trends = await update_and_retrieve_trends(session=session, trends=retrieved_trends)

                if retrieved_trends and len(retrieved_trends) > 0:
                    return rest_helper.on_write_data(
                        result=[TrendSerializer(trend).marshal() for trend in retrieved_trends])
                else:
                    return rest_helper.on_write_error(errors={"error": "Something went wrong"})


def check_if_trend_exist(session: ScopedSession, name: str):
    query = select(TrendModel).filter(TrendModel.name == name)
    result = session.execute(query)
    return result.scalars().one_or_none()


def check_if_suspicious_trend_exist(session: ScopedSession, name: str):
    query = select(SuspiciousTrendModel).filter(SuspiciousTrendModel.name == name)
    result = session.execute(query)
    return result.scalars().one_or_none()


def check_if_account_exist(session: ScopedSession, acct: str):
    query = select(AccountModel).filter(AccountModel.acct == acct)
    result = session.execute(query)
    return result.scalars().one_or_none()


def create_or_update_account(session: ScopedSession, account: dict):
    insert_stmt = insert(AccountModel).values(**account)

    insert_stmt = insert_stmt.on_conflict_do_update(
        index_elements=["acct"],
        set_=dict(
            locked=account["locked"],
            bot=account["bot"],
            discoverable=account["discoverable"],
            group=account["group"],
            note=account["note"],
            url=account["url"],
            avatar=account["avatar"],
            avatar_static=account["avatar_static"],
            header=account["header"],
            header_static=account["header_static"],
            followers_count=account["followers_count"],
            following_count=account["following_count"],
            statuses_count=account["statuses_count"],
            last_status_at=account["last_status_at"],
        )
    )

    return session.execute(insert_stmt)


def create_or_update_suspicious_trend(
        session: ScopedSession,
        name: str,
        url: str,
        uses_in_last_seven_days: int,
        number_of_accounts: int
):
    insert_stmt = insert(SuspiciousTrendModel).values(
        dict(
            name=name,
            url=url,
            uses_in_last_seven_days=uses_in_last_seven_days,
            number_of_accounts=number_of_accounts
        )
    )

    insert_stmt = insert_stmt.on_conflict_do_update(
        index_elements=["url"],
        set_=dict(
            uses_in_last_seven_days=uses_in_last_seven_days,
            number_of_accounts=number_of_accounts
        )
    )

    return session.execute(insert_stmt)


async def get_global_trends(session: AsyncSession, limit: int, offset: int):
    query = select([func.count(TrendModel.id)])

    result = await session.execute(query)
    total_count = result.scalars().one()

    query = select(TrendModel).limit(limit).offset(offset)
    result = await session.execute(query)
    return result.scalars().all(), total_count, limit, offset


async def get_suspicious_trends_internal(session: AsyncSession, limit: int, offset: int):
    query = select([func.count(SuspiciousTrendModel.id)])

    result = await session.execute(query)
    total_count = result.scalars().one()

    query = select(SuspiciousTrendModel).limit(limit).offset(offset)
    result = await session.execute(query)
    return result.scalars().all(), total_count, limit, offset
