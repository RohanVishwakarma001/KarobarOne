from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.gatewayWebhookEventController import (
    gatewayWebhookEventController,
)
from app.db.session import getSyncDb
from app.schemas.github.gatewayWebhookEventSchema import (
    GatewayWebhookEventCreate,
    GatewayWebhookEventUpdate,
)

router = APIRouter(
    prefix="/gateway-webhook-events",
    tags=["Gateway Webhook Events"]
)


@router.post("/")
def create(
    event: GatewayWebhookEventCreate,
    db: Session = Depends(getSyncDb)
):
    return gatewayWebhookEventController.create(
        db,
        event
    )


@router.get("/")
def getAll(
    db: Session = Depends(getSyncDb)
):
    return gatewayWebhookEventController.getAll(db)


@router.get("/{eventId}")
def getById(
    eventId: UUID,
    db: Session = Depends(getSyncDb)
):
    return gatewayWebhookEventController.getById(
        db,
        eventId
    )


@router.put("/{eventId}")
def update(
    eventId: UUID,
    event: GatewayWebhookEventUpdate,
    db: Session = Depends(getSyncDb)
):
    return gatewayWebhookEventController.update(
        db,
        eventId,
        event
    )