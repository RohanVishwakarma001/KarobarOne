from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.shippingProfileSchema import (
    ShippingProfileCreate,
    ShippingProfileUpdate,
)
from app.services.github.shippingProfileService import (
    shippingProfileService,
)


class ShippingProfileController:

    def create(
        self,
        db: Session,
        profile: ShippingProfileCreate
    ):

        try:
            return shippingProfileService.create(
                db,
                profile
            )

        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )

    def getAll(
        self,
        db: Session
    ):

        return shippingProfileService.getAll(db)

    def getById(
        self,
        db: Session,
        profileId: UUID
    ):

        profile = shippingProfileService.getById(
            db,
            profileId
        )

        if profile is None:
            raise HTTPException(
                status_code=404,
                detail="Shipping Profile not found."
            )

        return profile

    def update(
        self,
        db: Session,
        profileId: UUID,
        profile: ShippingProfileUpdate
    ):

        updatedProfile = shippingProfileService.update(
            db,
            profileId,
            profile
        )

        if updatedProfile is None:
            raise HTTPException(
                status_code=404,
                detail="Shipping Profile not found."
            )

        return updatedProfile

    def delete(
        self,
        db: Session,
        profileId: UUID
    ):

        deleted = shippingProfileService.delete(
            db,
            profileId
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Shipping Profile not found."
            )

        return {
            "message": "Shipping Profile deleted successfully."
        }


shippingProfileController = ShippingProfileController()