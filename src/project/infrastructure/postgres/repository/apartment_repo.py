from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.apartment import ApartmentSchema
from project.infrastructure.postgres.models import Apartment
from project.core.config import settings


class ApartmentRepository:
    _collection: Type[Apartment] = Apartment

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_apartments(
        self,
        session: AsyncSession,
    ) -> list[ApartmentSchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.apartments;"
        apartments = await session.execute(text(query))
        return [ApartmentSchema.model_validate(obj=apartment) for apartment in apartments.mappings().all()]

    async def get_apartment_by_id(
        self,
        session: AsyncSession,
        apartment_id: int,
    ) -> ApartmentSchema | None:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.apartments WHERE id = :apartment_id;"
        result = await session.execute(text(query), {"apartment_id": apartment_id})
        apartment = result.mappings().first()
        return ApartmentSchema.model_validate(obj=apartment) if apartment else None

    async def insert_apartment(
        self,
        session: AsyncSession,
        **kwargs,
    ) -> ApartmentSchema | None:
        keys = ", ".join(kwargs.keys())
        values = ", ".join([f":{key}" for key in kwargs.keys()])
        query = f"INSERT INTO {settings.POSTGRES_SCHEMA}.apartments ({keys}) VALUES ({values}) RETURNING *;"
        result = await session.execute(text(query), kwargs)
        await session.commit()
        apartment = result.mappings().first()
        return ApartmentSchema.model_validate(obj=apartment) if apartment else None

    async def update_apartment(
        self,
        session: AsyncSession,
        apartment_id: int,
        **kwargs,
    ) -> ApartmentSchema | None:
        updates = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
        query = f"""
        UPDATE {settings.POSTGRES_SCHEMA}.apartments
        SET {updates}
        WHERE id = :apartment_id
        RETURNING *;
        """
        params = {"apartment_id": apartment_id, **kwargs}
        result = await session.execute(text(query), params)
        await session.commit()
        apartment = result.mappings().first()
        return ApartmentSchema.model_validate(obj=apartment) if apartment else None

    async def delete_apartment(
        self,
        session: AsyncSession,
        apartment_id: int,
    ) -> bool:
        query = f"DELETE FROM {settings.POSTGRES_SCHEMA}.apartments WHERE id = :apartment_id;"
        result = await session.execute(text(query), {"apartment_id": apartment_id})
        await session.commit()
        return result.rowcount > 0