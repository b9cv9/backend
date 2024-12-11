import datetime
from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.sales import SaleSchema
from project.infrastructure.postgres.models import Sale
from project.core.config import settings

class SaleRepository:
    _collection: Type[Sale] = Sale

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_sales(self, session: AsyncSession) -> list[SaleSchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.sales;"
        sales = await session.execute(text(query))
        return [SaleSchema.model_validate(obj=sale) for sale in sales.mappings().all()]

    async def get_sale_by_id(self, session: AsyncSession, sale_id: int) -> SaleSchema | None:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.sales WHERE id = :sale_id;"
        result = await session.execute(text(query), {"sale_id": sale_id})
        sale = result.mappings().first()
        return SaleSchema.model_validate(obj=sale) if sale else None

    async def insert_sale(
        self,
        session: AsyncSession,
        apartment_id: int,
        buyer_id: int,
        seller_id: int,
        realtor_id: int,
        sale_date: datetime.date,
        sale_price: float,
        commission: float,
        profit: float,
    ) -> SaleSchema | None:
        query = f"""
        INSERT INTO {settings.POSTGRES_SCHEMA}.sales (
            apartment_id, buyer_id, seller_id, realtor_id, sale_date, sale_price, commission, profit
        ) VALUES (
            :apartment_id, :buyer_id, :seller_id, :realtor_id, :sale_date, :sale_price, :commission, :profit
        ) RETURNING *;
        """
        result = await session.execute(
            text(query),
            {
                "apartment_id": apartment_id,
                "buyer_id": buyer_id,
                "seller_id": seller_id,
                "realtor_id": realtor_id,
                "sale_date": sale_date,
                "sale_price": sale_price,
                "commission": commission,
                "profit": profit,
            },
        )
        await session.commit()
        sale = result.mappings().first()
        return SaleSchema.model_validate(obj=sale) if sale else None

    async def update_sale(self, session: AsyncSession, sale_id: int, **kwargs) -> SaleSchema | None:
        updates = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
        query = f"""
        UPDATE {settings.POSTGRES_SCHEMA}.sales
        SET {updates}
        WHERE id = :sale_id
        RETURNING *;
        """
        params = {"sale_id": sale_id, **kwargs}
        result = await session.execute(text(query), params)
        await session.commit()
        sale = result.mappings().first()
        return SaleSchema.model_validate(obj=sale) if sale else None

    async def delete_sale(self, session: AsyncSession, sale_id: int) -> bool:
        query = f"DELETE FROM {settings.POSTGRES_SCHEMA}.sales WHERE id = :sale_id;"
        result = await session.execute(text(query), {"sale_id": sale_id})
        await session.commit()
        return result.rowcount > 0
