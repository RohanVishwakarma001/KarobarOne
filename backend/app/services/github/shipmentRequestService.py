from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.shipmentRequestRepository import (
    shipmentRequestRepository
)
from app.schemas.github.shipmentRequestSchema import (
    ShipmentRequestCreate,
    ShipmentRequestUpdate,
)


class ShipmentRequestService:

    def create(
        self,
        db: Session,
        request: ShipmentRequestCreate
    ):
        return shipmentRequestRepository.create(
            db=db,
            obj=request
        )

    def getAll(
        self,
        db: Session
    ):
        return shipmentRequestRepository.get_all(db)

    def getById(
        self,
        db: Session,
        requestId: UUID
    ):
        return shipmentRequestRepository.get(
            db=db,
            obj_id=requestId,
            id_field=shipmentRequestRepository.model.id
        )

    def update(
        self,
        db: Session,
        requestId: UUID,
        request: ShipmentRequestUpdate
    ):

        dbRequest = self.getById(
            db,
            requestId
        )

        if dbRequest is None:
            return None

        return shipmentRequestRepository.update(
            db=db,
            db_obj=dbRequest,
            obj=request
        )

    def delete(
        self,
        db: Session,
        requestId: UUID
    ):

        dbRequest = self.getById(
            db,
            requestId
        )

        if dbRequest is None:
            return False

        shipmentRequestRepository.delete(
            db=db,
            db_obj=dbRequest
        )

        return True


shipmentRequestService = ShipmentRequestService()