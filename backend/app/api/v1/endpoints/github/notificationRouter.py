from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.notificationController import (
    notificationController,
)
from app.db.session import getSyncDb
from app.schemas.github.schemas import (
    NotificationCreate,
    NotificationUpdate,
    NotificationResponse,
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@router.post(
    "/",
    response_model=NotificationResponse,
    status_code=201,
)
def createNotification(
    notification: NotificationCreate,
    db: Session = Depends(getSyncDb),
):
    return notificationController.create(
        db,
        notification,
    )


@router.get(
    "/",
    response_model=list[NotificationResponse],
)
def getNotifications(
    db: Session = Depends(getSyncDb),
):
    return notificationController.getAll(db)


@router.get(
    "/{notificationId}",
    response_model=NotificationResponse,
)
def getNotification(
    notificationId: UUID,
    db: Session = Depends(getSyncDb),
):
    return notificationController.getById(
        db,
        notificationId,
    )


@router.put(
    "/{notificationId}",
    response_model=NotificationResponse,
)
def updateNotification(
    notificationId: UUID,
    notification: NotificationUpdate,
    db: Session = Depends(getSyncDb),
):
    return notificationController.update(
        db,
        notificationId,
        notification,
    )


@router.delete(
    "/{notificationId}",
)
def deleteNotification(
    notificationId: UUID,
    db: Session = Depends(getSyncDb),
):
    return notificationController.delete(
        db,
        notificationId,
    )