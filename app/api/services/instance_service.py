# stdlib
from datetime import datetime
from typing import List

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.models.instance_model import InstanceModel


async def delete_all_instances(session: AsyncSession):
    query = delete(InstanceModel)
    await session.execute(query)


async def update_and_retrieve_instances(session: AsyncSession, instances: List[dict]):
    objects = [InstanceModel(
        id=instance["id"],
        name=instance["name"],
        added_at=datetime.strptime(instance["added_at"], "%Y-%m-%dT%H:%M:%S.%fZ") if instance["added_at"] else None,
        updated_at=datetime.strptime(instance["updated_at"], "%Y-%m-%dT%H:%M:%S.%fZ") if instance[
            "updated_at"] else None,
        uptime=instance["uptime"],
        up=instance["up"],
        dead=instance["dead"],
        version=instance["version"],
        ipv6=instance["ipv6"],
        https_score=instance["https_score"],
        https_rank=instance["https_rank"],
        obs_score=instance["obs_score"],
        obs_rank=instance["obs_rank"],
        users=instance["users"],
        statuses=instance["statuses"],
        connections=instance["connections"],
        open_registrations=instance["open_registrations"],
        info=instance["info"],
        thumbnail=instance["thumbnail"],
        thumbnail_proxy=instance["thumbnail_proxy"],
        active_users=instance["active_users"],
        email=instance["email"],
        admin=instance["admin"],
    ) for instance in instances]
    session.add_all(objects)

    query = select(InstanceModel)
    result = await session.execute(query)
    return result.scalars().all()
