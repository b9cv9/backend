from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.house_type import HouseTypeSchema
from project.infrastructure.postgres.models import HouseType
from project.core.config import settings

class HouseTypeRepository:
    _collection: Type[HouseType] = HouseType

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_house_types(self, session: AsyncSession) -> list[HouseTypeSchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.house_types;"
        house_types = await session.execute(text(query))
        return [HouseTypeSchema.model_validate(obj=house_type) for house_type in house_types.mappings().all()]

    async def get_house_type_by_id(self, session: AsyncSession, type_id: int) -> HouseTypeSchema | None:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.house_types WHERE id = :type_id;"
        result = await session.execute(text(query), {"type_id": type_id})
        house_type = result.mappings().first()
        return HouseTypeSchema.model_validate(obj=house_type) if house_type else None

    async def insert_house_type(self, session: AsyncSession, description: str, type: str | None) -> HouseTypeSchema | None:
        query = f"""
        INSERT INTO {settings.POSTGRES_SCHEMA}.house_types (description, type)
        VALUES (:description, :type) RETURNING *;
        """
        result = await session.execute(text(query), {"description": description, "type": type})
        await session.commit()
        house_type = result.mappings().first()
        return HouseTypeSchema.model_validate(obj=house_type) if house_type else None

    async def update_house_type(self, session: AsyncSession, type_id: int, **kwargs) -> HouseTypeSchema | None:
        updates = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
        query = f"""
        UPDATE {settings.POSTGRES_SCHEMA}.house_types
        SET {updates}
        WHERE id = :type_id
        RETURNING *;
        """
        params = {"type_id": type_id, **kwargs}
        result = await session.execute(text(query), params)
        await session.commit()
        house_type = result.mappings().first()
        return HouseTypeSchema.model_validate(obj=house_type) if house_type else None

    async def delete_house_type(self, session: AsyncSession, type_id: int) -> bool:
        query = f"DELETE FROM {settings.POSTGRES_SCHEMA}.house_types WHERE id = :type_id;"
        result = await session.execute(text(query), {"type_id": type_id})
        await session.commit()
        return result.rowcount > 0
