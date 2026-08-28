from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.shipmentRepository import (
    shipmentRepository,
)
from app.schemas.github.shipmentSchema import (
    ShipmentCreate,
    ShipmentUpdate,
)


class ShipmentService:

    def create(
        self,
        db: Session,
        shipment: ShipmentCreate
    ):
        return shipmentRepository.create(
            db=db,
            obj=shipment
        )

    def getAll(
        self,
        db: Session
    ):
        return shipmentRepository.get_all(db)

    def getById(
        self,
        db: Session,
        shipmentId: UUID
    ):
        return shipmentRepository.get(
            db=db,
            obj_id=shipmentId,
            id_field=shipmentRepository.model.id
        )

    def update(
        self,
        db: Session,
        shipmentId: UUID,
        shipment: ShipmentUpdate
    ):

        dbShipment = self.getById(
            db,
            shipmentId
        )

        if dbShipment is None:
            return None

        return shipmentRepository.update(
            db=db,
            db_obj=dbShipment,
            obj=shipment
        )

    def delete(
        self,
        db: Session,
        shipmentId: UUID
    ):

        dbShipment = self.getById(
            db,
            shipmentId
        )

        if dbShipment is None:
            return False

        shipmentRepository.delete(
            db=db,
            db_obj=dbShipment
        )

        return True


shipmentService = ShipmentService()