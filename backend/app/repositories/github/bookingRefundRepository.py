from app.db.models.github.models import BookingRefund
from app.repositories.github.base import BaseRepository


class BookingRefundRepository(BaseRepository[BookingRefund]):

    def __init__(self):
        super().__init__(BookingRefund)


bookingRefundRepository = BookingRefundRepository()