from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.house import HouseSchema
from project.infrastructure.postgres.models import House
from project.core.config import settings

class HouseRepository:
    _collection: Type[House] = House

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_houses(self, session: AsyncSession) -> list[HouseSchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.houses;"
        houses = await session.execute(text(query))
        return [HouseSchema.model_validate(obj=house) for house in houses.mappings().all()]

    async def get_house_by_id(self, session: AsyncSession, house_id: int) -> HouseSchema | None:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.houses WHERE id = :house_id;"
        result = await session.execute(text(query), {"house_id": house_id})
        house = result.mappings().first()
        return HouseSchema.model_validate(obj=house) if house else None

    async def insert_house(
        self, session: AsyncSession, street_id: int, house_number: str, type_id: int, floors: int | None
    ) -> HouseSchema | None:
        query = f"""
        INSERT INTO {settings.POSTGRES_SCHEMA}.houses (street_id, house_number, type_id, floors)
        VALUES (:street_id, :house_number, :type_id, :floors) RETURNING *;
        """
        result = await session.execute(
            text(query),
            {"street_id": street_id, "house_number": house_number, "type_id": type_id, "floors": floors},
        )
        await session.commit()
        house = result.mappings().first()
        return HouseSchema.model_validate(obj=house) if house else None

    async def update_house(self, session: AsyncSession, house_id: int, **kwargs) -> HouseSchema | None:
        updates = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
        query = f"""
        UPDATE {settings.POSTGRES_SCHEMA}.houses
        SET {updates}
        WHERE id = :house_id
        RETURNING *;
        """
        params = {"house_id": house_id, **kwargs}
        result = await session.execute(text(query), params)
        await session.commit()
        house = result.mappings().first()
        return HouseSchema.model_validate(obj=house) if house else None

    async def delete_house(self, session: AsyncSession, house_id: int) -> bool:
        query = f"DELETE FROM {settings.POSTGRES_SCHEMA}.houses WHERE id = :house_id;"
        result = await session.execute(text(query), {"house_id": house_id})
        await session.commit()
        return result.rowcount > 0
