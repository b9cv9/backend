from pydantic import BaseModel

class HouseSchema(BaseModel):
    id: int
    street_id: int
    house_number: str
    type_id: int
    floors: int | None

    class Config:
        orm_mode = True
