from app.db.models.github.models import BookingCancellation
from app.repositories.github.base import BaseRepository


class BookingCancellationRepository(BaseRepository[BookingCancellation]):

    def __init__(self):
        super().__init__(BookingCancellation)


bookingCancellationRepository = BookingCancellationRepository()