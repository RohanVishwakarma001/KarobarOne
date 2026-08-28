from app.db.models.github.models import Notification
from app.repositories.github.base import BaseRepository


class NotificationRepository(BaseRepository[Notification]):

    def __init__(self):
        super().__init__(Notification)


notificationRepository = NotificationRepository()