from app.db.models.github.models import Booking
from app.repositories.github.base import BaseRepository


class BookingRepository(BaseRepository[Booking]):

    def __init__(self):
        super().__init__(Booking)


bookingRepository = BookingRepository()