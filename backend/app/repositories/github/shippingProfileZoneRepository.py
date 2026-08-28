from app.db.models.github.shippingProfileZone import ShippingProfileZone
from app.repositories.github.base import BaseRepository


class ShippingProfileZoneRepository(BaseRepository):

    def __init__(self):
        super().__init__(ShippingProfileZone)


shippingProfileZoneRepository = ShippingProfileZoneRepository()