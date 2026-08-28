from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.schemas import (
    NotificationCreate,
    NotificationUpdate,
)
from app.services.github.notificationService import (
    notificationService,
)


class NotificationController:

    def create(
        self,
        db: Session,
        notification: NotificationCreate,
    ):
        return notificationService.create(
            db,
            notification,
        )

    def getAll(
        self,
        db: Session,
    ):
        return notificationService.getAll(db)

    def getById(
        self,
        db: Session,
        notificationId: UUID,
    ):
        item = notificationService.getById(
            db,
            notificationId,
        )

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Notification not found",
            )

        return item

    def update(
        self,
        db: Session,
        notificationId: UUID,
        notification: NotificationUpdate,
    ):
        item = notificationService.update(
            db,
            notificationId,
            notification,
        )

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Notification not found",
            )

        return item

    def delete(
        self,
        db: Session,
        notificationId: UUID,
    ):
        deleted = notificationService.delete(
            db,
            notificationId,
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Notification not found",
            )

        return {
            "message": "Notification deleted successfully"
        }


notificationController = NotificationController()