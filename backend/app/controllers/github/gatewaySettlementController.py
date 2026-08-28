from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.gatewaySettlementSchema import (
    GatewaySettlementCreate,
    GatewaySettlementUpdate,
)
from app.services.github.gatewaySettlementService import (
    gatewaySettlementService,
)


class GatewaySettlementController:

    def create(
        self,
        db: Session,
        settlement: GatewaySettlementCreate
    ):
        return gatewaySettlementService.create(
            db,
            settlement
        )

    def getAll(
        self,
        db: Session
    ):
        return gatewaySettlementService.getAll(db)

    def getById(
        self,
        db: Session,
        settlementId: UUID
    ):
        settlement = gatewaySettlementService.getById(
            db,
            settlementId
        )

        if settlement is None:
            raise HTTPException(
                status_code=404,
                detail="Settlement not found."
            )

        return settlement

    def update(
        self,
        db: Session,
        settlementId: UUID,
        settlement: GatewaySettlementUpdate
    ):
        dbSettlement = gatewaySettlementService.update(
            db,
            settlementId,
            settlement
        )

        if dbSettlement is None:
            raise HTTPException(
                status_code=404,
                detail="Settlement not found."
            )

        return dbSettlement

    def delete(
        self,
        db: Session,
        settlementId: UUID
    ):
        deleted = gatewaySettlementService.delete(
            db,
            settlementId
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Settlement not found."
            )

        return {
            "message": "Settlement deleted successfully."
        }


gatewaySettlementController = GatewaySettlementController()