from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.shippingZoneRepository import (
    shippingZoneRepository
)
from app.schemas.github.shippingZoneSchema import (
    ShippingZoneCreate,
    ShippingZoneUpdate,
)


class ShippingZoneService:

    def create(
        self,
        db: Session,
        zone: ShippingZoneCreate
    ):

        existingZone = shippingZoneRepository.getByZoneCode(
            db,
            zone.zone_code
        )

        if existingZone:
            raise ValueError(
                "Zone code already exists."
            )

        return shippingZoneRepository.create(
            db=db,
            obj=zone
        )

    def getAll(
        self,
        db: Session
    ):

        return shippingZoneRepository.get_all(db)

    def getById(
        self,
        db: Session,
        zoneId: UUID
    ):

        return shippingZoneRepository.get(
            db=db,
            obj_id=zoneId,
            id_field=shippingZoneRepository.model.id
        )

    def update(
        self,
        db: Session,
        zoneId: UUID,
        zone: ShippingZoneUpdate
    ):

        dbZone = self.getById(
            db,
            zoneId
        )

        if dbZone is None:
            return None

        return shippingZoneRepository.update(
            db=db,
            db_obj=dbZone,
            obj=zone
        )

    def delete(
        self,
        db: Session,
        zoneId: UUID
    ):

        dbZone = self.getById(
            db,
            zoneId
        )

        if dbZone is None:
            return False

        shippingZoneRepository.delete(
            db=db,
            db_obj=dbZone
        )

        return True


shippingZoneService = ShippingZoneService()