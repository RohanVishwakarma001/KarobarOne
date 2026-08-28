from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.shippingPartnerRepository import (
    shippingPartnerRepository,
)
from app.schemas.github.shippingPartnerSchema import (
    ShippingPartnerCreate,
    ShippingPartnerUpdate,
)


class ShippingPartnerService:

    def create(
        self,
        db: Session,
        partner: ShippingPartnerCreate
    ):

        existingPartner = (
            shippingPartnerRepository.getByPartnerCode(
                db,
                partner.partner_code
            )
        )

        if existingPartner:
            raise ValueError(
                "Partner code already exists."
            )

        return shippingPartnerRepository.create(
            db=db,
            obj=partner
        )

    def getAll(
        self,
        db: Session
    ):

        return shippingPartnerRepository.get_all(db)

    def getById(
        self,
        db: Session,
        partnerId: UUID
    ):

        return shippingPartnerRepository.get(
            db=db,
            obj_id=partnerId,
            id_field=shippingPartnerRepository.model.id
        )

    def update(
        self,
        db: Session,
        partnerId: UUID,
        partner: ShippingPartnerUpdate
    ):

        dbPartner = self.getById(
            db,
            partnerId
        )

        if dbPartner is None:
            return None

        return shippingPartnerRepository.update(
            db=db,
            db_obj=dbPartner,
            obj=partner
        )

    def delete(
        self,
        db: Session,
        partnerId: UUID
    ):

        dbPartner = self.getById(
            db,
            partnerId
        )

        if dbPartner is None:
            return False

        shippingPartnerRepository.delete(
            db=db,
            db_obj=dbPartner
        )

        return True


shippingPartnerService = ShippingPartnerService()