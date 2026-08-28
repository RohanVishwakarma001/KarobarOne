from app.db.models.github.appointment import Appointment
from app.repositories.github.base import BaseRepository


class AppointmentRepository(
    BaseRepository[Appointment]
):

    def __init__(self):
        super().__init__(Appointment)


appointmentRepository = AppointmentRepository()