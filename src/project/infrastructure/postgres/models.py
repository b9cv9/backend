from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from project.infrastructure.postgres.database import Base


class Apartment(Base):
    __tablename__ = "apartments"

    id: Mapped[int] = mapped_column(primary_key=True)
    apartment_number: Mapped[str] = mapped_column(nullable=False)
    square_meters: Mapped[float] = mapped_column(nullable=False)
    status_id: Mapped[int] = mapped_column(nullable=False)
    owner_price: Mapped[float] = mapped_column(nullable=False)

    owner_id: Mapped[int] = mapped_column(ForeignKey("owners.id"))
    owner = relationship("Owner", back_populates="apartments")
    sales_rent = relationship("SalesRent", back_populates="apartment")


class SalesRent(Base):
    __tablename__ = "sales_rent"

    id: Mapped[int] = mapped_column(primary_key=True)
    apartment_id: Mapped[int] = mapped_column(ForeignKey("apartments.id"))
    renter_id: Mapped[int] = mapped_column(ForeignKey("renters.id"))
    realtor_id: Mapped[int] = mapped_column(ForeignKey("realtors.id"))
    sale_date: Mapped[str] = mapped_column(nullable=False)
    rent_start: Mapped[str] = mapped_column(nullable=True)
    rent_end: Mapped[str] = mapped_column(nullable=True)
    sale_price: Mapped[float] = mapped_column(nullable=True)

    apartment = relationship("Apartment", back_populates="sales_rent")
    renter = relationship("Renter", back_populates="sales_rent")


class Owner(Base):
    __tablename__ = "owners"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    contact_info: Mapped[str] = mapped_column(nullable=True)

    apartments = relationship("Apartment", back_populates="owner")
