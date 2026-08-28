from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.shippingProfileZoneRepository import (
    shippingProfileZoneRepository,
)
from app.schemas.github.shippingProfileZoneSchema import (
    ShippingProfileZoneCreate,
)


class ShippingProfileZoneService:

    def create(
        self,
        db: Session,
        obj: ShippingProfileZoneCreate
    ):
        return shippingProfileZoneRepository.create(
            db=db,
            obj=obj
        )

    def getAll(
        self,
        db: Session
    ):
        return shippingProfileZoneRepository.get_all(db)

    def getById(
        self,
        db: Session,
        objId: UUID
    ):
        return shippingProfileZoneRepository.get(
            db=db,
            obj_id=objId,
            id_field=shippingProfileZoneRepository.model.id
        )

    def delete(
        self,
        db: Session,
        objId: UUID
    ):
        obj = self.getById(db, objId)

        if obj is None:
            return False

        shippingProfileZoneRepository.delete(
            db=db,
            db_obj=obj
        )

        return True


shippingProfileZoneService = ShippingProfileZoneService()