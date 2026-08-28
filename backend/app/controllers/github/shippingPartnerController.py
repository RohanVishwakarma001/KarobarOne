from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.shippingPartnerSchema import (
    ShippingPartnerCreate,
    ShippingPartnerUpdate,
)
from app.services.github.shippingPartnerService import (
    shippingPartnerService
)


class ShippingPartnerController:

    def create(
        self,
        db: Session,
        partner: ShippingPartnerCreate
    ):
        return shippingPartnerService.create(db, partner)

    def getAll(
        self,
        db: Session
    ):
        return shippingPartnerService.getAll(db)

    def getById(
        self,
        db: Session,
        partnerId: UUID
    ):

        partner = shippingPartnerService.getById(
            db,
            partnerId
        )

        if partner is None:
            raise HTTPException(
                status_code=404,
                detail="Shipping Partner not found"
            )

        return partner

    def update(
        self,
        db: Session,
        partnerId: UUID,
        partner: ShippingPartnerUpdate
    ):

        updatedPartner = shippingPartnerService.update(
            db,
            partnerId,
            partner
        )

        if updatedPartner is None:
            raise HTTPException(
                status_code=404,
                detail="Shipping Partner not found"
            )

        return updatedPartner

    def delete(
        self,
        db: Session,
        partnerId: UUID
    ):

        deleted = shippingPartnerService.delete(
            db,
            partnerId
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Shipping Partner not found"
            )

        return {
            "message": "Shipping Partner deleted successfully."
        }


shippingPartnerController = ShippingPartnerController()