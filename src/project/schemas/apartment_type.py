from pydantic import BaseModel

class ApartmentTypeSchema(BaseModel):
    id: int
    description: str
    num_rooms: int | None
    is_furnished: bool | None

    class Config:
        orm_mode = True
