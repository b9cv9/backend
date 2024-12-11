from pydantic.v1 import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from pydantic import BaseModel


class ApartmentPhotoSchema(BaseModel):
    id: int
    apartment_id: int
    photo_url: str

    class Config:
        orm_mode = True