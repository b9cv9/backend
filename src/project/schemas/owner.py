from datetime import date

from pydantic import BaseModel

class OwnerSchema(BaseModel):
    owners_id: int
    username: str
    password: str
    name: str
    contact_info: str
    birth_date: date
    gender: str

    class Config:
        orm_mode = True