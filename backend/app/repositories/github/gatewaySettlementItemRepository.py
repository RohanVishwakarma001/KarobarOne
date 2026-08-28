from app.db.models.github.gatewaySettlementItem import GatewaySettlementItem
from app.repositories.github.base import BaseRepository


class GatewaySettlementItemRepository(
    BaseRepository[GatewaySettlementItem]
):

    def __init__(self):
        super().__init__(GatewaySettlementItem)


gatewaySettlementItemRepository = GatewaySettlementItemRepository()