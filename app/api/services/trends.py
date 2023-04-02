# stdlib

import aiohttp
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

import settings
from app.api.models.trend_model import TrendModel
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
