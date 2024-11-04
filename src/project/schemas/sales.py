import datetime
from pydantic import BaseModel, ConfigDict

class SalesRentSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    apartment_id: int
    renter_id: int
    realtor_id: int
    sale_date: datetime.datetime
    rent_start: datetime.datetime | None = None
    rent_end: datetime.datetime | None = None
    sale_price: float | None = None