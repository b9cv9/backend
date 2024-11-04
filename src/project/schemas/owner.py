import datetime
from pydantic import BaseModel, ConfigDict

class OwnerSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    contact_info: str | None = None