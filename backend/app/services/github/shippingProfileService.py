from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.shippingProfileRepository import (
    shippingProfileRepository,
)
from app.schemas.github.shippingProfileSchema import (
    ShippingProfileCreate,
    ShippingProfileUpdate,
)


class ShippingProfileService:

    def create(
        self,
        db: Session,
        profile: ShippingProfileCreate
    ):

        existingProfile = (
            shippingProfileRepository.getByProfileName(
                db,
                profile.profile_name
            )
        )

        if existingProfile:
            raise ValueError(
                "Profile name already exists."
            )

        return shippingProfileRepository.create(
            db=db,
            obj=profile
        )

    def getAll(
        self,
        db: Session
    ):

        return shippingProfileRepository.get_all(db)

    def getById(
        self,
        db: Session,
        profileId: UUID
    ):

        return shippingProfileRepository.get(
            db=db,
            obj_id=profileId,
            id_field=shippingProfileRepository.model.id
        )

    def update(
        self,
        db: Session,
        profileId: UUID,
        profile: ShippingProfileUpdate
    ):

        dbProfile = self.getById(
            db,
            profileId
        )

        if dbProfile is None:
            return None

        return shippingProfileRepository.update(
            db=db,
            db_obj=dbProfile,
            obj=profile
        )

    def delete(
        self,
        db: Session,
        profileId: UUID
    ):

        dbProfile = self.getById(
            db,
            profileId
        )

        if dbProfile is None:
            return False

        shippingProfileRepository.delete(
            db=db,
            db_obj=dbProfile
        )

        return True


shippingProfileService = ShippingProfileService()