from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.analytics import AnalyticsSchema
from project.infrastructure.postgres.models import Analytics
from project.core.config import settings

class AnalyticsRepository:
    _collection: Type[Analytics] = Analytics

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_analytics(self, session: AsyncSession) -> list[AnalyticsSchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.analytics;"
        analytics = await session.execute(text(query))
        return [AnalyticsSchema.model_validate(obj=analytic) for analytic in analytics.mappings().all()]
