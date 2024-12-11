from pydantic import BaseModel

class DistrictSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
