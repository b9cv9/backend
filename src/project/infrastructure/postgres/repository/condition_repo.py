from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.condition import ConditionSchema
from project.infrastructure.postgres.models import Condition
from project.core.config import settings

class ConditionRepository:
    _collection: Type[Condition] = Condition

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_conditions(self, session: AsyncSession) -> list[ConditionSchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.conditions;"
        conditions = await session.execute(text(query))
        return [ConditionSchema.model_validate(obj=condition) for condition in conditions.mappings().all()]

    async def get_condition_by_id(self, session: AsyncSession, condition_id: int) -> ConditionSchema | None:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.conditions WHERE id = :condition_id;"
        result = await session.execute(text(query), {"condition_id": condition_id})
        condition = result.mappings().first()
        return ConditionSchema.model_validate(obj=condition) if condition else None

    async def insert_condition(
        self, session: AsyncSession, description: str, price: float, for_sale: bool
    ) -> ConditionSchema | None:
        query = f"""
        INSERT INTO {settings.POSTGRES_SCHEMA}.conditions (description, price, for_sale)
        VALUES (:description, :price, :for_sale) RETURNING *;
        """
        result = await session.execute(
            text(query),
            {"description": description, "price": price, "for_sale": for_sale},
        )
        await session.commit()
        condition = result.mappings().first()
        return ConditionSchema.model_validate(obj=condition) if condition else None

    async def update_condition(self, session: AsyncSession, condition_id: int, **kwargs) -> ConditionSchema | None:
        updates = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
        query = f"""
        UPDATE {settings.POSTGRES_SCHEMA}.conditions
        SET {updates}
        WHERE id = :condition_id
        RETURNING *;
        """
        params = {"condition_id": condition_id, **kwargs}
        result = await session.execute(text(query), params)
        await session.commit()
        condition = result.mappings().first()
        return ConditionSchema.model_validate(obj=condition) if condition else None

    async def delete_condition(self, session: AsyncSession, condition_id: int) -> bool:
        query = f"DELETE FROM {settings.POSTGRES_SCHEMA}.conditions WHERE id = :condition_id;"
        result = await session.execute(text(query), {"condition_id": condition_id})
        await session.commit()
        return result.rowcount > 0
