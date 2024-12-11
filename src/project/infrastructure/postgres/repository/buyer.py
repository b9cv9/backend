from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.buyer import BuyerSchema
from project.infrastructure.postgres.models import Buyer
from project.core.config import settings

class BuyerRepository:
    _collection: Type[Buyer] = Buyer

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_buyers(self, session: AsyncSession) -> list[BuyerSchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.buyers;"
        buyers = await session.execute(text(query))
        return [BuyerSchema.model_validate(obj=buyer) for buyer in buyers.mappings().all()]

    async def get_buyer_by_id(self, session: AsyncSession, buyer_id: int) -> BuyerSchema | None:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.buyers WHERE id = :buyer_id;"
        result = await session.execute(text(query), {"buyer_id": buyer_id})
        buyer = result.mappings().first()
        return BuyerSchema.model_validate(obj=buyer) if buyer else None

    async def insert_buyer(self, session: AsyncSession, **kwargs) -> BuyerSchema | None:
        keys = ", ".join(kwargs.keys())
        values = ", ".join([f":{key}" for key in kwargs.keys()])
        query = f"INSERT INTO {settings.POSTGRES_SCHEMA}.buyers ({keys}) VALUES ({values}) RETURNING *;"
        result = await session.execute(text(query), kwargs)
        await session.commit()
        buyer = result.mappings().first()
        return BuyerSchema.model_validate(obj=buyer) if buyer else None

    async def update_buyer(self, session: AsyncSession, buyer_id: int, **kwargs) -> BuyerSchema | None:
        updates = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
        query = f"""
        UPDATE {settings.POSTGRES_SCHEMA}.buyers
        SET {updates}
        WHERE id = :buyer_id
        RETURNING *;
        """
        params = {"buyer_id": buyer_id, **kwargs}
        result = await session.execute(text(query), params)
        await session.commit()
        buyer = result.mappings().first()
        return BuyerSchema.model_validate(obj=buyer) if buyer else None

    async def delete_buyer(self, session: AsyncSession, buyer_id: int) -> bool:
        query = f"DELETE FROM {settings.POSTGRES_SCHEMA}.buyers WHERE id = :buyer_id;"
        result = await session.execute(text(query), {"buyer_id": buyer_id})
        await session.commit()
        return result.rowcount > 0
