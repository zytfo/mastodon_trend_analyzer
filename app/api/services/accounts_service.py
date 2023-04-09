from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.models.account_model import AccountModel


async def get_accounts(session: AsyncSession, limit: int, offset: int):
    query = select([func.count(AccountModel.id)])

    result = await session.execute(query)
    total_count = result.scalars().one()

    query = select(AccountModel).limit(limit).offset(offset)
    result = await session.execute(query)
    return result.scalars().all(), total_count, limit, offset
