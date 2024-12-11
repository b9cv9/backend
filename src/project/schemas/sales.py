from pydantic import BaseModel
from datetime import datetime

class SaleSchema(BaseModel):
    id: int
    apartment_id: int
    buyer_id: int
    seller_id: int
    realtor_id: int
    sale_date: datetime
    sale_price: float
    commission: float
    profit: float

    class Config:
        orm_mode = True
