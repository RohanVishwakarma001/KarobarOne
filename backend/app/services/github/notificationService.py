from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.notificationRepository import (
    notificationRepository,
)
from app.schemas.github.schemas import (
    NotificationCreate,
    NotificationUpdate,
)


class NotificationService:

    def create(
        self,
        db: Session,
        notification: NotificationCreate,
    ):
        return notificationRepository.create(
            db,
            notification,
        )

    def getAll(
        self,
        db: Session,
    ):
        return notificationRepository.get_all(db)

    def getById(
        self,
        db: Session,
        notificationId: UUID,
    ):
        return notificationRepository.get(
            db,
            notificationId,
            notificationRepository.model.id,
        )

    def update(
        self,
        db: Session,
        notificationId: UUID,
        notification: NotificationUpdate,
    ):
        dbNotification = self.getById(
            db,
            notificationId,
        )

        if dbNotification is None:
            return None

        return notificationRepository.update(
            db,
            dbNotification,
            notification,
        )

    def delete(
        self,
        db: Session,
        notificationId: UUID,
    ):
        dbNotification = self.getById(
            db,
            notificationId,
        )

        if dbNotification is None:
            return False

        notificationRepository.delete(
            db,
            dbNotification,
        )

        return True


notificationService = NotificationService()