from pydantic import BaseModel

class ConditionSchema(BaseModel):
    id: int
    description: str
    price: float
    for_sale: bool

    class Config:
        orm_mode = True
