from pydantic import BaseModel
from datetime import datetime

class StatusSchema(BaseModel):
    id: int
    date_listed: datetime | None
    is_active: bool

    class Config:
        orm_mode = True
