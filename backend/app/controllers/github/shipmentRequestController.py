from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.shipmentRequestSchema import (
    ShipmentRequestCreate,
    ShipmentRequestUpdate,
)
from app.services.github.shipmentRequestService import (
    shipmentRequestService,
)


class ShipmentRequestController:

    def create(
        self,
        db: Session,
        request: ShipmentRequestCreate
    ):
        return shipmentRequestService.create(
            db,
            request
        )

    def getAll(
        self,
        db: Session
    ):
        return shipmentRequestService.getAll(db)

    def getById(
        self,
        db: Session,
        requestId: UUID
    ):

        request = shipmentRequestService.getById(
            db,
            requestId
        )

        if request is None:
            raise HTTPException(
                status_code=404,
                detail="Shipment Request not found."
            )

        return request

    def update(
        self,
        db: Session,
        requestId: UUID,
        request: ShipmentRequestUpdate
    ):

        updatedRequest = shipmentRequestService.update(
            db,
            requestId,
            request
        )

        if updatedRequest is None:
            raise HTTPException(
                status_code=404,
                detail="Shipment Request not found."
            )

        return updatedRequest

    def delete(
        self,
        db: Session,
        requestId: UUID
    ):

        deleted = shipmentRequestService.delete(
            db,
            requestId
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Shipment Request not found."
            )

        return {
            "message": "Shipment Request deleted successfully."
        }


shipmentRequestController = ShipmentRequestController()