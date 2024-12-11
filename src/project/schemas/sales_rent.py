from pydantic import BaseModel
from datetime import datetime

class SalesRentSchema(BaseModel):
    id: int
    apartment_id: int
    renter_id: int
    owner_id: int
    realtor_id: int
    sale_date: datetime
    sale_price: float
    commission: float
    profit: float
    rent_start: datetime | None
    rent_end: datetime | None

    class Config:
        orm_mode = True
