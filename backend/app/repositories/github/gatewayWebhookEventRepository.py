from app.db.models.github.gatewayWebhookEvent import GatewayWebhookEvent
from app.repositories.github.base import BaseRepository


class GatewayWebhookEventRepository(
    BaseRepository[GatewayWebhookEvent]
):

    def __init__(self):
        super().__init__(GatewayWebhookEvent)


gatewayWebhookEventRepository = GatewayWebhookEventRepository()