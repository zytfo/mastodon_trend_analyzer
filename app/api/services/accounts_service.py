from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.models.account_model import AccountModel


async def get_accounts(session: AsyncSession, limit: int, offset: int, instance: str = None):
    if instance:
        query = select([func.count(AccountModel.id)]).filter(AccountModel.instance_url.ilike("%" + instance + "%"))
    else:
        query = select([func.count(AccountModel.id)])

    result = await session.execute(query)
    total_count = result.scalars().one()

    if instance:
        query = select(AccountModel) \
            .filter(AccountModel.instance_url.ilike("%" + instance + "%")) \
            .limit(limit) \
            .offset(offset)
    else:
        query = select(AccountModel) \
            .limit(limit) \
            .offset(offset)

    result = await session.execute(query)
    return result.scalars().all(), total_count, limit, offset
