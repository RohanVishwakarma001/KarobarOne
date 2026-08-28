from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.shippingRateSchema import (
    ShippingRateCreate,
    ShippingRateUpdate,
)
from app.services.github.shippingRateService import (
    shippingRateService,
)


class ShippingRateController:

    def create(
        self,
        db: Session,
        rate: ShippingRateCreate
    ):
        return shippingRateService.create(
            db,
            rate
        )

    def getAll(
        self,
        db: Session
    ):
        return shippingRateService.getAll(db)

    def getById(
        self,
        db: Session,
        rateId: UUID
    ):

        rate = shippingRateService.getById(
            db,
            rateId
        )

        if rate is None:
            raise HTTPException(
                status_code=404,
                detail="Shipping Rate not found."
            )

        return rate

    def update(
        self,
        db: Session,
        rateId: UUID,
        rate: ShippingRateUpdate
    ):

        updatedRate = shippingRateService.update(
            db,
            rateId,
            rate
        )

        if updatedRate is None:
            raise HTTPException(
                status_code=404,
                detail="Shipping Rate not found."
            )

        return updatedRate

    def delete(
        self,
        db: Session,
        rateId: UUID
    ):

        deleted = shippingRateService.delete(
            db,
            rateId
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Shipping Rate not found."
            )

        return {
            "message": "Shipping Rate deleted successfully."
        }


shippingRateController = ShippingRateController()