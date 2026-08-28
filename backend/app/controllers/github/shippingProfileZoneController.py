from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.shippingProfileZoneSchema import (
    ShippingProfileZoneCreate,
)
from app.services.github.shippingProfileZoneService import (
    shippingProfileZoneService,
)


class ShippingProfileZoneController:

    def create(
        self,
        db: Session,
        obj: ShippingProfileZoneCreate
    ):
        return shippingProfileZoneService.create(db, obj)

    def getAll(
        self,
        db: Session
    ):
        return shippingProfileZoneService.getAll(db)

    def getById(
        self,
        db: Session,
        objId: UUID
    ):
        obj = shippingProfileZoneService.getById(
            db,
            objId
        )

        if obj is None:
            raise HTTPException(
                status_code=404,
                detail="Record not found."
            )

        return obj

    def delete(
        self,
        db: Session,
        objId: UUID
    ):
        deleted = shippingProfileZoneService.delete(
            db,
            objId
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Record not found."
            )

        return {
            "message": "Deleted successfully."
        }


shippingProfileZoneController = ShippingProfileZoneController()