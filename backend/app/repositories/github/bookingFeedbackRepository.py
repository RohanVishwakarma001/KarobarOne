from app.db.models.github.models import BookingFeedback
from app.repositories.github.base import BaseRepository


class BookingFeedbackRepository(BaseRepository[BookingFeedback]):

    def __init__(self):
        super().__init__(BookingFeedback)


bookingFeedbackRepository = BookingFeedbackRepository()