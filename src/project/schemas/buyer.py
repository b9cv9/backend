from pydantic import BaseModel
from datetime import date

class BuyerSchema(BaseModel):
    id: int
    username: str
    password: str
    name: str
    contact_info: str
    birth_date: date
    gender: str

    class Config:
        orm_mode = True
