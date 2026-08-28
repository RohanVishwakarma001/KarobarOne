from app.db.models.github.models import OfferTarget
from app.repositories.github.base import BaseRepository


class OfferTargetRepository(BaseRepository[OfferTarget]):

    def __init__(self):
        super().__init__(OfferTarget)


offerTargetRepository = OfferTargetRepository()