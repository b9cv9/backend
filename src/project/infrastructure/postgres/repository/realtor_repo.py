from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.realtor import RealtorSchema
from project.infrastructure.postgres.models import Realtor
from project.core.config import settings

class RealtorRepository:
    _collection: Type[Realtor] = Realtor

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_realtors(self, session: AsyncSession) -> list[RealtorSchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.realtors;"
        realtors = await session.execute(text(query))
        return [RealtorSchema.model_validate(obj=realtor) for realtor in realtors.mappings().all()]

    async def get_realtor_by_id(self, session: AsyncSession, realtor_id: int) -> RealtorSchema | None:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.realtors WHERE id = :realtor_id;"
        result = await session.execute(text(query), {"realtor_id": realtor_id})
        realtor = result.mappings().first()
        return RealtorSchema.model_validate(obj=realtor) if realtor else None

    async def insert_realtor(self, session: AsyncSession, **kwargs) -> RealtorSchema | None:
        keys = ", ".join(kwargs.keys())
        values = ", ".join([f":{key}" for key in kwargs.keys()])
        query = f"INSERT INTO {settings.POSTGRES_SCHEMA}.realtors ({keys}) VALUES ({values}) RETURNING *;"
        result = await session.execute(text(query), kwargs)
        await session.commit()
        realtor = result.mappings().first()
        return RealtorSchema.model_validate(obj=realtor) if realtor else None

    async def update_realtor(self, session: AsyncSession, realtor_id: int, **kwargs) -> RealtorSchema | None:
        updates = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
        query = f"""
        UPDATE {settings.POSTGRES_SCHEMA}.realtors
        SET {updates}
        WHERE id = :realtor_id
        RETURNING *;
        """
        params = {"realtor_id": realtor_id, **kwargs}
        result = await session.execute(text(query), params)
        await session.commit()
        realtor = result.mappings().first()
        return RealtorSchema.model_validate(obj=realtor) if realtor else None

    async def delete_realtor(self, session: AsyncSession, realtor_id: int) -> bool:
        query = f"DELETE FROM {settings.POSTGRES_SCHEMA}.realtors WHERE id = :realtor_id;"
        result = await session.execute(text(query), {"realtor_id": realtor_id})
        await session.commit()
        return result.rowcount > 0
