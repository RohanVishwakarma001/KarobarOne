from sqlalchemy.orm import Session

from app.db.models.github.shippingPartner import ShippingPartner
from app.repositories.github.base import BaseRepository


class ShippingPartnerRepository(BaseRepository):

    def __init__(self):
        super().__init__(ShippingPartner)

    def getByPartnerCode(
        self,
        db: Session,
        partnerCode: str
    ):
        return (
            db.query(ShippingPartner)
            .filter(
                ShippingPartner.partner_code == partnerCode
            )
            .first()
        )


shippingPartnerRepository = ShippingPartnerRepository()