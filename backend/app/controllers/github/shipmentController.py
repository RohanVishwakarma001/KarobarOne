from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.shipmentSchema import (
    ShipmentCreate,
    ShipmentUpdate,
)
from app.services.github.shipmentService import (
    shipmentService,
)


class ShipmentController:

    def create(
        self,
        db: Session,
        shipment: ShipmentCreate
    ):
        return shipmentService.create(
            db,
            shipment
        )

    def getAll(
        self,
        db: Session
    ):
        return shipmentService.getAll(db)

    def getById(
        self,
        db: Session,
        shipmentId: UUID
    ):

        shipment = shipmentService.getById(
            db,
            shipmentId
        )

        if shipment is None:
            raise HTTPException(
                status_code=404,
                detail="Shipment not found."
            )

        return shipment

    def update(
        self,
        db: Session,
        shipmentId: UUID,
        shipment: ShipmentUpdate
    ):

        updatedShipment = shipmentService.update(
            db,
            shipmentId,
            shipment
        )

        if updatedShipment is None:
            raise HTTPException(
                status_code=404,
                detail="Shipment not found."
            )

        return updatedShipment

    def delete(
        self,
        db: Session,
        shipmentId: UUID
    ):

        deleted = shipmentService.delete(
            db,
            shipmentId
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Shipment not found."
            )

        return {
            "message": "Shipment deleted successfully."
        }


shipmentController = ShipmentController()