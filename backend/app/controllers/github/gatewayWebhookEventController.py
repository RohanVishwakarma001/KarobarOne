from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.gatewayWebhookEventSchema import (
    GatewayWebhookEventCreate,
    GatewayWebhookEventUpdate,
)
from app.services.github.gatewayWebhookEventService import (
    gatewayWebhookEventService,
)


class GatewayWebhookEventController:

    def create(
        self,
        db: Session,
        event: GatewayWebhookEventCreate
    ):
        return gatewayWebhookEventService.create(
            db,
            event
        )

    def getAll(
        self,
        db: Session
    ):
        return gatewayWebhookEventService.getAll(db)

    def getById(
        self,
        db: Session,
        eventId: UUID
    ):
        event = gatewayWebhookEventService.getById(
            db,
            eventId
        )

        if event is None:
            raise HTTPException(
                status_code=404,
                detail="Webhook event not found."
            )

        return event

    def update(
        self,
        db: Session,
        eventId: UUID,
        event: GatewayWebhookEventUpdate
    ):
        dbEvent = gatewayWebhookEventService.update(
            db,
            eventId,
            event
        )

        if dbEvent is None:
            raise HTTPException(
                status_code=404,
                detail="Webhook event not found."
            )

        return dbEvent


gatewayWebhookEventController = GatewayWebhookEventController()