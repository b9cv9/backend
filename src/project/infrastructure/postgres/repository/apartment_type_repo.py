from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.apartment_type import ApartmentTypeSchema
from project.infrastructure.postgres.models import ApartmentType
from project.core.config import settings

class ApartmentTypeRepository:
    _collection: Type[ApartmentType] = ApartmentType

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_apartment_types(self, session: AsyncSession) -> list[ApartmentTypeSchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.apartment_types;"
        apartment_types = await session.execute(text(query))
        return [ApartmentTypeSchema.model_validate(obj=apartment_type) for apartment_type in apartment_types.mappings().all()]

    async def get_apartment_type_by_id(self, session: AsyncSession, type_id: int) -> ApartmentTypeSchema | None:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.apartment_types WHERE id = :type_id;"
        result = await session.execute(text(query), {"type_id": type_id})
        apartment_type = result.mappings().first()
        return ApartmentTypeSchema.model_validate(obj=apartment_type) if apartment_type else None

    async def insert_apartment_type(
        self, session: AsyncSession, description: str, num_rooms: int | None, is_furnished: bool | None
    ) -> ApartmentTypeSchema | None:
        query = f"""
        INSERT INTO {settings.POSTGRES_SCHEMA}.apartment_types (description, num_rooms, is_furnished)
        VALUES (:description, :num_rooms, :is_furnished) RETURNING *;
        """
        result = await session.execute(
            text(query),
            {"description": description, "num_rooms": num_rooms, "is_furnished": is_furnished},
        )
        await session.commit()
        apartment_type = result.mappings().first()
        return ApartmentTypeSchema.model_validate(obj=apartment_type) if apartment_type else None

    async def update_apartment_type(self, session: AsyncSession, type_id: int, **kwargs) -> ApartmentTypeSchema | None:
        updates = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
        query = f"""
        UPDATE {settings.POSTGRES_SCHEMA}.apartment_types
        SET {updates}
        WHERE id = :type_id
        RETURNING *;
        """
        params = {"type_id": type_id, **kwargs}
        result = await session.execute(text(query), params)
        await session.commit()
        apartment_type = result.mappings().first()
        return ApartmentTypeSchema.model_validate(obj=apartment_type) if apartment_type else None

    async def delete_apartment_type(self, session: AsyncSession, type_id: int) -> bool:
        query = f"DELETE FROM {settings.POSTGRES_SCHEMA}.apartment_types WHERE id = :type_id;"
        result = await session.execute(text(query), {"type_id": type_id})
        await session.commit()
        return result.rowcount > 0
