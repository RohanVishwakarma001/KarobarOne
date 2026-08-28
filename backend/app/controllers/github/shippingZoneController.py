from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.shippingZoneSchema import (
    ShippingZoneCreate,
    ShippingZoneUpdate,
)
from app.services.github.shippingZoneService import (
    shippingZoneService
)


class ShippingZoneController:

    def create(
        self,
        db: Session,
        zone: ShippingZoneCreate
    ):

        try:
            return shippingZoneService.create(
                db,
                zone
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

        return shippingZoneService.getAll(db)

    def getById(
        self,
        db: Session,
        zoneId: UUID
    ):

        zone = shippingZoneService.getById(
            db,
            zoneId
        )

        if zone is None:
            raise HTTPException(
                status_code=404,
                detail="Shipping Zone not found."
            )

        return zone

    def update(
        self,
        db: Session,
        zoneId: UUID,
        zone: ShippingZoneUpdate
    ):

        updatedZone = shippingZoneService.update(
            db,
            zoneId,
            zone
        )

        if updatedZone is None:
            raise HTTPException(
                status_code=404,
                detail="Shipping Zone not found."
            )

        return updatedZone

    def delete(
        self,
        db: Session,
        zoneId: UUID
    ):

        deleted = shippingZoneService.delete(
            db,
            zoneId
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Shipping Zone not found."
            )

        return {
            "message": "Shipping Zone deleted successfully."
        }


shippingZoneController = ShippingZoneController()