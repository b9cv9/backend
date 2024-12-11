import datetime
from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.status import StatusSchema
from project.infrastructure.postgres.models import Status
from project.core.config import settings

class StatusRepository:
    _collection: Type[Status] = Status

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_statuses(self, session: AsyncSession) -> list[StatusSchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.status;"
        statuses = await session.execute(text(query))
        return [StatusSchema.model_validate(obj=status) for status in statuses.mappings().all()]

    async def get_status_by_id(self, session: AsyncSession, status_id: int) -> StatusSchema | None:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.status WHERE id = :status_id;"
        result = await session.execute(text(query), {"status_id": status_id})
        status = result.mappings().first()
        return StatusSchema.model_validate(obj=status) if status else None

    async def insert_status(self, session: AsyncSession, date_listed: datetime.date | None, is_active: bool) -> StatusSchema | None:
        query = f"""
        INSERT INTO {settings.POSTGRES_SCHEMA}.status (date_listed, is_active)
        VALUES (:date_listed, :is_active) RETURNING *;
        """
        result = await session.execute(
            text(query),
            {"date_listed": date_listed, "is_active": is_active},
        )
        await session.commit()
        status = result.mappings().first()
        return StatusSchema.model_validate(obj=status) if status else None

    async def update_status(self, session: AsyncSession, status_id: int, **kwargs) -> StatusSchema | None:
        updates = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
        query = f"""
        UPDATE {settings.POSTGRES_SCHEMA}.status
        SET {updates}
        WHERE id = :status_id
        RETURNING *;
        """
        params = {"status_id": status_id, **kwargs}
        result = await session.execute(text(query), params)
        await session.commit()
        status = result.mappings().first()
        return StatusSchema.model_validate(obj=status) if status else None

    async def delete_status(self, session: AsyncSession, status_id: int) -> bool:
        query = f"DELETE FROM {settings.POSTGRES_SCHEMA}.status WHERE id = :status_id;"
        result = await session.execute(text(query), {"status_id": status_id})
        await session.commit()
        return result.rowcount > 0
