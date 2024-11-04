from fastapi import APIRouter
from project.infrastructure.postgres.repository.apartment_repo import ApartmentRepository
from project.infrastructure.postgres.database import PostgresDatabase
from project.schemas.apartment import ApartmentSchema


router = APIRouter()


@router.get("/all_apartments", response_model=list[ApartmentSchema])
async def get_all_apartments() -> list[ApartmentSchema]:
    apartment_repo = ApartmentRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await apartment_repo.check_connection(session=session)
        all_apartments = await apartment_repo.get_all_apartments(session=session)

    return all_apartments