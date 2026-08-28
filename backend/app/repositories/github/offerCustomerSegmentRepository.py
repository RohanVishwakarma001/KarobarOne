from app.db.models.github.models import OfferCustomerSegment
from app.repositories.github.base import BaseRepository


class OfferCustomerSegmentRepository(
    BaseRepository[OfferCustomerSegment]
):

    def __init__(self):
        super().__init__(OfferCustomerSegment)


offerCustomerSegmentRepository = OfferCustomerSegmentRepository()