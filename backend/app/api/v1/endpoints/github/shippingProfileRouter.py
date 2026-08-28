from typing import List
from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.db.session import getSyncDb
from app.controllers.github.shippingProfileController import (
    shippingProfileController,
)
from app.schemas.github.shippingProfileSchema import (
    ShippingProfileCreate,
    ShippingProfileUpdate,
    ShippingProfileResponse,
)

router = APIRouter(
    prefix="/shipping-profiles",
    tags=["Shipping Profiles"]
)


@router.post(
    "/",
    response_model=ShippingProfileResponse,
    status_code=201
)
def createShippingProfile(
    profile: ShippingProfileCreate,
    db: Session = Depends(getSyncDb)
):
    return shippingProfileController.create(
        db,
        profile
    )


@router.get(
    "/",
    response_model=List[ShippingProfileResponse]
)
def getShippingProfiles(
    db: Session = Depends(getSyncDb)
):
    return shippingProfileController.getAll(db)


@router.get(
    "/{profileId}",
    response_model=ShippingProfileResponse
)
def getShippingProfile(
    profileId: UUID,
    db: Session = Depends(getSyncDb)
):
    return shippingProfileController.getById(
        db,
        profileId
    )


@router.put(
    "/{profileId}",
    response_model=ShippingProfileResponse
)
def updateShippingProfile(
    profileId: UUID,
    profile: ShippingProfileUpdate,
    db: Session = Depends(getSyncDb)
):
    return shippingProfileController.update(
        db,
        profileId,
        profile
    )


@router.delete(
    "/{profileId}"
)
def deleteShippingProfile(
    profileId: UUID,
    db: Session = Depends(getSyncDb)
):
    return shippingProfileController.delete(
        db,
        profileId
    )