from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.agency import AgencySchema
from project.infrastructure.postgres.models import Agency
from project.core.config import settings

class AgencyRepository:
    _collection: Type[Agency] = Agency

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_agencies(self, session: AsyncSession) -> list[AgencySchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.agencies;"
        agencies = await session.execute(text(query))
        return [AgencySchema.model_validate(obj=agency) for agency in agencies.mappings().all()]

    async def get_agency_by_id(self, session: AsyncSession, agency_id: int) -> AgencySchema | None:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.agencies WHERE id = :agency_id;"
        result = await session.execute(text(query), {"agency_id": agency_id})
        agency = result.mappings().first()
        return AgencySchema.model_validate(obj=agency) if agency else None

    async def insert_agency(self, session: AsyncSession, **kwargs) -> AgencySchema | None:
        keys = ", ".join(kwargs.keys())
        values = ", ".join([f":{key}" for key in kwargs.keys()])
        query = f"INSERT INTO {settings.POSTGRES_SCHEMA}.agencies ({keys}) VALUES ({values}) RETURNING *;"
        result = await session.execute(text(query), kwargs)
        await session.commit()
        agency = result.mappings().first()
        return AgencySchema.model_validate(obj=agency) if agency else None

    async def update_agency(self, session: AsyncSession, agency_id: int, **kwargs) -> AgencySchema | None:
        updates = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
        query = f"""
        UPDATE {settings.POSTGRES_SCHEMA}.agencies
        SET {updates}
        WHERE id = :agency_id
        RETURNING *;
        """
        params = {"agency_id": agency_id, **kwargs}
        result = await session.execute(text(query), params)
        await session.commit()
        agency = result.mappings().first()
        return AgencySchema.model_validate(obj=agency) if agency else None

    async def delete_agency(self, session: AsyncSession, agency_id: int) -> bool:
        query = f"DELETE FROM {settings.POSTGRES_SCHEMA}.agencies WHERE id = :agency_id;"
        result = await session.execute(text(query), {"agency_id": agency_id})
        await session.commit()
        return result.rowcount > 0
