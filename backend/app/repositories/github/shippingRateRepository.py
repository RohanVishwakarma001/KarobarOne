from app.db.models.github.shippingRate import ShippingRate
from app.repositories.github.base import BaseRepository


class ShippingRateRepository(BaseRepository):

    def __init__(self):
        super().__init__(ShippingRate)


shippingRateRepository = ShippingRateRepository()