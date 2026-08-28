from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.gatewaySettlementRepository import (
    gatewaySettlementRepository,
)
from app.schemas.github.gatewaySettlementSchema import (
    GatewaySettlementCreate,
    GatewaySettlementUpdate,
)


class GatewaySettlementService:

    def create(
        self,
        db: Session,
        settlement: GatewaySettlementCreate
    ):
        return gatewaySettlementRepository.create(
            db=db,
            obj=settlement
        )

    def getAll(
        self,
        db: Session
    ):
        return gatewaySettlementRepository.get_all(db)

    def getById(
        self,
        db: Session,
        settlementId: UUID
    ):
        return gatewaySettlementRepository.get(
            db=db,
            obj_id=settlementId,
            id_field=gatewaySettlementRepository.model.id
        )

    def update(
        self,
        db: Session,
        settlementId: UUID,
        settlement: GatewaySettlementUpdate
    ):
        dbSettlement = self.getById(
            db,
            settlementId
        )

        if dbSettlement is None:
            return None

        return gatewaySettlementRepository.update(
            db=db,
            db_obj=dbSettlement,
            obj=settlement
        )

    def delete(
        self,
        db: Session,
        settlementId: UUID
    ):
        dbSettlement = self.getById(
            db,
            settlementId
        )

        if dbSettlement is None:
            return False

        gatewaySettlementRepository.delete(
            db=db,
            db_obj=dbSettlement
        )

        return True


gatewaySettlementService = GatewaySettlementService()