from pydantic import BaseModel
from datetime import date

class RealtorSchema(BaseModel):
    id: int
    username: str
    password: str
    name: str
    contact_info: str
    birth_date: date
    gender: str
    agency_id: int

    class Config:
        orm_mode = True
