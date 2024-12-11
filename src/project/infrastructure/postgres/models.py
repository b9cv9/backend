from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Date, CHAR, DECIMAL, Integer, DateTime, ForeignKey, Float, Boolean, Text
from datetime import date
from project.infrastructure.postgres.database import Base


class Analytics(Base):
    __tablename__ = "analytics"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("buyers.id"), nullable=False)
    apartment_id: Mapped[int] = mapped_column(ForeignKey("apartments.id"), nullable=False)
    event_type: Mapped[str] = mapped_column(String(255), nullable=False)
    event_timestamp: Mapped[date] = mapped_column(nullable=False)

    user: Mapped["Buyer"] = relationship("Buyer", back_populates="analytics")
    apartment: Mapped["Apartment"] = relationship("Apartment", back_populates="analytics_events")


class Agency(Base):
    __tablename__ = "agencies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    contact_info: Mapped[str] = mapped_column(String(255), nullable=False)
    comission_rate: Mapped[float] = mapped_column(DECIMAL(5, 2))

    realtors: Mapped[list["Realtor"]] = relationship("Realtor", back_populates="agency")


class Owner(Base):
    __tablename__ = "owners"

    owners_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    contact_info: Mapped[str] = mapped_column(String(255), nullable=False)
    birth_date: Mapped[date] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(CHAR(1), nullable=False)

    apartments: Mapped[list["Apartment"]] = relationship("Apartment", back_populates="owner")
    sales: Mapped[list["Sale"]] = relationship("Sale", back_populates="seller")
    rentals: Mapped[list["SalesRent"]] = relationship("SalesRent", back_populates="owner")


class Realtor(Base):
    __tablename__ = "realtors"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    contact_info: Mapped[str] = mapped_column(String(255), nullable=False)
    birth_date: Mapped[date] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    agency_id: Mapped[int] = mapped_column(ForeignKey("agencies.id"), nullable=False)

    agency: Mapped["Agency"] = relationship("Agency", back_populates="realtors")
    sales: Mapped[list["Sale"]] = relationship("Sale", back_populates="realtor")
    rentals: Mapped[list["SalesRent"]] = relationship("SalesRent", back_populates="realtor")


class Buyer(Base):
    __tablename__ = "buyers"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    contact_info: Mapped[str] = mapped_column(String(255), nullable=False)
    birth_date: Mapped[date] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(CHAR(1), nullable=False)

    sales: Mapped[list["Sale"]] = relationship("Sale", back_populates="buyer")
    rentals: Mapped[list["SalesRent"]] = relationship("SalesRent", back_populates="buyer")


class District(Base):
    __tablename__ = "districts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    streets: Mapped[list["Street"]] = relationship("Street", back_populates="district")


class Street(Base):
    __tablename__ = "streets"

    id: Mapped[int] = mapped_column(primary_key=True)
    district_id: Mapped[int] = mapped_column(ForeignKey("districts.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    district: Mapped["District"] = relationship("District", back_populates="streets")
    houses: Mapped[list["House"]] = relationship("House", back_populates="street")


class HouseType(Base):
    __tablename__ = "house_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(100))


class House(Base):
    __tablename__ = "houses"

    id: Mapped[int] = mapped_column(primary_key=True)
    street_id: Mapped[int] = mapped_column(ForeignKey("streets.id"), nullable=False)
    house_number: Mapped[str] = mapped_column(String(50), nullable=False)
    type_id: Mapped[int] = mapped_column(ForeignKey("house_types.id"), nullable=False)
    floors: Mapped[int] = mapped_column()

    street: Mapped["Street"] = relationship("Street", back_populates="houses")


class ApartmentType(Base):
    __tablename__ = "apartment_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    num_rooms: Mapped[int] = mapped_column()
    is_furnished: Mapped[bool] = mapped_column()


class Condition(Base):
    __tablename__ = "conditions"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    for_sale: Mapped[bool] = mapped_column(nullable=False)


class Status(Base):
    __tablename__ = "status"

    id: Mapped[int] = mapped_column(primary_key=True)
    date_listed: Mapped[date] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(nullable=False)


class Apartment(Base):
    __tablename__ = "apartments"

    id: Mapped[int] = mapped_column(primary_key=True)
    house_id: Mapped[int] = mapped_column(ForeignKey("houses.id"), nullable=True)
    apartment_number: Mapped[str] = mapped_column(String(50), nullable=False)
    type_id: Mapped[int] = mapped_column(ForeignKey("apartment_types.id"), nullable=False)
    square_meters: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("owners.owners_id"), nullable=True)
    condition_id: Mapped[int] = mapped_column(ForeignKey("conditions.id"), nullable=True)
    status_id: Mapped[int] = mapped_column(ForeignKey("status.id"), nullable=True)
    owner_price: Mapped[float] = mapped_column(nullable=False)

    owner: Mapped["Owner"] = relationship("Owner", back_populates="apartments")


class ApartmentPhoto(Base):
    __tablename__ = "apartment_photos"

    id: Mapped[int] = mapped_column(primary_key=True)
    apartment_id: Mapped[int] = mapped_column(ForeignKey("apartments.id"), nullable=False)
    photo_url: Mapped[str] = mapped_column(String(255), nullable=False)

    apartment: Mapped["Apartment"] = relationship("Apartment")


class Sale(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(primary_key=True)
    apartment_id: Mapped[int] = mapped_column(ForeignKey("apartments.id"), nullable=False)
    buyer_id: Mapped[int] = mapped_column(ForeignKey("buyers.id"), nullable=False)
    seller_id: Mapped[int] = mapped_column(ForeignKey("owners.owners_id"), nullable=False)
    realtor_id: Mapped[int] = mapped_column(ForeignKey("realtors.id"), nullable=False)
    sale_date: Mapped[date] = mapped_column(DateTime, nullable=False)
    sale_price: Mapped[float] = mapped_column(nullable=False)
    commission: Mapped[float] = mapped_column(nullable=False)
    profit: Mapped[float] = mapped_column(nullable=False)

    buyer: Mapped["Buyer"] = relationship("Buyer", back_populates="sales")
    seller: Mapped["Owner"] = relationship("Owner", back_populates="sales")
    realtor: Mapped["Realtor"] = relationship("Realtor", back_populates="sales")


class SalesRent(Base):
    __tablename__ = "sales_rent"

    id: Mapped[int] = mapped_column(primary_key=True)
    apartment_id: Mapped[int] = mapped_column(ForeignKey("apartments.id"), nullable=False)
    renter_id: Mapped[int] = mapped_column(ForeignKey("buyers.id"), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("owners.owners_id"), nullable=False)
    realtor_id: Mapped[int] = mapped_column(ForeignKey("realtors.id"), nullable=False)
    start_date: Mapped[date] = mapped_column(nullable=False)
    end_date: Mapped[date] = mapped_column(nullable=True)
    rent_price: Mapped[float] = mapped_column(nullable=False)

    renter: Mapped["Buyer"] = relationship("Buyer", back_populates="rentals")
    owner: Mapped["Owner"] = relationship("Owner", back_populates="rentals")
    realtor: Mapped["Realtor"] = relationship("Realtor", back_populates="rentals")
