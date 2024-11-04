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
