from app.db.models.github.models import Offer
from app.repositories.github.base import BaseRepository


class OfferRepository(BaseRepository[Offer]):

    def __init__(self):
        super().__init__(Offer)


offerRepository = OfferRepository()