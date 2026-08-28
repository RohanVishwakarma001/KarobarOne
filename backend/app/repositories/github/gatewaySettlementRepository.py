from app.db.models.github.gatewaySettlement import GatewaySettlement
from app.repositories.github.base import BaseRepository


class GatewaySettlementRepository(
    BaseRepository[GatewaySettlement]
):

    def __init__(self):

        super().__init__(GatewaySettlement)


gatewaySettlementRepository = GatewaySettlementRepository()