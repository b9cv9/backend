from pydantic import BaseModel

class AgencySchema(BaseModel):
    id: int
    name: str
    address: str
    contact_info: str
    comission_rate: float | None

    class Config:
        orm_mode = True