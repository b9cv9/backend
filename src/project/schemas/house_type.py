from pydantic import BaseModel

class HouseTypeSchema(BaseModel):
    id: int
    description: str
    type: str | None

    class Config:
        orm_mode = True
