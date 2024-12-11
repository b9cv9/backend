from pydantic import BaseModel

class StreetSchema(BaseModel):
    id: int
    district_id: int
    name: str

    class Config:
        orm_mode = True
