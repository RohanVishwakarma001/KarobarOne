from app.db.models.github.models import OfferExclusion
from app.repositories.github.base import BaseRepository


class OfferExclusionRepository(
    BaseRepository[OfferExclusion]
):

    def __init__(self):
        super().__init__(OfferExclusion)


offerExclusionRepository = OfferExclusionRepository()