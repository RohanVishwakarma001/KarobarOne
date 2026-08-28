from sqlalchemy.orm import Session

from app.db.models.github.shippingZone import ShippingZone
from app.repositories.github.base import BaseRepository


class ShippingZoneRepository(BaseRepository):

    def __init__(self):
        super().__init__(ShippingZone)

    def getByZoneCode(
        self,
        db: Session,
        zoneCode: str
    ):
        return (
            db.query(ShippingZone)
            .filter(
                ShippingZone.zone_code == zoneCode
            )
            .first()
        )


shippingZoneRepository = ShippingZoneRepository()