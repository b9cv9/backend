from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from project.infrastructure.postgres.models import ApartmentPhoto


class ApartmentPhotoRepository:
    """Repository for managing apartment photos."""

    def __init__(self, session: Session):
        self.session = session

    def get_photo_by_id(self, photo_id: int) -> ApartmentPhoto | None:
        """Retrieve a single apartment photo by its ID."""
        statement = select(ApartmentPhoto).where(ApartmentPhoto.id == photo_id)
        result = self.session.execute(statement).scalar_one_or_none()
        return result

    def get_photos_by_apartment_id(self, apartment_id: int) -> list[ApartmentPhoto]:
        """Retrieve all photos for a given apartment."""
        statement = select(ApartmentPhoto).where(ApartmentPhoto.apartment_id == apartment_id)
        result = self.session.execute(statement).scalars().all()
        return result

    def add_photo(self, apartment_id: int, photo_url: str) -> ApartmentPhoto:
        """Add a new photo to an apartment."""
        new_photo = ApartmentPhoto(apartment_id=apartment_id, url=photo_url)
        self.session.add(new_photo)
        self.session.commit()
        self.session.refresh(new_photo)
        return new_photo

    def update_photo(self, photo_id: int, new_url: str) -> ApartmentPhoto | None:
        """Update the URL of an existing photo."""
        statement = (
            update(ApartmentPhoto)
            .where(ApartmentPhoto.id == photo_id)
            .values(url=new_url)
            .returning(ApartmentPhoto)
        )
        result = self.session.execute(statement).scalar_one_or_none()
        if result:
            self.session.commit()
        return result

    def delete_photo(self, photo_id: int) -> bool:
        """Delete a photo by its ID."""
        statement = delete(ApartmentPhoto).where(ApartmentPhoto.id == photo_id)
        result = self.session.execute(statement).rowcount
        if result:
            self.session.commit()
        return bool(result)
