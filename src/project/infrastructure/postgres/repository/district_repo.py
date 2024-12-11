from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.district import DistrictSchema
from project.infrastructure.postgres.models import District
from project.core.config import settings

class DistrictRepository:
    _collection: Type[District] = District

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_districts(self, session: AsyncSession) -> list[DistrictSchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.districts;"
        districts = await session.execute(text(query))
        return [DistrictSchema.model_validate(obj=district) for district in districts.mappings().all()]

    async def get_district_by_id(self, session: AsyncSession, district_id: int) -> DistrictSchema | None:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.districts WHERE id = :district_id;"
        result = await session.execute(text(query), {"district_id": district_id})
        district = result.mappings().first()
        return DistrictSchema.model_validate(obj=district) if district else None

    async def insert_district(self, session: AsyncSession, name: str) -> DistrictSchema | None:
        query = f"INSERT INTO {settings.POSTGRES_SCHEMA}.districts (name) VALUES (:name) RETURNING *;"
        result = await session.execute(text(query), {"name": name})
        await session.commit()
        district = result.mappings().first()
        return DistrictSchema.model_validate(obj=district) if district else None

    async def update_district(self, session: AsyncSession, district_id: int, name: str) -> DistrictSchema | None:
        query = f"""
        UPDATE {settings.POSTGRES_SCHEMA}.districts
        SET name = :name
        WHERE id = :district_id
        RETURNING *;
        """
        params = {"district_id": district_id, "name": name}
        result = await session.execute(text(query), params)
        await session.commit()
        district = result.mappings().first()
        return DistrictSchema.model_validate(obj=district) if district else None

    async def delete_district(self, session: AsyncSession, district_id: int) -> bool:
        query = f"DELETE FROM {settings.POSTGRES_SCHEMA}.districts WHERE id = :district_id;"
        result = await session.execute(text(query), {"district_id": district_id})
        await session.commit()
        return result.rowcount > 0
