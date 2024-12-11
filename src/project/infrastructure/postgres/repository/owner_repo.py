from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.owner import OwnerSchema
from project.infrastructure.postgres.models import Owner
from project.core.config import settings


class OwnerRepository:
    _collection: Type[Owner] = Owner

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_owners(
        self,
        session: AsyncSession,
    ) -> list[OwnerSchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.owners;"
        owners = await session.execute(text(query))
        return [OwnerSchema.model_validate(obj=owner) for owner in owners.mappings().all()]

    async def get_owner_by_id(
        self,
        session: AsyncSession,
        owner_id: int,
    ) -> OwnerSchema | None:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.owners WHERE owners_id = :owner_id;"
        result = await session.execute(text(query), {"owner_id": owner_id})
        owner = result.mappings().first()
        return OwnerSchema.model_validate(obj=owner) if owner else None

    async def insert_owner(
        self,
        session: AsyncSession,
        **kwargs,
    ) -> OwnerSchema | None:
        keys = ", ".join(kwargs.keys())
        values = ", ".join([f":{key}" for key in kwargs.keys()])
        query = f"INSERT INTO {settings.POSTGRES_SCHEMA}.owners ({keys}) VALUES ({values}) RETURNING *;"
        result = await session.execute(text(query), kwargs)
        await session.commit()
        owner = result.mappings().first()
        return OwnerSchema.model_validate(obj=owner) if owner else None

    async def update_owner(
        self,
        session: AsyncSession,
        owner_id: int,
        **kwargs,
    ) -> OwnerSchema | None:
        updates = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
        query = f"""
        UPDATE {settings.POSTGRES_SCHEMA}.owners
        SET {updates}
        WHERE owners_id = :owner_id
        RETURNING *;
        """
        params = {"owner_id": owner_id, **kwargs}
        result = await session.execute(text(query), params)
        await session.commit()
        owner = result.mappings().first()
        return OwnerSchema.model_validate(obj=owner) if owner else None

    async def delete_owner(
        self,
        session: AsyncSession,
        owner_id: int,
    ) -> bool:
        query = f"DELETE FROM {settings.POSTGRES_SCHEMA}.owners WHERE owners_id = :owner_id;"
        result = await session.execute(text(query), {"owner_id": owner_id})
        await session.commit()
        return result.rowcount > 0
