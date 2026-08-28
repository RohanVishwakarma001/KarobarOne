from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.shippingRateRepository import shippingRateRepository
from app.schemas.github.shippingRateSchema import (
    ShippingRateCreate,
    ShippingRateUpdate,
)


class ShippingRateService:

    def create(
        self,
        db: Session,
        rate: ShippingRateCreate
    ):
        return shippingRateRepository.create(
            db=db,
            obj=rate
        )

    def getAll(
        self,
        db: Session
    ):
        return shippingRateRepository.get_all(db)

    def getById(
        self,
        db: Session,
        rateId: UUID
    ):
        return shippingRateRepository.get(
            db=db,
            obj_id=rateId,
            id_field=shippingRateRepository.model.id
        )

    def update(
        self,
        db: Session,
        rateId: UUID,
        rate: ShippingRateUpdate
    ):

        dbRate = self.getById(
            db,
            rateId
        )

        if dbRate is None:
            return None

        return shippingRateRepository.update(
            db=db,
            db_obj=dbRate,
            obj=rate
        )

    def delete(
        self,
        db: Session,
        rateId: UUID
    ):

        dbRate = self.getById(
            db,
            rateId
        )

        if dbRate is None:
            return False

        shippingRateRepository.delete(
            db=db,
            db_obj=dbRate
        )

        return True


shippingRateService = ShippingRateService()