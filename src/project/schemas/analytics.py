from pydantic import BaseModel
from datetime import date

class AnalyticsSchema(BaseModel):
    apartment_id: int
    price: int
    date_of_price: date
    reviews: str | None

    class Config:
        orm_mode = True
