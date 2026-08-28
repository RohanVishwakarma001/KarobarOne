from sqlalchemy.orm import Session

from app.repositories.github.gatewayWebhookEventRepository import (
    gatewayWebhookEventRepository,
)
from app.schemas.github.gatewayWebhookEventSchema import (
    GatewayWebhookEventCreate,
    GatewayWebhookEventUpdate,
)


class GatewayWebhookEventService:

    def create(
        self,
        db: Session,
        event: GatewayWebhookEventCreate
    ):
        return gatewayWebhookEventRepository.create(
            db=db,
            obj=event
        )

    def getAll(
        self,
        db: Session
    ):
        return gatewayWebhookEventRepository.get_all(db)

    def getById(
        self,
        db: Session,
        eventId
    ):
        return gatewayWebhookEventRepository.get(
            db=db,
            obj_id=eventId,
            id_field=gatewayWebhookEventRepository.model.id
        )

    def update(
        self,
        db: Session,
        eventId,
        event: GatewayWebhookEventUpdate
    ):
        dbEvent = self.getById(db, eventId)

        if dbEvent is None:
            return None

        return gatewayWebhookEventRepository.update(
            db=db,
            db_obj=dbEvent,
            obj=event
        )


gatewayWebhookEventService = GatewayWebhookEventService()