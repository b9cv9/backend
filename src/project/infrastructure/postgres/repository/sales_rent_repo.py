from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from datetime import datetime

from project.schemas.sales_rent import SalesRentSchema
from project.infrastructure.postgres.models import SalesRent
from project.core.config import settings


class SalesRentRepository:
    _collection: Type[SalesRent] = SalesRent

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_sales_rent(self, session: AsyncSession) -> list[SalesRentSchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.sales_rent;"
        sales_rent = await session.execute(text(query))
        return [SalesRentSchema.model_validate(obj=sale_rent) for sale_rent in sales_rent.mappings().all()]

    async def get_sales_rent_by_id(self, session: AsyncSession, rent_id: int) -> SalesRentSchema | None:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.sales_rent WHERE id = :rent_id;"
        result = await session.execute(text(query), {"rent_id": rent_id})
        sale_rent = result.mappings().first()
        return SalesRentSchema.model_validate(obj=sale_rent) if sale_rent else None

    async def insert_sales_rent(
        self,
        session: AsyncSession,
        apartment_id: int,
        renter_id: int,
        owner_id: int,
        realtor_id: int,
        sale_date: datetime,
        sale_price: float,
        commission: float,
        profit: float,
        rent_start: datetime | None = None,
        rent_end: datetime | None = None,
    ) -> SalesRentSchema | None:
        query = f"""
        INSERT INTO {settings.POSTGRES_SCHEMA}.sales_rent (
            apartment_id, renter_id, owner_id, realtor_id, sale_date, sale_price, commission, profit, rent_start, rent_end
        ) VALUES (
            :apartment_id, :renter_id, :owner_id, :realtor_id, :sale_date, :sale_price, :commission, :profit, :rent_start, :rent_end
        ) RETURNING *;
        """
        result = await session.execute(
            text(query),
            {
                "apartment_id": apartment_id,
                "renter_id": renter_id,
                "owner_id": owner_id,
                "realtor_id": realtor_id,
                "sale_date": sale_date,
                "sale_price": sale_price,
                "commission": commission,
                "profit": profit,
                "rent_start": rent_start,
                "rent_end": rent_end,
            },
        )
        await session.commit()
        sale_rent = result.mappings().first()
        return SalesRentSchema.model_validate(obj=sale_rent) if sale_rent else None

    async def update_sales_rent(self, session: AsyncSession, rent_id: int, **kwargs) -> SalesRentSchema | None:
        updates = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
        query = f"""
        UPDATE {settings.POSTGRES_SCHEMA}.sales_rent
        SET {updates}
        WHERE id = :rent_id
        RETURNING *;
        """
        params = {"rent_id": rent_id, **kwargs}
        result = await session.execute(text(query), params)
        await session.commit()
        sale_rent = result.mappings().first()
        return SalesRentSchema.model_validate(obj=sale_rent) if sale_rent else None

    async def delete_sales_rent(self, session: AsyncSession, rent_id: int) -> bool:
        query = f"DELETE FROM {settings.POSTGRES_SCHEMA}.sales_rent WHERE id = :rent_id;"
        result = await session.execute(text(query), {"rent_id": rent_id})
        await session.commit()
        return result.rowcount > 0
