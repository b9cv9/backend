from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.street import StreetSchema
from project.infrastructure.postgres.models import Street
from project.core.config import settings

class StreetRepository:
    _collection: Type[Street] = Street

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_streets(self, session: AsyncSession) -> list[StreetSchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.streets;"
        streets = await session.execute(text(query))
        return [StreetSchema.model_validate(obj=street) for street in streets.mappings().all()]

    async def get_street_by_id(self, session: AsyncSession, street_id: int) -> StreetSchema | None:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.streets WHERE id = :street_id;"
        result = await session.execute(text(query), {"street_id": street_id})
        street = result.mappings().first()
        return StreetSchema.model_validate(obj=street) if street else None

    async def insert_street(self, session: AsyncSession, district_id: int, name: str) -> StreetSchema | None:
        query = f"""
        INSERT INTO {settings.POSTGRES_SCHEMA}.streets (district_id, name)
        VALUES (:district_id, :name) RETURNING *;
        """
        result = await session.execute(text(query), {"district_id": district_id, "name": name})
        await session.commit()
        street = result.mappings().first()
        return StreetSchema.model_validate(obj=street) if street else None

    async def update_street(self, session: AsyncSession, street_id: int, **kwargs) -> StreetSchema | None:
        updates = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
        query = f"""
        UPDATE {settings.POSTGRES_SCHEMA}.streets
        SET {updates}
        WHERE id = :street_id
        RETURNING *;
        """
        params = {"street_id": street_id, **kwargs}
        result = await session.execute(text(query), params)
        await session.commit()
        street = result.mappings().first()
        return StreetSchema.model_validate(obj=street) if street else None

    async def delete_street(self, session: AsyncSession, street_id: int) -> bool:
        query = f"DELETE FROM {settings.POSTGRES_SCHEMA}.streets WHERE id = :street_id;"
        result = await session.execute(text(query), {"street_id": street_id})
        await session.commit()
        return result.rowcount > 0
