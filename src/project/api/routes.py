from fastapi import APIRouter, HTTPException
from src.project.infrastructure.postgres.database import PostgresDatabase
from src.project.infrastructure.postgres.repository.agency_repo import AgencyRepository
from src.project.infrastructure.postgres.repository.owner_repo import OwnerRepository
from src.project.infrastructure.postgres.repository.realtor_repo import RealtorRepository
from src.project.infrastructure.postgres.repository.buyer import BuyerRepository
from src.project.infrastructure.postgres.repository.district_repo import DistrictRepository
from src.project.infrastructure.postgres.repository.street_repo import StreetRepository
from src.project.infrastructure.postgres.repository.house_repo import HouseRepository
from src.project.infrastructure.postgres.repository.apartment_type_repo import ApartmentTypeRepository
from src.project.infrastructure.postgres.repository.condition_repo import ConditionRepository
from src.project.infrastructure.postgres.repository.status_repo import StatusRepository
from src.project.infrastructure.postgres.repository.apartment_repo import ApartmentRepository
from src.project.infrastructure.postgres.repository.apartment_photo_repo import ApartmentPhotoRepository
from src.project.infrastructure.postgres.repository.sales_repo import SaleRepository
from src.project.infrastructure.postgres.repository.sales_rent_repo import SalesRentRepository
from src.project.infrastructure.postgres.repository.house_type_repo import HouseTypeRepository
from src.project.schemas.agency import AgencySchema
from src.project.schemas.owner import OwnerSchema
from src.project.schemas.realtor import RealtorSchema
from src.project.schemas.buyer import BuyerSchema
from src.project.schemas.district import DistrictSchema
from src.project.schemas.street import StreetSchema
from src.project.schemas.house import HouseSchema
from src.project.schemas.apartment_type import ApartmentTypeSchema
from src.project.schemas.condition import ConditionSchema
from src.project.schemas.status import StatusSchema
from src.project.schemas.apartment import ApartmentSchema
from src.project.schemas.apartment_photo import ApartmentPhotoSchema
from src.project.schemas.sales import SaleSchema
from src.project.schemas.sales_rent import SalesRentSchema
from src.project.schemas.house_type import HouseTypeSchema

router = APIRouter()


# Agency CRUD

@router.get("/all_agencies", response_model=list[AgencySchema])
async def get_all_agencies():
    agency_repo = AgencyRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await agency_repo.check_connection(session=session)
        all_agencies = await agency_repo.get_all_agencies(session=session)

    return all_agencies


@router.get("/agency/{id}", response_model=AgencySchema)
async def get_agency_by_id(id: int) -> AgencySchema:
    agency_repo = AgencyRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await agency_repo.check_connection(session=session)
        agency = await agency_repo.get_agency_by_id(session=session, agency_id=id)

    if not agency:
        raise HTTPException(status_code=404, detail="Agency not found")

    return agency


@router.post("/agency", response_model=AgencySchema)
async def insert_agency(agency: AgencySchema) -> AgencySchema:
    agency_repo = AgencyRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await agency_repo.check_connection(session=session)
        new_agency = await agency_repo.insert_agency(session=session,
                                                     name=agency.name,
                                                     address=agency.address,
                                                     contact_info=agency.contact_info,
                                                     comission_rate=agency.comission_rate)

    if not new_agency:
        raise HTTPException(status_code=500, detail="Failed to insert agency")

    return new_agency


@router.delete("/agency/{id}", response_model=dict)
async def delete_agency(id: int) -> dict:
    agency_repo = AgencyRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await agency_repo.check_connection(session=session)
        deleted = await agency_repo.delete_agency(session=session, agency_id=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Agency not found or failed to delete")

    return {"message": "Agency deleted successfully"}


@router.put("/agency/{id}", response_model=AgencySchema)
async def update_agency(id: int, agency: AgencySchema) -> AgencySchema:
    agency_repo = AgencyRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await agency_repo.check_connection(session=session)
        updated_agency = await agency_repo.update_agency(session=session, agency_id=id, name=agency.name,
                                                         address=agency.address, contact_info=agency.contact_info,
                                                         comission_rate=agency.comission_rate)

    if not updated_agency:
        raise HTTPException(status_code=404, detail="Agency not found or failed to update")

    return updated_agency


# Owner CRUD

@router.get("/all_owners", response_model=list[OwnerSchema])
async def get_all_owners():
    owner_repo = OwnerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await owner_repo.check_connection(session=session)
        all_owners = await owner_repo.get_all_owners(session=session)

    return all_owners


@router.get("/owner/{id}", response_model=OwnerSchema)
async def get_owner_by_id(id: int) -> OwnerSchema:
    owner_repo = OwnerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await owner_repo.check_connection(session=session)
        owner = await owner_repo.get_owner_by_id(session=session, owner_id=id)

    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")

    return owner


@router.post("/owner", response_model=OwnerSchema)
async def insert_owner(owner: OwnerSchema) -> OwnerSchema:
    owner_repo = OwnerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await owner_repo.check_connection(session=session)
        new_owner = await owner_repo.insert_owner(session=session,
                                                  username=owner.username,
                                                  password=owner.password,
                                                  name=owner.name,
                                                  contact_info=owner.contact_info,
                                                  birth_date=owner.birth_date,
                                                  gender=owner.gender)

    if not new_owner:
        raise HTTPException(status_code=500, detail="Failed to insert owner")

    return new_owner


@router.delete("/owner/{id}", response_model=dict)
async def delete_owner(id: int) -> dict:
    owner_repo = OwnerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await owner_repo.check_connection(session=session)
        deleted = await owner_repo.delete_owner(session=session, owner_id=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Owner not found or failed to delete")

    return {"message": "Owner deleted successfully"}


@router.put("/owner/{id}", response_model=OwnerSchema)
async def update_owner(id: int, owner: OwnerSchema) -> OwnerSchema:
    owner_repo = OwnerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await owner_repo.check_connection(session=session)
        updated_owner = await owner_repo.update_owner(session=session, owner_id=id, username=owner.username,
                                                      password=owner.password, name=owner.name,
                                                      contact_info=owner.contact_info, birth_date=owner.birth_date,
                                                      gender=owner.gender)

    if not updated_owner:
        raise HTTPException(status_code=404, detail="Owner not found or failed to update")

    return updated_owner


# Realtor CRUD

@router.get("/all_realtors", response_model=list[RealtorSchema])
async def get_all_realtors():
    realtor_repo = RealtorRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await realtor_repo.check_connection(session=session)
        all_realtors = await realtor_repo.get_all_realtors(session=session)

    return all_realtors


@router.get("/realtor/{id}", response_model=RealtorSchema)
async def get_realtor_by_id(id: int) -> RealtorSchema:
    realtor_repo = RealtorRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await realtor_repo.check_connection(session=session)
        realtor = await realtor_repo.get_realtor_by_id(session=session, realtor_id=id)

    if not realtor:
        raise HTTPException(status_code=404, detail="Realtor not found")

    return realtor


@router.post("/realtor", response_model=RealtorSchema)
async def insert_realtor(realtor: RealtorSchema) -> RealtorSchema:
    realtor_repo = RealtorRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await realtor_repo.check_connection(session=session)
        new_realtor = await realtor_repo.insert_realtor(session=session, username=realtor.username, password=realtor.password,
                                                        name=realtor.name, contact_info=realtor.contact_info, birth_date=realtor.birth_date,
                                                        gender=realtor.gender, agency_id=realtor.agency_id)

    if not new_realtor:
        raise HTTPException(status_code=500, detail="Failed to insert realtor")

    return new_realtor


@router.delete("/realtor/{id}", response_model=dict)
async def delete_realtor(id: int) -> dict:
    realtor_repo = RealtorRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await realtor_repo.check_connection(session=session)
        deleted = await realtor_repo.delete_realtor(session=session, realtor_id=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Realtor not found or failed to delete")

    return {"message": "Realtor deleted successfully"}


@router.put("/realtor/{id}", response_model=RealtorSchema)
async def update_realtor(id: int, realtor: RealtorSchema) -> RealtorSchema:
    realtor_repo = RealtorRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await realtor_repo.check_connection(session=session)
        updated_realtor = await realtor_repo.update_realtor(session=session, realtor_id=id, username=realtor.username,
                                                            password=realtor.password, name=realtor.name,
                                                            contact_info=realtor.contact_info, birth_date=realtor.birth_date,
                                                            gender=realtor.gender, agency_id=realtor.agency_id)

    if not updated_realtor:
        raise HTTPException(status_code=404, detail="Realtor not found or failed to update")

    return updated_realtor


# Buyer CRUD

@router.get("/all_buyers", response_model=list[BuyerSchema])
async def get_all_buyers():
    buyer_repo = BuyerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await buyer_repo.check_connection(session=session)
        all_buyers = await buyer_repo.get_all_buyers(session=session)

    return all_buyers


@router.get("/buyer/{id}", response_model=BuyerSchema)
async def get_buyer_by_id(id: int) -> BuyerSchema:
    buyer_repo = BuyerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await buyer_repo.check_connection(session=session)
        buyer = await buyer_repo.get_buyer_by_id(session=session, buyer_id=id)

    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")

    return buyer


@router.post("/buyer", response_model=BuyerSchema)
async def insert_buyer(buyer: BuyerSchema) -> BuyerSchema:
    buyer_repo = BuyerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await buyer_repo.check_connection(session=session)
        new_buyer = await buyer_repo.insert_buyer(session=session, username=buyer.username, password=buyer.password,
                                                  name=buyer.name, contact_info=buyer.contact_info, birth_date=buyer.birth_date,
                                                  gender=buyer.gender)

    if not new_buyer:
        raise HTTPException(status_code=500, detail="Failed to insert buyer")

    return new_buyer


@router.delete("/buyer/{id}", response_model=dict)
async def delete_buyer(id: int) -> dict:
    buyer_repo = BuyerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await buyer_repo.check_connection(session=session)
        deleted = await buyer_repo.delete_buyer(session=session, buyer_id=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Buyer not found or failed to delete")

    return {"message": "Buyer deleted successfully"}


@router.put("/buyer/{id}", response_model=BuyerSchema)
async def update_buyer(id: int, buyer: BuyerSchema) -> BuyerSchema:
    buyer_repo = BuyerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await buyer_repo.check_connection(session=session)
        updated_buyer = await buyer_repo.update_buyer(session=session, buyer_id=id, username=buyer.username,
                                                      password=buyer.password, name=buyer.name,
                                                      contact_info=buyer.contact_info, birth_date=buyer.birth_date,
                                                      gender=buyer.gender)

    if not updated_buyer:
        raise HTTPException(status_code=404, detail="Buyer not found or failed to update")

    return updated_buyer


@router.get("/all_districts", response_model=list[DistrictSchema])
async def get_all_districts():
    district_repo = DistrictRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await district_repo.check_connection(session=session)
        all_districts = await district_repo.get_all_districts(session=session)

    return all_districts


@router.get("/district/{id}", response_model=DistrictSchema)
async def get_district_by_id(id: int) -> DistrictSchema:
    district_repo = DistrictRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await district_repo.check_connection(session=session)
        district = await district_repo.get_district_by_id(session=session, district_id=id)

    if not district:
        raise HTTPException(status_code=404, detail="District not found")

    return district


@router.post("/district", response_model=DistrictSchema)
async def insert_district(district: DistrictSchema) -> DistrictSchema:
    district_repo = DistrictRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await district_repo.check_connection(session=session)
        new_district = await district_repo.insert_district(session=session, name=district.name)

    if not new_district:
        raise HTTPException(status_code=500, detail="Failed to insert district")

    return new_district


@router.delete("/district/{id}", response_model=dict)
async def delete_district(id: int) -> dict:
    district_repo = DistrictRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await district_repo.check_connection(session=session)
        deleted = await district_repo.delete_district(session=session, district_id=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="District not found or failed to delete")

    return {"message": "District deleted successfully"}


@router.put("/district/{id}", response_model=DistrictSchema)
async def update_district(id: int, district: DistrictSchema) -> DistrictSchema:
    district_repo = DistrictRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await district_repo.check_connection(session=session)
        updated_district = await district_repo.update_district(session=session, district_id=id, name=district.name)

    if not updated_district:
        raise HTTPException(status_code=404, detail="District not found or failed to update")

    return updated_district



@router.get("/all_streets", response_model=list[StreetSchema])
async def get_all_streets():
    street_repo = StreetRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await street_repo.check_connection(session=session)
        all_streets = await street_repo.get_all_streets(session=session)

    return all_streets


@router.get("/street/{id}", response_model=StreetSchema)
async def get_street_by_id(id: int) -> StreetSchema:
    street_repo = StreetRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await street_repo.check_connection(session=session)
        street = await street_repo.get_street_by_id(session=session, street_id=id)

    if not street:
        raise HTTPException(status_code=404, detail="Street not found")

    return street


@router.post("/street", response_model=StreetSchema)
async def insert_street(street: StreetSchema) -> StreetSchema:
    street_repo = StreetRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await street_repo.check_connection(session=session)
        new_street = await street_repo.insert_street(session=session, name=street.name, district_id=street.district_id)

    if not new_street:
        raise HTTPException(status_code=500, detail="Failed to insert street")

    return new_street


@router.delete("/street/{id}", response_model=dict)
async def delete_street(id: int) -> dict:
    street_repo = StreetRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await street_repo.check_connection(session=session)
        deleted = await street_repo.delete_street(session=session, street_id=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Street not found or failed to delete")

    return {"message": "Street deleted successfully"}


@router.put("/street/{id}", response_model=StreetSchema)
async def update_street(id: int, street: StreetSchema) -> StreetSchema:
    street_repo = StreetRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await street_repo.check_connection(session=session)
        updated_street = await street_repo.update_street(session=session, street_id=id, name=street.name,
                                                         district_id=street.district_id)

    if not updated_street:
        raise HTTPException(status_code=404, detail="Street not found or failed to update")

    return updated_street



@router.get("/all_houses", response_model=list[HouseSchema])
async def get_all_houses():
    house_repo = HouseRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await house_repo.check_connection(session=session)
        all_houses = await house_repo.get_all_houses(session=session)

    return all_houses


@router.get("/house/{id}", response_model=HouseSchema)
async def get_house_by_id(id: int) -> HouseSchema:
    house_repo = HouseRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await house_repo.check_connection(session=session)
        house = await house_repo.get_house_by_id(session=session, house_id=id)

    if not house:
        raise HTTPException(status_code=404, detail="House not found")

    return house


@router.post("/house", response_model=HouseSchema)
async def insert_house(house: HouseSchema) -> HouseSchema:
    house_repo = HouseRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await house_repo.check_connection(session=session)
        new_house = await house_repo.insert_house(session=session, street_id=house.street_id, house_number=house.house_number,
                                                  type_id=house.type_id, floors=house.floors)

    if not new_house:
        raise HTTPException(status_code=500, detail="Failed to insert house")

    return new_house


@router.delete("/house/{id}", response_model=dict)
async def delete_house(id: int) -> dict:
    house_repo = HouseRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await house_repo.check_connection(session=session)
        deleted = await house_repo.delete_house(session=session, house_id=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="House not found or failed to delete")

    return {"message": "House deleted successfully"}


@router.put("/house/{id}", response_model=HouseSchema)
async def update_house(id: int, house: HouseSchema) -> HouseSchema:
    house_repo = HouseRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await house_repo.check_connection(session=session)
        updated_house = await house_repo.update_house(session=session, house_id=id, street_id=house.street_id, house_number=house.house_number,
                                                      type_id=house.house_type_id, floors=house.floors)

    if not updated_house:
        raise HTTPException(status_code=404, detail="House not found or failed to update")

    return updated_house



@router.get("/all_apartment_types", response_model=list[ApartmentTypeSchema])
async def get_all_apartment_types():
    apartment_type_repo = ApartmentTypeRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await apartment_type_repo.check_connection(session=session)
        all_apartment_types = await apartment_type_repo.get_all_apartment_types(session=session)

    return all_apartment_types


@router.get("/apartment_type/{id}", response_model=ApartmentTypeSchema)
async def get_apartment_type_by_id(id: int) -> ApartmentTypeSchema:
    apartment_type_repo = ApartmentTypeRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await apartment_type_repo.check_connection(session=session)
        apartment_type = await apartment_type_repo.get_apartment_type_by_id(session=session, type_id=id)

    if not apartment_type:
        raise HTTPException(status_code=404, detail="Apartment Type not found")

    return apartment_type


@router.post("/apartment_type", response_model=ApartmentTypeSchema)
async def insert_apartment_type(apartment_type: ApartmentTypeSchema) -> ApartmentTypeSchema:
    apartment_type_repo = ApartmentTypeRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await apartment_type_repo.check_connection(session=session)
        new_apartment_type = await apartment_type_repo.insert_apartment_type(session=session,
                                                                            num_rooms=apartment_type.num_rooms,
                                                                            is_furnished=apartment_type.is_furnished,
                                                                            description=apartment_type.description)

    if not new_apartment_type:
        raise HTTPException(status_code=500, detail="Failed to insert apartment type")

    return new_apartment_type


@router.delete("/apartment_type/{id}", response_model=dict)
async def delete_apartment_type(id: int) -> dict:
    apartment_type_repo = ApartmentTypeRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await apartment_type_repo.check_connection(session=session)
        deleted = await apartment_type_repo.delete_apartment_type(session=session, type_id=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Apartment Type not found or failed to delete")

    return {"message": "Apartment Type deleted successfully"}


@router.put("/apartment_type/{id}", response_model=ApartmentTypeSchema)
async def update_apartment_type(id: int, apartment_type: ApartmentTypeSchema) -> ApartmentTypeSchema:
    apartment_type_repo = ApartmentTypeRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await apartment_type_repo.check_connection(session=session)
        updated_apartment_type = await apartment_type_repo.update_apartment_type(session=session, type_id=id, apartment_type_id=id,
                                                                                num_rooms=apartment_type.num_rooms,
                                                                                is_furnished=apartment_type.is_furnished,
                                                                                description=apartment_type.description)


    if not updated_apartment_type:
        raise HTTPException(status_code=404, detail="Apartment Type not found or failed to update")

    return updated_apartment_type



@router.get("/all_conditions", response_model=list[ConditionSchema])
async def get_all_conditions():
    condition_repo = ConditionRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await condition_repo.check_connection(session=session)
        all_conditions = await condition_repo.get_all_conditions(session=session)

    return all_conditions


@router.get("/condition/{id}", response_model=ConditionSchema)
async def get_condition_by_id(id: int) -> ConditionSchema:
    condition_repo = ConditionRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await condition_repo.check_connection(session=session)
        condition = await condition_repo.get_condition_by_id(session=session, condition_id=id)

    if not condition:
        raise HTTPException(status_code=404, detail="Condition not found")

    return condition


@router.post("/condition", response_model=ConditionSchema)
async def insert_condition(condition: ConditionSchema) -> ConditionSchema:
    condition_repo = ConditionRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await condition_repo.check_connection(session=session)
        new_condition = await condition_repo.insert_condition(session=session, **condition.dict())

    if not new_condition:
        raise HTTPException(status_code=500, detail="Failed to insert condition")

    return new_condition


@router.delete("/condition/{id}", response_model=dict)
async def delete_condition(id: int) -> dict:
    condition_repo = ConditionRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await condition_repo.check_connection(session=session)
        deleted = await condition_repo.delete_condition(session=session, condition_id=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Condition not found or failed to delete")

    return {"message": "Condition deleted successfully"}


@router.put("/condition/{id}", response_model=ConditionSchema)
async def update_condition(id: int, condition: ConditionSchema) -> ConditionSchema:
    condition_repo = ConditionRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await condition_repo.check_connection(session=session)
        updated_condition = await condition_repo.update_condition(session=session, condition_id=id,
                                                                  name=condition.name)

    if not updated_condition:
        raise HTTPException(status_code=404, detail="Condition not found or failed to update")

    return updated_condition



@router.get("/all_statuses", response_model=list[StatusSchema])
async def get_all_statuses():
    status_repo = StatusRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await status_repo.check_connection(session=session)
        all_statuses = await status_repo.get_all_statuses(session=session)

    return all_statuses


@router.get("/status/{id}", response_model=StatusSchema)
async def get_status_by_id(id: int) -> StatusSchema:
    status_repo = StatusRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await status_repo.check_connection(session=session)
        status = await status_repo.get_status_by_id(session=session, status_id=id)

    if not status:
        raise HTTPException(status_code=404, detail="Status not found")

    return status


@router.post("/status", response_model=StatusSchema)
async def insert_status(status: StatusSchema) -> StatusSchema:
    status_repo = StatusRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await status_repo.check_connection(session=session)
        new_status = await status_repo.insert_status(session=session, date_listed=status.date_listed, is_active=status.is_active)

    if not new_status:
        raise HTTPException(status_code=500, detail="Failed to insert status")

    return new_status


@router.delete("/status/{id}", response_model=dict)
async def delete_status(id: int) -> dict:
    status_repo = StatusRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await status_repo.check_connection(session=session)
        deleted = await status_repo.delete_status(session=session, status_id=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Status not found or failed to delete")

    return {"message": "Status deleted successfully"}


@router.put("/status/{id}", response_model=StatusSchema)
async def update_status(id: int, status: StatusSchema) -> StatusSchema:
    status_repo = StatusRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await status_repo.check_connection(session=session)
        updated_status = await status_repo.update_status(session=session, status_id=id, date_listed=status.date_listed, is_active=status.is_active)

    if not updated_status:
        raise HTTPException(status_code=404, detail="Status not found or failed to update")

    return updated_status


@router.get("/all_apartments", response_model=list[ApartmentSchema])
async def get_all_apartments():
    apartment_repo = ApartmentRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await apartment_repo.check_connection(session=session)
        all_apartments = await apartment_repo.get_all_apartments(session=session)

    return all_apartments


@router.get("/apartment/{id}", response_model=ApartmentSchema)
async def get_apartment_by_id(id: int) -> ApartmentSchema:
    apartment_repo = ApartmentRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await apartment_repo.check_connection(session=session)
        apartment = await apartment_repo.get_apartment_by_id(session=session, apartment_id=id)

    if not apartment:
        raise HTTPException(status_code=404, detail="Apartment not found")

    return apartment


@router.post("/apartment", response_model=ApartmentSchema)
async def insert_apartment(apartment: ApartmentSchema) -> ApartmentSchema:
    apartment_repo = ApartmentRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await apartment_repo.check_connection(session=session)
        new_apartment = await apartment_repo.insert_apartment(session=session, **apartment.dict())

    if not new_apartment:
        raise HTTPException(status_code=500, detail="Failed to insert apartment")

    return new_apartment


@router.delete("/apartment/{id}", response_model=dict)
async def delete_apartment(id: int) -> dict:
    apartment_repo = ApartmentRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await apartment_repo.check_connection(session=session)
        deleted = await apartment_repo.delete_apartment(session=session, apartment_id=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Apartment not found or failed to delete")

    return {"message": "Apartment deleted successfully"}


@router.put("/apartment/{id}", response_model=ApartmentSchema)
async def update_apartment(id: int, apartment: ApartmentSchema) -> ApartmentSchema:
    apartment_repo = ApartmentRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await apartment_repo.check_connection(session=session)
        updated_apartment = await apartment_repo.update_apartment(session=session, apartment_id=id, **apartment.dict())

    if not updated_apartment:
        raise HTTPException(status_code=404, detail="Apartment not found or failed to update")

    return updated_apartment



@router.get("/all_apartment_photos", response_model=list[ApartmentPhotoSchema])
async def get_all_apartment_photos():
    apartment_photo_repo = ApartmentPhotoRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await apartment_photo_repo.check_connection(session=session)
        all_photos = await apartment_photo_repo.get_all_photos(session=session)

    return all_photos


@router.get("/apartment_photo/{id}", response_model=ApartmentPhotoSchema)
async def get_apartment_photo_by_id(id: int) -> ApartmentPhotoSchema:
    apartment_photo_repo = ApartmentPhotoRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await apartment_photo_repo.check_connection(session=session)
        photo = await apartment_photo_repo.get_photo_by_id(session=session, photo_id=id)

    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    return photo


@router.post("/apartment_photo", response_model=ApartmentPhotoSchema)
async def insert_apartment_photo(photo: ApartmentPhotoSchema) -> ApartmentPhotoSchema:
    apartment_photo_repo = ApartmentPhotoRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await apartment_photo_repo.check_connection(session=session)
        new_photo = await apartment_photo_repo.add_photo(session=session, apartment_id=photo.apartment_id, photo_url=photo.photo_url)

    if not new_photo:
        raise HTTPException(status_code=500, detail="Failed to insert photo")

    return new_photo


@router.delete("/apartment_photo/{id}", response_model=dict)
async def delete_apartment_photo(id: int) -> dict:
    apartment_photo_repo = ApartmentPhotoRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await apartment_photo_repo.check_connection(session=session)
        deleted = await apartment_photo_repo.delete_photo(session=session, photo_id=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Photo not found or failed to delete")

    return {"message": "Photo deleted successfully"}


@router.put("/apartment_photo/{id}", response_model=ApartmentPhotoSchema)
async def update_apartment_photo(id: int, photo: ApartmentPhotoSchema) -> ApartmentPhotoSchema:
    apartment_photo_repo = ApartmentPhotoRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        updated_photo = await apartment_photo_repo.update_photo(session=session, photo_id=id, new_url=photo.photo_url)

    if not updated_photo:
        raise HTTPException(status_code=404, detail="Photo not found or failed to update")

    return updated_photo


# Sale CRUD

@router.get("/all_sales", response_model=list[SaleSchema])
async def get_all_sales():
    sale_repo = SaleRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await sale_repo.check_connection(session=session)
        all_sales = await sale_repo.get_all_sales(session=session)

    return all_sales


@router.get("/sale/{id}", response_model=SaleSchema)
async def get_sale_by_id(id: int) -> SaleSchema:
    sale_repo = SaleRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await sale_repo.check_connection(session=session)
        sale = await sale_repo.get_sale_by_id(session=session, sale_id=id)

    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")

    return sale


@router.post("/sale", response_model=SaleSchema)
async def insert_sale(sale: SaleSchema) -> SaleSchema:
    sale_repo = SaleRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await sale_repo.check_connection(session=session)
        new_sale = await sale_repo.insert_sale(session=session, **sale.dict())

    if not new_sale:
        raise HTTPException(status_code=500, detail="Failed to insert sale")

    return new_sale


@router.delete("/sale/{id}", response_model=dict)
async def delete_sale(id: int) -> dict:
    sale_repo = SaleRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await sale_repo.check_connection(session=session)
        deleted = await sale_repo.delete_sale(session=session, sale_id=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Sale not found or failed to delete")

    return {"message": "Sale deleted successfully"}


@router.put("/sale/{id}", response_model=SaleSchema)
async def update_sale(id: int, sale: SaleSchema) -> SaleSchema:
    sale_repo = SaleRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await sale_repo.check_connection(session=session)
        updated_sale = await sale_repo.update_sale(session=session, id_sale=id, **sale.dict())

    if not updated_sale:
        raise HTTPException(status_code=404, detail="Sale not found or failed to update")

    return updated_sale


# SalesRent CRUD

@router.get("/all_sales_rent", response_model=list[SalesRentSchema])
async def get_all_sales_rent():
    sales_rent_repo = SalesRentRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await sales_rent_repo.check_connection(session=session)
        all_rentals = await sales_rent_repo.get_all_sales_rent(session=session)

    return all_rentals


@router.get("/sales_rent/{id}", response_model=SalesRentSchema)
async def get_sales_rent_by_id(id: int) -> SalesRentSchema:
    sales_rent_repo = SalesRentRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await sales_rent_repo.check_connection(session=session)
        rental = await sales_rent_repo.get_sales_rent_by_id(session=session, rent_id=id)

    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found")

    return rental


@router.post("/sales_rent", response_model=SalesRentSchema)
async def insert_sales_rent(sales_rent: SalesRentSchema) -> SalesRentSchema:
    sales_rent_repo = SalesRentRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await sales_rent_repo.check_connection(session=session)
        new_rent = await sales_rent_repo.insert_sales_rent(session=session, apartment_id=sales_rent.apartment_id,
                                                           renter_id=sales_rent.renter_id, owner_id=sales_rent.owner_id,
                                                           realtor_id=sales_rent.realtor_id, sale_date=sales_rent.sale_date,
                                                           sale_price=sales_rent.sale_price, commission=sales_rent.commission,
                                                           profit=sales_rent.profit, rent_start=sales_rent.rent_start,
                                                           rent_end=sales_rent.rent_end)

    if not new_rent:
        raise HTTPException(status_code=500, detail="Failed to insert rental")

    return new_rent


@router.delete("/sales_rent/{id}", response_model=dict)
async def delete_sales_rent(id: int) -> dict:
    sales_rent_repo = SalesRentRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await sales_rent_repo.check_connection(session=session)
        deleted = await sales_rent_repo.delete_sales_rent(session=session, rent_id=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Rental not found or failed to delete")

    return {"message": "Rental deleted successfully"}


@router.put("/sales_rent/{id}", response_model=SalesRentSchema)
async def update_sales_rent(id: int, sales_rent: SalesRentSchema) -> SalesRentSchema:
    sales_rent_repo = SalesRentRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await sales_rent_repo.check_connection(session=session)
        updated_rent = await sales_rent_repo.update_sales_rent(session=session, rent_id=id)

    if not updated_rent:
        raise HTTPException(status_code=404, detail="Rental not found or failed to update")

    return updated_rent

#for house_type_repo
@router.put("/house_type/{id}", response_model=HouseTypeSchema)
async def update_house_type(id: int, house_type: HouseTypeSchema) -> HouseTypeSchema:
    house_type_repo = HouseTypeRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await house_type_repo.check_connection(session=session)
        updated_type = await house_type_repo.update_house_type(session=session, description=house_type.description, type=house_type.type, type_id=id)

    if not updated_type:
        raise HTTPException(status_code=404, detail="House type not found or failed to update")

    return updated_type

@router.delete("/house_type/{id}", response_model=dict)
async def delete_house_type(id: int) -> dict:
    house_type_repo = HouseTypeRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await house_type_repo.check_connection(session=session)
        deleted = await house_type_repo.delete_house_type(session=session, type_id=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="House type not found or failed to delete")

    return {"message": "House type deleted successfully"}

@router.post("/house_type", response_model=HouseTypeSchema)
async def insert_house_type(house_type: HouseTypeSchema) -> HouseTypeSchema:
    house_type_repo = HouseTypeRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await house_type_repo.check_connection(session=session)
        new_type = await house_type_repo.insert_house_type(session=session, description=house_type.description, type=house_type.type)

    if not new_type:
        raise HTTPException(status_code=500, detail="Failed to insert house type")

    return new_type

@router.get("/house_type/{id}", response_model=HouseTypeSchema)
async def get_house_type_by_id(id: int) -> HouseTypeSchema:
    house_type_repo = HouseTypeRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await house_type_repo.check_connection(session=session)
        house_type = await house_type_repo.get_house_type_by_id(session=session, type_id=id)

    if not house_type:
        raise HTTPException(status_code=404, detail="House type not found")

    return house_type

@router.get("/all_house_types", response_model=list[HouseTypeSchema])
async def get_all_house_types():
    house_type_repo = HouseTypeRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await house_type_repo.check_connection(session=session)
        all_house_types = await house_type_repo.get_all_house_types(session=session)

    return all_house_types