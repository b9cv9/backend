import datetime
from pydantic import BaseModel, ConfigDict

class ApartmentSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    apartment_number: str
    square_meters: float
    status_id: int
    owner_price: float
    owner_id: int